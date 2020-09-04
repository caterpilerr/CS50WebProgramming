# Generated by Django 3.1 on 2020-09-03 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0019_auto_20200902_1538'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='category',
            field=models.CharField(choices=[('fashion', 'Fashion'), ('electronics', 'Electronics'), ('home', 'Home'), ('hobby', 'Hobby'), ('toys', 'Toys'), ('other', 'Other')], default='Other', max_length=64),
            preserve_default=False,
        ),
    ]
