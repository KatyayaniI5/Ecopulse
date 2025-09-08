"""
Invoice processing module using NLP to extract environmental impact data.
"""

import re
import logging
from typing import Dict, List, Optional, Tuple
from decimal import Decimal
import spacy
from transformers import pipeline
import pandas as pd
import numpy as np
from datetime import datetime

logger = logging.getLogger(__name__)


class InvoiceProcessor:
    """Main class for processing invoices and extracting environmental data."""
    
    def __init__(self):
        """Initialize the invoice processor with NLP models."""
        try:
            # Load spaCy model for entity extraction
            self.nlp = spacy.load("en_core_web_sm")
            logger.info("Loaded spaCy model successfully")
        except OSError:
            logger.warning("spaCy model not found, downloading...")
            spacy.cli.download("en_core_web_sm")
            self.nlp = spacy.load("en_core_web_sm")
        
        # Initialize transformers pipeline for text classification
        try:
            self.classifier = pipeline("text-classification", model="distilbert-base-uncased")
            logger.info("Loaded transformers model successfully")
        except Exception as e:
            logger.warning(f"Could not load transformers model: {e}")
            self.classifier = None
        
        # Material categories and their environmental impact factors
        self.material_factors = {
            'plastic': {
                'carbon_factor': 2.5,  # kg CO2 per kg
                'water_factor': 100,   # liters per kg
                'energy_factor': 15,   # kWh per kg
                'sustainability_rating': 3
            },
            'paper': {
                'carbon_factor': 0.8,
                'water_factor': 50,
                'energy_factor': 5,
                'sustainability_rating': 7
            },
            'recycled_paper': {
                'carbon_factor': 0.4,
                'water_factor': 25,
                'energy_factor': 2.5,
                'sustainability_rating': 9
            },
            'aluminum': {
                'carbon_factor': 8.1,
                'water_factor': 200,
                'energy_factor': 50,
                'sustainability_rating': 4
            },
            'steel': {
                'carbon_factor': 1.8,
                'water_factor': 150,
                'energy_factor': 20,
                'sustainability_rating': 6
            },
            'glass': {
                'carbon_factor': 0.7,
                'water_factor': 80,
                'energy_factor': 8,
                'sustainability_rating': 8
            },
            'wood': {
                'carbon_factor': 0.3,
                'water_factor': 30,
                'energy_factor': 3,
                'sustainability_rating': 8
            },
            'cotton': {
                'carbon_factor': 2.1,
                'water_factor': 10000,
                'energy_factor': 12,
                'sustainability_rating': 5
            },
            'organic_cotton': {
                'carbon_factor': 1.5,
                'water_factor': 7000,
                'energy_factor': 8,
                'sustainability_rating': 7
            },
            'polyester': {
                'carbon_factor': 3.2,
                'water_factor': 200,
                'energy_factor': 18,
                'sustainability_rating': 4
            }
        }
    
    def extract_text_from_file(self, file_path: str) -> str:
        """Extract text from uploaded file (PDF, image, etc.)."""
        try:
            # For now, assume text is already extracted
            # In production, implement OCR and PDF processing
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Error extracting text from file: {e}")
            return ""
    
    def extract_invoice_metadata(self, text: str) -> Dict:
        """Extract basic invoice metadata using regex patterns."""
        metadata = {}
        
        # Extract invoice number
        invoice_patterns = [
            r'invoice\s*#?\s*(\w+)',
            r'invoice\s*number\s*:?\s*(\w+)',
            r'#\s*(\w+)',
        ]
        for pattern in invoice_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                metadata['invoice_number'] = match.group(1)
                break
        
        # Extract dates
        date_patterns = [
            r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
            r'(\d{4}-\d{2}-\d{2})',
        ]
        dates = []
        for pattern in date_patterns:
            matches = re.findall(pattern, text)
            dates.extend(matches)
        
        if dates:
            metadata['invoice_date'] = dates[0]
            if len(dates) > 1:
                metadata['due_date'] = dates[1]
        
        # Extract total amount
        amount_patterns = [
            r'total\s*:?\s*\$?(\d+\.?\d*)',
            r'amount\s*due\s*:?\s*\$?(\d+\.?\d*)',
            r'grand\s*total\s*:?\s*\$?(\d+\.?\d*)',
        ]
        for pattern in amount_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                metadata['total_amount'] = Decimal(match.group(1))
                break
        
        # Extract supplier information
        supplier_patterns = [
            r'from\s*:?\s*([^\n]+)',
            r'supplier\s*:?\s*([^\n]+)',
            r'vendor\s*:?\s*([^\n]+)',
        ]
        for pattern in supplier_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                metadata['supplier_name'] = match.group(1).strip()
                break
        
        return metadata
    
    def extract_items(self, text: str) -> List[Dict]:
        """Extract individual items from invoice text."""
        items = []
        
        # Split text into lines and look for item patterns
        lines = text.split('\n')
        
        for line in lines:
            # Look for patterns like: "Item Description Qty Price Total"
            item_pattern = r'([^0-9]+)\s+(\d+\.?\d*)\s+\$?(\d+\.?\d*)\s+\$?(\d+\.?\d*)'
            match = re.search(item_pattern, line)
            
            if match:
                item = {
                    'description': match.group(1).strip(),
                    'quantity': Decimal(match.group(2)),
                    'unit_price': Decimal(match.group(3)),
                    'total_price': Decimal(match.group(4)),
                }
                items.append(item)
        
        return items
    
    def classify_material(self, description: str) -> str:
        """Classify material type from item description using NLP."""
        description_lower = description.lower()
        
        # Keyword-based classification
        material_keywords = {
            'plastic': ['plastic', 'pvc', 'polyethylene', 'polypropylene', 'pet', 'abs'],
            'paper': ['paper', 'cardboard', 'card', 'sheet'],
            'recycled_paper': ['recycled', 'recycled paper', 'eco-friendly paper'],
            'aluminum': ['aluminum', 'aluminium', 'aluminum can', 'aluminium can'],
            'steel': ['steel', 'iron', 'metal'],
            'glass': ['glass', 'bottle', 'jar'],
            'wood': ['wood', 'wooden', 'timber', 'lumber'],
            'cotton': ['cotton', 'fabric', 'textile'],
            'organic_cotton': ['organic cotton', 'organic fabric'],
            'polyester': ['polyester', 'poly', 'synthetic fabric'],
        }
        
        for material, keywords in material_keywords.items():
            if any(keyword in description_lower for keyword in keywords):
                return material
        
        # Use spaCy for more sophisticated classification
        doc = self.nlp(description)
        
        # Look for material-related entities
        for ent in doc.ents:
            if ent.label_ in ['PRODUCT', 'ORG', 'MISC']:
                ent_text = ent.text.lower()
                for material, keywords in material_keywords.items():
                    if any(keyword in ent_text for keyword in keywords):
                        return material
        
        # Default to unknown material
        return 'unknown'
    
    def calculate_environmental_impact(self, item: Dict) -> Dict:
        """Calculate environmental impact for an item."""
        material_type = self.classify_material(item['description'])
        quantity = item.get('quantity', 1)
        
        # Default weight assumption (1 kg per unit if not specified)
        weight_kg = item.get('weight_kg', quantity)
        
        impact = {
            'material_type': material_type,
            'weight_kg': weight_kg,
            'carbon_footprint_kg': 0,
            'water_footprint_l': 0,
            'energy_footprint_kwh': 0,
        }
        
        if material_type in self.material_factors:
            factors = self.material_factors[material_type]
            impact['carbon_footprint_kg'] = weight_kg * factors['carbon_factor']
            impact['water_footprint_l'] = weight_kg * factors['water_factor']
            impact['energy_footprint_kwh'] = weight_kg * factors['energy_factor']
        
        return impact
    
    def process_invoice(self, file_path: str) -> Dict:
        """Main method to process an invoice and extract all relevant data."""
        try:
            # Extract text from file
            text = self.extract_text_from_file(file_path)
            if not text:
                raise ValueError("Could not extract text from file")
            
            # Extract metadata
            metadata = self.extract_invoice_metadata(text)
            
            # Extract items
            items = self.extract_items(text)
            
            # Calculate environmental impact for each item
            processed_items = []
            total_carbon = 0
            total_water = 0
            total_energy = 0
            
            for item in items:
                impact = self.calculate_environmental_impact(item)
                item.update(impact)
                processed_items.append(item)
                
                total_carbon += impact['carbon_footprint_kg']
                total_water += impact['water_footprint_l']
                total_energy += impact['energy_footprint_kwh']
            
            # Calculate overall invoice impact
            invoice_impact = {
                'total_carbon_footprint_kg': total_carbon,
                'total_water_footprint_l': total_water,
                'total_energy_footprint_kwh': total_energy,
                'sustainability_score': self.calculate_sustainability_score(processed_items),
            }
            
            return {
                'metadata': metadata,
                'items': processed_items,
                'environmental_impact': invoice_impact,
                'processing_status': 'success',
            }
            
        except Exception as e:
            logger.error(f"Error processing invoice: {e}")
            return {
                'processing_status': 'failed',
                'error': str(e),
            }
    
    def calculate_sustainability_score(self, items: List[Dict]) -> float:
        """Calculate overall sustainability score for the invoice."""
        if not items:
            return 0.0
        
        total_score = 0
        total_weight = 0
        
        for item in items:
            material_type = item.get('material_type', 'unknown')
            weight = item.get('weight_kg', 1)
            
            if material_type in self.material_factors:
                score = self.material_factors[material_type]['sustainability_rating']
            else:
                score = 5  # Default neutral score
            
            total_score += score * weight
            total_weight += weight
        
        return total_score / total_weight if total_weight > 0 else 0.0
    
    def get_material_alternatives(self, material_type: str) -> List[Dict]:
        """Get alternative materials with better environmental impact."""
        if material_type not in self.material_factors:
            return []
        
        current_rating = self.material_factors[material_type]['sustainability_rating']
        alternatives = []
        
        for alt_material, factors in self.material_factors.items():
            if alt_material != material_type and factors['sustainability_rating'] > current_rating:
                improvement = factors['sustainability_rating'] - current_rating
                alternatives.append({
                    'material': alt_material,
                    'sustainability_rating': factors['sustainability_rating'],
                    'improvement': improvement,
                    'carbon_factor': factors['carbon_factor'],
                    'water_factor': factors['water_factor'],
                    'energy_factor': factors['energy_factor'],
                })
        
        # Sort by improvement (highest first)
        alternatives.sort(key=lambda x: x['improvement'], reverse=True)
        return alternatives[:5]  # Return top 5 alternatives 