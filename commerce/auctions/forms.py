from django import forms

CATEGORIES_CHOICES = [
    ("fashion", "Fashion"),
    ("electronics", "Electronics"),
    ("home", "Home"),
    ("hobby", "Hobby"),
    ("toys", "Toys"),
    ("other", "Other")
]

DURATION_CHOICES = [
    ("3", "3 days"),
    ("7", "7 days"),
    ("14", "14 days"),
    ("30", "30 days")
]


class ListingForm(forms.Form):
    title = forms.CharField(
        label="Title",
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "autofocus": None
            }
        )
    )
    category = forms.ChoiceField(
        label="Category",
        choices=CATEGORIES_CHOICES,
        widget=forms.Select(
            attrs={
                "class": "custom-select"
            }
        )
    )
    photo = forms.FileField(
        label="Photo",
        required=False,
        widget=forms.FileInput(
            attrs={
                "class": "custom-file-input",
                "aria-describedby": "item-photo-input"
            }
        )
    )
    description = forms.CharField(
        label="Item Description",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 8
                }
            )
        )
    duration = forms.ChoiceField(
        label="Duraion",
        choices=DURATION_CHOICES,
        widget=forms.Select(
            attrs={
                "class": "custom-select"
            }
        )
    )
    start_price = forms.DecimalField(
        min_value=1,
        max_digits=13,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            "class": "form-control"
        }),
    )
    quantity = forms.IntegerField(
        min_value=0,
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )


class BidForm(forms.Form):
    value = forms.DecimalField(
        min_value=0,
        max_digits=13,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            "class": "form-control"
        })
    )
