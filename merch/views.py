from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.utils.html import mark_safe
import json
import segno
from .models import Size, Order, CustomUser, TournamentConfig
from .forms import UserSignupForm, UserLoginForm, UserProfileForm, TournamentRegistrationForm


def signup_view(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('merch:index')
    
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome to the EYT Gamer Army, {user.gamer_tag}!')
            return redirect('merch:index')
    else:
        form = UserSignupForm()
    
    return render(request, 'merch/signup.html', {'form': form})


def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('merch:index')
    
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.gamer_tag}!')
                return redirect('merch:index')
    else:
        form = UserLoginForm()
    
    return render(request, 'merch/login.html', {'form': form})


def logout_view(request):
    """User logout view"""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('merch:index')


@login_required
def profile_view(request):
    """User profile view"""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('merch:profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    # Get user's orders
    orders = request.user.orders.all()
    
    return render(request, 'merch/profile.html', {
        'form': form,
        'orders': orders
    })


def index(request):
    """Main product page"""
    return render(request, 'merch/index.html')


@require_http_methods(["GET"])
def get_available_sizes(request):
    """API endpoint to get available sizes"""
    sizes = Size.objects.filter(available_quantity__gt=0).values('name', 'available_quantity')
    return JsonResponse(list(sizes), safe=False)

@require_http_methods(["POST"])
@login_required
def create_order(request):
    """API endpoint to create new order (requires authentication)"""
    try:
        data = json.loads(request.body)
        
        # Validate required fields
        required_fields = ['preferred_number', 'size', 'color']
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
        
        # Create order linked to user
        order = Order.objects.create(
            user=request.user,
            full_name=request.user.full_name,
            gamer_tag=request.user.gamer_tag,
            preferred_number=data['preferred_number'],
            size=data['size'],
            color=data['color'],
            phone=request.user.phone,
            email=request.user.email
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


def tournament_view(request):
    """Tournament landing page showing the QR code that opens the registration portal"""
    config = TournamentConfig.get_config()
    register_url = request.build_absolute_uri(reverse('merch:tournament_register'))

    qr_svg = None
    if register_url:
        qr = segno.make(register_url, error='m')
        qr_svg = mark_safe(qr.svg_inline(scale=8, border=2, dark='#0a0a0a', light='#ffffff'))

    return render(request, 'merch/tournament.html', {
        'config': config,
        'qr_svg': qr_svg,
        'register_url': register_url,
    })


def tournament_register(request):
    """Registration portal reached by scanning the tournament QR code"""
    config = TournamentConfig.get_config()

    if config and not config.is_registration_open:
        return render(request, 'merch/tournament_register.html', {
            'config': config,
            'form': None,
            'closed': True,
        })

    if config and config.is_full:
        return render(request, 'merch/tournament_register.html', {
            'config': config,
            'form': None,
            'full': True,
        })

    if request.method == 'POST':
        form = TournamentRegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.payment_status = 'PENDING'
            registration.save()
            messages.success(
                request,
                f'Registration confirmed! Welcome, #{registration.gamer_tag}. '
                'Complete your payment using the details below to secure your spot.'
            )
            return redirect('merch:tournament_register')
    else:
        form = TournamentRegistrationForm()

    return render(request, 'merch/tournament_register.html', {
        'config': config,
        'form': form,
        'closed': False,
        'full': False,
    })