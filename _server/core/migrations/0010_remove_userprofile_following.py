# Generated by Django 5.0.4 on 2024-05-02 03:22

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0009_userprofile_following"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="userprofile",
            name="following",
        ),
    ]
