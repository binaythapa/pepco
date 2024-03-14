# Generated by Django 4.2.10 on 2024-03-10 17:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0006_excelfile_title"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="file",
            name="title",
        ),
        migrations.RemoveField(
            model_name="file",
            name="excel_files",
        ),
        migrations.AddField(
            model_name="file",
            name="excel_files",
            field=models.ForeignKey(
                default="",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="files",
                to="api.excelfile",
            ),
        ),
    ]
