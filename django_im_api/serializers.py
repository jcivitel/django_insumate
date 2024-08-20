from django.contrib.auth.models import User
from rest_framework import serializers

from django_im_backend.models import UserProfile, MealEntry, RecentSearch


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            "user",
            "height",
            "weight",
            "morning_factor",
            "noon_factor",
            "evening_factor",
        ]


class MealEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = MealEntry
        fields = ["KE", "timestamp", "barcode", "name"]


class RecentSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecentSearch
        fields = ["barcode", "name", "timestamp"]
