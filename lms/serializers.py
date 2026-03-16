from rest_framework import serializers
from .models import Course, Lesson, Subscription
from .validators import LMSLinkValidator

class LessonSerializer(serializers.ModelSerializer):
    """Полный сериализатор урока для отдельных эндпоинтов."""

    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [LMSLinkValidator(field='video_url')]


class CourseLessonSerializer(serializers.ModelSerializer):
    """Урезанный сериализатор урока для вложенного вывода в курсе."""

    class Meta:
        model = Lesson
        fields = (
            "id",
            "title",
            "description",
            "preview",
            "video_url",
        )


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = CourseLessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = (
            "id",
            "title",
            "preview",
            "description",
            "lessons_count",
            "lessons",
            'is_subscribed'
        )

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Subscription.objects.filter(user=request.user, course=obj).exists()