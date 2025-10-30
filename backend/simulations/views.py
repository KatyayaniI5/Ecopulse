from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from decimal import Decimal

from .models import Simulation, SimulationParameter, SimulationResult
from .serializers import (
    SimulationSerializer,
    SimulationParameterSerializer,
    SimulationResultSerializer,
    CreateSimulationSerializer
)


class SimulationListView(generics.ListCreateAPIView):
    """View for listing and creating simulations."""
    serializer_class = SimulationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Simulation.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SimulationDetailView(generics.RetrieveUpdateDestroyAPIView):
    """View for retrieving, updating, and deleting a simulation."""
    serializer_class = SimulationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Simulation.objects.filter(user=self.request.user)


class CreateSimulationView(APIView):
    """View for creating a new simulation with parameters."""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = CreateSimulationSerializer(data=request.data)
        if serializer.is_valid():
            simulation = serializer.save(user=request.user)
            
            # Create simulation parameters if provided
            parameters_data = request.data.get('parameters', [])
            for param_data in parameters_data:
                param_data['simulation'] = simulation.id
                param_serializer = SimulationParameterSerializer(data=param_data)
                if param_serializer.is_valid():
                    param_serializer.save()
            
            return Response(SimulationSerializer(simulation).data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RunSimulationView(APIView):
    """View for running a simulation and calculating results."""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, pk):
        simulation = get_object_or_404(Simulation, pk=pk, user=request.user)
        
        # Update status to running
        simulation.status = 'running'
        simulation.save()
        
        try:
            # TODO: Implement actual simulation logic
            # This would calculate the environmental impact based on parameters
            
            # Placeholder calculations
            base_carbon = Decimal('100.00')  # Example base values
            base_water = Decimal('500.00')
            base_energy = Decimal('50.00')
            base_cost = Decimal('1000.00')
            
            # Simulate some improvements (placeholder logic)
            simulated_carbon = base_carbon * Decimal('0.85')  # 15% reduction
            simulated_water = base_water * Decimal('0.90')    # 10% reduction
            simulated_energy = base_energy * Decimal('0.80')  # 20% reduction
            simulated_cost = base_cost * Decimal('0.95')      # 5% reduction
            
            # Update simulation with results
            simulation.base_carbon_footprint = base_carbon
            simulation.base_water_usage = base_water
            simulation.base_energy_usage = base_energy
            simulation.base_cost = base_cost
            
            simulation.simulated_carbon_footprint = simulated_carbon
            simulation.simulated_water_usage = simulated_water
            simulation.simulated_energy_usage = simulated_energy
            simulation.simulated_cost = simulated_cost
            
            simulation.carbon_reduction = base_carbon - simulated_carbon
            simulation.water_reduction = base_water - simulated_water
            simulation.energy_reduction = base_energy - simulated_energy
            simulation.cost_savings = base_cost - simulated_cost
            
            simulation.status = 'completed'
            simulation.save()
            
            # Create detailed results
            result_data = {
                'carbon_breakdown': {
                    'materials': float(simulated_carbon * Decimal('0.6')),
                    'transport': float(simulated_carbon * Decimal('0.2')),
                    'energy': float(simulated_carbon * Decimal('0.2')),
                },
                'water_breakdown': {
                    'direct_usage': float(simulated_water * Decimal('0.7')),
                    'indirect_usage': float(simulated_water * Decimal('0.3')),
                },
                'energy_breakdown': {
                    'electricity': float(simulated_energy * Decimal('0.5')),
                    'fuel': float(simulated_energy * Decimal('0.3')),
                    'renewable': float(simulated_energy * Decimal('0.2')),
                },
                'cost_breakdown': {
                    'materials': float(simulated_cost * Decimal('0.4')),
                    'energy': float(simulated_cost * Decimal('0.3')),
                    'labor': float(simulated_cost * Decimal('0.3')),
                },
                'recommendations': [
                    'Consider switching to recycled materials',
                    'Optimize transportation routes',
                    'Implement energy-efficient processes'
                ],
                'implementation_steps': [
                    'Audit current material usage',
                    'Research alternative suppliers',
                    'Calculate ROI for changes'
                ]
            }
            
            # Save or update detailed results
            result, created = SimulationResult.objects.get_or_create(
                simulation=simulation,
                defaults={
                    'carbon_breakdown': result_data['carbon_breakdown'],
                    'water_breakdown': result_data['water_breakdown'],
                    'energy_breakdown': result_data['energy_breakdown'],
                    'cost_breakdown': result_data['cost_breakdown'],
                    'recommendations': result_data['recommendations'],
                    'implementation_steps': result_data['implementation_steps'],
                    'confidence_level': Decimal('0.85')
                }
            )
            
            if not created:
                # Update existing result
                result.carbon_breakdown = result_data['carbon_breakdown']
                result.water_breakdown = result_data['water_breakdown']
                result.energy_breakdown = result_data['energy_breakdown']
                result.cost_breakdown = result_data['cost_breakdown']
                result.recommendations = result_data['recommendations']
                result.implementation_steps = result_data['implementation_steps']
                result.save()
            
            return Response({
                'message': 'Simulation completed successfully',
                'simulation': SimulationSerializer(simulation).data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            simulation.status = 'failed'
            simulation.save()
            return Response({
                'error': f'Simulation failed: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SimulationResultsView(APIView):
    """View for retrieving detailed simulation results."""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, pk):
        simulation = get_object_or_404(Simulation, pk=pk, user=request.user)
        
        try:
            result = simulation.detailed_result
            return Response(SimulationResultSerializer(result).data, status=status.HTTP_200_OK)
        except SimulationResult.DoesNotExist:
            return Response({
                'error': 'No detailed results available for this simulation'
            }, status=status.HTTP_404_NOT_FOUND)


class SimulationTemplatesView(APIView):
    """View for retrieving simulation templates."""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        templates = [
            {
                'id': 'material_substitution',
                'name': 'Material Substitution',
                'description': 'Simulate the impact of switching to more sustainable materials',
                'parameters': [
                    {'type': 'material', 'name': 'Current Material', 'required': True},
                    {'type': 'material', 'name': 'Alternative Material', 'required': True},
                    {'type': 'quantity', 'name': 'Quantity', 'required': True}
                ]
            },
            {
                'id': 'supplier_change',
                'name': 'Supplier Change',
                'description': 'Analyze the environmental impact of changing suppliers',
                'parameters': [
                    {'type': 'supplier', 'name': 'Current Supplier', 'required': True},
                    {'type': 'supplier', 'name': 'New Supplier', 'required': True},
                    {'type': 'custom', 'name': 'Transportation Distance', 'required': False}
                ]
            },
            {
                'id': 'energy_efficiency',
                'name': 'Energy Efficiency',
                'description': 'Simulate energy-saving measures and their impact',
                'parameters': [
                    {'type': 'energy', 'name': 'Current Energy Usage', 'required': True},
                    {'type': 'energy', 'name': 'Proposed Energy Usage', 'required': True},
                    {'type': 'custom', 'name': 'Implementation Cost', 'required': False}
                ]
            }
        ]
        
        return Response(templates, status=status.HTTP_200_OK) 