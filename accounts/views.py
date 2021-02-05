from django.shortcuts import render, redirect
from typing import Dict
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
import string

def signup(request: HttpRequest) -> HttpResponse:
    context: Dict[str, str] = dict()
    if request.method == "POST":
        email: str = request.POST.get("email")
        uname: str = request.POST.get("uname")
        password: str = request.POST.get("pass")
        conf_pass: str = request.POST.get("conf_pass")
        is_uname_valid = False

        if uname != None and uname.isalnum():
            is_uname_valid = True
        elif uname != None:
            is_uname_valid = True
            for char in uname:
                if char not in "-_":
                    is_uname_valid = False
                    break;
        
        if password == None or password.__len__() < 8:
            context["pass_error"] = "Password must be atleast 8 chars long"
        elif password != conf_pass:
            context["conf_pass_error"] = "Password Doesnt match wth confirm password"
        elif not is_uname_valid:
            context["uname_error"] = "Username Contains invalid characters"
        elif email == None or User.objects.filter(email__iexact=email).exists():
            context["email_error"] = "Email Already Exists"
        elif User.objects.filter(username__iexact=uname).exists():
            context["uname_error"] = "Username Already Exists"
        else:
            User.objects.create_user(username=uname, email=email, password=password)
            return redirect("/")
        
    return render(request, "accounts/signup.html", context)
