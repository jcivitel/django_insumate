# Generated by Django 5.0.7 on 2024-07-17 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("django_im_backend", "0002_mealentry"),
    ]

    operations = [
        migrations.AddField(
            model_name="mealentry",
            name="barcode",
            field=models.TextField(default=1, help_text="Meal barcode"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="mealentry",
            name="name",
            field=models.TextField(default="NaN", help_text="Meal name"),
            preserve_default=False,
        ),
    ]
