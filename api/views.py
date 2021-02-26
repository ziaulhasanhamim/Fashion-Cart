from django.http import JsonResponse, HttpRequest
from decorators.authorization import only_authorized
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
