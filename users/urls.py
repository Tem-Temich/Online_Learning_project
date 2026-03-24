from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    PaymentListAPIView,
    UserProfileAPIView,
    UserRegisterAPIView,
    UserViewSet,
PaymentCreateAPIView
)

router = DefaultRouter()
router.register("users", UserViewSet, basename="user")

urlpatterns = [
    path("payments/", PaymentListAPIView.as_view(), name="payments-list"),
    path("profile/", UserProfileAPIView.as_view(), name="user-profile"),
    path("register/", UserRegisterAPIView.as_view(), name="user-register"),
    path("", include(router.urls)),
    path("payments/create/", PaymentCreateAPIView.as_view(), name="payment-create"),
]

