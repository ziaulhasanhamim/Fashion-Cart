from django.shortcuts import render, Http404, redirect
from typing import Dict
from django.http import HttpRequest, HttpResponse, JsonResponse
from decorators.authorization import only_authorized
import json
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
        context["reviews"] = request.user.reviews.order_by("-timestamp")
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
            if review_query.exists:
                review = review_query.first()
                review.rating = rating
                review.message = msg
                review.save()
            else:
                Review.objects.create(rating=rating, message=msg, product_id=product_id, user=request.user)
            return redirect(request.POST.get("returnurl", "/"))
        raise Http404()
    return redirect("/")
