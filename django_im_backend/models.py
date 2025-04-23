from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tutorial_completed = models.BooleanField(default=False)
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
    barcode = models.TextField(help_text="Meal barcode", null=True)
    name = models.TextField(help_text="Meal name")

    def __str__(self):
        return f"{self.timestamp} - {self.user.username}"


class RecentSearch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    barcode = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]

    @classmethod
    def add_search(cls, user, barcode, name):
        new_search = cls.objects.create(user=user, barcode=barcode, name=name)

        user_searches = cls.objects.filter(user=user)
        if user_searches.count() > 5:
            oldest_search = user_searches.last()
            oldest_search.delete()

        return new_search


@receiver(post_save, sender=RecentSearch)
def limit_recent_searches(sender, instance, created, **kwargs):
    if created:
        user_searches = RecentSearch.objects.filter(user=instance.user)
        if user_searches.count() > 5:
            oldest_search = user_searches.last()
            oldest_search.delete()
