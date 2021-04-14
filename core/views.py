from django.shortcuts import render, Http404, redirect
from django.db.models import Avg
from typing import Dict
from django.http import HttpRequest, HttpResponse, JsonResponse
from decorators.authorization import only_authorized
import json
import datetime
from .models import Product, Category, Slider, Order, OrderItem, Review


def index(request: HttpRequest) -> HttpResponse :
    context = {
        "latest_men_products": Product.objects.filter(for_gender="men").order_by("-timestamp").prefetch_related("categories")[:20],
        "latest_women_products": Product.objects.filter(for_gender="women").order_by("-timestamp").prefetch_related("categories")[:20],
        "best_sold_men_products": Product.objects.filter(for_gender="men").order_by("sold").prefetch_related("categories")[:20],
        "best_sold_women_products": Product.objects.filter(for_gender="women").order_by("sold").prefetch_related("categories")[:20],
        "men_categories": Category.objects.filter(featured_in="men").exclude(image='').order_by("?")[:4],
        "women_categories": Category.objects.filter(featured_in="women").exclude(image='').order_by("?")[:4],
        "sliders": Slider.objects.filter(enabled=True),
    }
    return render(request, "core/index.html", context)


def test(request):
    try:
        print(datetime.datetime.strptime(request.POST["date"], '%Y-%m-%d, %H:%M:%S'))
    except ValueError:
        print(datetime.datetime.strptime(request.POST["date"], '%Y-%m-%d'))
    return render(request, "core/test.html", {})


@only_authorized
def cart(request: HttpRequest) -> HttpResponse:
    context: Dict[str, str] = dict()
    if request.method == "POST":
        try:
            productId = int(request.POST.get("id", 0))
            quantity = int(request.POST.get("quantity", 0))
            context["return_url"] = request.POST.get("returnurl", "/")
            if quantity == 0 or abs(quantity) > 1000:
                raise Exception("")
        except Exception as e:
            return HttpResponse(f"error occured. bad request.")
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
                request.cart.order_items.create(product=product, quantity=quantity)
        else:
            return HttpResponse("error occured. bad request.")
    elif request.method == "GET":
        context["return_url"] = request.GET.get("returnurl", "/")
    return render(request, "core/cart.html", context)


def product_detail(request: HttpRequest, slug: str) -> HttpResponse :
    product_query = Product.objects.filter(url=slug)
    context: Dict[str, object] = dict()
    if product_query.exists():
        product = product_query.first()
        context["product"] = product
        context["user_given_review"] = False
        context["user_review"] = None
        if request.user.is_authenticated:
            review_query = Review.objects.filter(product=product, user=request.user)
            context["user_given_review"] = review_query.exists()
            context["user_review"] = review_query.first() if context["user_given_review"] else None
        return render(request, "core/product-detail.html", context)
    return render(request, "404.html", {"msg": "Product Not Found"}, status=404)


def handler404(request: HttpRequest, exception) -> HttpResponse :
    return render(request, "404.html", {"msg": "Page Not Found"}, status=404)


@only_authorized
def update_reviews(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        product_id = int(request.POST.get("productId", "0"))
        product_query = Product.objects.filter(id=product_id)
        if product_query.exists():
            rating = float(request.POST.get("rating", "5.0"))
            msg = request.POST.get("message", "")
            review_query = Review.objects.filter(product_id=product_id, user=request.user)
            if review_query.exists():
                review = review_query.first()
                review.rating = rating
                review.message = msg
                review.save()
            else:
                Review.objects.create(rating=rating, message=msg, product_id=product_id, user=request.user)
            return redirect(request.POST.get("returnurl", "/"))
        raise Http404()
    return redirect("/")


def products(request: HttpRequest) -> HttpResponse:
    context: Dict[str, object] = dict()
    context["categories"] = Category.objects.all()
    return render(request, "core/products.html", context)


def category_products(request: HttpRequest, category: str) -> HttpResponse:
    context: Dict[str, object] = dict()
    context["category"] = category
    context["categories"] = Category.objects.all()
    return render(request, "core/products.html", context)


def gender_products(request: HttpRequest, gender: str) -> HttpResponse:
    context: Dict[str, object] = dict()
    context["gender"] = gender
    context["categories"] = Category.objects.all()
    return render(request, "core/products.html", context)


def category_gender_products(request: HttpRequest, category: str, gender: str) -> HttpResponse:
    context: Dict[str, object] = dict()
    context["category"] = category
    context["gender"] = gender
    context["categories"] = Category.objects.all()
    return render(request, "core/products.html", context)


@only_authorized
def checkout(request: HttpRequest) -> HttpResponse:
    if request.cart.items_count <= 0:
        return redirect("/")
    context: Dict[str, object] = dict()
    return render(request, "core/checkout.html", context)
