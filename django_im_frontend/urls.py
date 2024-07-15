from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("product-search/", views.quick_product_search, name="quick_product_search"),
    path("profile/", views.edit_profile, name="profile"),
]
