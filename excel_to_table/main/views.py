from django.shortcuts import render, HttpResponse,redirect
import pandas as pd
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import UploadWorkSheetForm, UserPermissionForm, TemplateForm,FormSheet
from .models import UploadTemplate,UserPermission
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, authenticate
from django.contrib import messages
from docx import Document
import docx
import pdfplumber
import sys
from .forms import UserPermissionForm, UploadWorkSheetForm
import os
from .models import UploadTemplate, UploadedForm
from django.conf import settings
from pathlib import Path
from django.http import JsonResponse
import json
# Create your views here.
from django.shortcuts import render

from .models import FormData,TempleData
def loginuser(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        if form.is_valid:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                auth_login(request, user)
                if user.is_superuser:
                    return redirect('upload')  # Superuser, redirect to the 'home' page
                else:
                    return redirect('upload')  
                
            else:
                if username == '' or password == '':
                    messages.error(
                        request, message='Please Enter Username and Passowrd Correctly')
                else:
                    messages.error(
                        request, message='Username or Password not correct')

    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def home(request):
    return render(request,"home.html")



def addtemplate(request):
    form = UploadWorkSheetForm()

    if request.method == 'POST':
        form = UploadWorkSheetForm(request.POST, request.FILES)
        if form.is_valid():
            
            upload_template_instance = form.save()
            template_master = upload_template_instance.worksheet_file.path
            print(template_master)
            if template_master.endswith('.docx'):
                t_id = upload_template_instance.id
                print(t_id)
                # Parse the Word document using python-docx
                doc = Document(template_master)
                header = doc.sections[0].header
                headers_data = []
                for table in header.tables:
                    header_data = []
                    for row in table.rows:
                        row_data = [cell.text for cell in row.cells]
                        unique_values = list(set(row_data))
                        # print(unique_values,'header row')
                        template_form_instance = TempleData(temp_data=unique_values,template_master_id=t_id)
                        template_form_instance.save()
                        header_data.append(unique_values)
                    headers_data.append(header_data)
                tables_data = []
                columns = None
                # Extract data from each table
                for table in doc.tables:
                    table_data = []
                    unique_values = set()  # Track unique values across top 3 rows
                    # Counter for appending "row" labels
                    row_counter = 1
                    for i, row in enumerate(table.rows):
                        row_data = []
                        for j, cell in enumerate(row.cells):
                            cell_text = cell.text.strip()  # Strip whitespace from cell text
                            # Check if it's the header row
                            if i < 3:
                                # Check for duplicate values in top 3 rows
                                if cell_text in unique_values:
                                    cell_text = ""  # Fill null value if duplicate
                                else:
                                    unique_values.add(cell_text)
                            row_data.append(cell_text)
                        table_data.append(row_data)
                        if i == 2 and '20 µ' in row_data and 'G4' in row_data:
                            row_data[-1] = 'M6(F6)/F9'
                            row_data[-2] = 'G4'
                            row_data[-3] = '20 µ'
                        if i == 3 and '20 µ' in row_data or 'G4' in row_data:
                            row_data[0]=""
                            row_data[1]=""
                        # Print the row label
                        # print(f"row{row_counter}", row_data)
                        template_form_instance = TempleData(temp_data=row_data,template_master_id=t_id)
                        template_form_instance.save()
                        row_counter += 1
                    tables_data.append(table_data)
            return redirect('selecttemplate')

        else:
            # Handle form errors - you can print them or log them for debugging
            print(form.errors)


    name=UploadTemplate.objects.all()

    context = {
        'form': form
    }
    return render(request, 'addtemplate.html', context)

def selecttemplate(request):
    tform=UserPermissionForm
    if request.method == 'POST':
        count_form = UserPermissionForm(request.POST, request.FILES)
        if count_form.is_valid():

            count_form.save()
            return redirect('formuploaded')
        else:
            print(count_form.errors)
    else:
        count_form = UserPermissionForm()
    context = {
        'tform': tform}
    return render(request, 'selecttemp.html', context)

def formuploaded(request):
    tform=FormSheet
    if request.method == 'POST':
        count_form = FormSheet(request.POST, request.FILES)
        if count_form.is_valid():   
            count_form.save()
        else:
            print(count_form.errors)
    else:
        count_form = FormSheet()
    context = {
        'tform': tform} 
    return render(request, 'addform.html', context)
# def typeform(request):
#     if request.method == 'POST':
#         form = UserPermissionForm(request.POST, request.FILES)
#         if form.is_valid():
#             upload_template_instance = form.save()
#             template_master = upload_template_instance.template_master.worksheet_file.path
#             print(template_master)
#             if template_master.endswith('.xlsx'):
#             # Parse the Excel file using Pandas
#                 df = pd.read_excel(template_master)
#                 df.fillna('', inplace=True)
#                 df.columns = ["" if 'Unnamed' in str(col) else col for col in df.columns]
#                 columns = df.columns.tolist()
#                 df = df[(df.T != '').any()]
#                 data = df.values.tolist()
#                 return render(request, 'your_template.html', {'form': form, 'columns': columns, 'data': data})
#             elif template_master.endswith('.docx'):
#                 t_id = upload_template_instance.template_master.id
#                 print(t_id)
#                 latest_entry = UserPermission.objects.latest('id')
#                 form_name = latest_entry.form_name
#                 print(form_name)
#                 # Parse the Word document using python-docx
#                 doc = Document(template_master)
#                 header = doc.sections[0].header
#                 headers_data = []
#                 for table in header.tables:
#                     header_data = []
#                     for row in table.rows:
#                         row_data = [cell.text for cell in row.cells]
#                         unique_values = list(set(row_data))
#                         # print(unique_values,'header row')
#                         template_form_instance = TempleData(temp_data=unique_values,template_master_id=t_id,form_data=form_name)
#                         template_form_instance.save()
#                         header_data.append(unique_values)
#                     headers_data.append(header_data)
#                 tables_data = []
#                 columns = None
#                 # Extract data from each table
#                 for table in doc.tables:
#                     table_data = []
#                     unique_values = set()  # Track unique values across top 3 rows
#                     # Counter for appending "row" labels
#                     row_counter = 1
#                     for i, row in enumerate(table.rows):
#                         row_data = []
#                         for j, cell in enumerate(row.cells):
#                             cell_text = cell.text.strip()  # Strip whitespace from cell text
#                             # Check if it's the header row
#                             if i < 3:
#                                 # Check for duplicate values in top 3 rows
#                                 if cell_text in unique_values:
#                                     cell_text = ""  # Fill null value if duplicate
#                                 else:
#                                     unique_values.add(cell_text)
#                             row_data.append(cell_text)
#                         table_data.append(row_data)
#                         if i == 2 and '20 µ' in row_data and 'G4' in row_data:
#                             row_data[-1] = 'M6(F6)/F9'
#                             row_data[-2] = 'G4'
#                             row_data[-3] = '20 µ'
#                         if i == 3 and '20 µ' in row_data or 'G4' in row_data:
#                             row_data[0]=""
#                             row_data[1]=""
#                         # Print the row label
#                         # print(f"row{row_counter}", row_data)
#                         template_form_instance = TempleData(temp_data=row_data,template_master_id=t_id,form_data=form_name)
#                         template_form_instance.save()
#                         row_counter += 1
#                     tables_data.append(table_data)
#                     # print(tables_data)

#                 return render(request, 'your_template.html', {'form': form, 'headers_data': headers_data,'columns': columns, 'tables_data': tables_data})
                
#             else:
#                 message = "Unsupported File Content, Unsupported File Structure or format, file is not found"
#                 return HttpResponse(f'<div class="error-message">{message}</div>')

#     else:
#         form = UserPermissionForm()

#     return render(request, 'your_template.html', {'form': form})



def editform(request):


    fid = UploadedForm.objects.latest('id')
    tid = UploadTemplate.objects.latest('id')
    tempform=TempleData.objects.filter(template_master=tid)

    tempid=tid.id
    formid=fid.id
    print(fid,'fid')
    print(tid,'tid')
    print(tempid,'tempid')
    print(formid,'firmid')
    # for formdetails in tempform:
    #     FormData.objects.create(
    #     step=formdetails.step,
    #     description=formdetails.description,
    #     std_value=formdetails.std_value,
    #     obs_value=formdetails.obs_value,
    #     start_time=formdetails.start_time,
    #     end_time=formdetails.end_time,
    #     creator=formdetails.creator,
    #     form_name=fid,
    #     upload_template=tid,
    #     )

    # # Retrieve the latest template_master_id
    # latest_entry = UserPermission.objects.latest('id')
    # form_name = latest_entry.form_name
    # print(form_name)

    # latest_template_master_id = latest_entry.template_master_id
    # # Retrieve FormData objects for the latest template_master_id
    # formdata = TempleData.objects.filter(template_master_id=latest_template_master_id,form_data=form_name)


    # print(formdata)
    # # Convert FormData objects to DataFrame
    # rows = []
    # for data in formdata:
    #     rows.append(eval(data.temp_data))
    # # Create DataFrame
    # df = pd.DataFrame(rows)
    # # Assign headers
    # headers = df.iloc[0]
    # df = df[1:]
    # df.columns = headers
    # print(df)

    # return render(request, 'formdata.html', {'df': df})
    # df = pd.DataFrame(rows)
    
    # df['form_data'] = df['form_data'].apply(lambda x: x.replace('[', '').replace(']', '').replace(',', ''))
    

# Printing header and content
  
    # html_table = df.to_html(index=False)

    # Pass the HTML table to the template context
    


# footer = doc.sections[0].header
                # footers_data = []
                # for table in footer.tables:
                #     footer_data = []
                #     for row in table.rows:
                #         row_data = [cell.text for cell in row.cells]
                #         unique_values = list(set(row_data))
                #         print(unique_values,'footer row')
                #         footer_data.append(unique_values)
                #     footers_data.append(footer_data)
                    
                # template_data_instance = TemplateData(header=headers_data,content=tables_data,template_ref_id=t_id)

# Save the instance to the database
                # template_data_instance.save()
# def display_excel(request):
#     pd.set_option('display.max_rows', None)
#     pd.set_option('display.max_columns', None)
#     excel_path = "static/ex.xlsx"  # Path to your Excel file

#     data = pd.read_excel(excel_path)
#     data = data.iloc[:, :-2]
#     data = data.loc[:, ~data.columns.str.startswith('Unnamed')]
#     data = data.drop(0)


#     data = data.rename(columns={
#         'Step': 'description',
#         'Actual Readings': 'actual_readings',
#         'Start Time': 'start_time',
#         'End Time (hour)': 'end_time'
#     })
#     print(data)

#     rm_col = ['Step No.', 'description', 'actual_readings', 'Unnamed: 3', 'Unnamed: 4', 'start_time', 'Unnamed: 6', 'end_time']
#     sorted_data = [col for col in rm_col if not col.startswith('Unnamed')]
    
#     print(sorted_data)



#     for index, row in data.iterrows():
#         step=1
#         description = "Transfer about 50 to 60 L purified water in Tank ID TLI2M20"
#         std_value = "50-60 L"
#         obs_value = "0"
#         start_time="0"
#         end_time = "0"
        

#         TemplateDetail.objects.create(
#             step=step,
#             description=description,
#             std_value=std_value,
#             obs_value=obs_value,
#             start_time=start_time,
#             end_time=end_time
#         )
        

#     # You can also query the saved data from the database and display it on the webpage
#     saved_data = TemplateDetail.objects.all()
#     return render(request, 'display_excel.html', {'data': data})
    


# def read_and_save_to_json(uploaded_file):
#     """
#     Read data from Excel, PDF, or Word file and save it into a JSON format.
#     """
#     file_extension = uploaded_file.name.split('.')[-1].lower()

#     if file_extension == 'xlsx':
#         data = pd.read_excel(uploaded_file)
#         json_data = data.to_json(orient='records')

#     elif file_extension == 'pdf':
#         with pdfplumber.open(uploaded_file) as pdf:
#             pages_text = []
#             for page in pdf.pages:
#                 text = page.extract_text()
#                 pages_text.append(text)
#         json_data = json.dumps(pages_text)

#     elif file_extension == 'docx':
#         doc = Document(uploaded_file)
#         doc_text = [para.text for para in doc.paragraphs]
#         json_data = json.dumps(doc_text)

#     else:
#         # Handle unsupported file types
#         return None

#     return json_data


# def wordreader(request):
#     doc = Document("static/11 Planner for AHU.docx")
#     tables_data = []
#     # Extract data from each table
#     for table in doc.tables:
#         table_data = []
#         for row in table.rows:
#             row_data = [cell.text for cell in row.cells]
#             table_data.append(row_data)
#         tables_data.append(table_data)
#         print(table_data)

    # Extract data from headers
    # for section in doc.sections:
    #     for paragraph in section.header.paragraphs:
    #         tables_data.append(paragraph.text)


# 
        
    # Extract data from footers
    # for section in doc.sections:
    #     for paragraph in section.footer.paragraphs:
    #         tables_data.append(paragraph.text)

    

    # Pass the extracted data to the template
    # return render(request, 'word.html', {'tables_data': tables_data})

# import docx 

# def rulebased(request):
#     # Import docx NOT python-docx 

# # Create an instance of a word document 
#     doc = docx.Document() 

#     # Add a Title to the document 
#     doc.add_heading('GeeksForGeeks', 0) 

#     # Adding a paragraph 
#     doc.add_heading('Page 1:', 3) 
#     doc.add_paragraph('GeeksforGeeks is a Computer Science portal for geeks.') 

#     # Adding a page break 
#     doc.add_page_break() 

#     # Adding a paragraph 
#     doc.add_heading('Page 2:', 3) 
#     doc.add_paragraph('GeeksforGeeks is a Computer Science portal for geeks.') 

#     # Now save the document to a location 
#     doc.save('gfg.docx') 


