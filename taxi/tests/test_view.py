from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer


class PublicTaxiTest(TestCase):
    def test_login_required(self):
        urls = [
            ("taxi:index", {}),
            ("taxi:manufacturer-list", {}),
            ("taxi:manufacturer-update", {"pk": 1}),
            ("taxi:manufacturer-delete", {"pk": 1}),
            ("taxi:manufacturer-create", {}),
            ("taxi:car-detail", {"pk": 1}),
            ("taxi:car-list", {}),
            ("taxi:car-update", {"pk": 1}),
            ("taxi:car-create", {}),
            ("taxi:car-delete", {"pk": 1}),
            ("taxi:driver-detail", {"pk": 1}),
            ("taxi:driver-list", {}),
            ("taxi:driver-update", {"pk": 1}),
            ("taxi:driver-create", {}),
            ("taxi:driver-delete", {"pk": 1}),
        ]
        for url_name, kwargs in urls:
            with self.subTest(url_name=url_name, kwargs=kwargs):
                response = self.client.get(reverse(url_name, kwargs=kwargs))
                self.assertNotEqual(response.status_code, 200)


class PrivateTaxiTest(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            username="test_driver",
            password="test1234",
        )
        self.manufacturer = Manufacturer.objects.create(
            name="test_manufacturer_name",
            country="test_country"
        )
        self.car = Car.objects.create(
            model="test_model",
            manufacturer=self.manufacturer,
        )
        self.client.force_login(self.driver)

    def test_driver_detail(self):
        response = self.client.get(
            reverse("taxi:driver-detail", kwargs={"pk": 1})
        )
        self.assertEqual(response.status_code, 200)

    def test_retrieve_drivers(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(
            list(response.context["driver_list"]),
            list(get_user_model().objects.all())
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_car_detail(self):
        response = self.client.get(
            reverse("taxi:car-detail", kwargs={"pk": 1})
        )
        self.assertEqual(response.status_code, 200)

    def test_retrieve_cars(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(
            list(response.context["car_list"]),
            list(Car.objects.all())
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_retrieve_manufacturers(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(Manufacturer.objects.all())
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")
