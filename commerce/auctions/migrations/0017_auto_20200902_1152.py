# Generated by Django 3.1 on 2020-09-02 11:52

import auctions.util
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0016_auto_20200902_1145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='image',
            field=models.ImageField(default='no_image.jpg', upload_to=auctions.util.user_directory_path),
        ),
    ]