# Generated by Django 4.1.4 on 2023-01-12 04:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0006_apiplaylog_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="apilog", name="price", field=models.FloatField(),
        ),
    ]
