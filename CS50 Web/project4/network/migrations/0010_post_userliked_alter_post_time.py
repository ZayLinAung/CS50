# Generated by Django 4.2.4 on 2023-09-27 03:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("network", "0009_alter_post_likes"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="userLiked",
            field=models.CharField(default="", max_length=64),
        ),
        migrations.AlterField(
            model_name="post",
            name="time",
            field=models.CharField(max_length=100),
        ),
    ]
