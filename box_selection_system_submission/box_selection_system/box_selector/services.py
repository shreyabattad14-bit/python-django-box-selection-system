from itertools import permutations
from decimal import Decimal
from .models import ShippingBox

def dimensions_fit(product_dimensions, box_dimensions):
    """Allow rotation: any permutation of product dimensions may fit."""
    product_dimensions = [Decimal(str(v)) for v in product_dimensions]
    box_dimensions = [Decimal(str(v)) for v in box_dimensions]
    return any(
        all(p <= b for p, b in zip(product_dimensions, perm))
        for perm in permutations(box_dimensions)
    )

def recommend_box(products):
    """
    Recommend the lowest-cost box for a single-box shipment.

    `products` is a list of dictionaries:
    {"length": ..., "width": ..., "height": ..., "weight": ..., "quantity": ...}

    This assignment intentionally uses a conservative packing rule:
    - total shipment weight must be within the box capacity;
    - total product volume must be within the box volume;
    - every individual product must fit inside the box in some orientation.

    Exact 3-D multi-item packing is NP-hard; documenting this trade-off keeps
    the small hiring assignment predictable and testable.
    """
    total_weight = sum(
        Decimal(str(p["weight"])) * int(p.get("quantity", 1)) for p in products
    )
    total_volume = sum(
        Decimal(str(p["length"])) * Decimal(str(p["width"])) * Decimal(str(p["height"]))
        * int(p.get("quantity", 1))
        for p in products
    )

    candidates = []
    for box in ShippingBox.objects.all():
        box_dims = (box.inner_length_cm, box.inner_width_cm, box.inner_height_cm)
        fits_dimensions = all(
            dimensions_fit((p["length"], p["width"], p["height"]), box_dims)
            for p in products
        )
        box_volume = box.inner_length_cm * box.inner_width_cm * box.inner_height_cm
        if fits_dimensions and total_weight <= box.max_weight_kg and total_volume <= box_volume:
            candidates.append(box)

    return min(candidates, key=lambda b: (b.cost, b.inner_length_cm*b.inner_width_cm*b.inner_height_cm), default=None)
