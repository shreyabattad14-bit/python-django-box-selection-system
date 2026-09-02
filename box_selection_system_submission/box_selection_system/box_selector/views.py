import json
from decimal import Decimal, InvalidOperation
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .services import recommend_box

REQUIRED = ("length", "width", "height", "weight")

def _decimal(value, field):
    try:
        value = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        raise ValueError(f"{field} must be a number")
    if value <= 0:
        raise ValueError(f"{field} must be greater than 0")
    return value

@require_POST
def recommend_box_api(request):
    try:
        payload = json.loads(request.body or "{}")
        products = payload.get("products")
        if not isinstance(products, list) or not products:
            return JsonResponse({"error": "products must be a non-empty list"}, status=400)

        cleaned = []
        for index, product in enumerate(products):
            if not isinstance(product, dict):
                return JsonResponse({"error": f"products[{index}] must be an object"}, status=400)
            missing = [field for field in REQUIRED if field not in product]
            if missing:
                return JsonResponse({"error": f"products[{index}] missing: {', '.join(missing)}"}, status=400)
            item = {field: _decimal(product[field], field) for field in REQUIRED}
            quantity = product.get("quantity", 1)
            if not isinstance(quantity, int) or quantity < 1:
                return JsonResponse({"error": f"products[{index}].quantity must be a positive integer"}, status=400)
            item["quantity"] = quantity
            cleaned.append(item)

        box = recommend_box(cleaned)
        if box is None:
            return JsonResponse({"recommended_box": None, "message": "No available box can safely fit this shipment."})

        return JsonResponse({
            "recommended_box": {
                "id": box.id,
                "name": box.name,
                "cost": str(box.cost),
                "max_weight_kg": str(box.max_weight_kg),
                "inner_dimensions_cm": [
                    str(box.inner_length_cm), str(box.inner_width_cm), str(box.inner_height_cm)
                ],
            }
        })
    except json.JSONDecodeError:
        return JsonResponse({"error": "Request body must be valid JSON"}, status=400)
    except ValueError as exc:
        return JsonResponse({"error": str(exc)}, status=400)
