from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db.models import Sum, Avg
from django.utils import timezone
import os

from .models import Invoice, InvoiceItem, MaterialCategory, Supplier
from .serializers import (
    InvoiceSerializer,
    InvoiceUploadSerializer,
    InvoiceItemSerializer,
    MaterialCategorySerializer,
    SupplierSerializer,
    InvoiceProcessingResultSerializer,
    EnvironmentalImpactSerializer
)
from nlp_module.invoice_processor import InvoiceProcessor


class InvoiceUploadView(APIView):
    """View for uploading invoices."""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = InvoiceUploadSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            invoice = serializer.save()
            
            # Start async processing
            self.process_invoice_async(invoice)
            
            return Response({
                'message': 'Invoice uploaded successfully',
                'invoice_id': invoice.id,
                'status': 'processing'
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def process_invoice_async(self, invoice):
        """Process invoice asynchronously."""
        try:
            # Update status to processing
            invoice.status = 'processing'
            invoice.save()
            
            # Process the invoice
            processor = InvoiceProcessor()
            result = processor.process_invoice(invoice.file.path)
            
            if result['processing_status'] == 'success':
                # Update invoice with extracted data
                metadata = result['metadata']
                invoice.invoice_number = metadata.get('invoice_number')
                invoice.invoice_date = metadata.get('invoice_date')
                invoice.due_date = metadata.get('due_date')
                invoice.total_amount = metadata.get('total_amount')
                invoice.supplier_name = metadata.get('supplier_name')
                invoice.extracted_text = str(result.get('items', []))
                invoice.status = 'processed'
                invoice.processed_at = timezone.now()
                invoice.save()
                
                # Create invoice items
                for item_data in result.get('items', []):
                    InvoiceItem.objects.create(
                        invoice=invoice,
                        description=item_data.get('description', ''),
                        quantity=item_data.get('quantity', 0),
                        unit_price=item_data.get('unit_price', 0),
                        total_price=item_data.get('total_price', 0),
                        material_type=item_data.get('material_type', 'unknown'),
                        weight_kg=item_data.get('weight_kg', 0),
                        carbon_footprint_kg=item_data.get('carbon_footprint_kg', 0),
                        water_footprint_l=item_data.get('water_footprint_l', 0),
                        energy_footprint_kwh=item_data.get('energy_footprint_kwh', 0),
                    )
            else:
                invoice.status = 'failed'
                invoice.processing_errors = result.get('error', 'Unknown error')
                invoice.save()
                
        except Exception as e:
            invoice.status = 'failed'
            invoice.processing_errors = str(e)
            invoice.save()


class InvoiceListView(generics.ListAPIView):
    """View for listing user's invoices."""
    
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Invoice.objects.filter(user=self.request.user)


class InvoiceDetailView(generics.RetrieveAPIView):
    """View for getting invoice details."""
    
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Invoice.objects.filter(user=self.request.user)


class InvoiceProcessingStatusView(APIView):
    """View for checking invoice processing status."""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, invoice_id):
        invoice = get_object_or_404(Invoice, id=invoice_id, user=request.user)
        
        return Response({
            'invoice_id': invoice.id,
            'status': invoice.status,
            'processed_at': invoice.processed_at,
            'errors': invoice.processing_errors,
        })


class MaterialCategoryListView(generics.ListAPIView):
    """View for listing material categories."""
    
    serializer_class = MaterialCategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = MaterialCategory.objects.all()


class SupplierListView(generics.ListAPIView):
    """View for listing suppliers."""
    
    serializer_class = SupplierSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Supplier.objects.all()


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def invoice_statistics(request):
    """Get invoice statistics for the user."""
    user = request.user
    
    # Get total invoices
    total_invoices = Invoice.objects.filter(user=user).count()
    processed_invoices = Invoice.objects.filter(user=user, status='processed').count()
    
    # Get environmental impact totals
    impact_data = InvoiceItem.objects.filter(
        invoice__user=user,
        invoice__status='processed'
    ).aggregate(
        total_carbon=Sum('carbon_footprint_kg'),
        total_water=Sum('water_footprint_l'),
        total_energy=Sum('energy_footprint_kwh'),
        avg_sustainability=Avg('invoice__items__material_type')
    )
    
    # Get material breakdown
    material_breakdown = InvoiceItem.objects.filter(
        invoice__user=user,
        invoice__status='processed'
    ).values('material_type').annotate(
        total_carbon=Sum('carbon_footprint_kg'),
        total_water=Sum('water_footprint_l'),
        total_energy=Sum('energy_footprint_kwh'),
        count=Sum('quantity')
    )
    
    return Response({
        'total_invoices': total_invoices,
        'processed_invoices': processed_invoices,
        'processing_rate': (processed_invoices / total_invoices * 100) if total_invoices > 0 else 0,
        'environmental_impact': {
            'total_carbon_kg': impact_data['total_carbon'] or 0,
            'total_water_l': impact_data['total_water'] or 0,
            'total_energy_kwh': impact_data['total_energy'] or 0,
        },
        'material_breakdown': list(material_breakdown),
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def reprocess_invoice(request, invoice_id):
    """Reprocess a failed invoice."""
    invoice = get_object_or_404(Invoice, id=invoice_id, user=request.user)
    
    if invoice.status != 'failed':
        return Response({
            'error': 'Invoice is not in failed status'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Clear previous errors and reprocess
    invoice.processing_errors = None
    invoice.save()
    
    # Start reprocessing
    upload_view = InvoiceUploadView()
    upload_view.process_invoice_async(invoice)
    
    return Response({
        'message': 'Invoice reprocessing started',
        'invoice_id': invoice.id,
        'status': 'processing'
    })


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_invoice(request, invoice_id):
    """Delete an invoice."""
    invoice = get_object_or_404(Invoice, id=invoice_id, user=request.user)
    
    # Delete the file
    if invoice.file and os.path.exists(invoice.file.path):
        os.remove(invoice.file.path)
    
    # Delete the invoice
    invoice.delete()
    
    return Response({
        'message': 'Invoice deleted successfully'
    }, status=status.HTTP_204_NO_CONTENT) 