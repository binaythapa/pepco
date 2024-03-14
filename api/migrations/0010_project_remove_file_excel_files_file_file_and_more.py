# Generated by Django 4.2.10 on 2024-03-10 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0009_alter_excelfile_file_remove_file_excel_files_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Project",
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
                ("title", models.CharField(blank=True, max_length=200)),
            ],
        ),
        migrations.RemoveField(
            model_name="file",
            name="excel_files",
        ),
        migrations.AddField(
            model_name="file",
            name="file",
            field=models.FileField(blank=True, upload_to="excel"),
        ),
        migrations.DeleteModel(
            name="ExcelFile",
        ),
        migrations.AddField(
            model_name="project",
            name="excel_files",
            field=models.ManyToManyField(related_name="files", to="api.file"),
        ),
    ]
