# Generated by Django 3.2.12 on 2022-03-29 18:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='realesed_date',
            new_name='release_date',
        ),
    ]