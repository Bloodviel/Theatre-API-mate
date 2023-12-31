# Generated by Django 4.2.3 on 2023-07-30 16:06

from django.db import migrations, models
import theatre.models


class Migration(migrations.Migration):
    dependencies = [
        ("theatre", "0005_alter_ticket_performance_alter_ticket_reservation"),
    ]

    operations = [
        migrations.AddField(
            model_name="play",
            name="image",
            field=models.ImageField(
                null=True, upload_to=theatre.models.play_image_file_path
            ),
        ),
    ]
