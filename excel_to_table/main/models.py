from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
# Create your models here.
from django.db import models


class Usertable(models.Model):        
    type_name = models.CharField(verbose_name="Type Name", max_length=150, unique=True,null=True, blank=True)
    password=models.CharField(max_length=200)
    status=models.BooleanField()
    class Meta:
        db_table = 'tbl_usertable'
    def __str__(self) -> str:
        return self.type_name
class UploadTemplate(models.Model):
    worksheet_name = models.CharField(max_length= 150,unique=True, null=True)
    creator = models.ForeignKey(Usertable, on_delete=models.SET_NULL,null=True)
    worksheet_file = models.FileField(upload_to = 'template', default = True)
    status=models.BooleanField(null=True)
    

    class Meta:
        db_table = 'tbl_uploadtemplate'
    def __str__(self) -> str:
        return self.worksheet_name
    
# class TemplateMaster(models.Model):
#     name=models.CharField(max_length=200,verbose_name='template name',  blank=False, null=True)
#     status=models.BooleanField()
#     class Meta:
#         db_table = 'tbl_templatemaster'
#     def __str__(self) -> str:
#         return self.name

class UserPermission(models.Model):
    user_table=models.ForeignKey(Usertable,verbose_name='User name', on_delete=models.SET_NULL, null=True)
    template_master=models.ForeignKey(UploadTemplate,verbose_name='template name', on_delete=models.SET_NULL, null=True)
    expiry_date=models.DateTimeField(default=datetime.now,verbose_name='select date')
    form_name = models.CharField(max_length= 150,unique=True, null=True)

    class Meta:
        db_table = 'tbl_userpermission'
    def __str__(self) -> str:
        return self.template_master


# class TemplateDetail(models.Model):
#     step = models.IntegerField()
#     description = models.CharField(max_length=200)
#     std_value = models.CharField(max_length=200)
#     obs_value = models.CharField(max_length=200)
#     start_time=models.CharField(max_length=200)
#     end_time=models.CharField(max_length=200)
#    # Assuming end_time is a datetime field
#     class Meta:
#         db_table = 'tbl_templatedetail'

    

# class TemplateData(models.Model):
#     header= models.CharField(max_length=2000)
#     content= models.TextField(max_length=2000000)
#     template_ref=models.ForeignKey(UploadTemplate,verbose_name='template name', on_delete=models.SET_NULL, null=True)
    
#     class Meta:
#         db_table = 'tbl_templatedata'
class TempleData(models.Model):
    temp_data=models.TextField(max_length=9999999999999)
    template_master=models.ForeignKey(UploadTemplate,verbose_name='template name', on_delete=models.SET_NULL, null=True)
    form_data=models.TextField(max_length=9999999999999)
    class Meta:
        db_table='tbl_templedata'



class FormData(models.Model):
    form_data=models.TextField(max_length=9999999999999)
    template_master=models.ForeignKey(UploadTemplate,verbose_name='template name', on_delete=models.SET_NULL, null=True)
    class Meta:
        db_table='tbl_formdata'

class UploadedForm(models.Model):
    form_name = models.CharField(max_length= 150,unique=True, null=True)

    class Meta:
        db_table = 'tbl_form'
    def __str__(self) -> str:
        return self.form_name