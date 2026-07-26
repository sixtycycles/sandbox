from django import forms
from .models import Item, Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            "user",
            "vendor",
        )

    def save(self, commit: bool = True) -> Order:
        order: Order = super().save(commit)
        order.save()
        return order


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
        # fields = ("order", "unit", "quantity", "cost_per_unit", "catalog_number", "description", "link_to_item")

    def save(self, commit: bool = True) -> Item:
        item: Item = super().save(commit)
        item.save()
        return item
