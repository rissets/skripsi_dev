# Generated by Django 5.0.1 on 2024-01-21 08:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("chat", "0004_teachableagent"),
    ]

    operations = [
        migrations.AddField(
            model_name="teachableagent",
            name="mode",
            field=models.CharField(
                choices=[("QA", "Question-Answer"), ("PDF", "PDF")],
                default="QA",
                max_length=255,
            ),
        ),
    ]
