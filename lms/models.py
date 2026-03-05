from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=200)
    preview = models.ImageField(upload_to='courses/', blank=True, null=True)
    description = models.TextField()


class Lesson(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    preview = models.ImageField(upload_to='lessons/', blank=True, null=True)
    video_url = models.URLField()

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons'
    )