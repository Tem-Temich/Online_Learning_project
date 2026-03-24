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
            "stripe_product_id",
            "stripe_price_id",
            "stripe_session_id",
            "payment_link",
        )
        read_only_fields = (
            "user",
            "payment_date",
            "stripe_product_id",
            "stripe_price_id",
            "stripe_session_id",
            "payment_link",
        )
class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = (
            "course",
            "lesson",
            "amount",
            "payment_method",
        )

    def validate(self, attrs):
        course = attrs.get("course")
        lesson = attrs.get("lesson")

        if not course and not lesson:
            raise serializers.ValidationError(
                "Нужно указать либо курс, либо урок."
            )

        if course and lesson:
            raise serializers.ValidationError(
                "Нельзя одновременно указать и курс, и урок."
            )

        return attrs

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "phone",
            "city",
            "avatar",
            "is_active",
            "is_staff",
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


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "email",
            "password",
            "phone",
            "city",
            "avatar",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password1 = validated_data.pop("password")
        created_user = User.objects.create_user(password=password1, **validated_data)
        return created_user