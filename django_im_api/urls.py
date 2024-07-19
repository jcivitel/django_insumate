from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserExport, ProductInfoViewSet

router = DefaultRouter()
router.register(r"product", ProductInfoViewSet, basename="product")
router.register(r"user", UserExport, basename="user")

urlpatterns = [
    path("v1/", include(router.urls)),
]
