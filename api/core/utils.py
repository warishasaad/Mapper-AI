"""
Utility functions for the Estate Mapper System - Real Data Processing Only

Provides helper functions for field cleaning, validation, transformation,
dependency management, and general system utilities.
"""

import re
import subprocess
import sys
import time
import json
import csv
import os
import logging
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime, date
from .models import FieldType

# ==================== DEPENDENCY MANAGEMENT ====================

def install_dependencies():
    """Install required dependencies if not present"""
    required_packages = [
        "httpx", "requests", "python-dateutil"
    ]

    optional_packages = [
    "PyPDF2", "PyMuPDF", "reportlab", "Pillow"]

    for package in optional_packages:
        try:
            if package == "PyPDF2":
                import PyPDF2
            elif package == "PyMuPDF":
                import fitz
            elif package == "Pillow":
                import PIL
            elif package == "reportlab":
                import reportlab
            else:
                __import__(package.lower())
        except ImportError:
            print(f"⚠️  Optional package {package} not installed - some features may be limited")
        
    for package in required_packages:
        try:
            package_name = package.replace("-", "_").lower()
            if package_name == "pymupdf":
                __import__("fitz")
            else:
                __import__(package_name)
        except ImportError:
            print(f"Installing required package {package}...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"✅ {package} installed successfully")
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to install {package}: {e}")
    
    # Optional packages (warn but don't fail)
    for package in optional_packages:
        try:
            if package == "PyPDF2":
                import PyPDF2
            elif package == "PyMuPDF":
                import fitz
            elif package == "Pillow":
                import PIL
            elif package == "reportlab":
                import reportlab
            else:
                __import__(package.lower())
        except ImportError:
            print(f"⚠️  Optional package {package} not installed - some features may be limited")

# ==================== FIELD PROCESSING UTILITIES ====================

def clean_field_name(field_name: str) -> str:
    """Clean field name for matching"""
    if not field_name:
        return ""
    
    clean = field_name.lower().strip()
    # Replace common separators with underscores
    clean = re.sub(r'[_\-\s]+', '_', clean)
    # Remove special characters except underscores
    clean = re.sub(r'[^\w]', '', clean)
    
    return clean

def normalize_field_value(field_value: str) -> str:
    """Normalize field value by removing extra whitespace and common prefixes"""
    if not field_value:
        return ""
    
    # Remove extra whitespace
    normalized = re.sub(r'\s+', ' ', field_value.strip())
    
    # Remove common empty value indicators
    empty_indicators = ['n/a', 'na', 'none', 'not applicable', 'not available', 'null', 'nil']
    normalized_lower = normalized.lower()
    
    if normalized_lower in empty_indicators:
        return ""
    
    return normalized

def extract_field_keywords(field_name: str) -> List[str]:
    """Extract meaningful keywords from field name"""
    clean_name = clean_field_name(field_name)
    
    # Common stop words to ignore
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
        'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
        'this', 'that', 'these', 'those', 'your', 'my', 'our', 'their'
    }
    
    # Split into words and filter
    words = clean_name.split('_')
    keywords = [word for word in words if word not in stop_words and len(word) > 1]
    
    return keywords

def calculate_confidence(pattern: str, field_name: str, match_type: str = "general") -> str:
    """Calculate confidence level for a field mapping"""
    
    # Exact matches get high confidence
    if match_type == "exact":
        return "high"
    
    # Semantic matches get medium to high
    if match_type == "semantic":
        return "medium"
    
    # Calculate word overlap for pattern matching
    pattern_words = set(pattern.lower().replace('_', ' ').split())
    field_words = set(field_name.lower().replace('_', ' ').split())
    
    if not pattern_words or not field_words:
        return "low"
    
    # Calculate Jaccard similarity
    intersection = len(pattern_words.intersection(field_words))
    union = len(pattern_words.union(field_words))
    
    jaccard = intersection / union if union > 0 else 0
    
    if jaccard >= 0.7:
        return "high"
    elif jaccard >= 0.4:
        return "medium"
    else:
        return "low"

# ==================== FIELD TYPE DETERMINATION ====================

def determine_field_type(cadence_path: str) -> FieldType:
    """Determine field type from Cadence path"""
    if not cadence_path:
        return FieldType.IDENTITY
    
    path_lower = cadence_path.lower()
    
    # Date fields
    if any(term in path_lower for term in ['date', '_of_birth', '_of_death', 'birth_date', 'death_date']):
        return FieldType.DATE
    
    # Contact fields
    elif any(term in path_lower for term in ['phone', 'email', 'telephone', 'contact']):
        return FieldType.CONTACT
    
    # Address fields
    elif any(term in path_lower for term in ['address', 'location', 'place_', 'street', 'city', 'postal', 'province']):
        return FieldType.ADDRESS
    
    # Relationship fields
    elif any(term in path_lower for term in ['relationship', 'spouse', 'child', 'parent', 'executor']):
        return FieldType.RELATIONSHIP
    
    # Financial fields
    elif any(term in path_lower for term in ['value', 'amount', 'cost', 'price', 'income', 'estate_value', 'financial']):
        return FieldType.FINANCIAL
    
    # Legal fields
    elif any(term in path_lower for term in ['will', 'legal', 'court', 'probate', 'administration']):
        return FieldType.LEGAL
    
    # Insurance fields
    elif any(term in path_lower for term in ['insurance', 'policy', 'coverage', 'benefit']):
        return FieldType.INSURANCE
    
    # Property fields
    elif any(term in path_lower for term in ['property', 'real_estate', 'land', 'home']):
        return FieldType.PROPERTY
    
    # Account fields
    elif any(term in path_lower for term in ['account', 'bank', 'rrsp', 'tfsa', 'rrif']):
        return FieldType.ACCOUNT
    
    # Task planner fields
    elif 'task_planner' in path_lower:
        return FieldType.TASK_PLANNER
    
    # Document fields
    elif any(term in path_lower for term in ['document', 'certificate', 'record']):
        return FieldType.DOCUMENT
    
    # Default to identity
    else:
        return FieldType.IDENTITY

def infer_field_type_from_value(field_value: str) -> Optional[FieldType]:
    """Infer field type from the value itself"""
    if not field_value:
        return None
    
    value = field_value.strip()
    
    # Email pattern
    if re.match(r'^[^@]+@[^@]+\.[^@]+$', value):
        return FieldType.CONTACT
    
    # Phone number patterns (more comprehensive)
    phone_digits = re.sub(r'[^\d]', '', value)
    if len(phone_digits) in [10, 11] and phone_digits.isdigit():
        return FieldType.CONTACT
    
    # Date patterns
    date_patterns = [
        r'^\d{4}-\d{2}-\d{2}$',      # YYYY-MM-DD
        r'^\d{2}/\d{2}/\d{4}$',      # MM/DD/YYYY
        r'^\d{1,2}/\d{1,2}/\d{4}$',  # M/D/YYYY
        r'^\d{8}$',                  # YYYYMMDD
        r'^\d{2}-\d{2}-\d{4}$',      # MM-DD-YYYY
    ]
    if any(re.match(pattern, value) for pattern in date_patterns):
        return FieldType.DATE
    
    # Currency pattern
    currency_cleaned = re.sub(r'[^\d.,]', '', value)
    if re.match(r'^\d+([,.]\d{1,2})?$', currency_cleaned):
        return FieldType.FINANCIAL
    
    # Canadian SIN pattern
    sin_digits = re.sub(r'[^\d]', '', value)
    if len(sin_digits) == 9 and sin_digits.isdigit():
        return FieldType.IDENTITY
    
    # Canadian postal code pattern
    if re.match(r'^[A-Za-z]\d[A-Za-z]\s?\d[A-Za-z]\d$', value):
        return FieldType.ADDRESS
    
    return None

# ==================== TEMPLATE GENERATION ====================

def generate_template(cadence_path: str) -> str:
    """Generate handlebars template with proper helpers"""
    
    if not cadence_path or cadence_path == "unknown.field":
        return "{{unknown.field}}"
    
    # Clean path for template
    clean_path = cadence_path.strip()
    
    # Name fields with formatting helpers
    if "name" in clean_path:
        if clean_path.endswith(".last") or "last_name" in clean_path:
            return f"{{{{#name:last {clean_path}}}}}"
        elif clean_path.endswith(".first") or "first_name" in clean_path:
            return f"{{{{#name:first {clean_path}}}}}"
        else:
            return f"{{{{#name {clean_path}}}}}"
    
    # Social Insurance Number with formatting
    elif "social_insurance_number" in clean_path or "sin" in clean_path:
        return f"{{{{#sin {clean_path}}}}}"
    
    # Date fields with formatting
    elif "date" in clean_path:
        if "yyyymmdd" in clean_path:
            base_path = clean_path.replace("_yyyymmdd", "")
            return f"{{{{#date:yyyymmdd {base_path}}}}}"
        elif "mdy" in clean_path:
            base_path = clean_path.replace("_mdy", "")
            return f"{{{{#date:mdy {base_path}}}}}"
        else:
            return f"{{{{#date {clean_path}}}}}"
    
    # Phone fields with formatting
    elif "phone" in clean_path:
        return f"{{{{#phone {clean_path}}}}}"
    
    # Address/location fields
    elif any(term in clean_path for term in ["address", "location", "place"]):
        if "province_code" in clean_path:
            return f"{{{{#location:province_code {clean_path}}}}}"
        elif "city_province" in clean_path:
            return f"{{{{#location:city_province {clean_path}}}}}"
        else:
            return f"{{{{#location {clean_path}}}}}"
    
    # Postal code with formatting
    elif "postal_code" in clean_path:
        return f"{{{{#postal_code {clean_path}}}}}"
    
    # Currency/financial fields
    elif any(term in clean_path for term in ["value", "amount", "cost", "price", "financial"]):
        return f"{{{{#currency {clean_path}}}}}"
    
    # Boolean/checkbox fields
    elif clean_path.startswith("task_planner.b_") or "checkbox" in clean_path:
        return f"{{{{#checkbox {clean_path}}}}}"
    
    # Array access patterns
    elif "[" in clean_path or ".0." in clean_path:
        # Handle array indexing
        if "name" in clean_path:
            return f"{{{{#name {clean_path}}}}}"
        elif "phone" in clean_path:
            return f"{{{{#phone {clean_path}}}}}"
        elif "address" in clean_path:
            return f"{{{{#location {clean_path}}}}}"
        else:
            return f"{{{{{clean_path}}}}}"
    
    # Email (direct access, no helper needed)
    elif "email" in clean_path:
        return f"{{{{{clean_path}}}}}"
    
    # Default case - direct property access
    else:
        return f"{{{{{clean_path}}}}}"

# ==================== VALIDATION UTILITIES ====================

def validate_field_value(field_name: str, field_value: str, cadence_path: str) -> Tuple[List[str], List[str]]:
    """Validate field value and return errors and warnings"""
    errors = []
    warnings = []
    
    if not field_value or not field_value.strip():
        return errors, warnings
    
    # Get validation rules based on path and field name
    rules = get_validation_rules_for_path(cadence_path, field_name)
    
    # Apply validation rules
    for rule in rules:
        try:
            if rule == "sin_format":
                if not validate_canadian_sin_format(field_value):
                    errors.append("Invalid SIN format")
            elif rule == "sin_checksum":
                if not validate_canadian_sin_checksum(field_value):
                    errors.append("Invalid SIN checksum")
            elif rule == "phone_format":
                if not validate_canadian_phone(field_value):
                    warnings.append("Phone number format may be invalid")
            elif rule == "email_format":
                if not validate_email_format(field_value):
                    errors.append("Invalid email format")
            elif rule == "date_format":
                if not validate_date_format(field_value):
                    warnings.append("Date format may need standardization")
            elif rule == "postal_code":
                if not validate_canadian_postal_code(field_value):
                    warnings.append("Postal code format may be invalid")
            elif rule.startswith("min_length:"):
                min_len = int(rule.split(":")[1])
                if len(field_value.strip()) < min_len:
                    warnings.append(f"Field may be too short (minimum {min_len} characters)")
        except Exception as e:
            warnings.append(f"Validation error: {str(e)}")
    
    return errors, warnings

def get_validation_rules_for_path(cadence_path: str, field_name: str = "") -> List[str]:
    """Get appropriate validation rules for a field"""
    rules = []
    path_lower = cadence_path.lower()
    name_lower = field_name.lower()
    
    # SIN validation
    if "sin" in path_lower or "social_insurance" in path_lower or "sin" in name_lower:
        rules.extend(["sin_format", "sin_checksum"])
    
    # Phone validation
    elif "phone" in path_lower or "telephone" in name_lower:
        rules.append("phone_format")
    
    # Email validation
    elif "email" in path_lower or "email" in name_lower:
        rules.append("email_format")
    
    # Date validation
    elif "date" in path_lower or any(term in name_lower for term in ["date", "birth", "death"]):
        rules.append("date_format")
    
    # Postal code validation
    elif "postal_code" in path_lower or "postal" in name_lower:
        rules.append("postal_code")
    
    # Name fields
    elif "name" in path_lower or "name" in name_lower:
        rules.append("min_length:2")
    
    # Address fields
    elif "address" in path_lower or "address" in name_lower:
        rules.append("min_length:5")
    
    return rules

def validate_canadian_postal_code(postal_code: str) -> bool:
    """Validate Canadian postal code format"""
    if not postal_code:
        return True
    
    # Canadian postal code pattern: A1A 1A1
    pattern = r'^[A-Za-z]\d[A-Za-z]\s?\d[A-Za-z]\d$'
    return re.match(pattern, postal_code.strip()) is not None

def validate_canadian_sin_format(sin: str) -> bool:
    """Validate Canadian SIN format"""
    if not sin:
        return True
    
    # Remove non-digits
    digits = re.sub(r'[^\d]', '', sin)
    return len(digits) == 9

def validate_canadian_sin_checksum(sin: str) -> bool:
    """Validate Canadian Social Insurance Number using Luhn algorithm"""
    if not sin:
        return True
    
    # Remove non-digits
    digits = re.sub(r'[^\d]', '', sin)
    
    if len(digits) != 9:
        return False
    
    try:
        # Luhn algorithm check
        checksum = 0
        for i, digit in enumerate(digits):
            n = int(digit)
            if i % 2 == 1:  # Every second digit
                n *= 2
                if n > 9:
                    n = n // 10 + n % 10
            checksum += n
        
        return checksum % 10 == 0
    except:
        return False

def validate_canadian_phone(phone: str) -> bool:
    """Validate Canadian phone number"""
    if not phone:
        return True
    
    digits = re.sub(r'[^\d]', '', phone)
    
    # Must be 10 or 11 digits
    if len(digits) == 10:
        # Valid Canadian area codes (subset)
        area_code = digits[:3]
        canadian_area_codes = [
            '204', '236', '249', '250', '289', '306', '343', '365', '403',
            '416', '418', '431', '437', '438', '450', '506', '514', '519',
            '548', '579', '581', '587', '604', '613', '639', '647', '672',
            '705', '709', '742', '778', '780', '782', '807', '819', '825',
            '867', '873', '902', '905'
        ]
        return area_code in canadian_area_codes
    elif len(digits) == 11 and digits[0] == '1':
        # North American with country code
        return validate_canadian_phone(digits[1:])
    
    return len(digits) >= 10

def validate_email_format(email: str) -> bool:
    """Validate email format"""
    if not email:
        return True
    
    # Basic email validation
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email.strip()) is not None

def validate_date_format(date_str: str) -> bool:
    """Validate date format"""
    if not date_str:
        return True
    
    # Accept various date formats
    date_patterns = [
        r'^\d{4}-\d{2}-\d{2}$',      # YYYY-MM-DD
        r'^\d{2}/\d{2}/\d{4}$',      # MM/DD/YYYY
        r'^\d{1,2}/\d{1,2}/\d{4}$',  # M/D/YYYY
        r'^\d{8}$',                  # YYYYMMDD
        r'^\d{2}-\d{2}-\d{4}$',      # MM-DD-YYYY
        r'^\d{4}/\d{2}/\d{2}$',      # YYYY/MM/DD
    ]
    
    return any(re.match(pattern, date_str.strip()) for pattern in date_patterns)

# ==================== FORMATTING UTILITIES ====================

def format_time(seconds: float) -> str:
    """Format time duration in human-readable format"""
    if seconds < 0.001:
        return f"{seconds*1000000:.0f}μs"
    elif seconds < 1:
        return f"{seconds*1000:.1f}ms"
    elif seconds < 60:
        return f"{seconds:.2f}s"
    else:
        minutes = int(seconds // 60)
        remaining_seconds = seconds % 60
        return f"{minutes}m {remaining_seconds:.1f}s"

def format_percentage(value: float, total: float = None) -> str:
    """Format percentage with proper handling of zero division"""
    if total is not None:
        if total == 0:
            return "0.0%"
        percentage = (value / total) * 100
    else:
        percentage = value
    
    return f"{percentage:.1f}%"

def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    size = float(size_bytes)
    
    while size >= 1024.0 and i < len(size_names) - 1:
        size /= 1024.0
        i += 1
    
    return f"{size:.1f} {size_names[i]}"

def format_currency(value: str) -> str:
    """Format currency value"""
    if not value:
        return ""
    
    # Remove non-numeric characters except decimal point
    clean_value = re.sub(r'[^\d.,]', '', value)
    
    try:
        # Handle different decimal separators
        if ',' in clean_value and '.' in clean_value:
            # Assume last separator is decimal
            if clean_value.rfind(',') > clean_value.rfind('.'):
                clean_value = clean_value.replace('.', '').replace(',', '.')
            else:
                clean_value = clean_value.replace(',', '')
        elif ',' in clean_value:
            # Could be thousands separator or decimal
            parts = clean_value.split(',')
            if len(parts) == 2 and len(parts[1]) <= 2:
                # Likely decimal separator
                clean_value = clean_value.replace(',', '.')
            else:
                # Likely thousands separator
                clean_value = clean_value.replace(',', '')
        
        float_value = float(clean_value)
        return f"${float_value:,.2f}"
    except:
        return value

def truncate_text(text: str, max_length: int = 50, suffix: str = "...") -> str:
    """Truncate text to specified length with suffix"""
    if not text or len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix

# ==================== SYSTEM UTILITIES ====================

def check_system_requirements() -> Dict[str, bool]:
    """Check system requirements and dependencies"""
    requirements = {
        "python_version": sys.version_info >= (3, 8),
        "httpx": False,
        "requests": False,
        "json": True,  # Built-in
        "csv": True,   # Built-in
        "re": True,    # Built-in
    }
    
    # Check optional dependencies
    optional_deps = ["httpx", "requests", "PyPDF2", "fitz", "reportlab"]
    
    for dep in optional_deps:
        try:
            if dep == "fitz":
                import fitz
            else:
                __import__(dep)
            requirements[dep] = True
        except ImportError:
            requirements[dep] = False
    
    return requirements

def get_system_info() -> Dict[str, Any]:
    """Get comprehensive system information"""
    import platform
    
    return {
        "platform": platform.platform(),
        "python_version": platform.python_version(),
        "architecture": platform.architecture()[0],
        "processor": platform.processor() or "Unknown",
        "current_directory": os.getcwd(),
        "timestamp": datetime.now().isoformat(),
        "requirements": check_system_requirements()
    }

# ==================== DATA PROCESSING UTILITIES ====================

def extract_potential_fields_from_text(text: str) -> Dict[str, str]:
    """Extract potential field-value pairs from text"""
    fields = {}
    
    # Common field-value patterns
    patterns = [
        r'([A-Za-z\s]+):\s*([^\n\r]+)',      # "Field Name: Value"
        r'([A-Za-z\s]+)\s*=\s*([^\n\r]+)',   # "Field Name = Value"
        r'([A-Za-z\s]+)\s*\|\s*([^\n\r]+)',  # "Field Name | Value"
        r'([A-Za-z\s]+)\s*-\s*([^\n\r]+)',   # "Field Name - Value"
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text)
        for field_name, field_value in matches:
            field_name = field_name.strip()
            field_value = field_value.strip()
            
            # Filter out obvious non-fields
            if (3 <= len(field_name) <= 50 and 
                1 <= len(field_value) <= 200 and
                not field_name.lower().startswith(('the ', 'this ', 'that ', 'these '))):
                fields[field_name] = field_value
    
    return fields

def clean_extracted_fields(fields: Dict[str, str]) -> Dict[str, str]:
    """Clean extracted fields by removing invalid entries"""
    cleaned = {}
    
    # Words that indicate this is not a real field
    invalid_indicators = {
        'page', 'section', 'form', 'instructions', 'note', 'warning',
        'example', 'sample', 'demo', 'test', 'lorem', 'ipsum'
    }
    
    for field_name, field_value in fields.items():
        field_name_lower = field_name.lower()
        
        # Skip fields with invalid indicators
        if any(indicator in field_name_lower for indicator in invalid_indicators):
            continue
        
        # Skip very short or very long field names
        if len(field_name) < 3 or len(field_name) > 50:
            continue
        
        # Skip empty or whitespace-only values
        if not field_value or not field_value.strip():
            continue
        
        # Normalize the value
        normalized_value = normalize_field_value(field_value)
        if normalized_value:
            cleaned[field_name] = normalized_value
    
    return cleaned

# ==================== EXPORT FUNCTIONS ====================

def export_mapping_results_to_csv(results: List, filename: str) -> bool:
    """Export mapping results to CSV file"""
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'field_name', 'cadence_path', 'template', 'confidence',
                'field_type', 'processing_time', 'validation_errors', 'warnings',
                'conditional_logic', 'subject_resolved'
            ]
            
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for result in results:
                # Handle metadata safely
                metadata = getattr(result, 'metadata', {}) or {}
                subject_resolved = metadata.get('dynamic_subject_resolved', False)
                
                row = {
                    'field_name': result.field_name,
                    'cadence_path': result.cadence_path,
                    'template': result.template,
                    'confidence': result.confidence,
                    'field_type': result.field_type.value if hasattr(result.field_type, 'value') else str(result.field_type),
                    'processing_time': f"{result.processing_time:.4f}",
                    'validation_errors': '; '.join(result.validation_errors) if result.validation_errors else '',
                    'warnings': '; '.join(result.warnings) if result.warnings else '',
                    'conditional_logic': 'Yes' if result.conditional_logic else 'No',
                    'subject_resolved': 'Yes' if subject_resolved else 'No'
                }
                writer.writerow(row)
        
        return True
    except Exception as e:
        logging.error(f"Failed to export to CSV: {e}")
        return False

def export_statistics_to_json(stats: Dict, filename: str) -> bool:
    """Export statistics to JSON file"""
    try:
        # Convert any non-serializable objects
        def make_serializable(obj):
            if isinstance(obj, dict):
                return {key: make_serializable(value) for key, value in obj.items()}
            elif isinstance(obj, list):
                return [make_serializable(item) for item in obj]
            elif hasattr(obj, 'value'):  # Enum objects
                return obj.value
            elif hasattr(obj, '__dict__'):  # Custom objects
                return make_serializable(obj.__dict__)
            elif isinstance(obj, (int, float, str, bool, type(None))):
                return obj
            else:
                return str(obj)
        
        serializable_stats = make_serializable(stats)
        
        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(serializable_stats, jsonfile, indent=2, ensure_ascii=False)
        
        return True
    except Exception as e:
        logging.error(f"Failed to export to JSON: {e}")
        return False

# ==================== CONFIGURATION UTILITIES ====================

def load_config_file(config_path: str) -> Dict:
    """Load configuration from JSON file"""
    try:
        if not os.path.exists(config_path):
            logging.warning(f"Config file not found: {config_path}")
            return {}
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        logging.info(f"Configuration loaded from {config_path}")
        return config
    except Exception as e:
        logging.error(f"Error loading config file: {e}")
        return {}

def save_config_file(config: Dict, config_path: str) -> bool:
    """Save configuration to JSON file"""
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        logging.info(f"Configuration saved to {config_path}")
        return True
    except Exception as e:
        logging.error(f"Error saving config file: {e}")
        return False

# ==================== LOGGING UTILITIES ====================

def setup_logging(level: str = "INFO", log_file: str = "estate_mapper.log") -> None:
    """Setup logging configuration"""
    
    # Create logs directory if it doesn't exist
    log_dir = os.path.dirname(log_file) if os.path.dirname(log_file) else "."
    os.makedirs(log_dir, exist_ok=True)
    
    format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format=format_string,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(log_file, mode='a', encoding='utf-8')
        ]
    )
    
    # Log system startup
    logging.info("Estate Mapper System - Logging initialized")
    logging.info(f"Log level: {level}")
    logging.info(f"Log file: {log_file}")

def create_progress_indicator(current: int, total: int, width: int = 50) -> str:
    """Create a simple ASCII progress indicator"""
    if total == 0:
        return "[" + "█" * width + "] 100.0%"
    
    progress = min(current / total, 1.0)
    filled = int(width * progress)
    bar = "█" * filled + "░" * (width - filled)
    percentage = progress * 100
    
    return f"[{bar}] {percentage:.1f}% ({current}/{total})"

# ==================== FILE UTILITIES ====================

def validate_file_path(file_path: str, extensions: List[str] = None) -> bool:
    """Validate file path and extensions"""
    if not file_path:
        return False
    
    if not os.path.exists(file_path):
        return False
    
    if not os.path.isfile(file_path):
        return False
    
    if extensions:
        file_ext = os.path.splitext(file_path)[1].lower()
        return file_ext in [ext.lower() if ext.startswith('.') else f'.{ext.lower()}' for ext in extensions]
    
    return True

def get_file_info(file_path: str) -> Dict[str, Any]:
    """Get comprehensive file information"""
    if not os.path.exists(file_path):
        return {"error": "File not found"}
    
    try:
        stat_info = os.stat(file_path)
        return {
            "size": stat_info.st_size,
            "size_formatted": format_file_size(stat_info.st_size),
            "modified": time.ctime(stat_info.st_mtime),
            "extension": os.path.splitext(file_path)[1],
            "filename": os.path.basename(file_path),
            "directory": os.path.dirname(file_path),
            "absolute_path": os.path.abspath(file_path)
        }
    except Exception as e:
        return {"error": f"Error getting file info: {e}"}

# ==================== INITIALIZATION ====================

def initialize_utils():
    """Initialize utilities and perform system checks"""
    # Setup basic logging if not already configured
    if not logging.getLogger().handlers:
        setup_logging()
    
    # Log system information
    system_info = get_system_info()
    logging.info("System Information:")
    logging.info(f"  Platform: {system_info['platform']}")
    logging.info(f"  Python Version: {system_info['python_version']}")
    logging.info(f"  Architecture: {system_info['architecture']}")
    
    # Check requirements
    requirements = check_system_requirements()
    logging.info("System Requirements:")
    for req, status in requirements.items():
        status_str = "✅" if status else "❌"
        logging.info(f"  {req}: {status_str}")
    
    logging.info("Estate Mapper Utilities initialized successfully")

# Auto-initialize when module is imported
if __name__ != "__main__":
    try:
        initialize_utils()
    except Exception as e:
        print(f"Warning: Utils initialization failed: {e}")

# Module test function
def test_utils():
    """Test utility functions"""
    print("Testing Estate Mapper Utilities...")
    
    # Test field cleaning
    test_field = "Deceased's Full Name"
    cleaned = clean_field_name(test_field)
    print(f"Field cleaning: '{test_field}' -> '{cleaned}'")
    
    # Test validation
    test_sin = "123-456-782"
    sin_valid = validate_canadian_sin_checksum(test_sin)
    print(f"SIN validation: '{test_sin}' -> {sin_valid}")
    
    # Test template generation
    test_path = "deceased.name"
    template = generate_template(test_path)
    print(f"Template generation: '{test_path}' -> '{template}'")
    
    # Test field type determination
    field_type = determine_field_type("contact[*].email.email_address")
    print(f"Field type: contact email -> {field_type}")
    
    print("✅ Utilities test completed")

if __name__ == "__main__":
    test_utils()