from django import forms
from django.utils.translation import gettext_lazy as _
from virtualpools.models import Stock, StockInfo


class CreateStockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = (
            "name",
            "maker",
            "model_name",
            "spec",
        )


class CreateStockInfoForm(forms.ModelForm):
    class Meta:
        model = StockInfo
        fields = (
            "num_stock",
            "place",
            "is_new",
            "contact_person",
            "contact_info",
        )
