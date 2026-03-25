from django.db import models
from django.conf import settings

class Course(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    title = models.CharField(max_length=200)
    preview = models.ImageField(upload_to='courses/', blank=True, null=True)
    description = models.TextField()
    materials_updated_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Дата последнего обновления материалов"
    )


class Lesson(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    preview = models.ImageField(upload_to='lessons/', blank=True, null=True)
    video_url = models.URLField()

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons'
    )



class Subscription(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='subscriptions'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='subscriptions'
    )

    class Meta:
        unique_together = ('user', 'course')