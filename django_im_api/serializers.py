from rest_framework import serializers

from django_im_backend.models import UserProfile


class UserExportSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["user", "weight", "height", "morning_factor", "noon_factor", "evening_factor"]
