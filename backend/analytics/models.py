from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class CarbonFootprint(models.Model):
    """Model for tracking carbon footprint over time."""
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='carbon_footprints')
    
    # Date and period
    date = models.DateField()
    period_type = models.CharField(
        max_length=20,
        choices=[
            ('daily', 'Daily'),
            ('weekly', 'Weekly'),
            ('monthly', 'Monthly'),
            ('quarterly', 'Quarterly'),
            ('yearly', 'Yearly'),
        ],
        default='monthly'
    )
    
    # Carbon footprint data
    total_carbon_kg = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    scope_1_kg = models.DecimalField(max_digits=10, decimal_places=3, default=0)  # Direct emissions
    scope_2_kg = models.DecimalField(max_digits=10, decimal_places=3, default=0)  # Indirect emissions (energy)
    scope_3_kg = models.DecimalField(max_digits=10, decimal_places=3, default=0)  # Other indirect emissions
    
    # Other environmental metrics
    water_footprint_l = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    energy_footprint_kwh = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    waste_kg = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    
    # Business metrics for normalization
    revenue_usd = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    employees_count = models.IntegerField(default=1)
    
    # Calculated metrics
    carbon_intensity_kg_per_usd = models.DecimalField(max_digits=10, decimal_places=6, default=0)
    carbon_intensity_kg_per_employee = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Carbon Footprint')
        verbose_name_plural = _('Carbon Footprints')
        unique_together = ['user', 'date', 'period_type']
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.user.username} - {self.date} ({self.period_type})"
    
    def save(self, *args, **kwargs):
        """Calculate derived metrics before saving."""
        # Calculate carbon intensity metrics
        if self.revenue_usd > 0:
            self.carbon_intensity_kg_per_usd = self.total_carbon_kg / self.revenue_usd
        
        if self.employees_count > 0:
            self.carbon_intensity_kg_per_employee = self.total_carbon_kg / self.employees_count
        
        super().save(*args, **kwargs)


class MaterialBreakdown(models.Model):
    """Model for tracking carbon footprint by material type."""
    
    carbon_footprint = models.ForeignKey(CarbonFootprint, on_delete=models.CASCADE, related_name='material_breakdowns')
    
    # Material information
    material_type = models.CharField(max_length=100)
    material_name = models.CharField(max_length=255, blank=True, null=True)
    
    # Quantities and impacts
    quantity_kg = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    carbon_footprint_kg = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    water_footprint_l = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    energy_footprint_kwh = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    
    # Percentage of total
    percentage_of_total = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Material Breakdown')
        verbose_name_plural = _('Material Breakdowns')
        unique_together = ['carbon_footprint', 'material_type']
    
    def __str__(self):
        return f"{self.material_type} - {self.carbon_footprint.date}"


class SupplierBreakdown(models.Model):
    """Model for tracking carbon footprint by supplier."""
    
    carbon_footprint = models.ForeignKey(CarbonFootprint, on_delete=models.CASCADE, related_name='supplier_breakdowns')
    
    # Supplier information
    supplier_name = models.CharField(max_length=255)
    supplier_id = models.IntegerField(blank=True, null=True)
    
    # Quantities and impacts
    total_spend_usd = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    carbon_footprint_kg = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    water_footprint_l = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    energy_footprint_kwh = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    
    # Supplier sustainability rating
    supplier_sustainability_rating = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 11)],
        default=5
    )
    
    # Percentage of total
    percentage_of_total = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Supplier Breakdown')
        verbose_name_plural = _('Supplier Breakdowns')
        unique_together = ['carbon_footprint', 'supplier_name']
    
    def __str__(self):
        return f"{self.supplier_name} - {self.carbon_footprint.date}"


class SustainabilityGoal(models.Model):
    """Model for tracking sustainability goals and targets."""
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sustainability_goals')
    
    # Goal information
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    
    # Goal type
    goal_type = models.CharField(
        max_length=50,
        choices=[
            ('carbon_reduction', 'Carbon Reduction'),
            ('water_reduction', 'Water Reduction'),
            ('energy_reduction', 'Energy Reduction'),
            ('waste_reduction', 'Waste Reduction'),
            ('renewable_energy', 'Renewable Energy'),
            ('sustainable_materials', 'Sustainable Materials'),
            ('supplier_sustainability', 'Supplier Sustainability'),
        ]
    )
    
    # Target values
    target_value = models.DecimalField(max_digits=15, decimal_places=3)
    current_value = models.DecimalField(max_digits=15, decimal_places=3, default=0)
    unit = models.CharField(max_length=50)  # kg, L, kWh, %, etc.
    
    # Timeline
    start_date = models.DateField()
    target_date = models.DateField()
    achieved_date = models.DateField(blank=True, null=True)
    
    # Status
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('achieved', 'Achieved'),
        ('overdue', 'Overdue'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    # Progress tracking
    progress_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Sustainability Goal')
        verbose_name_plural = _('Sustainability Goals')
        ordering = ['-target_date']
    
    def __str__(self):
        return f"{self.name} - {self.user.username}"
    
    def calculate_progress(self):
        """Calculate progress percentage."""
        if self.target_value > 0:
            self.progress_percentage = (self.current_value / self.target_value) * 100
        else:
            self.progress_percentage = 0
        
        # Update status based on progress and dates
        from django.utils import timezone
        today = timezone.now().date()
        
        if self.progress_percentage >= 100:
            self.status = 'achieved'
            if not self.achieved_date:
                self.achieved_date = today
        elif today > self.target_date:
            self.status = 'overdue'
        else:
            self.status = 'active'


class EnvironmentalReport(models.Model):
    """Model for generating environmental reports."""
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='environmental_reports')
    
    # Report information
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    
    # Report period
    start_date = models.DateField()
    end_date = models.DateField()
    
    # Report type
    REPORT_TYPES = [
        ('monthly', 'Monthly Report'),
        ('quarterly', 'Quarterly Report'),
        ('annual', 'Annual Report'),
        ('custom', 'Custom Report'),
    ]
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES, default='monthly')
    
    # Report data (stored as JSON)
    report_data = models.JSONField(default=dict)
    
    # Report status
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('generated', 'Generated'),
        ('published', 'Published'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # File attachment
    report_file = models.FileField(upload_to='reports/', blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    generated_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        verbose_name = _('Environmental Report')
        verbose_name_plural = _('Environmental Reports')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.user.username}" 