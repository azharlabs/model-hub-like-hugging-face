# Generated by Django 4.1.3 on 2022-12-21 04:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("files", "0004_remove_files_updated_date_files_script_code_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="files",
            name="updated_date",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="updatefileinfo",
            name="files",
            field=models.ForeignKey(
                default=1, on_delete=django.db.models.deletion.CASCADE, to="files.files"
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="updatefileinfo",
            name="updated_author",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
    ]
