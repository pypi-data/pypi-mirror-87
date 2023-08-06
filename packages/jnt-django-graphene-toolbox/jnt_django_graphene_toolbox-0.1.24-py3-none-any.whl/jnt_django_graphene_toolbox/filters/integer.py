from django import forms
from django_filters import Filter


class IntegerFilter(Filter):
    """Filter for integers."""

    field_class = forms.IntegerField
