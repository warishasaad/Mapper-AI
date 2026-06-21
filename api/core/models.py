"""
Enhanced Data Models for Complete MapperAI System - Production Ready

Contains all data classes, enums, and type definitions for the complete
estate mapping system with all advanced features. This is the single source of truth.
"""

from dataclasses import dataclass, field
from enum import Enum, IntFlag, auto
from typing import Dict, List, Optional, Any, Tuple, Union
from datetime import datetime
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

# ==================== CORE ENUMS (Consolidated) ====================

class SubjectRole(Enum):
    SPOUSE = "spouse"; SURVIVING_SPOUSE = "surviving_spouse"; WIDOW_WIDOWER = "widow_widower"; CHILD = "child"; ADULT_CHILD = "adult_child"; MINOR_CHILD = "minor_child"; EXECUTOR = "executor"; EXECUTRIX = "executrix"; ADMINISTRATOR = "administrator"; TRUSTEE = "trustee"; BENEFICIARY = "beneficiary"; HEIR = "heir"; NEXT_OF_KIN = "next_of_kin"; GUARDIAN = "guardian"; ATTORNEY = "attorney"; LEGAL_REPRESENTATIVE = "legal_representative"; POWER_OF_ATTORNEY = "power_of_attorney"; CLAIMANT = "claimant"; APPLICANT = "applicant"; PETITIONER = "petitioner"; SURVIVOR = "survivor"; DEPENDENT = "dependent"; PARENT = "parent"; SIBLING = "sibling"; FAMILY_MEMBER = "family_member"; ESTATE_REPRESENTATIVE = "estate_representative"; FIDUCIARY = "fiduciary"; DEATH_BENEFIT_APPLICATION = "death_benefit_application"; UNKNOWN = "unknown"

class ConfidenceLevel(Enum):
    CRITICAL = 1.0; CERTAIN = 1.0; HIGH = 0.9; MEDIUM = 0.7; LOW = 0.5; UNCERTAIN = 0.3

class FieldType(Enum):
    IDENTITY = "identity"; CONTACT = "contact"; DATE = "date"; FINANCIAL = "financial"; LEGAL = "legal"; GOVERNMENT = "government"; LOCATION = "location"; PERSON_NAME = "person_name"; DEATH_DATE = "death_date"; VEHICLE_IDENTIFIER = "vehicle_identifier"; SIGNATURE = "signature"; CHECKBOX = "checkbox"; MILITARY = "military"; INSURANCE = "insurance"; MEDICAL = "medical"; EMPLOYMENT = "employment"; EDUCATION = "education"; RELATIONSHIP = "relationship"; PROPERTY = "property"; BUSINESS = "business"; ADDRESS = "address"; DOCUMENT = "document"; ACCOUNT = "account"; TASK_PLANNER = "task_planner"; CONDITIONAL = "conditional"; COMPUTED = "computed"; REFERENCE = "reference"

class PDFFieldType(IntFlag):
    TEMPLATE = auto(); REQUIRED = auto(); SIGNATURE = auto(); CHECKBOX = auto(); DATE = auto(); READONLY = auto(); MULTILINE = auto(); PASSWORD = auto(); DROPDOWN = auto(); RADIO = auto()

class PDFFormType(Enum):
    DEATH_BENEFIT_APPLICATION = "death_benefit_application"; ESTATE_INFORMATION = "estate_information"; LIFE_INSURANCE_CLAIM = "life_insurance_claim"; VEHICLE_TRANSFER = "vehicle_transfer"; MILITARY_BENEFITS = "military_benefits"; FIREARM_TRANSFER = "firearm_transfer"; ELECTORAL_ADMINISTRATION = "electoral_administration"; TAX_ADMINISTRATION = "tax_administration"; DEATH_NOTIFICATION = "death_notification"; LOYALTY_PROGRAM_TRANSFER = "loyalty_program_transfer"; UNKNOWN = "unknown"; PROBATE_APPLICATION = "probate_application"; PENSION_SURVIVOR_BENEFIT = "pension_survivor_benefit"; TAX_CLEARANCE = "tax_clearance"; PROPERTY_TRANSFER = "property_transfer"; BANK_ACCOUNT_CLOSURE = "bank_account_closure"; CRA_T1_FINAL_RETURN = "cra_t1_final_return"; RRSP_RRIF_TRANSFER = "rrsp_rrif_transfer"; DIGITAL_ACCOUNT_CLOSURE = "digital_account_closure"

class ConditionalType(Enum):
    SHOW_IF = "show_if"; HIDE_IF = "hide_if"; REQUIRED_IF = "required_if"; OPTIONAL_IF = "optional_if"; ENABLE_IF = "enable_if"; DISABLE_IF = "disable_if"; CALCULATE_IF = "calculate_if"; VALIDATE_IF = "validate_if"

class ProcessingPriority(Enum):
    CRITICAL = "critical"; HIGH = "high"; MEDIUM = "medium"; LOW = "low"; DEFERRED = "deferred"

class ProvincialJurisdiction(Enum):
    ALBERTA = "AB"; BRITISH_COLUMBIA = "BC"; MANITOBA = "MB"; NEW_BRUNSWICK = "NB"; NEWFOUNDLAND_LABRADOR = "NL"; NORTHWEST_TERRITORIES = "NT"; NOVA_SCOTIA = "NS"; NUNAVUT = "NU"; ONTARIO = "ON"; PRINCE_EDWARD_ISLAND = "PE"; QUEBEC = "QC"; SASKATCHEWAN = "SK"; YUKON = "YT"; FEDERAL = "FED"

class FormComplexity(Enum):
    SIMPLE = "simple"; MODERATE = "moderate"; COMPLEX = "complex"; EXPERT = "expert"

class ValidationSeverity(Enum):
    ERROR = "error"; WARNING = "warning"; INFO = "info"; SUGGESTION = "suggestion"

class ProcessingStage(Enum):
    EXTRACTION = "extraction"; MAPPING = "mapping"; VALIDATION = "validation"; ENHANCEMENT = "enhancement"; COMPLETION = "completion"; FINALIZATION = "finalization"

class QualityCategory(Enum):
    EXCELLENT = "excellent"; GOOD = "good"; ACCEPTABLE = "acceptable"; POOR = "poor"; CRITICAL = "critical"

# ==================== MISSING ENUMS THAT WERE CAUSING THE ERROR ====================

class FormIntent(Enum):
    PROBATE = "probate"
    ADMINISTRATION = "administration"
    DEATH_BENEFITS = "death_benefits"
    SURVIVOR_BENEFITS = "survivor_benefits"
    LIFE_INSURANCE = "life_insurance"
    ESTATE_INFO = "estate_information"
    ASSET_TRANSFER = "asset_transfer"
    ACCOUNT_CLOSURE = "account_closure"
    TAX_CLEARANCE = "tax_clearance"
    GUARDIANSHIP = "guardianship"
    TRUST_ADMIN = "trust_administration"
    UNKNOWN = "unknown"

class ContextualConfidence(Enum):
    VERY_HIGH = "very_high"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    VERY_LOW = "very_low"

class LegalDocumentType(Enum):
    PROBATE_APPLICATION = "probate_application"
    LETTERS_OF_ADMINISTRATION = "letters_of_administration"
    ESTATE_CERTIFICATE = "estate_certificate"
    CPP_DEATH_BENEFIT_APP = "cpp_death_benefit_application"
    QPP_SURVIVOR_PENSION = "qpp_survivor_pension_application"
    LIFE_INSURANCE_CLAIM = "life_insurance_claim_form"
    BANK_ESTATE_PACKAGE = "bank_estate_package"
    VEHICLE_TRANSFER = "vehicle_transfer_form"
    PROPERTY_TRANSFER = "property_transfer_form"
    CRA_REQUEST_FORM = "cra_request_form"
    ESTATE_TRUSTEE_APP = "estate_trustee_application"
    CLEARANCE_CERTIFICATE = "clearance_certificate_request"
    BENEFICIARY_DESIGNATION = "beneficiary_designation_form"
    ESTATE_SUMMARY = "estate_information_summary"
    UNKNOWN_LEGAL_DOC = "unknown_legal_document"

# ==================== CORE DATA CLASSES (Consolidated) ====================



class OllamaConfig(BaseSettings):
    """
    Loads Ollama AI configuration from environment variables.
    Reads from a .env file automatically.
    """
    base_url: str = Field(alias='OLLAMA_BASE_URL', default="http://ollama:11434") 
    model: str = Field(alias='OLLAMA_MODEL', default="phi3:mini")  
    enabled: bool = Field(alias='OLLAMA_ENABLED', default=True)
    timeout: float = Field(alias='OLLAMA_TIMEOUT', default=120.0)

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

@dataclass
class ConditionalLogic:
    show_if: Optional[str] = None
    required_if: Optional[str] = None
    skip_if: Optional[str] = None

@dataclass
class FieldDependency:
    source_field: str
    dependent_field: str
    dependency_type: str
    condition: str
    confidence: float = 0.7

@dataclass
class SubjectEvidence:
    source: str
    pattern: str
    confidence: float
    context: str
    rule_type: str

@dataclass
class SubjectDetectionResult:
    role: SubjectRole
    confidence: float
    evidence: List[SubjectEvidence]
    metadata: Dict[str, Any]
    fallback_roles: List[SubjectRole] = field(default_factory=list)
    dynamic_mappings: Dict[str, str] = field(default_factory=dict)
    conditional_fields: List[str] = field(default_factory=list)
    relevant_sections: List[str] = field(default_factory=list)

@dataclass
class ConditionalRule:
    rule_id: str
    rule_name: str
    source_field: str
    target_fields: List[str]
    condition_type: ConditionalType
    condition_text: str
    logic_expression: str
    confidence: float
    detection_method: str
    rule_category: str = "general"; legal_requirement: bool = False; business_logic: bool = False; semantic_relationship: bool = False; progressive_disclosure: bool = False; form_specific: bool = False; form_type: Optional[str] = None; subject_role: Optional[str] = None; jurisdiction: Optional[str] = None; depends_on: List[str] = field(default_factory=list); blocks: List[str] = field(default_factory=list); related_rules: List[str] = field(default_factory=list); priority: int = 100; execution_order: int = 0; validation_rules: List[str] = field(default_factory=list)

@dataclass
class DataInference:
    inferred_field: str
    inferred_value: Any
    inference_method: str
    confidence: float
    source_fields: List[str]
    reasoning: str
    requires_validation: bool = True
    provincial_specific: bool = False

@dataclass
class VisualFieldContext:
    bounding_box: Tuple[float, float, float, float]
    page_number: int
    section_header: Optional[str] = None; nearby_text: List[str] = field(default_factory=list); visual_grouping: Optional[str] = None; layout_position: str = ""; font_size: Optional[float] = None; is_in_table: bool = False; table_context: Optional[Dict] = None

@dataclass
class TemplateValidationResult:
    is_valid: bool
    template_errors: List[str] = field(default_factory=list)
    template_warnings: List[str] = field(default_factory=list)

@dataclass
class JurisdictionalContext:
    primary_jurisdiction: ProvincialJurisdiction
    secondary_jurisdictions: List[ProvincialJurisdiction] = field(default_factory=list)

@dataclass
class ProvincialRule:
    rule_id: str
    jurisdiction: ProvincialJurisdiction
    rule_type: str
    description: str
    applies_to_forms: List[str]
    rule_logic: str
    validation_function: Optional[str] = None; error_message: str = ""; legal_reference: Optional[str] = None; effective_date: Optional[datetime] = None; expiry_date: Optional[datetime] = None

@dataclass
class MappingResult:
    field_name: str
    cadence_path: str
    template: str
    confidence: str
    field_type: FieldType
    processing_time: float
    validation_errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    related_fields: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    conditional_logic: Optional[ConditionalLogic] = None
    field_dependencies: List[FieldDependency] = field(default_factory=list)
    provincial_context: Optional[JurisdictionalContext] = None
    missing_data_inferences: List[DataInference] = field(default_factory=list)
    template_validation_result: Optional[TemplateValidationResult] = None
    visual_context: Optional[VisualFieldContext] = None
    ai_enhancement_details: Optional[Dict] = None
    processing_stage: ProcessingStage = ProcessingStage.MAPPING
    priority: ProcessingPriority = ProcessingPriority.MEDIUM

@dataclass
class BatchProcessingResult:
    results: List[MappingResult]
    total_fields: int; mapped_fields: int; unmapped_fields: int; high_confidence_mappings: int; processing_time: float; fields_per_second: float; mapping_accuracy: float; metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PatternMatchingStats:
    total_patterns_detected: int = 0; pattern_types: Dict[str, int] = field(default_factory=dict); confidence_distribution: Dict[str, int] = field(default_factory=dict); field_coverage: float = 0.0; subject_detection_accuracy: float = 0.0; processing_efficiency: float = 0.0; form_complexity_score: float = 0.0; pattern_diversity_score: float = 0.0; semantic_coverage_score: float = 0.0

@dataclass
class FormSection:
    name: str
    fields: List[str]
    conditional: bool = False
    condition_rules: List[ConditionalRule] = field(default_factory=list)

@dataclass
class PDFFieldExtraction:
    field_name: str; field_value: str; field_type: PDFFieldType; bbox: Tuple[float, float, float, float]; page_number: int; confidence: float; raw_data: Dict[str, Any] = field(default_factory=dict); section_name: Optional[str] = None; is_conditional: bool = False

@dataclass
class PDFFormInfo:
    form_type: PDFFormType; form_title: str; total_fields: int; fillable_fields: int; signature_fields: int; date_fields: int; required_fields: int; conditional_fields: int = 0; form_sections: List[str] = field(default_factory=list); form_version: str = "unknown"; conditional_logic_detected: bool = False

@dataclass
class ConditionalAnalysisResult:
    total_conditional_fields: int = 0; conditional_mappings: List[Dict] = field(default_factory=list); field_dependencies: List[FieldDependency] = field(default_factory=list); form_sections: List[Dict] = field(default_factory=dict); condition_types: Dict[str, int] = field(default_factory=dict); confidence_distribution: Dict[str, int] = field(default_factory=dict); extraction_errors: List[str] = field(default_factory=list); processing_time: float = 0.0
    def __len__(self): return self.total_conditional_fields
    def __bool__(self): return self.total_conditional_fields > 0

@dataclass
class PDFMappingResult:
    pdf_field: PDFFieldExtraction; cadence_mapping: Optional[Any]; mapped_path: str; template: str; confidence: str; validation_errors: List[str] = field(default_factory=list); warnings: List[str] = field(default_factory=list); transformation_applied: List[str] = field(default_factory=list); conditional_logic: Optional[ConditionalLogic] = None; field_dependencies: List[FieldDependency] = field(default_factory=list); section_context: Optional[Any] = None

@dataclass
class AIEnhancementError(Exception):
    message: str
    details: Optional[Dict] = None

@dataclass
class SchemaField:
    path: str
    field_type: str
    description: str
    value_options: List[str] = field(default_factory=list)
    is_array: bool = False; is_required: bool = False; metadata: Dict = field(default_factory=dict)

@dataclass
class ProcessingMetrics:
    stage_timings: Dict[ProcessingStage, float] = field(default_factory=dict)
    ai_model_performance: Dict[str, Dict] = field(default_factory=dict)
    error_rates_by_stage: Dict[ProcessingStage, float] = field(default_factory=dict)
    provincial_processing_stats: Dict[ProvincialJurisdiction, Dict] = field(default_factory=dict)
    form_type_success_rates: Dict[str, float] = field(default_factory=dict)

@dataclass
class MissingDataAnalysis:
    missing_fields: List[str]
    critical_missing: List[str]
    inferable_fields: List[DataInference]
    data_collection_suggestions: List[str]
    form_completion_percentage: float
    blocking_issues: List[str]

@dataclass
class PDFFieldMapping:
    pdf_field_name: str; cadence_path: str; handlebars_template: str; field_type: PDFFieldType; form_type: Optional[PDFFormType] = None; validation_rules: List[str] = field(default_factory=list); transformation_rules: List[str] = field(default_factory=list); conditional_logic: Optional[ConditionalLogic] = None; description: str = ""; examples: List[str] = field(default_factory=list)

@dataclass
class PDFStats:
    forms_processed: int = 0; fields_extracted: int = 0; fields_mapped: int = 0; signature_fields_found: int = 0; validation_errors: int = 0; processing_time: float = 0.0; form_types_detected: int = 0; transformation_applications: int = 0; high_confidence_mappings: int = 0; conditional_logic_detected: int = 0; form_sections_identified: int = 0

@dataclass
class MappingPattern:
    pattern: str; cadence_path: str; confidence: str; field_type: FieldType = FieldType.IDENTITY

@dataclass
class CrossFieldValidationRule:
    rule_id: str; name: str; description: str; source_fields: List[str]; target_field: str; validation_logic: str; error_message: str; severity: ValidationSeverity = ValidationSeverity.ERROR; applies_to_jurisdictions: List[ProvincialJurisdiction] = field(default_factory=list)

@dataclass
class CrossFieldValidationResult:
    rule_id: str; is_valid: bool; message: str; severity: ValidationSeverity; affected_fields: List[str]; suggested_corrections: List[str] = field(default_factory=list)

# ==================== HELPER FUNCTIONS ====================

def create_mapping_result(field_name: str, cadence_path: str, confidence: str = "medium") -> MappingResult:
    """Helper to create a basic mapping result"""
    return MappingResult(
        field_name=field_name,
        cadence_path=cadence_path,
        template=f"{{{{{cadence_path}}}}}",
        confidence=confidence,
        field_type=FieldType.IDENTITY,
        processing_time=0.0
    )

def create_batch_result(total_fields: int, mapped_fields: int, processing_time: float) -> BatchProcessingResult:
    """Helper to create a batch processing result"""
    return BatchProcessingResult(
        results=[],
        total_fields=total_fields,
        mapped_fields=mapped_fields,
        unmapped_fields=total_fields - mapped_fields,
        high_confidence_mappings=0,
        processing_time=processing_time,
        fields_per_second=0.0,
        mapping_accuracy=0.0
    )

# ==================== CONSTANTS ====================

# Default field mappings for common estate forms
DEFAULT_ESTATE_MAPPINGS = {
    "deceased_name": "deceased.name",
    "deceased_first_name": "deceased.first_name",
    "deceased_last_name": "deceased.last_name",
    "date_of_death": "deceased.date_of_death",
    "death_date": "deceased.date_of_death",
    "social_insurance_number": "deceased.social_insurance_number",
    "sin": "deceased.social_insurance_number",
    "applicant_name": "applicant.name",
    "applicant_address": "applicant.address",
    "applicant_phone": "applicant.phone",
    "spouse_name": "spouse.name",
    "executor_name": "estate_reps[*].name",
    "estate_value": "financial_information.total_estate_value"
}

# Canadian provincial form types
CANADIAN_FORM_TYPES = [
    "death_benefit_application",
    "estate_information", 
    "life_insurance_claim",
    "probate_application",
    "bank_account_closure",
    "vehicle_transfer",
    "tax_clearance",
    "property_transfer"
]

# Validation rules for Canadian data
CANADIAN_VALIDATION_RULES = {
    "sin_format": r"^\d{3}-?\d{3}-?\d{3}$",
    "postal_code": r"^[A-Za-z]\d[A-Za-z]\s?\d[A-Za-z]\d$",
    "phone_canadian": r"^(\+1\s?)?(\d{3}|\(\d{3}\))\s?\d{3}\s?\d{4}$"
}

# Export all important classes and functions
__all__ = [
    # Enums
    'FieldType', 'ProvincialJurisdiction', 'FormComplexity', 'ProcessingStage', 
    'ValidationSeverity', 'SubjectRole', 'ProcessingPriority', 'PDFFieldType', 'PDFFormType',
    'QualityCategory', 'FormIntent', 'ContextualConfidence', 'LegalDocumentType', 'ConditionalType',
    'ConfidenceLevel',
    
    # Configuration
    'OllamaConfig',
    
    # Core Results
    'MappingResult', 'BatchProcessingResult', 'PDFMappingResult',
    
    # Validation
    'CrossFieldValidationResult', 'CrossFieldValidationRule',
    
    # Conditional Logic
    'ConditionalLogic', 'FieldDependency', 'ConditionalRule', 'ConditionalAnalysisResult',
    
    # Subject Detection
    'SubjectDetectionResult', 'SubjectEvidence',
    
    # PDF Processing
    'PDFFieldExtraction', 'PDFFormInfo', 'PDFStats', 'PDFFieldMapping',
    
    # Visual Analysis
    'VisualFieldContext', 'FormSection',
    
    # Provincial
    'ProvincialRule', 'JurisdictionalContext',
    
    # Templates
    'TemplateValidationResult',
    
    # Missing Data
    'MissingDataAnalysis', 'DataInference',
    
    # Schema
    'SchemaField',
    
    # Processing
    'ProcessingMetrics', 'PatternMatchingStats',
    
    # Helpers
    'create_mapping_result', 'create_batch_result',
    
    # Constants
    'DEFAULT_ESTATE_MAPPINGS', 'CANADIAN_FORM_TYPES', 'CANADIAN_VALIDATION_RULES'
]