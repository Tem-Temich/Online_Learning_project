from rest_framework import serializers

from lms.models import Course, Lesson
from lms.serializers import CourseSerializer, LessonSerializer
from .models import Payment, User


class PaymentSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    lesson = LessonSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = (
            "id",
            "user",
            "payment_date",
            "course",
            "lesson",
            "amount",
            "payment_method",
        )


class UserProfileSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "phone",
            "city",
            "avatar",
            "payments",
        )

