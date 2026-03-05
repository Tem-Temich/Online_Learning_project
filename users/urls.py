from django.urls import path

from .views import PaymentListAPIView, UserProfileAPIView

urlpatterns = [
    path("payments/", PaymentListAPIView.as_view(), name="payments-list"),
    path("profile/", UserProfileAPIView.as_view(), name="user-profile"),
]

