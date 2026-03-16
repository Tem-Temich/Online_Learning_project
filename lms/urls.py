from django.urls import path
from .views import (
    LessonListCreateAPIView,
    LessonRetrieveUpdateDestroyAPIView,
    SubscriptionAPIView
)

urlpatterns = [
    path("lessons/", LessonListCreateAPIView.as_view(), name="lesson-list"),
    path("lessons/<int:pk>/", LessonRetrieveUpdateDestroyAPIView.as_view(), name="lesson-detail"),
    path("subscription/", SubscriptionAPIView.as_view(), name="subscription"),]