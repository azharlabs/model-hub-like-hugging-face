# Generated by Django 4.1.4 on 2023-01-17 16:55

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0013_alter_product_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="id",
            field=models.UUIDField(
                db_index=True,
                default=uuid.uuid4,
                editable=False,
                primary_key=True,
                serialize=False,
            ),
        ),
    ]
