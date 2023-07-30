# Generated by Django 4.2.3 on 2023-07-30 13:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("theatre", "0004_play_description"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ticket",
            name="performance",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="tickets",
                to="theatre.performance",
            ),
        ),
        migrations.AlterField(
            model_name="ticket",
            name="reservation",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="tickets",
                to="theatre.reservation",
            ),
        ),
    ]
