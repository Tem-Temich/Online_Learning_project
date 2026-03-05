from django.contrib import admin

from .models import User, Payment


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "is_active", "is_staff")
    search_fields = ("email",)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "payment_date", "course", "lesson", "amount", "payment_method")
    list_filter = ("payment_method", "payment_date")
