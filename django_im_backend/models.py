from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    height = models.FloatField(help_text="Height in centimeters")
    weight = models.FloatField(help_text="Weight in kilograms")
    morning_factor = models.FloatField()
    noon_factor = models.FloatField()
    evening_factor = models.FloatField()

    def __str__(self):
        return f"{self.user.username}'s Profile"


class MealEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    KE = models.FloatField(help_text="Carbohydrate units")
    timestamp = models.DateTimeField(auto_now_add=True)
    barcode = models.TextField(help_text="Meal barcode")
    name = models.TextField(help_text="Meal name")

    def __str__(self):
        return f"{self.timestamp} - {self.user.username}"
