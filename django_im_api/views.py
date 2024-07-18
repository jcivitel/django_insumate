from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from django_im_backend.models import UserProfile
from django_im_frontend.functions import get_product_info
from .serializers import UserExportSerializer


class UserExport(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserExportSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)


class ProductInfoViewSet(viewsets.ViewSet):
    def list(self, request):
        return Response({
            "help": "you need to append the product id",
            "example": f"{request.path}/4008400221823"
        })

    def retrieve(self, request, pk=None):
        product_info = get_product_info(pk)
        if product_info:
            return Response(product_info)
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
