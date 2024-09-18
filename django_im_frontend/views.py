import base64
import io
import json
from datetime import timedelta, datetime

from PIL import Image
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Sum
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST
from pyzbar.pyzbar import decode

from django_im_api.functions import check_openfood_connection
from django_im_backend.models import UserProfile, MealEntry, RecentSearch
from .decorators import check_registration_enabled, not_logged_in
from .forms import UserProfileForm, CalculatorForm, MealEntryForm, RegisterForm
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


@user_passes_test(not_logged_in, login_url="dashboard")
@check_registration_enabled
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})


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
    try:
        RecentSearch.add_search(
            request.user, barcode, template_opts["product_info"]["name"]
        )
    except:
        messages.error(request, "Product is not complete in our database 😥")

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


@login_required
def statistics_view(request):
    template = loader.get_template("stats.html")
    template_opts = dict()

    today = timezone.now().date()

    # Startzeit auf Mitternacht setzen
    start_of_day = datetime.combine(today, datetime.min.time())
    start_of_day = timezone.make_aware(start_of_day)

    # Zeitabstände von 30 Minuten erstellen
    time_intervals = [
        (
            start_of_day + timedelta(minutes=30 * i),
            start_of_day + timedelta(minutes=30 * (i + 1)),
        )
        for i in range(48)  # 48 30-Minuten-Intervalle in einem Tag
    ]

    # KEs für jedes Intervall summieren
    ke_data = []
    for start, end in time_intervals:
        sum_ke = (
            MealEntry.objects.filter(
                user=request.user, timestamp__range=(start, end)
            ).aggregate(Sum("KE"))["KE__sum"]
            or 0
        )
        ke_data.append({"time": start.strftime("%H:%M"), "ke": round(sum_ke, 2)})
    template_opts["chart_data"] = json.dumps(ke_data)

    entry_list = []
    for start, end in time_intervals:
        entries = MealEntry.objects.values_list("timestamp", "KE", "name").filter(
            user=request.user, timestamp__range=(start, end)
        )
        filtered_entries = [item for item in entries if item[2]]
        if filtered_entries:
            entry_list.append(
                {"time": start.strftime("%H:%M"), "entries": filtered_entries}
            )

    template_opts["entry_list"] = entry_list

    return HttpResponse(template.render(template_opts, request))


@require_POST
def barcode_scanner(request):
    try:
        image_data = request.POST.get("image")
        if not image_data:
            return JsonResponse({"success": False, "message": "Kein Bild empfangen"})

        image_data = image_data.split(",")[1]
        image_data = base64.b64decode(image_data)

        image = Image.open(io.BytesIO(image_data))

        decoded_objects = decode(image)

        if decoded_objects:
            barcode_data = decoded_objects[0].data.decode("utf-8")
            return JsonResponse({"success": True, "barcode": barcode_data})
        else:
            return JsonResponse({"success": False, "message": "Kein Barcode gefunden"})

    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)})


@login_required
def create_meal_entry(request):
    template = loader.get_template("create_meal_entry.html")
    template_opts = dict()

    if request.method == "POST":
        form = MealEntryForm(request.POST)
        if form.is_valid():
            meal_entry = form.save(commit=False)
            meal_entry.user = request.user
            meal_entry.save()
            return redirect("dashboard")
    else:
        form = MealEntryForm()
        template_opts["form"] = form

        try:
            profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            messages.success(request, "Please update your profile first 😊")
            return HttpResponseRedirect(reverse("profile"))

        time_of_day, current_factor = get_current_factor(profile)

        template_opts["time_of_day"] = time_of_day
        template_opts["current_factor"] = current_factor

    return HttpResponse(template.render(template_opts, request))
