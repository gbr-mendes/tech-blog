# Generated by Django 3.2.12 on 2022-04-10 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_alter_post_main_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='main_image',
            field=models.ImageField(blank=True, null=True, upload_to='media/posts/images/%Y/%m'),
        ),
    ]
