from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from .models import Product, Category


def index(request: HttpRequest) -> HttpResponse :
    context = {
        "latest_men_products": Product.objects.filter(for_gender="men").order_by("-timestamp")[:20],
        "latest_women_products": Product.objects.filter(for_gender="women").order_by("-timestamp")[:20],
        "best_sold_men_products": Product.objects.filter(for_gender="men").order_by("sold")[:20],
        "best_sold_women_products": Product.objects.filter(for_gender="women").order_by("sold")[:20],
        "men_categories": Category.objects.filter(featured_in="men").exclude(image='').order_by("?")[:4],
        "women_categories": Category.objects.filter(featured_in="women").exclude(image='').order_by("?")[:4]
    }
    return render(request, "core/index.html", context)


def cart(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        print(request.body)
        return JsonResponse("ok", safe=False)
    return HttpResponse("Hello World")
