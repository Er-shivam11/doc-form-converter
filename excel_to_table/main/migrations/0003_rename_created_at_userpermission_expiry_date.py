# Generated by Django 4.2.6 on 2024-02-07 10:00

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0002_userpermission_created_at"),
    ]

    operations = [
        migrations.RenameField(
            model_name="userpermission",
            old_name="created_at",
            new_name="expiry_date",
        ),
    ]
