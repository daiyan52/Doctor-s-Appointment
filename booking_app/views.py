from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegistrationForm, SlotBookingForm, VaccinationCenterForm
from .models import VaccinationSlot, VaccinationCenter
from django.db.models import Count


def dashboard(request):
    bookings = VaccinationSlot.objects.filter(user=request.user).order_by(
        "-date", "-slot_time"
    )
    return render(request, "dashboard.html", {"bookings": bookings})


def home_view(request):
    return render(request, "home.html")


def signup_view(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("book_slot")
    else:
        form = UserRegistrationForm()
    return render(request, "signup.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("book_slot")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def book_slot(request):
    if request.method == "POST":
        form = SlotBookingForm(request.POST)
        if form.is_valid():
            slot = form.save(commit=False)
            slot.user = request.user
            slots_count = VaccinationSlot.objects.filter(
                vaccination_center=slot.vaccination_center, date=slot.date
            ).count()

            if slots_count < slot.vaccination_center.total_slots_per_day:
                slot.save()
                return redirect("success_page")
            else:
                form.add_error(None, "No slots available for the selected date")
    else:
        form = SlotBookingForm()
    return render(request, "book_slot.html", {"form": form})


@login_required
def add_center(request):
    if not request.user.is_superuser:
        return redirect("login")

    if request.method == "POST":
        form = VaccinationCenterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home_view")
    else:
        form = VaccinationCenterForm()
    return render(request, "add_center.html", {"form": form})


def success_page(request):
    return render(request, "success.html")


def search_centers(request):
    query = request.GET.get("query", "")
    centers = VaccinationCenter.objects.filter(name__icontains=query)
    return render(request, "search_centers.html", {"centers": centers, "query": query})


@login_required
def dosage_details(request):
    if not request.user.is_superuser:
        return redirect("login")

    centers = VaccinationCenter.objects.annotate(dosages_given=Count("vaccinationslot"))
    return render(request, "dosage_details.html", {"centers": centers})
