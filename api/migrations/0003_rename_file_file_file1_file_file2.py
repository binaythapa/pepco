# Generated by Django 4.2.10 on 2024-03-10 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0002_file"),
    ]

    operations = [
        migrations.RenameField(
            model_name="file",
            old_name="file",
            new_name="file1",
        ),
        migrations.AddField(
            model_name="file",
            name="file2",
            field=models.FileField(blank=True, upload_to="excel/"),
        ),
    ]
