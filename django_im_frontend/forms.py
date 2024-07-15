from django import forms


class QuickSearch(forms.Form):
    barcode = forms.CharField(
        max_length=100,
        label="Barcode",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
