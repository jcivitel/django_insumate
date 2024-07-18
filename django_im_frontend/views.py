from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import loader
from django.urls import reverse
from django.utils import timezone

from django_im_backend.models import UserProfile, MealEntry, RecentSearch
from .forms import QuickSearch, UserProfileForm, CalculatorForm
from .functions import get_product_info, get_current_factor


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"WELCOME {user}❤️")
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password")
    return render(request, "login.html")


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out 🫡")
    return redirect("login")


@login_required
def dashboard(request):
    template = loader.get_template("dashboard.html")
    template_opts = dict()
    thirty_minutes_ago = timezone.now() - timedelta(minutes=30)

    recent_entries = MealEntry.objects.filter(
        user=request.user, timestamp__gte=thirty_minutes_ago
    ).order_by("-timestamp")

    template_opts["recent_entries"] = recent_entries
    template_opts["sum"] = recent_entries.aggregate(Sum("KE"))["KE__sum"] or 0

    template_opts["recent_searches"] = RecentSearch.objects.filter(user=request.user)[
        :5
    ]

    return HttpResponse(template.render(template_opts, request))


@login_required
def quick_product_search(request):
    template = loader.get_template("product_info.html")
    template_opts = dict()

    if request.method == "POST":
        quicksearchform = QuickSearch(request.POST)
        if quicksearchform.is_valid():
            barcode = quicksearchform.cleaned_data["barcode"]
            template_opts["product_info"] = get_product_info(barcode)
            template_opts["quicksearchform"] = quicksearchform
            if template_opts["product_info"] is None:
                messages.error(request, "Invalid barcode 😯")
    else:
        quicksearchform = QuickSearch()
        template_opts["quicksearchform"] = quicksearchform

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
            messages.success(request, "Your profile has been updated 😎")
            template_opts["profile_form"] = profile_form
    else:
        profile_form = UserProfileForm(instance=profile)
        template_opts["profile_form"] = profile_form

    return HttpResponse(template.render(template_opts, request))


@login_required
def calculate(request, barcode=None):
    template = loader.get_template("calculator.html")
    template_opts = dict()
    if barcode is None and request.method == "GET":
        calc_form = CalculatorForm()
        template_opts["calc_form"] = calc_form
        return HttpResponse(template.render(template_opts, request))

    if request.method == "POST":
        calc_form = CalculatorForm(request.POST)
        if calc_form.is_valid():
            if get_product_info(calc_form.cleaned_data["barcode"]) is not None:
                return HttpResponseRedirect(
                    f"/calculator/{calc_form.cleaned_data["barcode"]}"
                )
            else:
                messages.error(request, "Invalid barcode 😯")
                return HttpResponseRedirect(reverse("calculator"))

    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        messages.success(request, "Please update your profile first 😊")
        return HttpResponseRedirect(reverse("profile"))

    time_of_day, current_factor = get_current_factor(profile)
    template_opts["product_info"] = get_product_info(barcode)

    template_opts["time_of_day"] = time_of_day
    template_opts["current_factor"] = current_factor
    RecentSearch.add_search(
        request.user, barcode, template_opts["product_info"]["name"]
    )

    return HttpResponse(template.render(template_opts, request))


@login_required
def set_meal(request):
    if request.method == "POST":
        MealEntry.objects.create(
            user=request.user,
            KE=request.POST["suggested_ce"],
            barcode=request.POST["barcode"],
            name=get_product_info(request.POST["barcode"])["name"],
        )
        messages.success(request, "Your meal has been set😉")
    return HttpResponseRedirect(reverse("dashboard"))


@login_required
def delete_entry(request, entry_id):
    MealEntry.objects.get(id=entry_id).delete()
    messages.success(request, "Your entry has been deleted😌")
    return HttpResponseRedirect(reverse("dashboard"))
