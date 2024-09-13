from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from django_im_backend.models import UserProfile, MealEntry, RecentSearch
from django_im_frontend.functions import get_product_info
from .functions import (
    check_mysql_connection,
    check_redis_connection,
    check_openfood_connection,
)
from .serializers import (
    UserProfileSerializer,
    MealEntrySerializer,
    RecentSearchSerializer,
)


class UserProfileExport(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)


class MealEntryExport(viewsets.ReadOnlyModelViewSet):
    serializer_class = MealEntrySerializer

    def get_queryset(self):
        return MealEntry.objects.filter(user=self.request.user)


class RecentSearchExport(viewsets.ReadOnlyModelViewSet):
    serializer_class = RecentSearchSerializer

    def get_queryset(self):
        return RecentSearch.objects.filter(user=self.request.user)


class ProductInfoViewSet(viewsets.ViewSet):
    def list(self, request):
        full_url = request.build_absolute_uri(request.path)
        example_url = f"{full_url}4008400221823"
        return Response(
            {
                "help": "you need to append the product id",
                "example": example_url,
            }
        )

    def retrieve(self, request, pk=None):
        product_info = get_product_info(pk)
        if product_info:
            return Response(product_info)
        return Response(
            {"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND
        )


class StatusAPIView(viewsets.ReadOnlyModelViewSet):
    def list(self, request, *args, **kwargs):
        mysql_status = check_mysql_connection()
        redis_status = check_redis_connection()
        openfood_status = check_openfood_connection()

        status = {
            "mysql": "up" if mysql_status else "down",
            "redis": "up" if redis_status else "down",
            "openfood_api": "up" if openfood_status else "down",
        }

        return Response(status)
