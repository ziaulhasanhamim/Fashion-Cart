from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse, Http404
from typing import Dict
from core.models import Order
from decorators.authorization import only_admin


@only_admin
def orders(request: HttpRequest) -> HttpResponse:
    context: Dict[str, object] = dict()
    context["orders"] = Order.objects.filter(date_ordered__isnull=False).order_by("-date_ordered")
    return render(request, "custom_admin/orders.html", context)


@only_admin
def manage_orders(request: HttpRequest, id: int) -> HttpResponse:
    if request.method == "POST":
        print(request.POST)
        return HttpResponse("hello")
    if request.method == "GET":
        context: Dict[str, object] = dict()
        context["order"] = get_object_or_404(Order, id=id)
        return render(request, "custom_admin/manage_orders.html", context)
