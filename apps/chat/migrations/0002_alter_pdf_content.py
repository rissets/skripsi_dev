# Generated by Django 5.0.1 on 2024-01-16 06:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("chat", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pdf",
            name="content",
            field=models.TextField(blank=True, null=True),
        ),
    ]
