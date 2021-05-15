from django.http import JsonResponse, HttpRequest, Http404, HttpResponseForbidden
from decorators.authorization import only_authorized
from core.models import Product, ShippingAndBilling, PaymentOptionChoies, OrderStatusChoices
from django.db.models import Avg
from typing import Dict, List
import math
import json
import datetime
import time
from django.core.mail import send_mass_mail, send_mail
from django.conf import settings
from django.utils.html import strip_tags
from django.template.loader import render_to_string
import threading


@only_authorized
def cart(request: HttpRequest) -> JsonResponse:
    if request.method == "GET":
        items = request.cart.get_items()
        cart_items = [
            {
                "id": item.id,
                "title": item.product.title,
                "price": item.product.get_price(),
                "image": item.product.thumbnail.url,
                "quantity": item.quantity
            }
            for item in items
        ]
        return JsonResponse(cart_items, safe=False)

    if request.method == "POST":
        data = json.loads(request.body)
        if data.get("op", None) == "remove_all":
            request.cart.delete()
        elif data.get("op", None) == "add":
            items = request.cart.order_items.filter(id=data.get("id", 0))
            if items.exists():
                if data.get("quantity", 1) == 0 or abs(data.get("quantity", 1)) > 1000:
                    return JsonResponse("Bad Request", safe=False)
                item = items.first()
                item.quantity += data.get("quantity", 1)
                item.save()
            else:
                return JsonResponse("Bad Request", safe=False)
        elif data.get("op", None) == "remove":
            items = request.cart.order_items.filter(id=data.get("id", 0))
            if items.exists():
                items.first().delete()
        return JsonResponse("Ok", safe=False)


def product_list(request: HttpRequest) -> JsonResponse:
    if request.method == "GET":
        per_page = 1
        page = int(request.GET.get("page", "1")) - 1
        rating = float(request.GET.get("rating", "0.0"))
        category: str = request.GET.get("category", None)
        gender: str = request.GET.get("gender", None)
        max_price = float(request.GET.get("max", "9999999999.99"))
        min_price = float(request.GET.get("min", "0"))
        order_by = request.GET.get("order_by", "-timestamp")
        skip = page * per_page
        product_query = []
        if rating != 0.0:
            if category != None and gender != None:
                product_query = Product.objects.annotate(rating=Avg("reviews__rating")).filter(
                    categories__name__iexact=category,
                    for_gender=gender,
                    price__gte=min_price,
                    price__lte=max_price,
                    rating__gte=rating).order_by(order_by)

            elif category != None:
                product_query = Product.objects.annotate(rating=Avg("reviews__rating")).filter(
                    categories__name__iexact=category,
                    price__gte=min_price,
                    price__lte=max_price,
                    rating__gte=rating).order_by(order_by)

            elif gender != None:
                product_query = Product.objects.annotate(rating=Avg("reviews__rating")).filter(
                    for_gender=gender,
                    price__gte=min_price,
                    price__lte=max_price,
                    rating__gte=rating).order_by(order_by)

            else:
                product_query = Product.objects.annotate(rating=Avg("reviews__rating")).filter(
                    price__gte=min_price,
                    price__lte=max_price,
                    rating__gte=rating
                ).order_by(order_by)
        else:
            if category != None and gender != None:
                product_query = Product.objects.annotate(rating=Avg("reviews__rating")).filter(
                    categories__name__iexact=category,
                    for_gender=gender,
                    price__gte=min_price,
                    price__lte=max_price).order_by(order_by)

            elif category != None:
                product_query = Product.objects.annotate(rating=Avg("reviews__rating")).filter(
                    categories__name__iexact=category,
                    price__gte=min_price,
                    price__lte=max_price).order_by(order_by)

            elif gender != None:
                product_query = Product.objects.annotate(rating=Avg("reviews__rating")).filter(
                    for_gender=gender,
                    price__gte=min_price,
                    price__lte=max_price).order_by(order_by)

            else:
                product_query = Product.objects.annotate(rating=Avg("reviews__rating")).filter(
                    price__gte=min_price,
                    price__lte=max_price
                ).order_by(order_by)

        product_count = product_query.count()
        products_needs_to_render = product_query[skip:skip + per_page]
        products = [
            {
                "title": product.title,
                "summary": product.summary,
                "price": product.price,
                "discount_price": product.discount_price,
                "image": product.thumbnail.url,
                "url": product.url,
                "categories": [
                    category.name for category in product.categories.all()
                ],
                "avg_rating_start": product.get_avg_stars(),
                "review_count": product.reviews.count()
            }
            for product in products_needs_to_render
        ]
        paging_info = {
            "product_count": product_count,
            "page_count": math.ceil(product_count / per_page),
            "current_page": page + 1,
            "product_in_current_page": products_needs_to_render.count()
        }
        context = {
            "paging_info": paging_info,
            "products": products
        }
        return JsonResponse(context)
    return Http404()


@only_authorized
def shipping_charge(request: HttpRequest) -> JsonResponse:
    context: Dict[str, object] = dict()
    if request.method == "POST":
        body = json.loads(request.body)
        state: str = body.get("state", None)
        city: str = body.get("city", None)
        if state.lower() == "khulna" and city.lower() == "khulna":
            context["charge"] = 0
            return JsonResponse(context)
        context["charge"] = 4
        return JsonResponse(context)        


@only_authorized
def place_order(request: HttpRequest) -> JsonResponse:
    if request.method == "POST":
        body = json.loads(request.body)
        state: str = body.get("state", None)
        city: str = body.get("city", None)
        address: str = body.get("address", None)
        name: str = body.get("name", None)
        phone: str = body.get("phone", None)
        payment_option: str = body.get("paymentOption", "bkash")
        bkash_number: str = body.get("bkashNumber", None)
        if state and city and address and name and phone:
            if payment_option == "bkash" and not bkash_number:
                return HttpResponseForbidden("Bad Request")
            shipping = ShippingAndBilling()
            shipping.name = name
            shipping.state = state
            shipping.city = city
            shipping.address = address
            shipping.phone_number = phone
            if payment_option == "bkash":
                shipping.payment_option = PaymentOptionChoies.BKASH
                shipping.bkash_number = bkash_number
            else:                
                shipping.payment_option = PaymentOptionChoies.CASH_ON_DELIVERY
            if state.lower() == "khulna" and city.lower() == "khulna":
                shipping.shipping_charge = 0
            else:
                shipping.shipping_charge = 4
            shipping.save()
            request.cart.shipping = shipping
            request.cart.date_ordered = datetime.datetime.now()
            request.cart.status = OrderStatusChoices.PENDING
            request.cart.save()
            t1 = threading.Thread(target=cleanup_place_order, args=[request])
            t1.daemon = True
            t1.start()
            return JsonResponse("Updated", safe=False)


def cleanup_place_order(request: HttpRequest):
    for item in request.cart.order_items.all():
        item.product.sold += item.quantity
        item.product.save()
    send_new_order_email(["ziaulhasan174@gmail.com"], f"{request._get_scheme()}://{request.get_host()}/admin/orders/manage/{request.cart.id}")


def send_new_order_email(to_emails: List[str], url: str):
    from_email = settings.EMAIL_HOST_USER
    subject = "New Order Received"
    for to_email in to_emails: 
        html_message = render_to_string('core/order_email.html', {"email": to_email, "url": url})
        plain_message = strip_tags(html_message)
        send_mail(subject, plain_message, from_email, [to_email], fail_silently=False, html_message=html_message)
