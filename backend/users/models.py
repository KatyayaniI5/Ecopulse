from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Custom user model for EcoMSME AI platform."""
    
    # Company information
    company_name = models.CharField(max_length=255, blank=True, null=True)
    company_size = models.CharField(
        max_length=20,
        choices=[
            ('micro', 'Micro (1-10 employees)'),
            ('small', 'Small (11-50 employees)'),
            ('medium', 'Medium (51-250 employees)'),
        ],
        blank=True,
        null=True
    )
    industry_sector = models.CharField(
        max_length=100,
        choices=[
            ('manufacturing', 'Manufacturing'),
            ('textile', 'Textile & Fashion'),
            ('food', 'Food & Beverage'),
            ('construction', 'Construction'),
            ('technology', 'Technology'),
            ('retail', 'Retail'),
            ('other', 'Other'),
        ],
        blank=True,
        null=True
    )
    
    # Contact information
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    
    # Preferences
    language = models.CharField(
        max_length=10,
        choices=[
            ('en', 'English'),
            ('es', 'Spanish'),
            ('fr', 'French'),
            ('de', 'German'),
            ('zh', 'Chinese'),
        ],
        default='en'
    )
    timezone = models.CharField(max_length=50, default='UTC')
    
    # Environmental goals
    carbon_reduction_target = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text='Target carbon reduction percentage',
        null=True,
        blank=True
    )
    target_year = models.IntegerField(
        help_text='Target year for carbon reduction',
        null=True,
        blank=True
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
    
    def __str__(self):
        return self.email or self.username
    
    @property
    def full_name(self):
        """Return the user's full name."""
        return f"{self.first_name} {self.last_name}".strip() or self.username


class CompanyProfile(models.Model):
    """Extended company profile information."""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='company_profile')
    
    # Company details
    registration_number = models.CharField(max_length=100, blank=True, null=True)
    tax_id = models.CharField(max_length=100, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    
    # Sustainability information
    sustainability_officer = models.CharField(max_length=255, blank=True, null=True)
    sustainability_contact_email = models.EmailField(blank=True, null=True)
    
    # Certifications
    iso_14001_certified = models.BooleanField(default=False)
    iso_9001_certified = models.BooleanField(default=False)
    other_certifications = models.TextField(blank=True, null=True)
    
    # Environmental policies
    has_environmental_policy = models.BooleanField(default=False)
    environmental_policy_date = models.DateField(blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Company Profile')
        verbose_name_plural = _('Company Profiles')
    
    def __str__(self):
        return f"Profile for {self.user.company_name or self.user.username}" 