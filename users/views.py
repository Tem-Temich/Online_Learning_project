from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet

from lms.permissions import IsModerator
from .models import Payment, User
from .serializers import (
    PaymentSerializer,
    UserProfileSerializer,
    UserRegisterSerializer,
    UserSerializer,
PaymentCreateSerializer
)
from .services import create_stripe_product, create_stripe_price, create_stripe_session

class PaymentListAPIView(ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = (IsAuthenticated,)

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


class UserRegisterAPIView(CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = (AllowAny,)
    queryset = User.objects.all()


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsModerator)

class PaymentCreateAPIView(CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)

        product = create_stripe_product(payment)
        price = create_stripe_price(payment, product.id)
        session = create_stripe_session(price.id)

        payment.stripe_product_id = product.id
        payment.stripe_price_id = price.id
        payment.stripe_session_id = session.id
        payment.payment_link = session.url
        payment.save()