# Generated by Django 4.1.4 on 2023-01-23 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("files", "0008_remove_files_product_files_project"),
    ]

    operations = [
        migrations.RemoveField(model_name="files", name="script_code",),
        migrations.AlterField(
            model_name="files",
            name="script_file",
            field=models.FileField(
                blank=True, null=True, upload_to="projects/data/%Y/%m/%d/"
            ),
        ),
    ]
