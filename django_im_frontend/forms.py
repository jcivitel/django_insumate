from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django_im_backend.models import UserProfile, MealEntry


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {"class": "form-control text-emphasis", "placeholder": "username"}
        )
        self.fields["email"].widget.attrs.update(
            {"class": "form-control", "placeholder": "email"}
        )
        self.fields["password1"].widget.attrs.update(
            {"class": "form-control", "placeholder": "password"}
        )
        self.fields["password2"].widget.attrs.update(
            {"class": "form-control", "placeholder": "password again"}
        )


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["height", "weight", "morning_factor", "noon_factor", "evening_factor"]

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields["height"].widget.attrs.update(
            {"class": "form-control", "placeholder": "height"}
        )
        self.fields["weight"].widget.attrs.update(
            {"class": "form-control", "placeholder": "weight"}
        )
        self.fields["morning_factor"].widget.attrs.update(
            {"class": "form-control", "placeholder": "morning_factor"}
        )
        self.fields["noon_factor"].widget.attrs.update(
            {"class": "form-control", "placeholder": "noon_factor"}
        )
        self.fields["evening_factor"].widget.attrs.update(
            {"class": "form-control", "placeholder": "evening_factor"}
        )

    height = forms.FloatField(
        label="Size",
        help_text="Size in centimeters",
        min_value=0,
        max_value=300,
    )
    weight = forms.FloatField(
        label="Weight",
        help_text="weight in kilogramm",
        min_value=0,
        max_value=500,
    )
    morning_factor = forms.FloatField(
        label="Morning factor", min_value=0, max_value=5, step_size=0.5
    )
    noon_factor = forms.FloatField(
        label="Lunch factor", min_value=0, max_value=5, step_size=0.5
    )
    evening_factor = forms.FloatField(
        label="Dinner factor", min_value=0, max_value=5, step_size=0.5
    )


class CalculatorForm(forms.Form):
    barcode = forms.CharField(
        max_length=100,
        label="Barcode",
        widget=forms.NumberInput(
            attrs={"class": "form-control", "autofocus": "", "placeholder": "Barcode"}
        ),
    )


class MealEntryForm(forms.ModelForm):
    class Meta:
        model = MealEntry
        fields = ["KE", "name"]
        widgets = {
            "KE": forms.NumberInput(
                attrs={
                    "step": "0.1",
                    "class": "form-control",
                    "readonly": "",
                }
            ),
            "name": forms.TextInput(
                attrs={"class": "form-control mb-3", "placeholder": "Name"}
            ),
        }
