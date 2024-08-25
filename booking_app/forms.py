from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import VaccinationSlot, VaccinationCenter

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control w-100', 'placeholder': 'Enter your username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control w-100', 'placeholder': 'Enter your password'})
    )


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your username"})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Enter your email"})
    )
    password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Enter your password"})
    )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Confirm your password"})
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Enter your username"}
        )
        self.fields["email"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Enter your email"}
        )
        self.fields["password1"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Enter your password"}
        )
        self.fields["password2"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Confirm your password"}
        )


class SlotBookingForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"})
    )
    slot_time = forms.ChoiceField(
        choices=VaccinationSlot.SLOT_TIMES,
        widget=forms.Select(attrs={"class": "form-control"})
    )

    class Meta:
        model = VaccinationSlot
        fields = ['vaccination_center', 'date', 'slot_time']


class VaccinationCenterForm(forms.ModelForm):
    class Meta:
        model = VaccinationCenter
        fields = ["name", "address", "working_hours", "total_slots_per_day"]

    def __init__(self, *args, **kwargs):
        super(VaccinationCenterForm, self).__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Enter center name"}
        )
        self.fields["address"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Enter address"}
        )
        self.fields["working_hours"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Enter working hours"}
        )
        self.fields["total_slots_per_day"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Enter total slots per day"}
        )
