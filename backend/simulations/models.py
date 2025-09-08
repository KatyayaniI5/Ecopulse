from django.db import models
from django.contrib.auth import get_user_model
from invoices.models import Invoice, MaterialCategory

User = get_user_model()


class Simulation(models.Model):
    """Model for storing what-if simulation scenarios."""
    
    SIMULATION_TYPES = [
        ('material_substitution', 'Material Substitution'),
        ('supplier_change', 'Supplier Change'),
        ('quantity_adjustment', 'Quantity Adjustment'),
        ('process_optimization', 'Process Optimization'),
        ('energy_efficiency', 'Energy Efficiency'),
        ('custom', 'Custom Scenario'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='simulations')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    simulation_type = models.CharField(max_length=30, choices=SIMULATION_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # Base scenario (current state)
    base_carbon_footprint = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    base_water_usage = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    base_energy_usage = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    base_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Simulated scenario (projected state)
    simulated_carbon_footprint = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    simulated_water_usage = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    simulated_energy_usage = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    simulated_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Impact calculations
    carbon_reduction = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    water_reduction = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    energy_reduction = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cost_savings = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Related data
    related_invoices = models.ManyToManyField(Invoice, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.get_simulation_type_display()}"


class SimulationParameter(models.Model):
    """Model for storing simulation parameters and changes."""
    
    PARAMETER_TYPES = [
        ('material', 'Material'),
        ('quantity', 'Quantity'),
        ('supplier', 'Supplier'),
        ('process', 'Process'),
        ('energy', 'Energy'),
        ('custom', 'Custom'),
    ]
    
    simulation = models.ForeignKey(Simulation, on_delete=models.CASCADE, related_name='parameters')
    parameter_type = models.CharField(max_length=20, choices=PARAMETER_TYPES)
    parameter_name = models.CharField(max_length=100)
    original_value = models.TextField()
    new_value = models.TextField()
    unit = models.CharField(max_length=20, blank=True)
    
    def __str__(self):
        return f"{self.parameter_name}: {self.original_value} → {self.new_value}"


class SimulationResult(models.Model):
    """Model for storing detailed simulation results."""
    
    simulation = models.OneToOneField(Simulation, on_delete=models.CASCADE, related_name='detailed_result')
    
    # Detailed breakdowns
    carbon_breakdown = models.JSONField(default=dict)  # Store detailed carbon calculations
    water_breakdown = models.JSONField(default=dict)   # Store detailed water calculations
    energy_breakdown = models.JSONField(default=dict)  # Store detailed energy calculations
    cost_breakdown = models.JSONField(default=dict)    # Store detailed cost calculations
    
    # Recommendations
    recommendations = models.JSONField(default=list)   # Store AI-generated recommendations
    implementation_steps = models.JSONField(default=list)  # Store implementation guidance
    
    # Metadata
    calculation_method = models.CharField(max_length=50, default='standard')
    confidence_level = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Results for {self.simulation.name}" 