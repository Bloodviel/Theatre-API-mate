# Generated by Django 4.2.3 on 2023-07-29 12:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("theatre", "0003_alter_genre_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="play",
            name="description",
            field=models.TextField(default="Beautiful performance"),
        ),
    ]
