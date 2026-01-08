from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json
from .models import Size, Order

def index(request):
    """Main product page"""
    return render(request, 'merch/index.html')

@require_http_methods(["GET"])
def get_available_sizes(request):
    """API endpoint to get available sizes"""
    sizes = Size.objects.filter(available_quantity__gt=0).values('name', 'available_quantity')
    return JsonResponse(list(sizes), safe=False)

@require_http_methods(["POST"])
def create_order(request):
    """API endpoint to create new order"""
    try:
        data = json.loads(request.body)
        
        # Validate required fields
        required_fields = ['full_name', 'gamer_tag', 'preferred_number', 'size', 'color']
        for field in required_fields:
            if not data.get(field):
                return JsonResponse({'error': f'{field} is required'}, status=400)
        
        # Check size availability
        try:
            size = Size.objects.get(name=data['size'])
            if not size.is_available:
                return JsonResponse({'error': 'Selected size is no longer available'}, status=400)
        except Size.DoesNotExist:
            return JsonResponse({'error': 'Invalid size selected'}, status=400)
        
        # Create order
        order = Order.objects.create(
            full_name=data['full_name'],
            gamer_tag=data['gamer_tag'],
            preferred_number=data['preferred_number'],
            size=data['size'],
            color=data['color'],
            phone=data.get('phone', ''),
            email=data.get('email', '')
        )
        
        # Decrease size availability
        size.available_quantity -= 1
        size.save()
        
        return JsonResponse({
            'success': True,
            'order_id': order.id,
            'message': 'Order placed successfully!'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)