from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
import pandas as pd
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import pandas as pd
from .forms import UploadWorkSheetForm,UserPermissionForm,TemplateForm
import os
import pandas as pd
import pandas as pd
from .models import TemplateDetail,UploadTemplate
import numpy as np
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, authenticate
from django.contrib import messages
from django.shortcuts import render, redirect
import pandas as pd
import json
from docx import Document
import docx
import pdfplumber
import sys
from docx import Document
from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
import json
from docx import Document
import pdfplumber
from django.shortcuts import render
from django.http import JsonResponse

import pandas as pd
import json
from docx import Document
import pdfplumber
from django.shortcuts import render, redirect
import docx2txt


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
            # return redirect('checktype')
        else:
            print(count_form.errors)
    else:
        count_form = UserPermissionForm()
    context = {
        'tform': tform}
    return render(request, 'selecttemp.html', context)


def typeform(request):
    if request.method == 'POST':
        form = UserPermissionForm(request.POST, request.FILES)
        if form.is_valid():
            upload_template_instance = form.save()
            template_master = upload_template_instance.template_master.worksheet_file

            # Parse the Excel file using Pandas
            df = pd.read_excel(template_master)
            df.fillna('', inplace=True)
            df.columns = ["" if 'Unnamed' in str(col) else col for col in df.columns]
            columns = df.columns.tolist()
            df = df[(df.T != '').any()]
            data = df.values.tolist()

            # print(data)
            data_json = json.dumps(data)
            # print(data_json)

            return render(request, 'your_template.html', {'form': form, 'columns': columns, 'data': data})

    else:
        form = UserPermissionForm()

    return render(request, 'your_template.html', {'form': form})

def display_excel(request):
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    excel_path = "static/ex.xlsx"  # Path to your Excel file

    data = pd.read_excel(excel_path)
    data = data.iloc[:, :-2]
    data = data.loc[:, ~data.columns.str.startswith('Unnamed')]
    data = data.drop(0)


    data = data.rename(columns={
        'Step': 'description',
        'Actual Readings': 'actual_readings',
        'Start Time': 'start_time',
        'End Time (hour)': 'end_time'
    })
    print(data)

    rm_col = ['Step No.', 'description', 'actual_readings', 'Unnamed: 3', 'Unnamed: 4', 'start_time', 'Unnamed: 6', 'end_time']
    sorted_data = [col for col in rm_col if not col.startswith('Unnamed')]
    
    print(sorted_data)



    for index, row in data.iterrows():
        step=1
        description = "Transfer about 50 to 60 L purified water in Tank ID TLI2M20"
        std_value = "50-60 L"
        obs_value = "0"
        start_time="0"
        end_time = "0"
        

        TemplateDetail.objects.create(
            step=step,
            description=description,
            std_value=std_value,
            obs_value=obs_value,
            start_time=start_time,
            end_time=end_time
        )
        

    # You can also query the saved data from the database and display it on the webpage
    saved_data = TemplateDetail.objects.all()
    return render(request, 'display_excel.html', {'data': data})
    


def read_and_save_to_json(uploaded_file):
    """
    Read data from Excel, PDF, or Word file and save it into a JSON format.
    """
    file_extension = uploaded_file.name.split('.')[-1].lower()

    if file_extension == 'xlsx':
        data = pd.read_excel(uploaded_file)
        json_data = data.to_json(orient='records')

    elif file_extension == 'pdf':
        with pdfplumber.open(uploaded_file) as pdf:
            pages_text = []
            for page in pdf.pages:
                text = page.extract_text()
                pages_text.append(text)
        json_data = json.dumps(pages_text)

    elif file_extension == 'docx':
        doc = Document(uploaded_file)
        doc_text = [para.text for para in doc.paragraphs]
        json_data = json.dumps(doc_text)

    else:
        # Handle unsupported file types
        return None

    return json_data
from docx import Document
from django.shortcuts import render

from docx import Document
from django.shortcuts import render

from docx import Document
from django.shortcuts import render

def wordreader(request):
    doc = Document("static/11 Planner for AHU.docx")
    tables_data = []
    # Extract data from each table
    for table in doc.tables:
        table_data = []
        for row in table.rows:
            row_data = [cell.text for cell in row.cells]
            table_data.append(row_data)
        tables_data.append(table_data)
        print(table_data)

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
    return render(request, 'word.html', {'tables_data': tables_data})


