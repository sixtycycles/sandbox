from django import forms
from .models import Item, Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            "vendor",
        )


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = (
            "unit",
            "quantity",
            "cost_per_unit",
            "catalog_number",
            "description",
            "link_to_item",
        )
