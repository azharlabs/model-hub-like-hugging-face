# Generated by Django 4.1.4 on 2023-01-07 13:57

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0004_remove_product_model_remove_product_scripts"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="banner_pic",
            field=models.ImageField(default=1, upload_to="product/banner/%Y/%m/%d/"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="product",
            name="profile_pic",
            field=models.ImageField(default=1, upload_to="product/profile/%Y/%m/%d/"),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="product",
            name="description",
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]
