# Generated by Django 4.1.3 on 2022-11-24 07:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Project",
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
                ("project_name", models.CharField(db_index=True, max_length=256)),
                ("image", models.ImageField(upload_to="projects/%Y/%m/%d/")),
                ("description", models.TextField()),
                ("created_date", models.DateTimeField(auto_now_add=True)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="project",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
