# Generated by Django 4.1.4 on 2023-01-10 09:48

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ("taggit", "0006_alter_taggeditem_object_id"),
        ("product", "0010_product_featured"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="tags",
            field=taggit.managers.TaggableManager(
                blank=True,
                help_text="A comma-separated list of tags.",
                through="taggit.TaggedItem",
                to="taggit.Tag",
                verbose_name="Tags",
            ),
        ),
    ]
