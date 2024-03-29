# Generated by Django 4.2.10 on 2024-03-10 10:57

import api.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0003_rename_file_file_file1_file_file2"),
    ]

    operations = [
        migrations.AlterField(
            model_name="file",
            name="file1",
            field=models.FileField(blank=True, upload_to=api.models.file_upload_path),
        ),
        migrations.AlterField(
            model_name="file",
            name="file2",
            field=models.FileField(blank=True, upload_to=api.models.file_upload_path),
        ),
    ]
