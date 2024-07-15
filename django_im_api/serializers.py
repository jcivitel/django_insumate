from rest_framework import serializers

from django_im_backend.models import UserProfile


class UserExportSer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["user", "weight", "height"]
