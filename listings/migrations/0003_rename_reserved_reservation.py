# Generated by Django 3.2 on 2022-01-28 11:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("listings", "0002_reserved"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Reserved",
            new_name="Reservation",
        ),
    ]