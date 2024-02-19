from django import forms
from .models import UserPermission,UploadTemplate
from bootstrap_datepicker_plus.widgets import DateTimePickerInput


class TemplateForm(forms.ModelForm):
    class Meta:
        model = UserPermission
        fields = "__all__"
        widgets = {
            'template_master': forms.Select(attrs={'class': 'form-control custom-class'}),
            'expiry_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
class UserPermissionForm(forms.ModelForm):
    class Meta:
        model = UserPermission
        fields = "__all__"

class UploadWorkSheetForm(forms.ModelForm):
    class Meta:
        model = UploadTemplate
        fields = "__all__"     
