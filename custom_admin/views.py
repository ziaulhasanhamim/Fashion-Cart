from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from typing import Dict
from core.models import Order
from decorators.authorization import only_admin


@only_admin
def orders(request: HttpRequest) -> HttpResponse:
    context: Dict[str, object] = dict()
    context["orders"] = Order.objects.filter(date_ordered__isnull=False);
    return render(request, "custom_admin/orders.html", context)
