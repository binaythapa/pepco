# Generated by Django 4.2.10 on 2024-03-12 11:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0016_sql"),
    ]

    operations = [
        migrations.RenameField(
            model_name="sql",
            old_name="Mapping",
            new_name="mapping",
        ),
    ]