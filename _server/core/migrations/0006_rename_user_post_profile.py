# Generated by Django 5.0.3 on 2024-05-01 05:13

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0005_alter_userprofile_bio_alter_userprofile_cat_breed_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="post",
            old_name="user",
            new_name="profile",
        ),
    ]