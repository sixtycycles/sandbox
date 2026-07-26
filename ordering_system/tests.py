from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Item, Order, Vendor

User = get_user_model()


class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("u1", "u1@example.com", "pw-good-1")
        self.other = User.objects.create_user("u2", "u2@example.com", "pw-good-1")
        self.vendor = Vendor.objects.create(name="Acme", zip="90095")
        self.order = Order.objects.create(user=self.user, vendor=self.vendor)

    def test_str_methods(self):
        self.assertIn("Acme", str(self.vendor))
        self.assertEqual(
            str(self.order), f"#{self.order.pk}: {self.user} from {self.vendor}"
        )

    def test_order_related_name_items(self):
        # Item.order has related_name="items" so the reverse accessor works
        # (templates rely on order.items.all).
        item = Item.objects.create(order=self.order, unit="widget", quantity=2)
        self.assertIn(item, self.order.items.all())

    def test_get_absolute_url(self):
        item = Item.objects.create(order=self.order, unit="widget")
        self.assertEqual(
            item.get_absolute_url(), reverse("item-detail", kwargs={"pk": item.pk})
        )
        self.assertEqual(
            self.order.get_absolute_url(),
            reverse("order-detail", kwargs={"pk": self.order.pk}),
        )


class AuthRedirectTests(TestCase):
    """LoginRequiredMiddleware should bounce anonymous users to the login page."""

    def test_anon_order_list_redirects_to_login(self):
        resp = self.client.get(reverse("order-list"))
        self.assertEqual(resp.status_code, 302)
        self.assertIn(reverse("login"), resp.headers["Location"])

    def test_anon_order_detail_redirects_to_login(self):
        resp = self.client.get(reverse("order-detail", kwargs={"pk": 1}))
        self.assertEqual(resp.status_code, 302)
        self.assertIn(reverse("login"), resp.headers["Location"])

    def test_anon_landing_is_public(self):
        # landing_page is decorated @login_not_required
        resp = self.client.get(reverse("landing-page"))
        self.assertEqual(resp.status_code, 200)

    def test_login_page_is_reachable_when_anonymous(self):
        resp = self.client.get(reverse("login"))
        self.assertEqual(resp.status_code, 200)


class OwnershipEnforcementTests(TestCase):
    """A user must only be able to access their own orders/items (no IDOR)."""

    def setUp(self):
        self.owner = User.objects.create_user("owner", "o@example.com", "pw-good-1")
        self.stranger = User.objects.create_user(
            "stranger", "s@example.com", "pw-good-1"
        )
        self.vendor = Vendor.objects.create(name="Acme")
        self.order = Order.objects.create(user=self.owner, vendor=self.vendor)
        self.item = Item.objects.create(order=self.order, unit="widget")

    def test_owner_can_view_their_order(self):
        self.client.force_login(self.owner)
        resp = self.client.get(reverse("order-detail", kwargs={"pk": self.order.pk}))
        self.assertEqual(resp.status_code, 200)

    def test_stranger_cannot_view_others_order(self):
        self.client.force_login(self.stranger)
        resp = self.client.get(reverse("order-detail", kwargs={"pk": self.order.pk}))
        self.assertEqual(resp.status_code, 403)

    def test_stranger_cannot_view_others_item(self):
        self.client.force_login(self.stranger)
        resp = self.client.get(reverse("item-detail", kwargs={"pk": self.item.pk}))
        self.assertEqual(resp.status_code, 403)

    def test_stranger_cannot_edit_others_order(self):
        self.client.force_login(self.stranger)
        resp = self.client.get(reverse("order-edit", kwargs={"pk": self.order.pk}))
        self.assertEqual(resp.status_code, 403)

    def test_stranger_cannot_delete_others_item(self):
        self.client.force_login(self.stranger)
        resp = self.client.post(reverse("item-delete", kwargs={"pk": self.item.pk}))
        self.assertEqual(resp.status_code, 403)
        # item must still exist
        self.assertTrue(Item.objects.filter(pk=self.item.pk).exists())


class CreateFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("u1", "u1@example.com", "pw-good-1")
        self.vendor = Vendor.objects.create(name="Acme")

    def test_create_order_assigns_current_user(self):
        self.client.force_login(self.user)
        resp = self.client.post(reverse("order-create"), {"vendor": self.vendor.pk})
        self.assertEqual(resp.status_code, 302)
        created = Order.objects.get(vendor=self.vendor)
        self.assertEqual(created.user, self.user)

    def test_create_order_requires_authentication(self):
        resp = self.client.post(reverse("order-create"), {"vendor": self.vendor.pk})
        self.assertEqual(resp.status_code, 302)
        self.assertFalse(Order.objects.exists())

    def test_create_item_assigns_to_the_orders_owner(self):
        order = Order.objects.create(user=self.user, vendor=self.vendor)
        self.client.force_login(self.user)
        resp = self.client.post(
            reverse("item-create", kwargs={"pk": order.pk}),
            {"unit": "gizmo", "quantity": 3},
        )
        self.assertEqual(resp.status_code, 302)
        item = Item.objects.get(unit="gizmo")
        self.assertEqual(item.order, order)
        self.assertEqual(item.order.user, self.user)
