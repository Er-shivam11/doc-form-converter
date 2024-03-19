# Generated by Django 4.2.6 on 2024-03-19 07:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0040_remove_templedata_form_data"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="userpermission",
            name="form_name",
        ),
        migrations.AddField(
            model_name="formdata",
            name="form_name",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="main.uploadedform",
                verbose_name="Form",
            ),
        ),
    ]
