from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserExport

router = DefaultRouter()
router.register(r"userexport", UserExport, basename="userexport")

urlpatterns = [
    path("v1/", include(router.urls)),
]
