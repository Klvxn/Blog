# Generated by Django 4.0.6 on 2022-07-11 01:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0005_rename_text_blogpost_content'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blogpost',
            old_name='content',
            new_name='text',
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='slug',
            field=models.SlugField(max_length=200, unique=True),
        ),
    ]