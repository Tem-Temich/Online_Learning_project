from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from lms.models import Course, Subscription


@shared_task
def send_course_update_email(course_id):
    course = Course.objects.get(pk=course_id)

    emails = list(
        Subscription.objects.filter(course=course, user__is_active=True)
        .exclude(user__email="")
        .values_list("user__email", flat=True)
        .distinct()
    )

    if not emails:
        return "Нет подписчиков"

    subject = f"Обновление курса: {course.title}"
    message = (
        f"Курс «{course.title}» был обновлён.\n"
        f"Проверьте новые материалы в личном кабинете."
    )

    sent = 0
    for email in emails:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
        sent += 1

    return f"Отправлено писем: {sent}"