# Generated by Django 5.1.3 on 2024-11-26 15:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("diary", "0004_user_age"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="calorie_goal",
            field=models.IntegerField(default=3000),
            preserve_default=False,
        ),
    ]
