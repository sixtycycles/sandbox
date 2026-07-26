from django.db import models
from django.db.models.query import QuerySet
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from localflavor.us.models import USPostalCodeField, USZipCodeField, USStateField
from localflavor.us.us_states import US_STATES, STATE_CHOICES


# do a custom user so we can extend later if needed.
class User(AbstractUser):
    uid = models.CharField(max_length=10, default="0000000000")


class Vendor(models.Model):
    name = models.CharField(
        max_length=250,
        null=True,
    )
    street = models.CharField(
        max_length=500,
        null=True,
    )
    city = models.CharField(
        max_length=250,
        null=True,
    )
    state = USStateField(
        choices=STATE_CHOICES,
        null=True,
    )
    zip = USZipCodeField()
    email = models.EmailField(null=True)
    phone = models.CharField(
        max_length=20,
        null=True,
    )

    def __str__(self):
        return f"{self.name}"


class DeliveryLabel(models.Model):
    deliver_to = models.CharField(
        max_length=250,
        null=True,
        blank=False,
        help_text="name of person to receive the order @ ucla",
    )
    email = models.EmailField(blank=True, null=True)
    room_number = models.CharField(max_length=250, null=True, blank=True)
    ship_method = models.CharField(max_length=250, null=True, blank=True)
    delivery_date = models.DateField(null=True, blank=True)
    mark_urgent = models.BooleanField(default=False, blank=True)
    order_contact_name = models.CharField(
        max_length=250,
        null=True,
        blank=True,
        help_text="who to contact for info about this order",
    )
    order_contact_email = models.EmailField(null=True, blank=True, help_text="")
    order_contact_phone = models.CharField(
        max_length=20, null=True, blank=True, help_text=""
    )

    def __str__(self):
        return f"{self.deliver_to}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    timestamp_created = models.DateTimeField(auto_now=True)
    # requirements = models.ForeignKey(
    #     OrderRequirement, on_delete=models.SET_DEFAULT, default=1
    # )
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    # delivery_label = models.ForeignKey(
    #     DeliveryLabel,
    #     models.CASCADE,
    # )
    # category = models.CharField(max_length=500, blank=True, default="generic")

    # files = models.ForeignKey(OrderFileUpload, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"#{self.pk}: {self.user} from {self.vendor}"

    def get_absolute_url(self) -> str:
        return reverse("order-detail", kwargs={"pk": self.pk})


# class Order(models.Model):
#     name = models.CharField(max_length=255)
#
#     items: QuerySet["Item"]
#
#     class Meta:
#         verbose_name = "Order"
#         verbose_name_plural = "Orders"
#
#     def __str__(self) -> str:
#         return f"{self.name}"
#
#     def get_absolute_url(self) -> str:
#         return reverse("order-detail", kwargs={"pk": self.pk})


class Item(models.Model):
    class Meta:
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"

    order = models.ForeignKey(Order, on_delete=models.CASCADE, default=0)
    quantity = models.IntegerField(default=1)
    unit = models.CharField(max_length=100, help_text="(The thing you are ordering)")
    catalog_number = models.CharField(max_length=100, blank=True, null=True)
    cost_per_unit = models.FloatField(blank=True, null=True)
    description = models.TextField(
        blank=True,
        null=True,
        help_text="(anything you think we may need to know to get your order right)",
    )
    link_to_item = models.URLField(
        blank=True, null=True, help_text="(a link to the item you wish to purchase)"
    )

    def __str__(self) -> str:
        return f"{self.quantity} x {self.unit}"

    def get_absolute_url(self) -> str:
        return reverse("order-item-detail", args=(self.order.id, self.id))


# class Item(models.Model):
#     order = models.ForeignKey(
#         Order,
#         related_name="items",
#         on_delete=models.CASCADE,
#     )
#     name = models.CharField(max_length=255)
#
#
#     class Meta:
#         verbose_name = "Order Item"
#         verbose_name_plural = "Order Items"
#
#     def __str__(self) -> str:
#         return f"{self.name}"
