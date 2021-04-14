from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest, HttpResponse, Http404
from typing import Dict
from core.models import Order
from decorators.authorization import only_admin
import datetime


@only_admin
def orders(request: HttpRequest) -> HttpResponse:
    context: Dict[str, object] = dict()
    context["orders"] = Order.objects.filter(date_ordered__isnull=False).order_by("-date_ordered")
    return render(request, "custom_admin/orders.html", context)


@only_admin
def manage_orders(request: HttpRequest, id: int) -> HttpResponse:
    order = get_object_or_404(Order, id=id)
    if request.method == "POST":
        context: Dict[str, object] = dict()
        context["errors"] = dict()
        context["order"] = order
        status = request.POST.get("status", None)
        if status == None:
            return HttpResponse("Status Should be there", status=403)
        try:
            status = int(status)
        except Exception:
            return HttpResponse("Wrong Value For Status", status=403)
        if order.status not in [-1, 3] and order.status != status:
            cancellation_reason = request.POST.get("cancellation-reason", None)
            date_delivered = request.POST.get("date-delivered", None)
            if status == -1:
                if cancellation_reason:
                    order.status = status
                    order.cancellion_reason = cancellation_reason
                    order.save()
                    return redirect("custom_admin:orders")
                return HttpResponse("Cancellion Reason Should be there", status=403)
            if status == 3:
                if date_delivered:
                    validated_date = None
                    try:
                        validated_date = datetime.datetime.strptime(date_delivered, '%Y-%m-%d, %H:%M:%S')
                    except ValueError:
                        try:
                            validated_date = datetime.datetime.strptime(date_delivered, '%Y-%m-%d')
                        except ValueError:
                            context["errors"]["date_delivered"] = "Date and Time is not Formatted Correctly. Correct Format: '%Y-%m-%d, %H:%M:%S'. Example: 2005-11-19, 21:23:43"
                            context["status"] = 3
                            return render(request, "custom_admin/manage_orders.html", context)
                    if validated_date <= order.date_ordered.replace(tzinfo=None) or validated_date >= datetime.datetime.now():
                        context["errors"]["date_delivered"] = "Delivered Date Should be greater Than placed date and Less than Current DateTime"
                        context["status"] = 3
                        return render(request, "custom_admin/manage_orders.html", context)
                    order.status = status
                    order.date_delivered = validated_date
                    order.save()
                    return redirect("custom_admin:orders")
                return HttpResponse("Delivered Date Should be there", status=403)
            if status == 1 and order.status == 2:
                context["errors"]["status"] = "You can't make the order status Pending. It is already in Proccessing Stage"
                context["status"] = 1
                return render(request, "custom_admin/manage_orders.html", context)
            if status == 2:
                order.status = status
                order.save()
                return redirect("custom_admin:orders")
            return HttpResponse("Bad Request", status=403)
        return redirect("custom_admin:orders")
    if request.method == "GET":
        context: Dict[str, object] = dict()
        context["order"] = get_object_or_404(Order, id=id)
        return render(request, "custom_admin/manage_orders.html", context)
