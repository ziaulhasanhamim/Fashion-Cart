from django.shortcuts import render
from typing import Dict
from django.http import HttpRequest, HttpResponse, JsonResponse
from decorators.authorization import only_authorized
import json
from .models import Product, Category, Slider, Order, OrderItem


def index(request: HttpRequest) -> HttpResponse :
    context = {
        "latest_men_products": Product.objects.filter(for_gender="men").order_by("-timestamp")[:20],
        "latest_women_products": Product.objects.filter(for_gender="women").order_by("-timestamp")[:20],
        "best_sold_men_products": Product.objects.filter(for_gender="men").order_by("sold")[:20],
        "best_sold_women_products": Product.objects.filter(for_gender="women").order_by("sold")[:20],
        "men_categories": Category.objects.filter(featured_in="men").exclude(image='').order_by("?")[:4],
        "women_categories": Category.objects.filter(featured_in="women").exclude(image='').order_by("?")[:4],
        "sliders": Slider.objects.filter(enabled=True),
    }
    return render(request, "core/index.html", context)


@only_authorized
def cart(request: HttpRequest) -> HttpResponse:
    context: Dict[str, str] = dict()
    if request.method == "POST":
        try:
            productId = int(request.POST["id"])
            quantity = int(request.POST["quantity"])
            context["return_url"] = request.POST.get("returnurl", "/")
            if quantity == 0 or abs(quantity) > 1000:
                raise Exception("")
        except Exception as e:
            return HttpResponse("error occured. bad request.")
        products = Product.objects.filter(id=productId)

        if products.exists():
            product = products.first()
            items = request.cart.order_items.filter(product=product)
            if items.exists():
                item = items.first()
                item.quantity += quantity
                if item.quantity < 1:
                    item.delete()
                else:
                    item.save()
            elif quantity > 0:
                request.cart.order_items.create(product=product, quantity=1)
        else:
            return HttpResponse("error occured. bad request.")
    elif request.method == "GET":
        context["return_url"] = request.GET.get("returnurl", "/")
    return render(request, "core/cart.html", context)


@only_authorized
def cart_items(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        items = request.cart.get_items();
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


def product_detail(request: HttpRequest, slug: str) -> HttpResponse :
    product_query = Product.objects.filter(url=slug)
    if product_query.exists():
        return render(request, "core/product-detail.html", {"product": product_query.first()})
    return render(request, "404.html", {"msg": "Product Not Found"}, status=404)


def handler404(request: HttpRequest, exception) -> HttpResponse :
    return render(request, "404.html", {"msg": "Page Not Found"}, status=404)
