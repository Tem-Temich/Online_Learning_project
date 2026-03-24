import stripe
from django.conf import settings


stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_product(payment):
    if payment.course:
        product_name = payment.course.title
    else:
        product_name = payment.lesson.title

    product = stripe.Product.create(
        name=product_name,
    )
    return product


def create_stripe_price(payment, product_id):
    price = stripe.Price.create(
        currency="rub",
        unit_amount=int(payment.amount * 100),
        product=product_id,
    )
    return price


def create_stripe_session(price_id):
    session = stripe.checkout.Session.create(
        success_url="https://example.com/success/",
        cancel_url="https://example.com/cancel/",
        line_items=[
            {
                "price": price_id,
                "quantity": 1,
            }
        ],
        mode="payment",
    )
    return session