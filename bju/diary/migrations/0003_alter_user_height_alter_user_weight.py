# Generated by Django 5.1.3 on 2024-11-25 19:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("diary", "0002_alter_user_email"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="height",
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name="user",
            name="weight",
            field=models.FloatField(),
        ),
    ]
