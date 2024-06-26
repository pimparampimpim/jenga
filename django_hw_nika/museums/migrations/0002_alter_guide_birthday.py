# Generated by Django 4.2.1 on 2024-05-07 01:32

from django.db import migrations, models
import museums.validators


class Migration(migrations.Migration):

    dependencies = [
        ("museums", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="guide",
            name="birthday",
            field=models.DateField(
                validators=[museums.validators.check_birthday], verbose_name="birthday"
            ),
        ),
    ]
