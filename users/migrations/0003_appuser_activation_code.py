# Generated by Django 4.2.6 on 2023-10-06 10:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_alter_appuser_managers_remove_appuser_username_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="appuser",
            name="activation_code",
            field=models.CharField(blank=True, max_length=8, null=True),
        ),
    ]
