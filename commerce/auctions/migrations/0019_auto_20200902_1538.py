# Generated by Django 3.1 on 2020-09-02 15:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0018_auto_20200902_1535'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watchlistitem',
            name='listing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctions.listing'),
        ),
    ]
