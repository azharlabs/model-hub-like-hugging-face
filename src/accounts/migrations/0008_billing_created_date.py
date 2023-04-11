# Generated by Django 4.1.4 on 2023-01-09 10:31

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0007_billing"),
    ]

    operations = [
        migrations.AddField(
            model_name="billing",
            name="created_date",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]