from core.models import Order
from django.http import HttpRequest
class CartMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response;

    def __call__(self, request: HttpRequest):
        if request.user.is_authenticated:
            order, created = Order.objects.get_or_create(user=request.user.customer, date_ordered__isnull=True)
            request.cart = order
        response = self.get_response(request)
        return response
    