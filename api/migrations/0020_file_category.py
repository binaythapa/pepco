# Generated by Django 4.2.10 on 2024-03-13 06:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0019_category"),
    ]

    operations = [
        migrations.AddField(
            model_name="file",
            name="category",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="api.category",
            ),
        ),
    ]
