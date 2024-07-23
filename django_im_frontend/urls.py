from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.edit_profile, name="profile"),
    path("calculator/", views.calculate, name="calculator"),
    path("calculator/<str:barcode>/", views.calculate, name="calculator"),
    path("set-meal/", views.set_meal, name="set_meal"),
    path("delete-entry/<int:entry_id>", views.delete_entry, name="delete-entry"),
    path("statistics/", views.statistics_view, name="statistics"),
    path("barcode-scanner/", views.barcode_scanner, name="barcode_scanner"),
]
