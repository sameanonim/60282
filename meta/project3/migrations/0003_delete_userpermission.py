# Generated by Django 4.2.2 on 2023-07-21 08:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("project3", "0002_alter_user_avatar"),
    ]

    operations = [
        migrations.DeleteModel(
            name="UserPermission",
        ),
    ]