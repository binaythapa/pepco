# Generated by Django 4.2.10 on 2024-03-12 11:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0015_index"),
    ]

    operations = [
        migrations.CreateModel(
            name="sql",
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
                ("sql_query", models.TextField()),
                (
                    "Mapping",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="api.mapping"
                    ),
                ),
            ],
        ),
    ]
