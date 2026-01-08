"""
Initialize Size data for EYTGaming Merch
Run with: python manage.py shell < populate_sizes.py
"""
from merch.models import Size

# Define sizes with initial stock
sizes_data = [
    {'name': 'S', 'available_quantity': 25},
    {'name': 'M', 'available_quantity': 30},
    {'name': 'L', 'available_quantity': 35},
    {'name': 'XL', 'available_quantity': 30},
    {'name': '2XL', 'available_quantity': 20},
]

# Create or update sizes
for size_data in sizes_data:
    size, created = Size.objects.get_or_create(
        name=size_data['name'],
        defaults={'available_quantity': size_data['available_quantity']}
    )
    if created:
        print(f"Created size: {size.name} with {size.available_quantity} units")
    else:
        print(f"Size {size.name} already exists with {size.available_quantity} units")

print(f"\nTotal sizes in database: {Size.objects.count()}")
