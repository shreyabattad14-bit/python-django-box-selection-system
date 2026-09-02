from decimal import Decimal
from django.test import TestCase, Client
from .models import ShippingBox
from .services import dimensions_fit, recommend_box

class BoxSelectionTests(TestCase):
    def setUp(self):
        ShippingBox.objects.create(
            name="Small", inner_length_cm=10, inner_width_cm=10, inner_height_cm=10,
            max_weight_kg=2, cost=50
        )
        ShippingBox.objects.create(
            name="Medium", inner_length_cm=20, inner_width_cm=15, inner_height_cm=10,
            max_weight_kg=5, cost=80
        )
        ShippingBox.objects.create(
            name="Heavy", inner_length_cm=30, inner_width_cm=20, inner_height_cm=20,
            max_weight_kg=20, cost=120
        )

    def test_rotation_is_allowed(self):
        self.assertTrue(dimensions_fit((11, 9, 8), (10, 11, 9)))

    def test_cheapest_fitting_box_is_selected(self):
        box = recommend_box([{
            "length": Decimal("9"), "width": Decimal("9"), "height": Decimal("9"),
            "weight": Decimal("1"), "quantity": 1
        }])
        self.assertEqual(box.name, "Small")

    def test_weight_capacity_is_checked(self):
        box = recommend_box([{
            "length": Decimal("9"), "width": Decimal("9"), "height": Decimal("9"),
            "weight": Decimal("3"), "quantity": 1
        }])
        self.assertEqual(box.name, "Medium")

    def test_no_box_when_dimensions_do_not_fit(self):
        box = recommend_box([{
            "length": Decimal("31"), "width": Decimal("9"), "height": Decimal("9"),
            "weight": Decimal("1"), "quantity": 1
        }])
        self.assertIsNone(box)

    def test_quantity_affects_weight_and_volume(self):
        box = recommend_box([{
            "length": Decimal("9"), "width": Decimal("9"), "height": Decimal("9"),
            "weight": Decimal("1"), "quantity": 3
        }])
        self.assertEqual(box.name, "Medium")

    def test_api_success(self):
        client = Client()
        response = client.post(
            "/api/recommend-box/",
            data='{"products":[{"length":9,"width":9,"height":9,"weight":1}]}',
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["recommended_box"]["name"], "Small")

    def test_api_rejects_invalid_json(self):
        response = Client().post("/api/recommend-box/", data="{bad", content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_api_rejects_missing_fields(self):
        response = Client().post(
            "/api/recommend-box/",
            data='{"products":[{"length":9,"width":9,"height":9}]}',
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
