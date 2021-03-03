from django.http import JsonResponse, HttpRequest, Http404
from decorators.authorization import only_authorized
from core.models import Product
import math
import json

@only_authorized
def cart(request: HttpRequest) -> JsonResponse:
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


def product_list(request: HttpRequest) -> JsonResponse:
    if request.method == "GET":
        per_page = 1
        page = int(request.GET.get("page", "1")) - 1
        category: str = request.GET.get("category", None)
        gender: str = request.GET.get("gender", None)
        skip = page * per_page
        product_query = []
        if category != None and gender != None:
            product_query = Product.objects.filter(categories__name__iexact=category, for_gender=gender)
        elif category != None:
            print("category")
            product_query = Product.objects.filter(categories__name__iexact=category)
        elif gender != None:
            product_query = Product.objects.filter(for_gender=gender)
        else:
            product_query = Product.objects.all()
        
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
