# AI-Assisted Box Selection System

A small Django application that recommends the lowest-cost shipping box that can safely contain a shipment.

## Features

- Product and shipping-box data models.
- Django admin for managing products and boxes.
- JSON API for box recommendations.
- Rotation-aware dimension checking.
- Weight-capacity validation.
- Quantity-aware shipment weight and volume.
- Automated Django test suite.

## Design decision

Exact 3-D packing of multiple differently shaped items is a complex packing problem. For this assignment, the recommendation uses a conservative single-box rule: every product must individually fit in the box in some orientation, while total shipment weight and total product volume must fit within the box limits. Among valid boxes, the lowest-cost box is selected.

This makes the behavior deterministic and easy to verify. A production system could replace this rule with a dedicated packing algorithm or bin-packing service.

## Setup

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py test
python manage.py runserver
```

## API

### POST `/api/recommend-box/`

Example request:

```json
{
  "products": [
    {
      "length": 9,
      "width": 9,
      "height": 9,
      "weight": 1,
      "quantity": 1
    }
  ]
}
```

Example successful response:

```json
{
  "recommended_box": {
    "id": 1,
    "name": "Small",
    "cost": "50.00",
    "max_weight_kg": "2.000",
    "inner_dimensions_cm": ["10.00", "10.00", "10.00"]
  }
}
```

If no box is suitable:

```json
{
  "recommended_box": null,
  "message": "No available box can safely fit this shipment."
}
```

## Admin

Create an admin account with:

```bash
python manage.py createsuperuser
```

Then visit `/admin/`.

## Verification

The repository includes automated tests covering rotation, cheapest-box selection, weight limits, dimensions, quantity, API success, invalid JSON, and missing fields.

See `TEST_OUTPUT.md` for the test run captured during preparation.
