from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Payment, User
from .serializers import PaymentSerializer, UserProfileSerializer


class PaymentListAPIView(ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def get_queryset(self):
        qs = super().get_queryset()

        course_id = self.request.query_params.get("course")
        lesson_id = self.request.query_params.get("lesson")
        payment_method = self.request.query_params.get("payment_method")
        ordering = self.request.query_params.get("ordering")

        if course_id:
            qs = qs.filter(course_id=course_id)

        if lesson_id:
            qs = qs.filter(lesson_id=lesson_id)

        if payment_method:
            qs = qs.filter(payment_method=payment_method)

        if ordering in ("payment_date", "-payment_date"):
            qs = qs.order_by(ordering)

        return qs


class UserProfileAPIView(RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user
