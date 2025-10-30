from rest_framework import serializers
from .models import Invoice, InvoiceItem, MaterialCategory, Supplier


class InvoiceItemSerializer(serializers.ModelSerializer):
    """Serializer for invoice items."""
    
    class Meta:
        model = InvoiceItem
        fields = [
            'id', 'description', 'quantity', 'unit_price', 'total_price',
            'material_type', 'weight_kg', 'volume_l',
            'carbon_footprint_kg', 'water_footprint_l', 'energy_footprint_kwh',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class InvoiceSerializer(serializers.ModelSerializer):
    """Serializer for invoices."""
    
    items = InvoiceItemSerializer(many=True, read_only=True)
    user = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = Invoice
        fields = [
            'id', 'user', 'file', 'file_name', 'file_size', 'file_type',
            'invoice_number', 'invoice_date', 'due_date', 'total_amount', 'currency',
            'supplier_name', 'supplier_address', 'supplier_email',
            'status', 'extracted_text', 'processing_errors',
            'items', 'created_at', 'updated_at', 'processed_at'
        ]
        read_only_fields = [
            'id', 'user', 'file_name', 'file_size', 'file_type',
            'status', 'extracted_text', 'processing_errors',
            'created_at', 'updated_at', 'processed_at'
        ]


class InvoiceUploadSerializer(serializers.ModelSerializer):
    """Serializer for invoice upload."""
    
    class Meta:
        model = Invoice
        fields = ['file']
    
    def validate_file(self, value):
        """Validate uploaded file."""
        # Check file size (10MB limit)
        if value.size > 10 * 1024 * 1024:
            raise serializers.ValidationError("File size must be less than 10MB")
        
        # Check file type
        allowed_types = ['application/pdf', 'image/jpeg', 'image/png', 'text/plain']
        if value.content_type not in allowed_types:
            raise serializers.ValidationError("File type not supported. Please upload PDF, JPEG, PNG, or text files.")
        
        return value
    
    def create(self, validated_data):
        """Create invoice record with file information."""
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['user'] = request.user
        
        # Set file metadata
        file_obj = validated_data['file']
        validated_data['file_name'] = file_obj.name
        validated_data['file_size'] = file_obj.size
        validated_data['file_type'] = file_obj.content_type
        
        return super().create(validated_data)


class MaterialCategorySerializer(serializers.ModelSerializer):
    """Serializer for material categories."""
    
    class Meta:
        model = MaterialCategory
        fields = [
            'id', 'name', 'description',
            'carbon_factor_kg_co2_per_kg', 'water_factor_l_per_kg', 'energy_factor_kwh_per_kg',
            'sustainability_rating', 'alternatives', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class SupplierSerializer(serializers.ModelSerializer):
    """Serializer for suppliers."""
    
    class Meta:
        model = Supplier
        fields = [
            'id', 'name', 'address', 'email', 'phone', 'website',
            'sustainability_rating', 'has_sustainability_certification', 'sustainability_certifications',
            'has_environmental_policy', 'carbon_neutral', 'renewable_energy_usage',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class InvoiceProcessingResultSerializer(serializers.Serializer):
    """Serializer for invoice processing results."""
    
    processing_status = serializers.CharField()
    metadata = serializers.DictField(required=False)
    items = serializers.ListField(required=False)
    environmental_impact = serializers.DictField(required=False)
    error = serializers.CharField(required=False)


class EnvironmentalImpactSerializer(serializers.Serializer):
    """Serializer for environmental impact data."""
    
    total_carbon_footprint_kg = serializers.DecimalField(max_digits=10, decimal_places=3)
    total_water_footprint_l = serializers.DecimalField(max_digits=10, decimal_places=3)
    total_energy_footprint_kwh = serializers.DecimalField(max_digits=10, decimal_places=3)
    sustainability_score = serializers.FloatField()
    
    # Breakdown by material
    material_breakdown = serializers.DictField(required=False)
    
    # Comparison data
    industry_average = serializers.DictField(required=False)
    improvement_potential = serializers.DictField(required=False) 