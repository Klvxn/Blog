# Generated by Django 3.2.9 on 2022-01-19 16:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("blogs", "0002_auto_20220119_1249"),
    ]

    operations = [
        migrations.RenameField(
            model_name="blogpost",
            old_name="user",
            new_name="User",
        ),
    ]
