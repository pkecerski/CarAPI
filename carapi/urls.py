from django.urls import path, include
from rest_framework import routers
from . import views


# Automatic URL routing for the API
router = routers.DefaultRouter()
# Basename 'cars' added, because both /cars and /popular use the same queryset
# Plus it allows us to test reverse URL
router.register(r"cars", views.CarViewSet, basename="cars")
router.register(r"rate", views.RateViewSet, basename="rate")
router.register(r"popular", views.PopularViewSet, basename="popular")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "api-auth/", include("rest_framework.urls", namespace="rest_framework")
    ),
]
