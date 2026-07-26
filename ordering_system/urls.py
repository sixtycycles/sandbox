from django.urls import path

from .views import (
    item_create_view,
    item_delete_view,
    item_detail_view,
    item_edit_view,
    order_add_item_view,
    order_create_view,
    order_delete_view,
    order_detail_view,
    order_list_view,
    order_edit_view,
)

urlpatterns = [
    path("item/<int:pk>/create/", item_create_view, name="item-create"),
    path("item/<int:pk>/edit/", item_edit_view, name="item-edit"),
    path("item/<int:pk>/delete/", item_delete_view, name="item-delete"),
    path("item/<int:pk>/", item_detail_view, name="item-detail"),
    path("create/", order_create_view, name="order-create"),
    path("<int:pk>/edit/", order_edit_view, name="order-edit"),
    path("<int:pk>/add_item/", order_add_item_view, name="order-add-item"),
    path("<int:pk>/delete/", order_delete_view, name="order-delete"),
    path("<int:pk>/", order_detail_view, name="order-detail"),
    path("", order_list_view, name="order-list"),
]
