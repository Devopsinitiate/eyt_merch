from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.conf import settings
from django.core.exceptions import ValidationError


class CustomUser(AbstractUser):
    """Extended user model for EYT Gamer Army members"""
    full_name = models.CharField(max_length=200)
    gamer_tag = models.CharField(max_length=100, unique=True)
    phone = models.CharField(max_length=20)
    
    class Meta:
        ordering = ['-date_joined']
    
    def __str__(self):
        return f"{self.gamer_tag} ({self.email})"

class Size(models.Model):
    """Available sizes with inventory tracking"""
    SIZE_CHOICES = [
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('2XL', '2X Large'),
    ]
    
    name = models.CharField(max_length=10, choices=SIZE_CHOICES, unique=True)
    available_quantity = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.get_name_display()} ({self.available_quantity} available)"
    
    @property
    def is_available(self):
        return self.available_quantity > 0


class Order(models.Model):
    """Customer orders for merchandise"""
    COLOR_CHOICES = [
        ('BLUE', 'Blue'),
        ('ASH', 'Light Heather Grey'),
    ]
    
    # User relationship
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders',
        null=True,  # Allow null for existing orders during migration
        blank=True
    )
    
    # Order information (kept for backward compatibility and flexibility)
    full_name = models.CharField(max_length=200, blank=True)
    gamer_tag = models.CharField(max_length=100, blank=True)
    preferred_number = models.CharField(max_length=10)
    
    # Product selection
    size = models.CharField(max_length=10)
    color = models.CharField(max_length=20, choices=COLOR_CHOICES)
    
    # Contact information
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.gamer_tag} - {self.size} - {self.color}"


class TournamentConfig(models.Model):
    """Single tournament configuration (fee, payment details, capacity)"""
    tournament_name = models.CharField(max_length=200, default='EYT GAMER ARMY TOURNAMENT')
    fee_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(max_length=10, default='NGN')
    account_name = models.CharField(max_length=200, blank=True)
    account_number = models.CharField(max_length=50, blank=True)
    bank_name = models.CharField(max_length=200, blank=True)
    max_participants = models.PositiveIntegerField(
        default=0,
        help_text='Maximum number of participants. 0 means unlimited.'
    )
    is_registration_open = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Tournament Configuration'
        verbose_name_plural = 'Tournament Configuration'

    def __str__(self):
        return self.tournament_name

    @classmethod
    def get_config(cls):
        """Return the single config instance (creating it with defaults if missing)"""
        config, _ = cls.objects.get_or_create(pk=1)
        return config

    @property
    def registered_count(self):
        return TournamentRegistration.objects.count()

    @property
    def spots_remaining(self):
        if not self.max_participants:
            return None
        return max(self.max_participants - self.registered_count, 0)

    @property
    def is_full(self):
        if not self.max_participants:
            return False
        return self.registered_count >= self.max_participants


class TournamentRegistration(models.Model):
    """External tournament registrations collected via QR code"""
    GENDER_CHOICES = [
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
        ('OTHER', 'Other'),
        ('NOT_SAY', 'Prefer not to say'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
    ]

    full_name = models.CharField(max_length=200)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    gamer_tag = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    payment_reference = models.CharField(
        max_length=200,
        blank=True,
        help_text='Bank transfer reference / receipt number (optional)'
    )
    payment_status = models.CharField(
        max_length=10,
        choices=PAYMENT_STATUS_CHOICES,
        default='PENDING'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.gamer_tag} ({self.full_name})"

    def clean(self):
        """Validate tournament capacity & registration state"""
        if self.pk is None:
            config = TournamentConfig.get_config()
            if config and not config.is_registration_open:
                raise ValidationError('Tournament registration is currently closed.')
            if config and config.is_full:
                raise ValidationError(
                    'Tournament registration is full. No more spots available.'
                )

    def save(self, *args, **kwargs):
        self.gamer_tag = self.gamer_tag.upper().strip()
        self.clean()
        super().save(*args, **kwargs)