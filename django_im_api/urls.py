from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    ProductInfoViewSet,
    UserProfileExport,
    MealEntryExport,
    RecentSearchExport,
)

router = DefaultRouter()
router.register(r"userinfo", UserProfileExport, basename="userinfo")
router.register(r"meal-entries", MealEntryExport, basename="meal-entries")
router.register(r"recent-searches", RecentSearchExport, basename="recent-searches")
router.register(r"product", ProductInfoViewSet, basename="product")
urlpatterns = [
    path("v1/", include(router.urls)),
]
