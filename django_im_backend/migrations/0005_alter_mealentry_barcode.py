# Generated by Django 5.0.7 on 2024-08-05 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("django_im_backend", "0004_recentsearch"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mealentry",
            name="barcode",
            field=models.TextField(help_text="Meal barcode", null=True),
        ),
    ]
