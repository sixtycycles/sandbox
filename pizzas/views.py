import json
from typing import Any, Dict, List, cast
from django.forms.models import BaseModelForm
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseRedirect
from django.http.request import HttpRequest
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_not_required
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView
from .forms import ItemForm, OrderForm
from .models import Item, Order


def _owned_order(request: HttpRequest, pk: int) -> Order:
    """Return the order with ``pk`` or raise 403 if it isn't owned by the user."""
    order = get_object_or_404(Order, pk=pk)
    if order.user_id != request.user.id:
        raise PermissionDenied
    return order


def _owned_item(request: HttpRequest, pk: int) -> Item:
    """Return the item with ``pk`` or raise 403 if its order isn't owned by the user."""
    item = get_object_or_404(Item, pk=pk)
    if item.order.user_id != request.user.id:
        raise PermissionDenied
    return item


@login_not_required
def landing_page(request):
    return render(request, "pizzas/landing.html")


def order_list_view(request):
    context = {}
    context["list_of_orders"] = Order.objects.filter(user=request.user)
    context["form"] = OrderForm()

    return render(request, "pizzas/order_list.html", context)


def order_create_view(request):
    context = {}
    form = OrderForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()

            return redirect("order-edit", pk=order.pk)

    context["form"] = form
    return render(request, "pizzas/order_create_form.html", context)


def order_detail_view(request, pk):
    context = {}
    context["order"] = _owned_order(request, pk)

    return render(request, "pizzas/order_detail.html", context)


def order_edit_view(request, pk):
    context = {}
    edit_this = _owned_order(request, pk)
    form = OrderForm(request.POST or None, instance=edit_this)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse("order-detail", kwargs={"pk": pk}))

    context["form"] = form

    return render(request, "pizzas/order_edit.html", context)


def order_delete_view(request, pk):
    context = {}
    obj = _owned_order(request, pk)

    if request.method == "POST":
        obj.delete()
        return HttpResponse("")

    return HttpResponseNotAllowed(
        [
            "POST",
        ]
    )


def item_create_view(request, pk):
    context = {}
    order = _owned_order(request, pk)

    form = ItemForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            item = form.save(commit=False)
            item.order = order
            item.save()
            return HttpResponseRedirect(reverse("item-detail", kwargs={"pk": item.pk}))

    context["form"] = form
    context["order_id"] = pk
    return render(request, "pizzas/item_create_form.html", context)


def item_edit_view(request, pk):
    context = {}
    item = _owned_item(request, pk)
    form = ItemForm(request.POST or None, instance=item)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse("item-detail", kwargs={"pk": item.pk}))

    context["form"] = form
    return render(request, "pizzas/item_edit_form.html", context)


def item_detail_view(request, pk):
    context = {}
    item = _owned_item(request, pk)
    context["item"] = item

    return render(request, "pizzas/item_detail.html", context)


def item_delete_view(request, pk):
    context = {}
    obj = _owned_item(request, pk)

    if request.method == "POST":
        obj.delete()
        return HttpResponse("")

    return HttpResponseNotAllowed(
        [
            "POST",
        ]
    )
