# Generated by Django 3.1 on 2020-08-28 09:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_auto_20200828_1148'),
    ]

    operations = [
        migrations.RenameField(
            model_name='watchlistitem',
            old_name='onwer',
            new_name='owner',
        ),
    ]