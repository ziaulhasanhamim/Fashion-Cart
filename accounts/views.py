from django.shortcuts import render, redirect
from typing import Dict
from django.contrib.auth.models import User
from django.contrib.auth import login as login_user, logout as logout_user
from django.http import HttpRequest, HttpResponse, Http404
import string
from core.models import Order
from decorators.authorization import only_anonymous, only_authorized


@only_anonymous
def signup(request: HttpRequest) -> HttpResponse:
    context: Dict[str, str] = dict()
    if request.method == "POST":
        email: str = request.POST.get("email")
        uname: str = request.POST.get("uname")
        password: str = request.POST.get("pass")
        conf_pass: str = request.POST.get("conf_pass")
        
        if password == None or password.__len__() < 8:
            context["pass_error"] = "Password must be atleast 8 chars long"
        elif password != conf_pass:
            context["conf_pass_error"] = "Password Doesnt match wth confirm password"
        elif uname == None:
            context["uname_error"] = "Username is required"
        elif email == None:
            context["email_error"] = "Email is required"
        elif User.objects.filter(email__iexact=email).exists():
            context["email_error"] = "Email Already Exists"
        elif User.objects.filter(username__iexact=uname).exists():
            context["uname_error"] = "Username Already Exists"
        else:
            User.objects.create_user(username=uname, email=email, password=password)
            return redirect("core:index")
        
    return render(request, "accounts/signup.html", context)


@only_anonymous
def login(request: HttpRequest) -> HttpResponse:
    context: Dict[str, str] = dict()

    if request.method == "POST":
        email: str = request.POST.get("email")
        password: str = request.POST.get("pass")
        user = User.objects.filter(email__iexact=email)

        if not user.exists():
            context["email_error"] = "Email Doesn't Exist"
        elif not user.first().check_password(password):
            context["pass_error"] = "Password Doesn't Match"
        else:
            login_user(request, user.first())
            if request.GET.get("returnurl", None) != None:
                return redirect(request.GET.get("returnurl"))
            return redirect("core:index")

    return render(request, "accounts/login.html", context)


def logout(request: HttpRequest) -> HttpResponse:
    logout_user(request)
    return redirect("accounts:login")


@only_authorized
def profile(request: HttpRequest) -> HttpResponse:
    context: Dict[str, object] = dict()
    return render(request, "accounts/profile.html", context)


@only_authorized
def orders(request: HttpRequest) -> HttpResponse:
    context: Dict[str, object] = dict()
    context["orders"] = Order.objects.filter(date_ordered__isnull=False).order_by("-date_ordered")
    return render(request, "accounts/orders.html", context)


@only_authorized
def order_details(request: HttpRequest, id: int) -> HttpResponse:
    context: Dict[str, object] = dict()
    order_query = Order.objects.filter(date_ordered__isnull=False, customer=request.user.customer, id=id)
    if order_query.exists():
        context["order"] = order_query.first()
        return render(request, "accounts/order-details.html", context)
    raise Http404()
