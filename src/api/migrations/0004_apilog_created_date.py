# Generated by Django 4.1.4 on 2023-01-07 14:06

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0003_apilog"),
    ]

    operations = [
        migrations.AddField(
            model_name="apilog",
            name="created_date",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]
