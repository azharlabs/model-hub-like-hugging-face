# Generated by Django 4.1.3 on 2022-11-25 14:42

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Newsletter",
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
                ("email", models.EmailField(db_index=True, max_length=254)),
                ("created_date", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
