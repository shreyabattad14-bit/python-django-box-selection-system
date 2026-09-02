from django.core.validators import MinValueValidator
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=150)
    length_cm = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.01)])
    width_cm = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.01)])
    height_cm = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.01)])
    weight_kg = models.DecimalField(max_digits=8, decimal_places=3, validators=[MinValueValidator(0.001)])

    def __str__(self):
        return self.name

class ShippingBox(models.Model):
    name = models.CharField(max_length=100, unique=True)
    inner_length_cm = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.01)])
    inner_width_cm = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.01)])
    inner_height_cm = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.01)])
    max_weight_kg = models.DecimalField(max_digits=8, decimal_places=3, validators=[MinValueValidator(0.001)])
    cost = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])

    def __str__(self):
        return self.name

class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        constraints = [
            models.CheckConstraint(condition=models.Q(quantity__gte=1), name="positive_order_quantity")
        ]
