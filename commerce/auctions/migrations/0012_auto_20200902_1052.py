# Generated by Django 3.1 on 2020-09-02 10:52

import auctions.util
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_auto_20200902_1049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='image',
            field=models.ImageField(default='no_image.png', upload_to=auctions.util.user_directory_path),
        ),
    ]
