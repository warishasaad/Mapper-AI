# --- START OF CORRECTED FILE: api/models_schema.py ---

from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from enum import Enum

# ==============================================================================
# CORRECTED IMPORT
# Using an absolute import path from the 'api' root to ensure consistency.
# ==============================================================================
try:
    from api.core.models import QualityCategory, FormIntent, ContextualConfidence, LegalDocumentType
except ImportError:
    # Fallback for environments where the structure might be different or during testing
    class QualityCategory(str, Enum):
        EXCELLENT = "excellent"; GOOD = "good"; ACCEPTABLE = "acceptable"; POOR = "poor"; CRITICAL = "critical"
    class FormIntent(str, Enum):
        PROBATE = "probate"; ADMINISTRATION = "administration"; DEATH_BENEFITS = "death_benefits"; SURVIVOR_BENEFITS = "survivor_benefits"; LIFE_INSURANCE = "life_insurance"; ESTATE_INFO = "estate_information"; ASSET_TRANSFER = "asset_transfer"; ACCOUNT_CLOSURE = "account_closure"; TAX_CLEARANCE = "tax_clearance"; GUARDIANSHIP = "guardianship"; TRUST_ADMIN = "trust_administration"; UNKNOWN = "unknown"
    class ContextualConfidence(str, Enum):
        VERY_HIGH = "very_high"; HIGH = "high"; MEDIUM = "medium"; LOW = "low"; VERY_LOW = "very_low"
    class LegalDocumentType(str, Enum):
        PROBATE_APPLICATION = "probate_application"; LETTERS_OF_ADMINISTRATION = "letters_of_administration"; ESTATE_CERTIFICATE = "estate_certificate"; CPP_DEATH_BENEFIT_APP = "cpp_death_benefit_application"; QPP_SURVIVOR_PENSION = "qpp_survivor_pension_application"; LIFE_INSURANCE_CLAIM = "life_insurance_claim_form"; BANK_ESTATE_PACKAGE = "bank_estate_package"; VEHICLE_TRANSFER = "vehicle_transfer_form"; PROPERTY_TRANSFER = "property_transfer_form"; CRA_REQUEST_FORM = "cra_request_form"; ESTATE_TRUSTEE_APP = "estate_trustee_application"; CLEARANCE_CERTIFICATE = "clearance_certificate_request"; BENEFICIARY_DESIGNATION = "beneficiary_designation_form"; ESTATE_SUMMARY = "estate_information_summary"; UNKNOWN_LEGAL_DOC = "unknown_legal_document"


# ==============================================================================
# API INPUT SCHEMA (REQUEST BODY)
# ==============================================================================
class ProcessFieldsRequest(BaseModel):
    """Defines the structure for making an API request with pre-extracted field data."""
    field_data: Dict[str, str]
    form_context: Optional[Dict[str, Any]] = None

# ==============================================================================
# API OUTPUT SCHEMAS (RESPONSE BODY COMPONENTS)
# ==============================================================================
class MappingResultSchema(BaseModel):
    """Detailed result for a single mapped field."""
    field_name: str
    cadence_path: str
    confidence: float
    method: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = {}

class ConditionalLogicSchema(BaseModel):
    """A single conditional rule detected in the form."""
    rule_id: str
    rule_name: str
    source_field: str
    target_fields: List[str]
    condition_type: str
    condition_text: str
    logic_expression: str
    confidence: float

class CrossFieldValidationResultSchema(BaseModel):
    """Result from the cross-field validation engine."""
    rule_id: str
    is_valid: bool
    message: str
    severity: str
    affected_fields: List[str]
    suggested_corrections: List[str]

class FormIntentAnalysisSchema(BaseModel):
    """Result from the semantic form intent analysis."""
    primary_intent: FormIntent
    confidence: ContextualConfidence
    evidence: List[str]
    processing_complexity: str

class DocumentClassificationSchema(BaseModel):
    """Result from the semantic document classification."""
    document_type: LegalDocumentType
    confidence: ContextualConfidence
    classification_evidence: List[str]

class SemanticContextSchema(BaseModel):
    """Comprehensive result from the semantic context engine."""
    form_intent: FormIntentAnalysisSchema
    document_classification: DocumentClassificationSchema
    overall_context_score: float

class FieldCompletionStatusSchema(BaseModel):
    """Schema for a single field's completion status."""
    field_name: str
    cadence_path: str
    is_filled: bool
    is_required: bool
    priority: str

class CompletionAnalysisSchema(BaseModel):
    """Comprehensive analysis of the form's completion status."""
    overall_completion_score: float
    form_readiness_assessment: str
    critical_missing: List[FieldCompletionStatusSchema]
    actionable_recommendations: List[str]

class QualityReportSchema(BaseModel):
    """Comprehensive quality assurance report for the processing job."""
    overall_score: float
    quality_category: QualityCategory
    mapping_quality: float
    completeness_score: float
    recommendations: List[str]
    critical_issues: List[str]

# ==============================================================================
# MAIN API RESPONSE SCHEMA
# ==============================================================================
class DocumentProcessingResponse(BaseModel):
    """
    The main response model for a successful document or field processing request.
    This structure contains all analysis results from the entire pipeline.
    """
    processing_metadata: Dict[str, Any]
    document_analysis: Dict[str, Any]
    subject_detection: Dict[str, Any]
    field_mappings: List[MappingResultSchema]
    conditional_logic_analysis: List[ConditionalLogicSchema]
    cross_field_validation: List[CrossFieldValidationResultSchema]
    semantic_context: SemanticContextSchema
    completion_analysis: CompletionAnalysisSchema
    quality_report: QualityReportSchema
    unmapped_fields: List[str]