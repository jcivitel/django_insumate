from django import forms

from django_im_backend.models import UserProfile


class QuickSearch(forms.Form):
    barcode = forms.CharField(
        max_length=100,
        label="Barcode",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["height", "weight", "morning_factor", "noon_factor", "evening_factor"]

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields["height"].widget.attrs.update({"class": "form-control"})
        self.fields["weight"].widget.attrs.update({"class": "form-control"})
        self.fields["morning_factor"].widget.attrs.update({"class": "form-control"})
        self.fields["noon_factor"].widget.attrs.update({"class": "form-control"})
        self.fields["evening_factor"].widget.attrs.update({"class": "form-control"})

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
    morning_factor = forms.FloatField(label="Morning factor", min_value=0, max_value=5, step_size=0.5)
    noon_factor = forms.FloatField(label="Lunch factor", min_value=0, max_value=5, step_size=0.5)
    evening_factor = forms.FloatField(label="Dinner factor", min_value=0, max_value=5, step_size=0.5)


class CalculatorForm(forms.Form):
    barcode = forms.CharField(
        max_length=100,
        label="Barcode",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
