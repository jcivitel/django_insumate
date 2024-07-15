from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader

from .forms import QuickSearch
from .functions import get_product_info


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password")
    return render(request, "login.html")


@login_required
def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def dashboard(request):
    template = loader.get_template("dashboard.html")

    template_opts = dict()

    return HttpResponse(template.render(template_opts, request))


@login_required
def quick_product_search(request):
    template = loader.get_template("product_info.html")
    template_opts = dict()

    if request.method == "POST":
        quicksearchform = QuickSearch(request.POST)
        if quicksearchform.is_valid():
            barcode = quicksearchform.cleaned_data["barcode"]
            cached_result = cache.get(f"product:{barcode}")
            if cached_result is not None:
                template_opts["product_info"] = cached_result
            else:
                template_opts["product_info"] = get_product_info(barcode)
                cache.set(f"product:{barcode}", template_opts["product_info"], 60 * 60 * 24)
            template_opts["quicksearchform"] = quicksearchform
    else:
        quicksearchform = QuickSearch()
        template_opts["quicksearchform"] = quicksearchform
        template_opts["product_info"] = ""

    return HttpResponse(template.render(template_opts, request))
