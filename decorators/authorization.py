from typing import Callable
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, reverse


def only_authorized(func: Callable[[HttpRequest], HttpResponse]) -> Callable[[HttpRequest], HttpResponse]:
    def wrapper(request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        else:
            return redirect(reverse("accounts:login") + f"?returnurl={request.path}")
    return wrapper


def only_anonymous(func: Callable[[HttpRequest], HttpResponse]) -> Callable[[HttpRequest], HttpResponse]:
    def wrapper(request: HttpRequest) -> HttpResponse:        
        if not request.user.is_authenticated:
            return func(request)
        else:
            return redirect("core:index")
    return wrapper


def only_admin(func: Callable[[HttpRequest], HttpResponse]) -> Callable[[HttpRequest], HttpResponse]:
    def wrapper(request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if request.user.is_authenticated and request.user.is_superuser:
            return func(request, *args, **kwargs)
        else:
            return redirect(f"/admin/login?next={request.path}")
    return wrapper
