# Generated by Django 4.2.6 on 2024-03-18 06:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0022_delete_templatedata"),
    ]

    operations = [
        migrations.CreateModel(
            name="TempData",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("temp_data", models.TextField(max_length=9999999999999)),
                (
                    "template_master",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="main.uploadtemplate",
                        verbose_name="template name",
                    ),
                ),
            ],
            options={
                "db_table": "tbl_tempdata",
            },
        ),
    ]
