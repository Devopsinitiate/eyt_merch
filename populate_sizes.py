import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eyt_merch.settings')
django.setup()

from merch.models import Size

# Create sizes with inventory
sizes_data = [
    {'name': 'S', 'available_quantity': 15},
    {'name': 'M', 'available_quantity': 25},
    {'name': 'L', 'available_quantity': 30},
    {'name': 'XL', 'available_quantity': 20},
    {'name': '2XL', 'available_quantity': 10},
]

for size_dict in sizes_data:
    size, created = Size.objects.get_or_create(
        name=size_dict['name'],
        defaults={'available_quantity': size_dict['available_quantity']}
    )
    if created:
        print(f"Created size: {size.name} with {size.available_quantity} units")
    else:
        print(f"Size {size.name} already exists")

print("\nSize population complete!")
