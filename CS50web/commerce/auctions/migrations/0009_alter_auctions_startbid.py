# Generated by Django 4.1.3 on 2022-11-21 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_bids_auction_id_watchlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctions',
            name='startbid',
            field=models.DecimalField(decimal_places=3, max_digits=10),
        ),
    ]