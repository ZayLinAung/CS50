# Generated by Django 4.1.3 on 2022-11-23 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_remove_bids_noofbids'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bids',
            name='currentBid',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=10),
        ),
    ]
