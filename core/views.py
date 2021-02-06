from django.shortcuts import render
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
    if request.method == "POST":
        try:
            productId = int(request.POST["id"])
            quantity = int(request.POST["quantity"])
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
    return HttpResponse("Hello World")
