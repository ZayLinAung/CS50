# Generated by Django 4.2.3 on 2023-08-11 15:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("network", "0003_post_likes"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="follower",
            field=models.DecimalField(decimal_places=3, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name="user",
            name="following",
            field=models.DecimalField(decimal_places=3, default=0, max_digits=10),
        ),
    ]