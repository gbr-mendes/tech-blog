# Generated by Django 3.2.12 on 2022-04-10 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='main_image',
            field=models.ImageField(default='templates/static/assets/img/post-bg.jpg', upload_to='media/posts/images/%Y/%m'),
        ),
    ]
