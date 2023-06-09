# Generated by Django 4.1.4 on 2023-01-07 18:02

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0005_product_banner_pic_product_profile_pic_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="manual",
            field=ckeditor_uploader.fields.RichTextUploadingField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="product", name="description", field=models.TextField(),
        ),
    ]
