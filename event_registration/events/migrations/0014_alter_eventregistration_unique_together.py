# Generated by Django 4.2.5 on 2023-09-08 10:02

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("events", "0013_alter_participant_email"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="eventregistration",
            unique_together={("event", "participant")},
        ),
    ]
