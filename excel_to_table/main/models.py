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
    

class UserPermission(models.Model):
    user_table=models.ForeignKey(Usertable,verbose_name='User name', on_delete=models.SET_NULL, null=True)
    template_master=models.ForeignKey(UploadTemplate,verbose_name='template name', on_delete=models.SET_NULL, null=True)
    expiry_date=models.DateTimeField(default=datetime.now,verbose_name='select date')
    class Meta:
        db_table = 'tbl_userpermission'
    def __str__(self) -> str:
        return self.template_master

class UploadedForm(models.Model):
    form_name = models.CharField(max_length= 150,unique=True, null=True)

    class Meta:
        db_table = 'tbl_form'
    def __str__(self) -> str:
        return self.form_name

class TempleData(models.Model):
    temp_data=models.TextField(max_length=9999999999999)
    template_master=models.ForeignKey(UploadTemplate,verbose_name='template name', on_delete=models.SET_NULL, null=True)
    class Meta:
        db_table='tbl_templedata'



class FormData(models.Model):
    form_data=models.TextField(max_length=9999999999999)
    template_master=models.ForeignKey(UploadTemplate,verbose_name='template name', on_delete=models.SET_NULL, null=True)
    creator=models.CharField(max_length=200,null=True)
    form_name=models.ForeignKey(UploadedForm,verbose_name='Form', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table='tbl_formdata'

class TempFormRelation(models.Model):
    user_table = models.ForeignKey(Usertable, verbose_name='User name', on_delete=models.SET_NULL, null=True)
    upload_template = models.ForeignKey(UploadTemplate, verbose_name='template name', on_delete=models.SET_NULL, null=True)
    form_details = models.ForeignKey(UploadedForm, verbose_name='form name', on_delete=models.SET_NULL, null=True, blank=True)
    class Meta:
        db_table = 'tbl_tempformrelation'
    def __str__(self) -> str:
        return self.upload_template