"""
Core mapping generation and field variations

Handles comprehensive mapping pattern generation, field variations,
and semantic analysis for estate form fields.

ENHANCED: Now includes PDF form field pattern recognition to fix unmapped fields
"""

from typing import Dict, List, Tuple, Set, Optional
import re
from .models import MappingPattern, FieldType
from .schema import cadence_schema

class PDFFieldProcessor:
    """Handles PDF-specific field naming patterns and normalization"""
    
    def __init__(self):
        # PDF form field prefixes and their meanings
        self.pdf_prefixes = {
            'txtf': 'text_field',
            'txtF': 'text_field', 
            'rb': 'radio_button',
            'cb': 'checkbox',
            'dte': 'date_field',
            'dd': 'dropdown',
            'btn': 'button'
        }
        
        # Common PDF form structure patterns to remove
        self.structure_patterns = [
            r'SC_ISP\d+\[0\]\.',      # Adobe form document prefix
            r'#pageSet\s*->\s*',       # Page set references
            r'Page\d+\s*->\s*',        # Page references
            r'page\d+\[0\]\.',         # Page array references
            r'#subform\s*->\s*',       # Subform references
            r'sub_[^\.]*\.',           # Sub-element prefixes
            r'\[0\]',                  # Array index [0]
            r'\[\d+\]',                # Array indices [1], [2], etc.
            r'BR\s+\d+\s*->\s*',      # Business rule references
        ]
    
    def clean_pdf_field_name(self, field_name: str) -> str:
        """Clean PDF field names to extract meaningful content"""
        if not field_name:
            return ""
        
        cleaned = field_name
        
        # Remove PDF structure patterns
        for pattern in self.structure_patterns:
            cleaned = re.sub(pattern, '', cleaned)
        
        # Normalize arrow separators and underscores
        cleaned = re.sub(r'\s*->\s*', ' ', cleaned)
        cleaned = re.sub(r'_', ' ', cleaned)
        
        # Remove extra whitespace
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        
        return cleaned
    
    def extract_pdf_field_info(self, field_name: str) -> Dict[str, str]:
        """Extract field type and base name from PDF field"""
        cleaned = self.clean_pdf_field_name(field_name)
        
        # Extract prefix
        prefix_match = re.match(r'^(txtf|txtF|rb|cb|dte|dd|btn)\s*(.*)$', cleaned, re.IGNORECASE)
        
        if prefix_match:
            prefix = prefix_match.group(1).lower()
            base_name = prefix_match.group(2).strip()
            field_type = self.pdf_prefixes.get(prefix, 'unknown')
            
            return {
                'prefix': prefix,
                'base_name': base_name,
                'field_type': field_type,
                'cleaned_name': cleaned
            }
        
        return {
            'prefix': '',
            'base_name': cleaned,
            'field_type': 'unknown',
            'cleaned_name': cleaned
        }

class EnhancedPatternMatcher:
    """Enhanced pattern matching for PDF form fields and semantic content"""
    
    def __init__(self):
        self.pdf_processor = PDFFieldProcessor()
        self.direct_pdf_mappings = self._get_direct_pdf_mappings()
        self.semantic_pdf_patterns = self._get_semantic_pdf_patterns()
    
    def _get_direct_pdf_mappings(self) -> Dict[str, str]:
        """Direct mappings for common PDF field names that were unmapped"""
        return {
            # CRITICAL FIXES - These were the 14 unmapped fields
            'txtF Sin': 'applicant.social_insurance_number',
            'txtf sin': 'applicant.social_insurance_number',
            'sin': 'applicant.social_insurance_number',
            
            'txtF FirstName': 'applicant.first_name',
            'txtf firstname': 'applicant.first_name', 
            'first name': 'applicant.first_name',
            'firstname': 'applicant.first_name',
            
            'txtF MiddleName': 'applicant.middle_name',
            'txtf middlename': 'applicant.middle_name',
            'middle name': 'applicant.middle_name',
            'middlename': 'applicant.middle_name',
            
            'txtF FamilyName': 'applicant.last_name',
            'txtf familyname': 'applicant.last_name',
            'family name': 'applicant.last_name',
            'familyname': 'applicant.last_name',
            'last name': 'applicant.last_name',
            
            'txtF EmailAddress': 'applicant.email_address',
            'txtf emailaddress': 'applicant.email_address',
            'email address': 'applicant.email_address',
            'emailaddress': 'applicant.email_address',
            
            'txtF relationship': 'estate_reps[*].relationship',
            'txtf relationship': 'estate_reps[*].relationship',
            'relationship': 'estate_reps[*].relationship',
            
            'txtF NamesOnTheAccount': 'financial_information.account_names',
            'txtf namesontheaccount': 'financial_information.account_names',
            'names on the account': 'financial_information.account_names',
            'namesontheaccount': 'financial_information.account_names',
            
            'dte Date of Signature': 'form_completion.signature_date',
            'dte date of signature': 'form_completion.signature_date',
            'date of signature': 'form_completion.signature_date',
            
            'dte dateWitnessSignature': 'form_completion.witness_signature_date',
            'dte datewitnesssignature': 'form_completion.witness_signature_date',
            'date witness signature': 'form_completion.witness_signature_date',
            'datewitnesssignature': 'form_completion.witness_signature_date',
            
            # Additional common PDF field patterns
            'txtF Dob': 'applicant.date_of_birth',
            'txtf dob': 'applicant.date_of_birth',
            'dob': 'applicant.date_of_birth',
            
            'txtF Date Death': 'deceased.date_of_death',
            'txtf date death': 'deceased.date_of_death',
            'date death': 'deceased.date_of_death',
            
            'txtF LastNameBirth': 'deceased.last_name',
            'txtf lastnamebirth': 'deceased.last_name',
            'last name birth': 'deceased.last_name',
            
            'txtF HomeAddress': 'applicant.address.street_address',
            'txtf homeaddress': 'applicant.address.street_address',
            'home address': 'applicant.address.street_address',
            
            'txtF Country': 'applicant.address.country',
            'txtf country': 'applicant.address.country',
            'country': 'applicant.address.country',
            
            'txtF city': 'applicant.address.city',
            'txtf city': 'applicant.address.city',
            'city': 'applicant.address.city',
            
            'txtF province': 'applicant.address.province',
            'txtf province': 'applicant.address.province',
            'province': 'applicant.address.province',
            
            'txtF postalcode': 'applicant.address.postal_code',
            'txtf postalcode': 'applicant.address.postal_code',
            'postal code': 'applicant.address.postal_code',
            'postalcode': 'applicant.address.postal_code',
            
            'txtF telephone': 'applicant.phone_number',
            'txtf telephone': 'applicant.phone_number',
            'telephone': 'applicant.phone_number',
            
            'txtF signature': 'form_completion.signatures[*]',
            'txtf signature': 'form_completion.signatures[*]',
            'signature': 'form_completion.signatures[*]',
            
            # Radio button mappings
            'rb Marital': 'deceased.marital_status',
            'rb marital': 'deceased.marital_status',
            'marital': 'deceased.marital_status',
            
            'rb CPP': 'financial_information.cpp_pension',
            'rb cpp': 'financial_information.cpp_pension',
            'cpp': 'financial_information.cpp_pension',
            
            'rb OAS': 'financial_information.old_age_security',
            'rb oas': 'financial_information.old_age_security',
            'oas': 'financial_information.old_age_security',
            
            'rb QPP': 'financial_information.quebec_pension',
            'rb qpp': 'financial_information.quebec_pension',
            'qpp': 'financial_information.quebec_pension',
            
            'rb isthereawill': 'estate_information.will_exists',
            'rb is there a will': 'estate_information.will_exists',
            'is there a will': 'estate_information.will_exists',
            
            'rb prefLang written': 'applicant.preferred_language',
            'rb preflang written': 'applicant.preferred_language',
            'preferred language written': 'applicant.preferred_language',
            
            'rb prefLang verbal': 'applicant.preferred_language',
            'rb preflang verbal': 'applicant.preferred_language',
            'preferred language verbal': 'applicant.preferred_language',
            
            'rb YesNo1': 'form_completion.yes_no_responses',
            'rb yesno1': 'form_completion.yes_no_responses',
            'yes no 1': 'form_completion.yes_no_responses',
            
            # Executor/Individual
            'Executor': 'estate_reps[*].name',
            'executor': 'estate_reps[*].name',
            'Individual': 'estate_reps[*].type',
            'individual': 'estate_reps[*].type',
        }
    
    def _get_semantic_pdf_patterns(self) -> List[Tuple[str, str, str]]:
        """Semantic patterns for PDF field content matching"""
        return [
            # Name patterns
            (r'(?i).*first.*name.*', 'applicant.first_name', 'high'),
            (r'(?i).*middle.*name.*', 'applicant.middle_name', 'high'),
            (r'(?i).*last.*name.*|.*family.*name.*|.*surname.*', 'applicant.last_name', 'high'),
            
            # Contact patterns
            (r'(?i).*email.*address.*|.*email.*', 'applicant.email_address', 'high'),
            (r'(?i).*phone.*|.*telephone.*|.*tel.*', 'applicant.phone_number', 'high'),
            (r'(?i).*home.*address.*|.*address.*', 'applicant.address.street_address', 'medium'),
            
            # Identity patterns
            (r'(?i).*sin.*|.*social.*insurance.*', 'applicant.social_insurance_number', 'high'),
            (r'(?i).*dob.*|.*date.*birth.*', 'applicant.date_of_birth', 'high'),
            
            # Financial patterns
            (r'(?i).*account.*name.*|.*names.*account.*', 'financial_information.account_names', 'high'),
            (r'(?i).*branch.*number.*', 'financial_information.bank_branch', 'high'),
            (r'(?i).*institution.*number.*', 'financial_information.bank_institution', 'high'),
            (r'(?i).*account.*number.*', 'financial_information.account_number', 'high'),
            
            # Form control patterns
            (r'(?i).*signature.*', 'form_completion.signatures[*]', 'medium'),
            (r'(?i).*date.*signature.*', 'form_completion.signature_date', 'high'),
            (r'(?i).*witness.*signature.*', 'form_completion.witness_signature_date', 'high'),
            
            # Estate patterns
            (r'(?i).*relationship.*', 'estate_reps[*].relationship', 'high'),
            (r'(?i).*executor.*', 'estate_reps[*].name', 'high'),
            (r'(?i).*marital.*status.*|.*marital.*', 'deceased.marital_status', 'high'),
            
            # Location patterns
            (r'(?i).*city.*', 'applicant.address.city', 'high'),
            (r'(?i).*province.*', 'applicant.address.province', 'high'),
            (r'(?i).*country.*', 'applicant.address.country', 'high'),
            (r'(?i).*postal.*code.*', 'applicant.address.postal_code', 'high'),
        ]
    
    def match_pdf_field(self, field_name: str) -> Optional[Tuple[str, str, str]]:
        """Match PDF field using multiple strategies"""
        if not field_name:
            return None
        
        # Strategy 1: Direct exact matching (highest priority)
        field_lower = field_name.lower().strip()
        if field_lower in self.direct_pdf_mappings:
            return (field_name, self.direct_pdf_mappings[field_lower], 'high')
        
        # Strategy 2: Clean field name and try again
        cleaned = self.pdf_processor.clean_pdf_field_name(field_name).lower()
        if cleaned in self.direct_pdf_mappings:
            return (field_name, self.direct_pdf_mappings[cleaned], 'high')
        
        # Strategy 3: Extract PDF field info and match base name
        pdf_info = self.pdf_processor.extract_pdf_field_info(field_name)
        base_name = pdf_info['base_name'].lower()
        if base_name in self.direct_pdf_mappings:
            return (field_name, self.direct_pdf_mappings[base_name], 'high')
        
        # Strategy 4: Semantic pattern matching
        for pattern, schema_path, confidence in self.semantic_pdf_patterns:
            if re.search(pattern, field_name) or re.search(pattern, cleaned):
                return (field_name, schema_path, confidence)
        
        return None

class CoreMappingGenerator:
    """Enhanced core mapping generator with PDF form field support"""
    
    def __init__(self):
        self.field_patterns = self._generate_comprehensive_field_variations()[0]
        self.entity_patterns = self._generate_comprehensive_field_variations()[1]
        
        # NEW: Add PDF pattern matcher
        self.pdf_matcher = EnhancedPatternMatcher()
        
        self.core_mappings = self._init_core_mappings()
        self.enhanced_mappings = self._enhance_core_mappings_with_schema()
    
    def _generate_comprehensive_field_variations(self) -> Tuple[Dict[str, List[str]], Dict[str, List[str]]]:
        """Generate natural language variations for ALL field types systematically"""
        
        # Core field type patterns for generating variations
        field_patterns = {
            "name": [
                "name", "full name", "legal name", "first name", "last name", "surname",
                "given name", "first and last name", "complete name", "birth name"
            ],
            "phone": [
                "phone", "phone number", "telephone", "telephone number", "contact number",
                "mobile", "mobile number", "cell phone", "home phone", "work phone"
            ],
            "email": [
                "email", "email address", "e-mail", "electronic mail", "contact email",
                "email contact", "electronic address"
            ],
            "address": [
                "address", "home address", "mailing address", "residence", "location",
                "street address", "postal address", "residential address", "contact address"
            ],
            "date": [
                "date", "birth date", "death date", "date of birth", "date of death",
                "birthday", "date born", "date died", "date created", "date updated"
            ],
            "location": [
                "location", "place", "city", "province", "country", "region",
                "place of birth", "place of death", "city and province"
            ],
            "sin": [
                "social insurance number", "sin", "social insurance no", "social insurance",
                "sin number", "social security number"
            ],
            "file": [
                "document", "attachment", "file", "proof", "certificate", "copy"
            ]
        }
        
        # Entity-specific patterns
        entity_patterns = {
            "deceased": [
                "deceased", "decedent", "deceased person", "person who died", "late"
            ],
            "spouse": [
                "spouse", "partner", "husband", "wife", "married partner"
            ],
            "estate_reps": [
                "executor", "estate representative", "estate rep", "administrator",
                "estate administrator", "representative", "estate executor"
            ],
            "children": [
                "child", "children", "son", "daughter", "offspring"
            ],
            "applicant": [
                "applicant", "person applying", "application person"
            ],
            "contact": [
                "contact", "contact person", "emergency contact"
            ],
            "funeral_home": [
                "funeral home", "funeral director", "mortuary"
            ],
            "insurance": [
                "insurance", "insurance policy", "coverage", "policy"
            ],
            "property": [
                "property", "asset", "real estate", "belongings"
            ],
            "account": [
                "account", "digital account", "online account", "subscription"
            ]
        }
        
        return field_patterns, entity_patterns
    
    def _enhance_core_mappings_with_schema(self) -> List[Tuple[str, str, str]]:
        """Enhanced mapping generation covering ALL 400+ schema paths"""
        schema_paths = cadence_schema.get_schema_paths()
        field_types = cadence_schema.field_types
        
        enhanced_mappings = []
        
        for path in schema_paths:
            # Parse the path to extract components
            path_clean = path.replace("[*]", "").replace(".", " ")
            path_parts = path.split(".")
            
            # Get entity (first part) and field (last part)
            entity = path_parts[0] if path_parts else ""
            field_name = path_parts[-1] if path_parts else ""
            
            # Determine field type from schema or infer from name
            field_type = field_types.get(path, self._infer_field_type(field_name))
            
            # Generate variations for this specific path
            variations = self._generate_path_variations(entity, field_name, field_type)
            
            # Add variations to enhanced mappings
            for variation in variations:
                confidence = self._calculate_confidence(variation, path)
                enhanced_mappings.append((variation, path, confidence))
        
        # Add comprehensive task planner mappings
        task_planner_mappings = self._generate_task_planner_mappings()
        enhanced_mappings.extend(task_planner_mappings)
        
        # Add insurance type mappings
        insurance_mappings = self._generate_insurance_mappings()
        enhanced_mappings.extend(insurance_mappings)
        
        # Add document type mappings
        document_mappings = self._generate_document_mappings()
        enhanced_mappings.extend(document_mappings)
        
        # NEW: Add PDF-specific mappings
        pdf_mappings = self._generate_pdf_mappings()
        enhanced_mappings.extend(pdf_mappings)
        
        return enhanced_mappings
    
    def _generate_pdf_mappings(self) -> List[Tuple[str, str, str]]:
        """Generate PDF form field specific mappings"""
        pdf_mappings = []
        
        # Get all direct PDF mappings and convert to tuple format
        for field_name, schema_path in self.pdf_matcher.direct_pdf_mappings.items():
            pdf_mappings.append((field_name, schema_path, 'high'))
        
        # Add semantic PDF patterns
        for pattern, schema_path, confidence in self.pdf_matcher.semantic_pdf_patterns:
            # Convert regex pattern to readable string for mapping
            pattern_text = pattern.replace(r'(?i).*', '').replace('.*', '').replace(r'\|', ' or ')
            pdf_mappings.append((pattern_text, schema_path, confidence))
        
        return pdf_mappings
    
    def _generate_path_variations(self, entity: str, field_name: str, field_type: str) -> List[str]:
        """Generate natural language variations for a specific schema path"""
        variations = []
        
        # Get entity variations
        entity_vars = self.entity_patterns.get(entity, [entity])
        
        # Get field type variations
        type_vars = self.field_patterns.get(field_type, [field_name])
        
        # Generate combinations
        for entity_var in entity_vars:
            for type_var in type_vars:
                # Direct combinations
                variations.append(f"{entity_var} {type_var}")
                variations.append(f"{type_var} of {entity_var}")
                variations.append(f"{entity_var} {field_name}")
                
                # Handle specific field names
                if field_name in ["name", "full_name"]:
                    variations.extend([
                        f"{entity_var} name",
                        f"{entity_var} full name",
                        f"name of {entity_var}",
                        f"full name of {entity_var}"
                    ])
                
                elif "date" in field_name:
                    variations.extend([
                        f"{entity_var} {field_name.replace('_', ' ')}",
                        f"date of {field_name.split('_')[-1]} {entity_var}",
                        f"when {entity_var} {field_name.split('_')[-1]}"
                    ])
                
                elif "address" in field_name:
                    variations.extend([
                        f"{entity_var} address",
                        f"address of {entity_var}",
                        f"{entity_var} location",
                        f"where {entity_var} lived"
                    ])
        
        # Clean and deduplicate
        return list(set([v.strip() for v in variations if v.strip()]))
    
    def _infer_field_type(self, field_name: str) -> str:
        """Infer field type from field name patterns"""
        field_name_lower = field_name.lower()
        
        if any(x in field_name_lower for x in ["name", "first", "last", "maiden"]):
            return "name"
        elif any(x in field_name_lower for x in ["phone", "telephone", "mobile"]):
            return "phone"
        elif "email" in field_name_lower:
            return "email"
        elif any(x in field_name_lower for x in ["address", "location", "place"]):
            return "location"
        elif any(x in field_name_lower for x in ["date", "birth", "death", "created", "updated"]):
            return "date"
        elif any(x in field_name_lower for x in ["attachment", "document", "file", "proof"]):
            return "file"
        elif "sin" in field_name_lower or "social_insurance" in field_name_lower:
            return "sin"
        else:
            return "string"
    
    def _calculate_confidence(self, variation: str, path: str) -> str:
        """Calculate confidence score for a mapping"""
        # Higher confidence for exact matches and common patterns
        if len(variation.split()) <= 3:
            return "high"
        elif len(variation.split()) <= 5:
            return "medium"
        else:
            return "low"
    
    def _generate_task_planner_mappings(self) -> List[Tuple[str, str, str]]:
        """Generate comprehensive task planner boolean field mappings"""
        mappings = []
        
        # Boolean field mappings with natural language variations
        boolean_fields = {
            "task_planner.b_will": [
                "will exists", "has will", "deceased had will", "left a will",
                "valid will", "will document", "last will and testament"
            ],
            "task_planner.b_has_spouse": [
                "has spouse", "married", "spouse exists", "surviving spouse",
                "widow", "widower", "partner", "married partner"
            ],
            "task_planner.b_has_children": [
                "has children", "any children", "surviving children", "kids",
                "sons", "daughters", "offspring", "dependents"
            ],
            "task_planner.b_has_pension_plan": [
                "pension plan", "has pension", "retirement plan", "pension benefits",
                "workplace pension", "employer pension"
            ],
            "task_planner.b_has_life_insurance_or_annuities": [
                "life insurance", "has life insurance", "insurance policy",
                "annuities", "death benefits", "insurance coverage"
            ],
            "task_planner.b_has_firearms": [
                "firearms", "guns", "weapons", "rifle", "pistol", "hunting rifle"
            ],
            "task_planner.b_has_or_lease_vehicles": [
                "vehicles", "cars", "automobile", "truck", "motorcycle", "boat",
                "leased vehicle", "owned vehicle"
            ]
        }
        
        for field_path, variations in boolean_fields.items():
            for variation in variations:
                mappings.append((variation, field_path, "high"))
        
        return mappings
    
    def _generate_insurance_mappings(self) -> List[Tuple[str, str, str]]:
        """Generate insurance-specific mappings"""
        mappings = []
        
        insurance_types = {
            "life_insurance": ["life insurance", "life policy", "term life", "whole life"],
            "health_medical_insurance": ["health insurance", "medical insurance", "health coverage"],
            "home_property_insurance": ["home insurance", "property insurance", "homeowners insurance"],
            "vehicle_insurance": ["car insurance", "auto insurance", "vehicle coverage"],
            "disability_insurance": ["disability insurance", "disability coverage"],
            "critical_illness_insurance": ["critical illness", "critical illness insurance"]
        }
        
        for insurance_type, variations in insurance_types.items():
            for variation in variations:
                mappings.append((variation, f"insurance[*].type", "high"))
        
        return mappings
    
    def _generate_document_mappings(self) -> List[Tuple[str, str, str]]:
        """Generate document type mappings"""
        mappings = []
        
        document_types = {
            "will": ["will", "last will", "testament", "will document"],
            "power_of_attorney": ["power of attorney", "POA", "attorney document"],
            "marriage_contract": ["marriage contract", "prenup", "prenuptial agreement"],
            "trust": ["trust", "trust document", "family trust"],
            "tax_documents": ["tax documents", "tax returns", "CRA documents"],
            "birth_certificate": ["birth certificate", "certificate of birth"],
            "death_certificate": ["death certificate", "proof of death"]
        }
        
        for doc_type, variations in document_types.items():
            for variation in variations:
                mappings.append((variation, f"key_document[*].type", "high"))
        
        return mappings
    
    def _init_core_mappings(self) -> List[Tuple[str, str, str]]:
        """Initialize comprehensive mapping patterns enhanced with full schema"""
        
        # Enhanced schema-based mappings (covers all 400+ paths)
        schema_enhanced_mappings = self._enhance_core_mappings_with_schema()
        
        # Legacy core mappings for backward compatibility
        base_mappings = [
            ("last name of deceased", "deceased.name", "high"),
            ("first name of deceased", "deceased.name", "high"),
            ("middle name of deceased", "deceased.name", "high"),
            ("full name of deceased", "deceased.name", "high"),
            ("deceased person full legal name", "deceased.name", "high"),
            ("estate representative phone", "estate_reps[*].phone", "high"),
            ("executor phone", "estate_reps[*].phone", "high"),
            ("estate representative email", "estate_reps[*].email", "high"),
            ("estate representative name", "estate_reps[*].name", "high"),
            ("executor name", "estate_reps[*].name", "high"),
            
            # Death and birth information
            ("last name", "deceased.name", "high"),
            ("first name", "deceased.name", "high"),
            ("deceased name", "deceased.name", "high"),
            ("full name", "deceased.name", "high"),
            ("date of death", "deceased.date_of_death", "high"),
            ("death date", "deceased.date_of_death", "high"),
            ("date of birth", "deceased.date_of_birth", "high"),
            ("birth date", "deceased.date_of_birth", "high"),
            ("place of death", "deceased.place_of_death", "high"),
            ("place of birth", "deceased.place_of_birth", "high"),
            ("cause of death", "deceased.cause_of_death", "high"),
            
            # Identity information
            ("social insurance number", "deceased.social_insurance_number", "high"),
            ("sin", "deceased.social_insurance_number", "high"),
            ("social insurance no", "deceased.social_insurance_number", "high"),
            
            # Address information
            ("home address", "deceased.home_address", "high"),
            ("mailing address", "deceased.mailing_address", "high"),
            ("address", "deceased.home_address", "medium"),
            
            # Contact information
            ("phone number", "deceased.phone[*].phone_number", "high"),
            ("telephone", "deceased.phone[*].phone_number", "high"),
            ("phone", "deceased.phone[*].phone_number", "high"),
            ("email", "deceased.email[*].email_address", "high"),
            ("email address", "deceased.email[*].email_address", "high"),
            
            # Applicant information
            ("applicant name", "applicant.name", "high"),
            ("applicant phone", "applicant.phone", "high"),
            ("applicant address", "applicant.address", "high"),
            ("relationship to deceased", "applicant.role", "high"),
            
            # Spouse information
            ("spouse name", "spouse.name", "high"),
            ("spouse date of birth", "spouse.date_of_birth", "high"),
            ("spouse sin", "spouse.social_insurance_number", "high"),
            ("spouse phone", "spouse.phone_number", "high"),
            
            # Financial information
            ("bank account", "financial_information[*].id", "high"),
            ("account number", "financial_information[*].id", "high"),
            ("financial institution", "financial_information[*].name", "high"),
            ("bank name", "financial_information[*].name", "high"),
            
            # Insurance information
            ("life insurance", "insurance__life[*].name", "high"),
            ("insurance company", "insurance__life[*].name", "high"),
            ("policy number", "insurance__life[*].id", "high"),
            ("coverage amount", "insurance__life[*].id", "high"),
            
            # Property information
            ("vehicle", "property[*].type", "medium"),
            ("property", "property[*].name", "medium"),
            ("real estate", "property[*].type", "medium"),
            
            # Will information
            ("will location", "will.location_hint", "high"),
            ("will date", "will.date_created", "high"),
            
            # Task planner questions
            ("has will", "task_planner.b_will", "high"),
            ("will exists", "task_planner.b_will", "high"),
            ("has spouse", "task_planner.b_has_spouse", "high"),
            ("has children", "task_planner.b_has_children", "high"),
            ("estate value", "task_planner.b_estate_value_ca", "high"),
            ("total estate value", "task_planner.b_estate_value_ca", "high"),
        ]
        
        # Combine all mappings
        all_mappings = base_mappings + schema_enhanced_mappings
        
        # Remove duplicates while preserving highest confidence
        final_mappings = self._deduplicate_mappings(all_mappings)
        
        return final_mappings
    
    def _deduplicate_mappings(self, mappings: List[Tuple[str, str, str]]) -> List[Tuple[str, str, str]]:
        """Remove duplicate mappings, keeping highest confidence ones"""
        mapping_dict = {}
        confidence_order = {"high": 3, "medium": 2, "low": 1}
        
        for variation, path, confidence in mappings:
            key = variation.lower().strip()
            current_score = confidence_order.get(confidence, 1)
            
            if key not in mapping_dict or confidence_order.get(mapping_dict[key][2], 1) < current_score:
                mapping_dict[key] = (variation, path, confidence)
        
        return list(mapping_dict.values())
    
    def get_core_mappings(self) -> List[Tuple[str, str, str]]:
        """Get all core mappings"""
        return self.core_mappings.copy()
    
    def get_enhanced_mappings(self) -> List[Tuple[str, str, str]]:
        """Get enhanced schema-based mappings"""
        return self.enhanced_mappings.copy()
    
    def search_mappings(self, query: str) -> List[Tuple[str, str, str]]:
        """Search mappings by query string"""
        query_lower = query.lower()
        matching_mappings = []
        
        for pattern, path, confidence in self.core_mappings:
            if query_lower in pattern.lower() or query_lower in path.lower():
                matching_mappings.append((pattern, path, confidence))
        
        return matching_mappings
    
    def get_mappings_by_entity(self, entity: str) -> List[Tuple[str, str, str]]:
        """Get mappings for a specific entity"""
        matching_mappings = []
        
        for pattern, path, confidence in self.core_mappings:
            if path.startswith(f"{entity}."):
                matching_mappings.append((pattern, path, confidence))
        
        return matching_mappings
    
    def get_mappings_by_confidence(self, confidence: str) -> List[Tuple[str, str, str]]:
        """Get mappings by confidence level"""
        matching_mappings = []
        
        for pattern, path, conf in self.core_mappings:
            if conf == confidence:
                matching_mappings.append((pattern, path, conf))
        
        return matching_mappings
    
    def get_statistics(self) -> Dict:
        """Get mapping statistics"""
        total_mappings = len(self.core_mappings)
        high_confidence = len(self.get_mappings_by_confidence("high"))
        medium_confidence = len(self.get_mappings_by_confidence("medium"))
        low_confidence = len(self.get_mappings_by_confidence("low"))
        
        entities = set()
        for _, path, _ in self.core_mappings:
            if "." in path:
                entities.add(path.split(".")[0])
        
        return {
            "total_mappings": total_mappings,
            "high_confidence": high_confidence,
            "medium_confidence": medium_confidence,
            "low_confidence": low_confidence,
            "entities_covered": len(entities),
            "entities": sorted(list(entities)),
            "coverage_percentage": (total_mappings / len(cadence_schema.get_schema_paths())) * 100,
            "pdf_specific_mappings": len(self.pdf_matcher.direct_pdf_mappings)
        }
    
    
    def match_pdf_field(self, field_name: str) -> Optional[Tuple[str, str, str]]:
        """Match PDF field name to schema path using enhanced PDF matching"""
        return self.pdf_matcher.match_pdf_field(field_name)
    
    def is_pdf_field(self, field_name: str) -> bool:
        """Check if field name appears to be from a PDF form"""
        pdf_indicators = ['txtf', 'txtF', 'rb', 'cb', 'dte', 'dd', 'SC_ISP', '#pageSet', 'page', '[0]']
        return any(indicator in field_name for indicator in pdf_indicators)

class SemanticAnalyzer:
    """Enhanced semantic analyzer with PDF field support"""
    
    def __init__(self):
        self.semantic_patterns = self._load_semantic_patterns()
        self.pdf_processor = PDFFieldProcessor()
    
    def _load_semantic_patterns(self) -> Dict[str, str]:
        """Load semantic analysis patterns"""
        return {
            # Death-related patterns
            "death.*date": "deceased.date_of_death",
            "date.*death": "deceased.date_of_death", 
            "death.*place": "deceased.place_of_death",
            "place.*death": "deceased.place_of_death",
            "cause.*death": "deceased.cause_of_death",
            
            # Birth-related patterns
            "birth.*date": "deceased.date_of_birth",
            "date.*birth": "deceased.date_of_birth",
            "birth.*place": "deceased.place_of_birth", 
            "place.*birth": "deceased.place_of_birth",
            
            # Insurance patterns
            "life.*insurance": "insurance__life[*].name",
            "insurance.*life": "insurance__life[*].name",
            "policy.*number": "insurance__life[*].id",
            "insurance.*policy": "insurance__life[*].id",
            
            # Estate representative patterns
            "executor.*name": "estate_reps[*].name",
            "estate.*representative.*name": "estate_reps[*].name",
            "executor.*phone": "estate_reps[*].phone",
            "estate.*representative.*phone": "estate_reps[*].phone",
            "executor.*email": "estate_reps[*].email",
            "estate.*representative.*email": "estate_reps[*].email",
            
            # Task planner patterns
            "has.*will": "task_planner.b_will",
            "will.*exists": "task_planner.b_will",
            "has.*spouse": "task_planner.b_has_spouse",
            "has.*children": "task_planner.b_has_children",
            "estate.*value": "task_planner.b_estate_value_ca",
            
            # NEW: PDF-specific patterns
            "txtf.*sin": "applicant.social_insurance_number",
            "txtf.*name": "applicant.first_name",
            "txtf.*email": "applicant.email_address",
            "rb.*marital": "deceased.marital_status",
            "dte.*signature": "form_completion.signature_date",
        }
    
    def analyze(self, field_name: str) -> str:
        """Enhanced semantic analysis with PDF field support"""
        # First try PDF-specific processing
        if core_mapping_generator.is_pdf_field(field_name):
            pdf_match = core_mapping_generator.match_pdf_field(field_name)
            if pdf_match:
                return pdf_match[1]  # Return schema path
        
        # Original semantic analysis
        clean_field = field_name.lower().strip()
        clean_field = re.sub(r'[^\w\s]', ' ', clean_field)
        clean_field = re.sub(r'\s+', ' ', clean_field)
        
        # Try pattern matching
        for pattern, path in self.semantic_patterns.items():
            if re.search(pattern, clean_field):
                return path
        
        # Try keyword-based analysis
        return self._keyword_analysis(clean_field)
    
    def _keyword_analysis(self, clean_field: str) -> str:
        """Enhanced keyword-based semantic analysis"""
        
        # Check for specific combinations
        if "death" in clean_field and "date" in clean_field:
            return "deceased.date_of_death"
        elif "death" in clean_field and ("place" in clean_field or "location" in clean_field):
            return "deceased.place_of_death"
        elif "birth" in clean_field and "date" in clean_field:
            return "deceased.date_of_birth"
        elif "birth" in clean_field and ("place" in clean_field or "location" in clean_field):
            return "deceased.place_of_birth"
        elif "insurance" in clean_field and "life" in clean_field:
            return "insurance__life[*].name"
        elif "policy" in clean_field and "number" in clean_field:
            return "insurance__life[*].id"
        elif any(term in clean_field for term in ["executor", "estate representative"]):
            if "name" in clean_field:
                return "estate_reps[*].name"
            elif "phone" in clean_field:
                return "estate_reps[*].phone"
            elif "email" in clean_field:
                return "estate_reps[*].email"
        elif clean_field.startswith("has ") and "will" in clean_field:
            return "task_planner.b_will"
        elif clean_field.startswith("has ") and "spouse" in clean_field:
            return "task_planner.b_has_spouse"
        elif clean_field.startswith("has ") and "children" in clean_field:
            return "task_planner.b_has_children"
        
        # NEW: PDF-specific keyword analysis
        elif "sin" in clean_field:
            return "applicant.social_insurance_number"
        elif "first" in clean_field and "name" in clean_field:
            return "applicant.first_name"
        elif "middle" in clean_field and "name" in clean_field:
            return "applicant.middle_name"
        elif "last" in clean_field and "name" in clean_field or "family" in clean_field:
            return "applicant.last_name"
        elif "email" in clean_field:
            return "applicant.email_address"
        elif "relationship" in clean_field:
            return "estate_reps[*].relationship"
        elif "signature" in clean_field and "date" in clean_field:
            return "form_completion.signature_date"
        
        return "unknown.field"

# Global instances
core_mapping_generator = CoreMappingGenerator()
semantic_analyzer = SemanticAnalyzer()