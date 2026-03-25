from datetime import timedelta

from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils import timezone


@shared_task
def deactivate_inactive_users():
    User = get_user_model()
    cutoff = timezone.now() - timedelta(days=30)

    updated_count = (
        User.objects.filter(
            is_active=True,
            last_login__lt=cutoff,
        )
        .exclude(is_staff=True)
        .exclude(is_superuser=True)
        .update(is_active=False)
    )

    return f"Заблокировано пользователей: {updated_count}"