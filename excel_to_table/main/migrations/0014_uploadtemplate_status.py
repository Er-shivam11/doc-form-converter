# Generated by Django 4.2.6 on 2024-02-15 06:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0013_delete_exceldata"),
    ]

    operations = [
        migrations.AddField(
            model_name="uploadtemplate",
            name="status",
            field=models.BooleanField(null=True),
        ),
    ]
