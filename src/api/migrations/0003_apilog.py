# Generated by Django 4.1.4 on 2023-01-07 14:02

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0005_product_banner_pic_product_profile_pic_and_more"),
        ("api", "0002_api_team_alter_api_active_alter_api_enddate"),
    ]

    operations = [
        migrations.CreateModel(
            name="apiLog",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        db_index=True,
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("price", models.IntegerField()),
                (
                    "api",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="api.api"
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="product.product",
                    ),
                ),
            ],
        ),
    ]
