# Generated by Django 4.2.6 on 2024-03-19 07:50

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0039_userpermission_form_name_delete_tempformrelation"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="templedata",
            name="form_data",
        ),
    ]