# Generated by Django 4.2.6 on 2024-03-15 09:47

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0018_formdata"),
    ]

    operations = [
        migrations.RenameField(
            model_name="formdata",
            old_name="TemplateMaster",
            new_name="template_master",
        ),
    ]
