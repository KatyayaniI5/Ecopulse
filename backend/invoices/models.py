from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Invoice(models.Model):
    """Model for storing uploaded invoices."""
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='invoices')
    
    # File information
    file = models.FileField(upload_to='invoices/')
    file_name = models.CharField(max_length=255)
    file_size = models.IntegerField(help_text='File size in bytes')
    file_type = models.CharField(max_length=50, help_text='MIME type of the file')
    
    # Invoice metadata
    invoice_number = models.CharField(max_length=100, blank=True, null=True)
    invoice_date = models.DateField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    currency = models.CharField(max_length=3, default='USD')
    
    # Supplier information
    supplier_name = models.CharField(max_length=255, blank=True, null=True)
    supplier_address = models.TextField(blank=True, null=True)
    supplier_email = models.EmailField(blank=True, null=True)
    
    # Processing status
    STATUS_CHOICES = [
        ('uploaded', 'Uploaded'),
        ('processing', 'Processing'),
        ('processed', 'Processed'),
        ('failed', 'Failed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='uploaded')
    
    # Processing results
    extracted_text = models.TextField(blank=True, null=True)
    processing_errors = models.TextField(blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    processed_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        verbose_name = _('Invoice')
        verbose_name_plural = _('Invoices')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Invoice {self.invoice_number or self.file_name} - {self.user.username}"


class InvoiceItem(models.Model):
    """Model for individual items in an invoice."""
    
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    
    # Item details
    description = models.CharField(max_length=500)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    # Environmental data
    material_type = models.CharField(max_length=100, blank=True, null=True)
    weight_kg = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    volume_l = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    
    # Carbon footprint data
    carbon_footprint_kg = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    water_footprint_l = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    energy_footprint_kwh = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Invoice Item')
        verbose_name_plural = _('Invoice Items')
    
    def __str__(self):
        return f"{self.description} - {self.invoice.invoice_number}"


class MaterialCategory(models.Model):
    """Model for categorizing materials and their environmental impact."""
    
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    
    # Environmental impact factors (per kg)
    carbon_factor_kg_co2_per_kg = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    water_factor_l_per_kg = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    energy_factor_kwh_per_kg = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    
    # Sustainability rating (1-10, 10 being most sustainable)
    sustainability_rating = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 11)],
        default=5
    )
    
    # Alternative materials
    alternatives = models.ManyToManyField('self', blank=True, symmetrical=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Material Category')
        verbose_name_plural = _('Material Categories')
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Supplier(models.Model):
    """Model for supplier information and sustainability ratings."""
    
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    
    # Sustainability information
    sustainability_rating = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 11)],
        default=5,
        help_text='Sustainability rating from 1-10'
    )
    has_sustainability_certification = models.BooleanField(default=False)
    sustainability_certifications = models.TextField(blank=True, null=True)
    
    # Environmental policies
    has_environmental_policy = models.BooleanField(default=False)
    carbon_neutral = models.BooleanField(default=False)
    renewable_energy_usage = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=0,
        help_text='Percentage of renewable energy usage'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Supplier')
        verbose_name_plural = _('Suppliers')
        ordering = ['name']
    
    def __str__(self):
        return self.name 