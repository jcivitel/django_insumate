from rest_framework import viewsets

from django_im_backend.models import UserProfile
from .serializers import UserExportSer


class UserExport(viewsets.ModelViewSet):
    # TODO: filter to user:
    queryset = UserProfile.objects.all()
    serializer_class = UserExportSer
