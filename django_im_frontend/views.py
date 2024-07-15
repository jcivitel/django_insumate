from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader

from django_im_backend.models import UserProfile
from .forms import QuickSearch, UserProfileForm, CalculatorForm
from .functions import get_product_info, get_current_factor


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
                print(f"got cache for {cached_result["name"]}")
            else:
                template_opts["product_info"] = get_product_info(barcode)
                cache.set(
                    f"product:{barcode}", template_opts["product_info"], 60 * 60 * 24
                )
            template_opts["quicksearchform"] = quicksearchform
    else:
        quicksearchform = QuickSearch()
        template_opts["quicksearchform"] = quicksearchform
        template_opts["product_info"] = ""

    return HttpResponse(template.render(template_opts, request))


@login_required
def edit_profile(request):
    template = loader.get_template("edit_profile.html")
    template_opts = dict()
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile(user=request.user)

    if request.method == "POST":
        profile_form = UserProfileForm(request.POST, instance=profile)
        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.user = request.user
            profile.save()
    else:
        profile_form = UserProfileForm(instance=profile)
        template_opts["profile_form"] = profile_form

    return HttpResponse(template.render(template_opts, request))


@login_required
def calculate(request, barcode=None):
    template = loader.get_template("calculator.html")
    template_opts = dict()
    if barcode is None:
        calc_form = CalculatorForm()
        template_opts["calc_form"] = calc_form
        return HttpResponse(template.render(template_opts, request))

    profile = UserProfile.objects.get(user=request.user)

    time_of_day, current_factor = get_current_factor(profile)
    cached_result = cache.get(f"product:{barcode}")
    if cached_result is not None:
        template_opts["product_info"] = cached_result["carbs"]
    else:
        template_opts["product_info"] = get_product_info(barcode)["carbs"]
        cache.set(
            f"product:{barcode}", template_opts["product_info"], 60 * 60 * 24
        )

    template_opts['time_of_day'] = time_of_day
    template_opts['current_factor'] = current_factor

    return HttpResponse(template.render(template_opts, request))
