# Generated by Django 4.1.3 on 2022-12-29 05:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0004_alter_post_id"),
    ]

    operations = [
        migrations.RemoveField(model_name="post", name="tags",),
    ]
