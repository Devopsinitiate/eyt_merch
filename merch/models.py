from django.db import models
from django.core.validators import MinValueValidator

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
    
    # Order information
    full_name = models.CharField(max_length=200)
    gamer_tag = models.CharField(max_length=100)
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