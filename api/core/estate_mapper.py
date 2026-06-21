# --- START OF FILE estate_mapper.py ---

"""
Production MapperAI Estate Mapper - Complete Conditional Logic & Dynamic Subject Modeling System
Solves core problems: isolated 1:1 mapping → intelligent conditional relationships

"""

import time
import logging
import asyncio
import re
from typing import Dict, List, Optional, Any, Tuple, Set
from dataclasses import field, asdict
from datetime import datetime
from enum import Enum, Flag, auto
from collections import Counter, defaultdict
from pathlib import Path
from dataclasses import asdict
from .pdf_processor import PDFProcessor
from fuzzywuzzy import fuzz

# ==============================================================================
# MODIFIED: Import the single source of truth for data models from models.py
# ==============================================================================
from .models import (
    MappingResult, SubjectRole, ConfidenceLevel, FieldType, PDFFieldType,
    PDFFormType, ConditionalType, SubjectEvidence, SubjectDetectionResult,
    ConditionalRule, BatchProcessingResult, PatternMatchingStats,
    PDFFieldExtraction, PDFFormInfo, ConditionalLogic, FieldDependency,
    ConditionalAnalysisResult, PDFMappingResult
)

try:
    from .cross_field_validator import CrossFieldValidator, CrossFieldValidationResult
    from .semantic_context_engine import SemanticContextEngine, SemanticContextAnalysis
    from .form_completion_engine import FormCompletionEngine, FormCompletionAnalysis
    ADVANCED_ENGINES_AVAILABLE = True
except ImportError:
    CrossFieldValidator, CrossFieldValidationResult = None, None
    SemanticContextEngine, SemanticContextAnalysis = None, None
    FormCompletionEngine, FormCompletionAnalysis = None, None
    ADVANCED_ENGINES_AVAILABLE = False
    print("Warning: Advanced analysis engines (validation, semantic, completion) not found. Functionality will be limited.")

try:
    from .ai_enhancer import OllamaAIEnhancer
    AI_ENHANCER_AVAILABLE = True
except ImportError:
    OllamaAIEnhancer = None
    AI_ENHANCER_AVAILABLE = False
    print("Warning: ai_enhancer.py not found. AI fallback mapping is disabled.")

try:
    from .form_logic_parser import ProductionConditionalLogicEngine
    CONDITIONAL_LOGIC_AVAILABLE = True
except ImportError:
    ProductionConditionalLogicEngine = None
    CONDITIONAL_LOGIC_AVAILABLE = False
    print("Warning: form_logic_parser.py not found. Conditional logic detection is disabled.")

try:
    import PyPDF2
    import fitz
    PDF_LIBRARIES_AVAILABLE = True
except ImportError:
    PDF_LIBRARIES_AVAILABLE = False
    print("Warning: PDF libraries not available. Install: pip install PyPDF2 PyMuPDF")

try:
    import pytesseract
    import cv2
    import numpy as np
    OCR_LIBRARIES_AVAILABLE = True
except ImportError:
    OCR_LIBRARIES_AVAILABLE = False
    print("Warning: OCR libraries not available. Install: pip install pytesseract opencv-python")

try:
    from .estate_forms_complete import EstateFormsPatternMatcher
    COMPREHENSIVE_SYSTEM_AVAILABLE = True
except ImportError:
    EstateFormsPatternMatcher = None
    COMPREHENSIVE_SYSTEM_AVAILABLE = False
    print("Warning: estate_forms_complete.py not found. Form-specific mapping will be disabled.")

## DYNAMIC PATH RESOLUTION: Step 1 - Import the necessary components
try:
    from .dynamic_path_resolver import DynamicPathResolver, PathResolutionResult
    from .schema import cadence_schema # Import the schema for path validation
    DYNAMIC_PATH_RESOLUTION_AVAILABLE = True
except ImportError:
    DynamicPathResolver, PathResolutionResult, cadence_schema = None, None, None
    DYNAMIC_PATH_RESOLUTION_AVAILABLE = False
    print("Warning: DynamicPathResolver or schema not found. Dynamic path resolution is disabled.")


logger = logging.getLogger(__name__)

def serialize_for_api(obj):
    """
    Convert Enum objects and dataclass objects to API-safe dictionaries
    """
    from enum import Enum
    from dataclasses import asdict, is_dataclass
    
    if isinstance(obj, Enum):
        return obj.value
    elif is_dataclass(obj):
        # Convert dataclass to dict and then serialize nested objects
        dict_obj = asdict(obj)
        return serialize_for_api(dict_obj)
    elif isinstance(obj, dict):
        return {key: serialize_for_api(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [serialize_for_api(item) for item in obj]
    else:
        return obj

def safe_check_field_type(field, field_type_flag):
    try:
        if hasattr(field, 'field_type') and isinstance(field.field_type, PDFFieldType): return bool(field.field_type & field_type_flag)
    except Exception: pass
    return False

class EstateSubjectDetector:
    def __init__(self): logger.info("EstateSubjectDetector Initialized.")
    def detect_subject_role(self, field_data, form_context=None) -> SubjectDetectionResult:
        role_scores = defaultdict(float)
        full_text = ' '.join(list(field_data.keys()) + list(field_data.values())).lower()
        if 'executor' in full_text: role_scores[SubjectRole.EXECUTOR] = 0.8
        if 'spouse' in full_text: role_scores[SubjectRole.SPOUSE] = 0.7
        if 'next of kin' in full_text: role_scores[SubjectRole.NEXT_OF_KIN] = 0.9
        if 'child' in full_text: role_scores[SubjectRole.CHILD] = 0.6

        # CALIFORNIA DMV DEATH REPORT DETECTION:
        # ===================================================
        if 'person reporting death' in full_text or 'dmv 22' in full_text or 'california dmv death report' in full_text:
            role_scores[SubjectRole.FAMILY_MEMBER] = 0.90
            role_scores[SubjectRole.ESTATE_REPRESENTATIVE] = 0.85
            role_scores[SubjectRole.NEXT_OF_KIN] = 0.80
            role_scores[SubjectRole.LEGAL_REPRESENTATIVE] = 0.75

        if 'relationship' in full_text and ('death' in full_text or 'deceased' in full_text):
            if 'license' in full_text or 'placard' in full_text or 'dmv' in full_text:
                role_scores[SubjectRole.FAMILY_MEMBER] = 0.85
                role_scores[SubjectRole.ESTATE_REPRESENTATIVE] = 0.80
                role_scores[SubjectRole.NEXT_OF_KIN] = 0.75

        # IMPROVED: Electoral-specific detection
        if 'elector signature' in full_text or 'electoral' in full_text:
            role_scores[SubjectRole.FAMILY_MEMBER] = 0.90      # Most common
            role_scores[SubjectRole.ESTATE_REPRESENTATIVE] = 0.85  # Formal role
            role_scores[SubjectRole.NEXT_OF_KIN] = 0.80        # Legal authority

        # ADD FLORIDA-SPECIFIC DETECTION (HIGH PRIORITY):
        if any(pattern in full_text for pattern in ['florida', 'hsmv', 'owner name', 'vehicle']):
            role_scores[SubjectRole.HEIR] = 0.95
            role_scores[SubjectRole.ESTATE_REPRESENTATIVE] = 0.90
            role_scores[SubjectRole.APPLICANT] = 0.85
        # ENHANCED FLORIDA DMV DETECTION (MORE SPECIFIC):
        if any(pattern in full_text for pattern in [
            'florida certificate', 'hsmv', 'florida dmv', 'vehicle owner',
            'owner name', 'co-owner name', 'florida resident' ]):
            role_scores[SubjectRole.APPLICANT] = 0.95
            role_scores[SubjectRole.ESTATE_REPRESENTATIVE] = 0.85
            role_scores[SubjectRole.HEIR] = 0.90

        # ADD ISP-1640 CHILD REARING PROVISION DETECTION:
        if 'sc_isp1640_e' in full_text or 'child rearing provision' in full_text or 'sub_info' in full_text:
            role_scores[SubjectRole.PARENT] = 0.95
            role_scores[SubjectRole.GUARDIAN] = 0.90
            role_scores[SubjectRole.FAMILY_MEMBER] = 0.85
            role_scores[SubjectRole.APPLICANT] = 0.80
            role_scores[SubjectRole.BENEFICIARY] = 0.75

        # ADD SERVICE CANADA CHILD BENEFITS DETECTION:
        if 'child rearing' in full_text or 'family allowance' in full_text or 'canada child benefit' in full_text:
            role_scores[SubjectRole.PARENT] = 0.90
            role_scores[SubjectRole.GUARDIAN] = 0.85
            role_scores[SubjectRole.FAMILY_MEMBER] = 0.80

        # ADD ISP-1640 FORM-SPECIFIC ENHANCEMENT:
        if form_context and form_context.get('detected_form') == 'service_canada_child_rearing_isp1640':
            role_scores[SubjectRole.PARENT] = 0.95
            role_scores[SubjectRole.GUARDIAN] = 0.90
            role_scores[SubjectRole.FAMILY_MEMBER] = 0.85
            role_scores[SubjectRole.APPLICANT] = 0.80
            role_scores[SubjectRole.BENEFICIARY] = 0.75

        # ADD CRA/TAX-SPECIFIC DETECTION:
        if 'legal representative' in full_text or 'signature representative' in full_text:
            role_scores[SubjectRole.ESTATE_REPRESENTATIVE] = 0.95
            role_scores[SubjectRole.LEGAL_REPRESENTATIVE] = 0.90
            role_scores[SubjectRole.EXECUTOR] = 0.85

        #  for Service Canada Employment Insurance INS2882 Form
        if form_context and form_context.get('detected_form') == 'service_canada_benefit_payment_ins2882':
            role_scores[SubjectRole.ESTATE_REPRESENTATIVE] = 0.95
            role_scores[SubjectRole.LEGAL_REPRESENTATIVE] = 0.90
            role_scores[SubjectRole.EXECUTOR] = 0.85

       # ADD IRS FORM 1310 REFUND CLAIM DETECTION:
        if form_context and form_context.get('detected_form') == 'irs_form_1310_refund_claim':
            role_scores[SubjectRole.ESTATE_REPRESENTATIVE] = 0.95
            role_scores[SubjectRole.SURVIVING_SPOUSE] = 0.90
            role_scores[SubjectRole.EXECUTOR] = 0.85
            role_scores[SubjectRole.LEGAL_REPRESENTATIVE] = 0.80

        # ADD THIS BLOCK for the new Maine form
        if form_context and form_context.get('detected_form') == 'maine_voter_death_notice':
            role_scores[SubjectRole.FAMILY_MEMBER] = 0.95 # This is the explicit role on the form
            role_scores[SubjectRole.APPLICANT] = 0.90
            for role in role_scores:
                role_scores[role] = min(1.0, role_scores[role] + 0.25)

        # SS-4 Estate form gets highest priority
        if form_context and form_context.get('detected_form') == 'irs_form_ss4_estate':
            role_scores[SubjectRole.EXECUTOR] = 0.95
            role_scores[SubjectRole.ESTATE_REPRESENTATIVE] = 0.90
            role_scores[SubjectRole.LEGAL_REPRESENTATIVE] = 0.85

        # Text-based detection (runs for all forms)
        elif 'responsible party' in full_text or 'executor, administrator, trustee' in full_text:
            role_scores[SubjectRole.EXECUTOR] = 0.90
            role_scores[SubjectRole.ESTATE_REPRESENTATIVE] = 0.85

         # ADD IRS FORM 1310 SPECIFIC TEXT DETECTION:
        if 'claiming refund due deceased taxpayer' in full_text or 'person claiming refund' in full_text:
            role_scores[SubjectRole.ESTATE_REPRESENTATIVE] = 0.90
            role_scores[SubjectRole.SURVIVING_SPOUSE] = 0.85
            role_scores[SubjectRole.EXECUTOR] = 0.80

        if 'surviving spouse requesting reissuance' in full_text:
            role_scores[SubjectRole.SURVIVING_SPOUSE] = 0.95
            role_scores[SubjectRole.ESTATE_REPRESENTATIVE] = 0.80

        if 'court appointed representative' in full_text or 'court-appointed representative' in full_text:
            role_scores[SubjectRole.ESTATE_REPRESENTATIVE] = 0.95
            role_scores[SubjectRole.EXECUTOR] = 0.90

        # Service Canada T4A Representative form specific logic
        if 'deemed person to represent' in full_text or 'deceased client' in full_text or 'txtF_SignatureOfPersonToR' in full_text:
            role_scores[SubjectRole.ESTATE_REPRESENTATIVE] = 0.90
            role_scores[SubjectRole.LEGAL_REPRESENTATIVE] = 0.85
            role_scores[SubjectRole.EXECUTOR] = 0.80

        if 'sc_isp1202' in full_text or 'purpose of issuing a t' in full_text:
            role_scores[SubjectRole.ESTATE_REPRESENTATIVE] = 0.95
            role_scores[SubjectRole.LEGAL_REPRESENTATIVE] = 0.90

        if 't4a' in full_text or 't-4' in full_text:
            role_scores[SubjectRole.ESTATE_REPRESENTATIVE] = 0.85
            role_scores[SubjectRole.LEGAL_REPRESENTATIVE] = 0.80

        if 'sub_sectiona' in full_text or 'sub_sectionb' in full_text:
            role_scores[SubjectRole.ESTATE_REPRESENTATIVE] = 0.80
            role_scores[SubjectRole.LEGAL_REPRESENTATIVE] = 0.75

        # ADD IRS FORM 56 FIDUCIARY DETECTION:
        if form_context and form_context.get('detected_form') == 'irs_form_56_fiduciary':
            role_scores[SubjectRole.EXECUTOR] = 0.95
            role_scores[SubjectRole.ESTATE_REPRESENTATIVE] = 0.90
            role_scores[SubjectRole.TRUSTEE] = 0.85
            role_scores[SubjectRole.LEGAL_REPRESENTATIVE] = 0.80

        # ADD FIREARM-SPECIFIC DETECTION:
        if 'transferee' in full_text or 'transferor' in full_text or 'atf' in full_text:
            role_scores[SubjectRole.HEIR] = 0.95               # Most common - inheriting firearm
            role_scores[SubjectRole.ESTATE_REPRESENTATIVE] = 0.90  # Executor handling transfer
            role_scores[SubjectRole.BENEFICIARY] = 0.85        # Named in will
            role_scores[SubjectRole.LEGAL_REPRESENTATIVE] = 0.80   # Attorney/legal help

        # ADD VEHICLE TRANSFER DETECTION:
        if 'vehicle' in full_text or 'license plate' in full_text or 'inheritance box' in full_text:
            role_scores[SubjectRole.HEIR] = 0.90              # Inheriting vehicle
            role_scores[SubjectRole.FAMILY_MEMBER] = 0.85     # Family transfer
            role_scores[SubjectRole.BENEFICIARY] = 0.80       # Named beneficiary
            role_scores[SubjectRole.ESTATE_REPRESENTATIVE] = 0.75  # Executor handling transfer
        # ADD CPP SURVIVOR DETECTION:
        if 'cpp survivors' in full_text or 'surviving spouse' in full_text or 'sc_isp1300' in full_text:
            role_scores[SubjectRole.SURVIVING_SPOUSE] = 0.95
            role_scores[SubjectRole.ESTATE_REPRESENTATIVE] = 0.85
            role_scores[SubjectRole.FAMILY_MEMBER] = 0.80
            role_scores[SubjectRole.BENEFICIARY] = 0.75

        # ADD CRA DEATH NOTIFICATION DETECTION:
        if 'notify canada revenue agency death' in full_text or 'rc4111' in full_text or 'relationship to the deceased person' in full_text:
            role_scores[SubjectRole.FAMILY_MEMBER] = 0.90
            role_scores[SubjectRole.ESTATE_REPRESENTATIVE] = 0.85
            role_scores[SubjectRole.NEXT_OF_KIN] = 0.80
            role_scores[SubjectRole.EXECUTOR] = 0.75

        # ADD CPP DEATH BENEFIT (ISP-1200) DETECTION:
        if any(pattern in full_text for pattern in ['isp-1200', 'isp 1200', 'application for a canada pension plan death benefit', 'order of priority']):
            role_scores[SubjectRole.EXECUTOR] = 0.95              # Top of the priority list
            role_scores[SubjectRole.ESTATE_REPRESENTATIVE] = 0.90 # General term for executor/admin
            role_scores[SubjectRole.APPLICANT] = 0.85             # The person applying
            role_scores[SubjectRole.SURVIVING_SPOUSE] = 0.80      # Lower priority on this form
            role_scores[SubjectRole.NEXT_OF_KIN] = 0.75           # Lowest priority
         # ADD THIS ELIF BLOCK
        elif 'surviving spouse' in full_text or 'common-law partner' in full_text:
            role_scores[SubjectRole.SURVIVING_SPOUSE] = 0.98
            role_scores[SubjectRole.SPOUSE] = 0.95
            role_scores[SubjectRole.APPLICANT] = 0.90

        # ADD HILTON HONORS SPECIFIC DETECTION:
        if any(pattern in full_text for pattern in [
            'hilton honors', 'executorAdministrator', 'points transfer',
            'deceased member', 'declaration in support']):
            role_scores[SubjectRole.EXECUTOR] = 0.95
            role_scores[SubjectRole.ESTATE_REPRESENTATIVE] = 0.90
            role_scores[SubjectRole.ADMINISTRATOR] = 0.85

        # IRS FORM 2848 SPECIFIC DETECTION:
        if any(pattern in full_text for pattern in [
            'power of attorney', 'declaration of representative', 'taxpayername',
            'representativesname', 'cafnumber', 'ptin', 'topmostsubform']):
            role_scores[SubjectRole.LEGAL_REPRESENTATIVE] = 0.95
            role_scores[SubjectRole.ATTORNEY] = 0.90
            role_scores[SubjectRole.POWER_OF_ATTORNEY] = 0.85

        # ADD MANITOBA FUNERAL INVOICE DETECTION:
        if any(pattern in full_text for pattern in ['eia case no', 'funeral home', 'total fees', 'manitoba invoice', 'schedule b']):
            role_scores[SubjectRole.ESTATE_REPRESENTATIVE] = 0.95  # Person responsible for estate debts
            role_scores[SubjectRole.APPLICANT] = 0.90             # Person applying for EIA benefit
            role_scores[SubjectRole.FAMILY_MEMBER] = 0.85         # Most common arranger
            role_scores[SubjectRole.EXECUTOR] = 0.80              # Formal title

         # ADD NEVADA DMV AFFIDAVIT DETECTION:
        if any(pattern in full_text for pattern in ['affidavit for transfer', 'vp-24', 'vp 24', 'nevada dmv', 'affiant']):
            role_scores[SubjectRole.HEIR] = 0.98                  # Heir is the primary legal role on this form.
            role_scores[SubjectRole.APPLICANT] = 0.90             # The person is applying for the title transfer.
            role_scores[SubjectRole.FAMILY_MEMBER] = 0.85         # The heir is almost always family.
            role_scores[SubjectRole.ESTATE_REPRESENTATIVE] = 0.80 # Can be filled by a representative.

        # ADD SERVICE CANADA ISP-1201 TEXT DETECTION:
        if any(pattern in full_text for pattern in ['isp-1201', 'isp 1201', 'notification of death', 'cpp', 'oas', 'funeral service provider']):
            # On this form, the "Information Provided By" field is key. It's not a formal legal role.
            role_scores[SubjectRole.FAMILY_MEMBER] = 0.90         # Most common role for reporting
            role_scores[SubjectRole.ESTATE_REPRESENTATIVE] = 0.85 # Can be a formal representative
            role_scores[SubjectRole.APPLICANT] = 0.80             # They are "applying" to notify
            role_scores[SubjectRole.LEGAL_REPRESENTATIVE] = 0.75

        if (form_context and form_context.get('detected_form') == 'social_security_death_payment_ssa8') or \
            any(pattern in full_text for pattern in ['ssa-8', 'lump-sum death payment', 'deceased wage earner', 'social_security_death_payment_ssa8']):
                # SSA-8 has strict federal payment hierarchy
                role_scores[SubjectRole.SURVIVING_SPOUSE] = 0.95
                role_scores[SubjectRole.CHILD] = 0.90
                role_scores[SubjectRole.APPLICANT] = 0.85

                # Apply mandatory confidence boost for confirmed SSA-8 forms
                for role in list(role_scores.keys()):
                    role_scores[role] = min(1.0, role_scores[role] + 0.20)

        # ADD CANADA POST MAIL FORWARDING DETECTION:
        if any(pattern in full_text for pattern in [
            'mail forwarding', 'canada post', 'requestor\'s details',
            'deceased individual', 'mail recipients']):
            role_scores[SubjectRole.FAMILY_MEMBER] = 0.85      # Person handling deceased's mail
            role_scores[SubjectRole.ESTATE_REPRESENTATIVE] = 0.80  # Formal representative
            role_scores[SubjectRole.APPLICANT] = 0.75         # Person requesting service
            role_scores[SubjectRole.NEXT_OF_KIN] = 0.70       # Often next of kin handles mail




        # --- CONTEXT-AWARE CONFIDENCE BOOST ---
        # If the form has already been identified as SSA-8, be more confident in the role.
        if form_context and form_context.get('detected_form') == 'social_security_death_payment_ssa8':
            if SubjectRole.SURVIVING_SPOUSE in role_scores:
                role_scores[SubjectRole.SURVIVING_SPOUSE] = min(1.0, role_scores[SubjectRole.SURVIVING_SPOUSE] + 0.30)
            if SubjectRole.CHILD in role_scores:
                role_scores[SubjectRole.CHILD] = min(1.0, role_scores[SubjectRole.CHILD] + 0.25)

        # ADD THIS BLOCK for the CPP Death Benefit (ISP-1200)
        if form_context and form_context.get('detected_form') == 'service_canada_cpp_death_benefit_isp1200':
            for role in role_scores:
                role_scores[role] = min(1.0, role_scores[role] + 0.30)

        # ADD THIS BLOCK for the Service Canada ISP-1201 form
        if form_context and form_context.get('detected_form') == 'service_canada_death_notification_isp1201':
            for role in role_scores:
                role_scores[role] = min(1.0, role_scores[role] + 0.25)

        # ADD THIS BLOCK for the Nevada DMV Affidavit
        if form_context and form_context.get('detected_form') == 'nevada_dmv_affidavit_vp24':
            for role in role_scores:
                role_scores[role] = min(1.0, role_scores[role] + 0.30)

         # ADD THIS BLOCK for the Manitoba Funeral Invoice
        if form_context and form_context.get('detected_form') == 'manitoba_funeral_home_invoice_schedule_b':
            for role in role_scores:
                role_scores[role] = min(1.0, role_scores[role] + 0.25)

        # Enhanced confidence for IRS forms
        if form_context and form_context.get('detected_form') == 'irs_form_ss4_estate':
            for role in role_scores:
                role_scores[role] = min(1.0, role_scores[role] + 0.20)

        # Enhanced confidence for ISP-1640 forms
        if form_context and form_context.get('detected_form') == 'service_canada_child_rearing_isp1640':
            for role in role_scores:
                role_scores[role] = min(1.0, role_scores[role] + 0.25)  # High boost

         # Enhanced confidence for california DMV death report
        if form_context and form_context.get('detected_form') == 'california_dmv_death_report_dmv22':
            for role in role_scores:
                role_scores[role] = min(1.0, role_scores[role] + 0.20)
        # Enhanced confidence for CRA death notification
        if form_context and form_context.get('detected_form') == 'cra_death_notification_rc4111':
            for role in role_scores:
                role_scores[role] = min(1.0, role_scores[role] + 0.25)

        # Service Canada T4A Representative form specific logic
        if form_context and form_context.get('detected_form') == 'service_canada_t4a_representative_isp1202':
            for role in role_scores:
                role_scores[role] = min(1.0, role_scores[role] + 0.25)

        # Enhanced confidence for CPP forms
        if form_context and form_context.get('detected_form') == 'service_canada_cpp_survivors_pension_isp1300':
            for role in role_scores:
                role_scores[role] = min(1.0, role_scores[role] + 0.20)

        # ADD ATF FORM ENHANCEMENT:
        if form_context and form_context.get('detected_form') == 'atf_form_5_firearm_transfer':
            for role in role_scores:
                role_scores[role] = min(1.0, role_scores[role] + 0.20)  # Higher boost for firearm forms

        # ADD CALIFORNIA DMV FORM ENHANCEMENT:
        if form_context and form_context.get('detected_form') == 'california_statement_of_facts_reg256':
            for role in role_scores:
                role_scores[role] = min(1.0, role_scores[role] + 0.25)  # Strong boost for vehicle forms

       # Enhanced confidence for IRS Form 56 Fiduciary
        if form_context and form_context.get('detected_form') == 'irs_form_56_fiduciary':
            for role in role_scores:
                role_scores[role] = min(1.0, role_scores[role] + 0.25)  # High boost for fiduciary forms

        # ADD CRA FORM ENHANCEMENT:
        if form_context and form_context.get('detected_form') == 'cra_legal_representative_appointment':
            for role in role_scores:
                role_scores[role] = min(1.0, role_scores[role] + 0.15)

        # Enhanced confidence for IRS Form 1310 Refund Claim
        if form_context and form_context.get('detected_form') == 'irs_form_1310_refund_claim':
            for role in role_scores:
                role_scores[role] = min(1.0, role_scores[role] + 0.25)  # High boost for refund claim forms

        # Enhanced confidence for Florida forms
        if form_context and form_context.get('detected_form') == 'florida_certificate_title_hsmv82040':
            for role in role_scores:
                role_scores[role] = min(1.0, role_scores[role] + 0.25)  # High boost for Florida forms

        # Enhanced confidence for Hilton Honors forms
        if form_context and form_context.get('detected_form') == 'hilton_honors_points_transfer':
            for role in role_scores:
                role_scores[role] = min(1.0, role_scores[role] + 0.25)  # High boost for loyalty programs

        # Enhanced confidence for IRS Form 2848
        if form_context and form_context.get('detected_form') == 'irs_form_2848_power_of_attorney':
            for role in role_scores:
                role_scores[role] = min(1.0, role_scores[role] + 0.25)

        # Enhanced confidence for electoral forms
        if form_context and form_context.get('detected_form') == 'electoral_deceased_removal_form':
            for role in role_scores:
                role_scores[role] = min(1.0, role_scores[role] + 0.10)
        if not role_scores: return SubjectDetectionResult(SubjectRole.APPLICANT, 0.3, [], {})
        primary_role = max(role_scores, key=role_scores.get)
        confidence = min(1.0, role_scores[primary_role] + 0.1 * (len(role_scores) > 1))
        return SubjectDetectionResult(primary_role, confidence, [], {})


    def _detect_form_type(self, fields: List[PDFFieldExtraction], pdf_path: str) -> PDFFormInfo:
        field_text = ' '.join(f.field_name.lower() for f in fields)
        form_type = PDFFormType.UNKNOWN




        # DEBUG CODE:
        print(f"🔍 DEBUG: Field text contains: {field_text[:400]}...")


        # ---  SSA-8 DETECTION TO THE TOP FOR HIGHEST PRIORITY ---
        if any(kw in field_text for kw in [
            'lump-sum death payment', 'ssa-8', '0960-0013', 'deceased wage earner',
            'form1[0].#subform']): # Added a structural key for more robustness
            print("✅ Matched: DEATH_BENEFIT_APPLICATION (SSA-8)")
            form_type = PDFFormType.DEATH_BENEFIT_APPLICATION
         # --- THIS NEW HIGH-PRIORITY BLOCK FOR CANADA POST ---
        elif any(kw in field_text for kw in [
            'mail forwarding', 'canada post', 'canadapost.ca/mailforwarding',
            'mail recipients', 'deceased individual', 'requestor\'s details',
            '33-086-784', 'effective service dates', 'current address', 'new address']):
            print("✅ Matched: DEATH_NOTIFICATION (Canada Post Mail Forwarding)")
            form_type = PDFFormType.DEATH_NOTIFICATION
        # ADD FLORIDA DETECTION FIRST (HIGHEST PRIORITY):
        elif any(kw in field_text for kw in ['owner name', 'co-owner name', 'customer number', 'florida', 'hsmv']):
            print("✅ Matched: VEHICLE_TRANSFER (Florida)")
            form_type = PDFFormType.VEHICLE_TRANSFER
        elif any(kw in field_text for kw in ['relationship to the deceased person', 'social insurance number sin', 'rc4111', 'notify canada revenue agency']):
            print("✅ Matched: TAX_ADMINISTRATION (CRA Death Notification)")
            form_type = PDFFormType.TAX_ADMINISTRATION
        # IRS FORM 56 FIDUCIARY RELATIONSHIP DETECTION
        elif any(kw in field_text for kw in [
            'notice concerning fiduciary relationship', 'form 56', 'form56',
            'fiduciary name', 'fiduciary\'s name', 'authority for fiduciary relationship',
            'court appointment', 'testate estate', 'intestate estate',
            'name of person for whom you are acting', 'identifying number',
            'federal tax form number', 'type of taxes']):
            print("✅ Matched: TAX_ADMINISTRATION (IRS Form 56 Fiduciary)")
            form_type = PDFFormType.TAX_ADMINISTRATION
        # MILITARY BENEFITS - Enhanced Detection (ADD THIS FIRST)
        elif any(kw in field_text for kw in [
            'mbr_name', 'mbr_ssn', 'mbr_grade',  # Member fields
            'death_gratuity', 'bureau_no', 'do_no',  # Military administrative
            'payee_sign', 'amt_due', 'adm_name',  # Payment/admin fields
            'xcert', 'xwidow', 'xrel',  # Military certification checkboxes
            'dd form 397', 'dd397', 'death gratuity payment',  # Form identifiers
            'service member', 'servicemember', 'military death']):
            print("✅ Matched: MILITARY_BENEFITS (Death Gratuity)")
            form_type = PDFFormType.MILITARY_BENEFITS
        elif any(kw in field_text for kw in ['sc_isp1300_e', 'cpp survivors pension', 'txtf_1a_sin', 'surviving spouse']):
            print("✅ Matched: DEATH_BENEFIT_APPLICATION (CPP)")
            form_type = PDFFormType.DEATH_BENEFIT_APPLICATION
        # ADD MAINE VOTER DEATH NOTICE DETECTION
        elif any(kw in field_text for kw in ['voter\'s death', 'registrar', 'immediate family member', 'maine', 'cvr']):
            print("✅ Matched: ELECTORAL_ADMINISTRATION (Maine Voter Death Notice)")
            form_type = PDFFormType.ELECTORAL_ADMINISTRATION
        # IRS FORM 2848 DETECTION - HIGH PRIORITY
        elif any(kw in field_text for kw in [
            'topmostsubform', 'taxpayername', 'representativesname', 'cafnumber', 'ptin',
            'taxpayerid', 'bodyrow', 'table_partii', 'designation', 'jurisdiction']):
            print("✅ Matched: TAX_ADMINISTRATION (IRS Form 2848)")
            form_type = PDFFormType.TAX_ADMINISTRATION
        # ADD HILTON HONORS DETECTION FIRST (HIGHEST PRIORITY):
        elif any(kw in field_text for kw in [
            'death of hilton honors member', 'member died on', 'executorAdministrator',
            'hilton honors', 'points transfer', 'deceased member']):
            print("✅ Matched: ESTATE_INFORMATION (Hilton Honors Points Transfer)")
            form_type = PDFFormType.ESTATE_INFORMATION
        # ADD IRS FORM DETECTION FIRST (before other patterns)
        elif any(kw in field_text for kw in [
            'topmostsubform[0].page1[0].f1_', 'employer identification number',
            'form ss-4', 'department of the treasury', 'internal revenue service']):
            print("✅ Matched: TAX_ADMINISTRATION (IRS SS-4)")
            form_type = PDFFormType.TAX_ADMINISTRATION
        # SERVICE CANADA DEATH NOTIFICATION (ISP-1201) - HIGHER PRIORITY
        elif any(kw in field_text for kw in ['isp-1201', 'isp 1201', 'canada pension plan', 'old age security', 'mother\'s maiden name', 'funeral service provider']):
            print("✅ Matched: DEATH_NOTIFICATION (Service Canada ISP-1201)")
            form_type = PDFFormType.DEATH_NOTIFICATION
        elif any(kw in field_text for kw in [
            'legal owner', 'dl id', 'parking placard-id', 'person reporting death',
            'date of birth1', 'date of year1', 'principal city', 'principal county',
            'telephone', 'e-mail', 'applicant date']):
            print("✅ Matched: DEATH_NOTIFICATION (California DMV Death Report)")
            form_type = PDFFormType.DEATH_NOTIFICATION  # Add this enum value
        elif any(kw in field_text for kw in ['legal representative', 'signature representative', 'representative repid', 'canada revenue']):
            print("✅ Matched: TAX_ADMINISTRATION (CRA Legal Rep)")
            form_type = PDFFormType.TAX_ADMINISTRATION
        elif any(kw in field_text for kw in ['elector signature', 'registers maintained', 'elections ontario']):
            print("✅ Matched: ELECTORAL_ADMINISTRATION")
            form_type = PDFFormType.ELECTORAL_ADMINISTRATION
        elif any(kw in field_text for kw in ['atf', 'firearm', 'transferee', 'transferor', 'topmostsubform', 'federal firearms license']):
            print("✅ Matched: FIREARM_TRANSFER")
            form_type = PDFFormType.FIREARM_TRANSFER
        elif any(kw in field_text for kw in ['death benefit', 'cpp', 'pension']):
            print("✅ Matched: DEATH_BENEFIT_APPLICATION")
            form_type = PDFFormType.DEATH_BENEFIT_APPLICATION
        elif any(kw in field_text for kw in ['statement of facts', 'license plate', 'vehicle vessel id', 'reg 256', 'california dmv']):
            print("✅ Matched: VEHICLE_TRANSFER (California DMV)")
            form_type = PDFFormType.VEHICLE_TRANSFER
        elif any(kw in field_text for kw in ['vin', 'vehicle', 'dmv']):
            print("✅ Matched: VEHICLE_TRANSFER")
            form_type = PDFFormType.VEHICLE_TRANSFER
        elif any(kw in field_text for kw in ['military', 'veteran']):
            print("✅ Matched: MILITARY_BENEFITS")
            form_type = PDFFormType.MILITARY_BENEFITS
        # ADD MANITOBA FUNERAL INVOICE DETECTION
        elif any(kw in field_text for kw in ['funeral home', 'invoice', 'eia case no', 'manitoba', 'total fees', 'schedule b', 'oversized casket']):
            print("✅ Matched: ESTATE_INFORMATION (Manitoba Funeral Invoice)")
            form_type = PDFFormType.ESTATE_INFORMATION
        elif any(kw in field_text for kw in [
            'mail forwarding', 'canada post', 'canadapost.ca/mailforwarding',
            'mail recipients', 'deceased individual', 'requestor\'s details',
            '33-086-784', 'effective service dates', 'current address', 'new address']):
            print("✅ Matched: DEATH_NOTIFICATION (Canada Post Mail Forwarding)")
            form_type = PDFFormType.DEATH_NOTIFICATION
        # Enhanced ISP-1640 Detection (ADD THIS FIRST - HIGHEST PRIORITY)
        elif any(kw in field_text for kw in [
            'sc_isp1640_e', 'child rearing provision', 'sub_info', 'sub_section_b',
            'sub_waiver', 'txtf_firstname', 'txtf_lastname', 'txtf_address',
            'txtf_emailaddress', 'table2', 'check_boxes', 'page3', 'page4', 'page5']):
            print("✅ Matched: DEATH_BENEFIT_APPLICATION (Service Canada Child Rearing ISP-1640)")
            form_type = PDFFormType.DEATH_BENEFIT_APPLICATION
        # NEVADA DMV AFFIDAVIT DETECTION
        elif any(kw in field_text for kw in ['affidavit for transfer', 'vp-24', 'vp 24', 'nevada dmv', 'affiant']):
            print("✅ Matched: VEHICLE_TRANSFER (Nevada VP-24)")
            form_type = PDFFormType.VEHICLE_TRANSFER
        # CPP DEATH BENEFIT APPLICATION (ISP-1200) - HIGH PRIORITY
        elif any(kw in field_text for kw in ['isp-1200', 'isp 1200', 'application for a canada pension plan death benefit', 'deceased contributor']):
            print("✅ Matched: DEATH_BENEFIT_APPLICATION (CPP Death Benefit ISP-1200)")
            form_type = PDFFormType.DEATH_BENEFIT_APPLICATION
        # SERVICE CANADA EMPLOYMENT INSURANCE DEATH BENEFIT - INS2882 (ADD THIS FIRST!)
        elif any(kw in field_text for kw in [
            'ins2882', 'esdc ins2882', 'request for payment of benefit',
            'deceased person', 'legal representative', 'employment insurance',
            'txtf_deceased_person', 'txtf_legal_representative', 'txtf_sin',
            'employment and social development canada', 'service canada']):
            print("✅ Matched: DEATH_BENEFIT_APPLICATION (Employment Insurance INS2882)")
            form_type = PDFFormType.DEATH_BENEFIT_APPLICATION


        else:
            print("❌ No match found")

        print(f"Final form_type: {form_type}")
        return PDFFormInfo(form_type=form_type, form_title=Path(pdf_path).name, total_fields=len(fields), fillable_fields=len(fields), signature_fields=0, date_fields=0, required_fields=0)
    async def analyze_conditional_logic(self, pdf_text: str, pdf_fields: List[PDFFieldExtraction]) -> ConditionalAnalysisResult: return ConditionalAnalysisResult()

class UniversalEstateMapper:
    def __init__(self, ollama_config=None):
        self.ollama_config = ollama_config
        self.subject_detector = EstateSubjectDetector()
        self.ai_enhancer = None
        if AI_ENHANCER_AVAILABLE and ollama_config:
            self.ai_enhancer = OllamaAIEnhancer(ollama_config)
            logger.info("AI Enhancer initialized for fallback mapping.")
        else:
            logger.warning("AI Enhancer is not available or not configured. AI fallback mapping is disabled.")

        if CONDITIONAL_LOGIC_AVAILABLE:
            self.conditional_processor = ProductionConditionalLogicEngine()
            logger.info("Initialized with ProductionConditionalLogicEngine.")
        else:
            self.conditional_processor = None
            logger.warning("Conditional logic processor is not available.")
        self.pdf_processor = PDFProcessor()
        if COMPREHENSIVE_SYSTEM_AVAILABLE:
            self.comprehensive_matcher = EstateFormsPatternMatcher()
            logger.info(f"Integrated with comprehensive matcher service: {len(self.comprehensive_matcher.get_all_form_identifiers())} forms")
        else:
            self.comprehensive_matcher = None
            logger.warning("Running in fallback mode: estate_forms_complete.py not found.")

        if ADVANCED_ENGINES_AVAILABLE:
            self.cross_field_validator = CrossFieldValidator()
            self.semantic_context_engine = SemanticContextEngine(ai_enhancer=None)
            self.form_completion_engine = FormCompletionEngine(ai_enhancer=None)
            logger.info("Initialized with advanced analysis engines (Validation, Semantic, Completion).")
        else:
            self.cross_field_validator = None
            self.semantic_context_engine = None
            self.form_completion_engine = None

        ## DYNAMIC PATH RESOLUTION: Step 2 - Instantiate the resolver in the mapper's constructor
        if DYNAMIC_PATH_RESOLUTION_AVAILABLE:
            # Provide the resolver with the full set of known schema paths for validation
            schema_paths_set = set(cadence_schema.get_schema_paths())
            self.path_resolver = DynamicPathResolver(schema_config={"paths": schema_paths_set})
            logger.info(f"DynamicPathResolver initialized with {len(schema_paths_set)} schema paths.")
        else:
            self.path_resolver = None
            logger.warning("Dynamic path resolver is not available.")

        self.universal_patterns = self._build_universal_patterns()

        self.stats = defaultdict(float)
        self.pattern_stats = PatternMatchingStats()

    def _build_universal_patterns(self) -> Dict[str, str]:
        """Builds a small set of universal, high-confidence fallback patterns."""
        return {
            'sin': 'applicant.social_insurance_number',
            'social security number': 'applicant.social_insurance_number',
            'ssn': 'applicant.social_insurance_number',
            'name': 'applicant.full_name',
            'full name': 'applicant.full_name',
            'phone': 'applicant.phone',
            'telephone': 'applicant.phone',
            'email': 'applicant.email',
            'address': 'applicant.home_address',
            'date of death': 'deceased.date_of_death',
            'date of birth': 'deceased.date_of_birth',
            'dob': 'deceased.date_of_birth'
        }

    async def process_pdf_file(self, pdf_path: str, **kwargs) -> Dict[str, Any]:
        """
        Processes a PDF file by extracting fields and then calling the core
        form processing logic. This version correctly uses proximity-based extraction.
        """
        try:
            # Step 1: Use the advanced proximity-based extraction from the PDFProcessor.
            # This returns a list of dictionaries, each containing the original complex field name
            # and the new, clean, human-readable label.
            labeled_fields_data = await self.pdf_processor._extract_fields_with_labels_by_proximity(pdf_path)

            # Step 2: Prepare the data for the main processing logic.
            field_data = {}
            field_name_map = {}
            initial_form_info = None

            if labeled_fields_data:
                # If proximity extraction was successful:
                # - 'field_data' will hold the original complex names and their values.
                # - 'field_name_map' will be our lookup table: {complex_name: clean_label}.
                field_data = {item['field_name']: item.get('field_value', '') for item in labeled_fields_data}
                field_name_map = {item['field_name']: item['field_label'] for item in labeled_fields_data}
                # We still run the basic extraction to get the FormInfo object.
                _, initial_form_info = await self.pdf_processor.extract_pdf_fields(pdf_path)
            else:
                # Fallback: If proximity extraction fails, use the old method.
                pdf_fields, initial_form_info = await self.pdf_processor.extract_pdf_fields(pdf_path)
                if not pdf_fields:
                    return {"error": "No fields could be extracted from the provided PDF."}
                field_data = {field.field_name: field.field_value for field in pdf_fields}
                # In the fallback case, the map will be empty, and the system will use the original names.

            # Step 3: Extract the full text for semantic analysis.
            pdf_text = await self.pdf_processor._extract_pdf_text(pdf_path)

            # Step 4: Call the main processing logic, passing the clean name map in the context.
            return await self.process_form(
                field_data=field_data,
                form_content=pdf_text,
                form_title=initial_form_info.form_title if initial_form_info else Path(pdf_path).name,
                context={"pdf_source": True, "field_name_map": field_name_map}
            )

        except Exception as e:
            logger.error(f"Critical error in process_pdf_file for {pdf_path}: {e}", exc_info=True)
            return {"error": f"An internal server error occurred while processing the PDF: {e}"}

    def detect_form(self, field_data: Dict[str, str], form_content: str = "", form_title: str = "") -> Tuple[Optional[str], float, Dict[str, Any]]:
        """
        Robust, weighted form detection engine that works for both interactive and flat PDFs.
        """
        if not self.comprehensive_matcher or not hasattr(self.comprehensive_matcher, 'FORM_DETECTION_PATTERNS'):
            return None, 0.0, {"method": "fallback", "result": "no_patterns_available"}

        try:
            field_names = list(field_data.keys())
            combined_text = (f"{form_title} {form_content} {' '.join(field_names)}").lower()

            best_match = None
            highest_score = 0.0

            for form_id, patterns in self.comprehensive_matcher.FORM_DETECTION_PATTERNS.items():
                score = 0.0

                # 1. Keyword Score (Weight: 40%) - Works on any PDF type
                keywords = patterns.get("keywords", [])
                if keywords:
                    hits = sum(1 for kw in keywords if kw.lower() in combined_text)
                    if hits > 0:
                        score += 0.40 * (hits / len(keywords))

                # 2. Required Field Score (Weight: 30%) - Good for known field names
                req_fields = patterns.get("required_fields", [])
                if req_fields:
                    hits = sum(1 for rf in req_fields if any(rf.lower() in fn.lower() for fn in field_names))
                    if hits > 0:
                        score += 0.30 * (hits / len(req_fields))

                # 3. Field Pattern Score (Weight: 30%) - Good for structured PDFs
                field_patterns = patterns.get("field_patterns", [])
                if field_patterns and any(re.search(p.lower(), combined_text) for p in field_patterns):
                    score += 0.30

                # Add a significant boost for core structural patterns
                if field_patterns and any(re.search(p, ' '.join(field_names)) for p in field_patterns):
                        score += 0.5

                if score > highest_score:
                    highest_score = score
                    best_match = form_id

            if highest_score > 0.5:
                metadata = self.comprehensive_matcher.get_form_metadata(best_match)
                detection_details = {
                    "form_id": best_match,
                    "score": min(1.0, highest_score),
                    "method": "weighted_pattern_scoring",
                    "category": metadata.category if metadata else "unknown"
                }
                return best_match, min(1.0, highest_score), detection_details

            return None, 0.0, {"method": "weighted_pattern_scoring", "result": "no_match_above_threshold"}

        except Exception as e:
            logger.error(f"Form detection failed: {e}", exc_info=True)
            return None, 0.0, {"error": str(e)}

    def _detect_subject_context(self, field_data: Dict[str, str], detected_form: Optional[str] = None) -> SubjectDetectionResult:
        ## DYNAMIC PATH RESOLUTION: This method now returns the full object for use by the resolver
        return self.subject_detector.detect_subject_role(field_data, {'detected_form': detected_form})

    async def map_field(self, field_name: str, field_value: str = "", detected_form: Optional[str] = None, subject_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Maps a field name to a Cadence schema path using a multi-layered approach:
        1. Exact Rule-Based Matching (Highest Confidence)
        2. Fuzzy String Matching (High Confidence - Corrects OCR errors)
        3. Universal Pattern Matching (Medium Confidence)
        4. AI Fallback (Variable Confidence)
        """
        # Use the comprehensive matcher if a form was detected
        if detected_form and self.comprehensive_matcher:
            
            # --- PRIORITY 1: EXACT MATCH ---
            # Try to find a perfect, case-insensitive match first.
            exact_path = self.comprehensive_matcher.map_field_to_cadence_path(detected_form, field_name)
            if exact_path:
                return {'cadence_path': exact_path, 'confidence_score': 98.0, 'method': 'comprehensive_exact_match'}

            # --- PRIORITY 2: FUZZY STRING MATCH (The Fix for OCR Errors) ---
            # Get all known, correct field labels for this form
            form_mappings = self.comprehensive_matcher.get_form_mapping(detected_form)
            if form_mappings:
                known_labels = [mapping.form_field for mapping in form_mappings]
                
                best_match_label = None
                highest_score = 0

                # Compare the misspelled OCR field_name against our list of perfect labels
                for label in known_labels:
                    # fuzz.token_set_ratio is excellent for this, as it handles typos and extra words
                    score = fuzz.token_set_ratio(field_name.lower(), label.lower())
                    if score > highest_score:
                        highest_score = score
                        best_match_label = label

                # If we find a very close match (e.g., > 85% similarity), we accept it as a correction.
                FUZZY_MATCH_THRESHOLD = 85
                if highest_score > FUZZY_MATCH_THRESHOLD:
                    corrected_path = self.comprehensive_matcher.map_field_to_cadence_path(detected_form, best_match_label)
                    if corrected_path:
                        logger.info(f"✅ Fuzzy match corrected OCR error: '{field_name}' -> '{best_match_label}' (Score: {highest_score})")
                        # Confidence is high but slightly penalized for not being an exact match.
                        return {'cadence_path': corrected_path, 'confidence_score': 90.0, 'method': 'fuzzy_string_match'}

        # --- PRIORITY 3: UNIVERSAL PATTERN MATCHING ---
        field_name_lower = field_name.lower().replace('_', ' ')
        for pattern, path in self.universal_patterns.items():
            if pattern in field_name_lower:
                return {'cadence_path': path, 'confidence_score': 75.0, 'method': 'universal_pattern'}

        # --- PRIORITY 4: AI FALLBACK ---
        if self.ai_enhancer:
            junk_keywords = ['clear form', 'reset', 'submit', 'print', 'button', 'click']
            if any(kw in field_name.lower() for kw in junk_keywords):
                return {'cadence_path': 'unknown.field', 'confidence_score': 10.0, 'method': 'filtered_skipped'}
            
            logger.info(f"🤖 No rule-based match for '{field_name}'. Asking AI for help...")
            ai_context = f"This field is from the '{detected_form}' form." if detected_form else ""
            ai_result = await self.ai_enhancer.enhance_field_mapping(field_name, field_value, context=ai_context)
            
            if ai_result.get("success") and "unknown.field" not in ai_result.get("path", ""):
                logger.info(f"✅ AI successfully mapped '{field_name}' to '{ai_result['path']}'")
                return {
                    'cadence_path': ai_result['path'],
                    'confidence_score': ai_result.get('confidence', 0.7) * 100,
                    'method': 'ollama_context_aware'
                }
            else:
                logger.warning(f"⚠️ AI could not map '{field_name}'. Reason: {ai_result.get('reason', 'Unknown')}")

        # --- FINAL FALLBACK ---
        return {'cadence_path': 'unknown.field', 'confidence_score': 0.0, 'method': 'unmapped'}

        # ---  STEP 4: USE OLLAMA AI AS A FALLBACK ---
        if self.ai_enhancer:
            # ... (junk filter) ...
            logger.info(f"🤖 No rule-based match found for '{field_name}'. Asking AI for help...")
            ai_context = f"This field is from the '{detected_form}' form." if detected_form else ""
            ai_result = await self.ai_enhancer.enhance_field_mapping(field_name, field_value, context=ai_context)
            
            # THIS IS THE FLAWED PART
            if ai_result.get("success") and "unknown.field" not in ai_result.get("path", ""):
                logger.info(f"✅ AI successfully mapped '{field_name}' to '{ai_result['path']}'")
                return {
                    'cadence_path': ai_result['path'],
                    'confidence_score': ai_result.get('confidence', 0.7) * 100,
                    'method': 'ai_fallback_mapping' # This was an old method name
                }
            else:
                logger.warning(f"⚠️ AI could not map '{field_name}'. Reason: {ai_result.get('reason', 'Unknown')}")
        # --- END NEW STEP ---

        # Final fallback if AI also fails or is disabled
        return {'cadence_path': 'notes.additional_field', 'confidence_score': 40.0, 'method': 'semantic_fallback'}
    async def process_form(self, field_data: Dict[str, str], form_content: str = "", form_title: str = "", context: Dict[str, Any] = None) -> Dict[str, Any]:
        start_time = time.time()
        try:
            # --- STAGE 1: INITIAL DETECTION AND MAPPING ---
            detected_form, confidence, detection_details = self.detect_form(field_data, form_content, form_title)
            
            ## DYNAMIC PATH RESOLUTION: Step 3 - Get the full SubjectDetectionResult object
            subject_result_obj = self._detect_subject_context(field_data, detected_form)
            # Create a dictionary version for the final API response
            subject_context_dict = {
                "primary_subject": subject_result_obj.role.value,
                "confidence": subject_result_obj.confidence,
                "dynamic_mappings": subject_result_obj.dynamic_mappings
            }

            logic_context = {"form_type": detected_form, "subject_role": subject_context_dict.get("primary_subject")}

            conditional_rules_objects = []
            if self.conditional_processor:
                conditional_rules_objects = await self.conditional_processor.detect_comprehensive_conditional_logic(
                    field_data=field_data, form_context=logic_context
                )

            field_mappings_dicts = []
            mapping_results_objects = []
            unmapped_fields = []

            for field_name, field_value in field_data.items():
                field_start_time = time.time()

                mapping_info = await self.map_field(
                    field_name=field_name,
                    field_value=field_value,
                    detected_form=detected_form, 
                    subject_context=subject_context_dict
                )

                original_path = mapping_info['cadence_path']
                
                # The path resolver should ONLY run if the mapping came from a rule-based system.
                # AI methods will have 'ai' or 'ollama' in their name. Rule-based ones won't.
                method = mapping_info.get('method', '')
                is_from_rules = 'ai' not in method and 'ollama' not in method
                
                if self.path_resolver and original_path and original_path.startswith('applicant.') and is_from_rules:
                
                    logger.info(f"Resolving dynamic path for '{field_name}' (initial: {original_path})")
                    resolution_result = self.path_resolver.resolve_path(original_path, subject_result_obj)
                    
                    # Update mapping_info with the resolved data
                    mapping_info['cadence_path'] = resolution_result.resolved_path
                    mapping_info['confidence_score'] = resolution_result.confidence * 100 # Convert 0-1 to 0-100 scale
                    mapping_info['method'] = resolution_result.resolution_method
                    
                    # Add metadata about the dynamic resolution
                    if 'metadata' not in mapping_info:
                        mapping_info['metadata'] = {}
                    mapping_info['metadata']['dynamic_subject_resolved'] = True
                    mapping_info['metadata']['resolution_details'] = asdict(resolution_result)
                    logger.info(f"Path resolved: '{original_path}' -> '{resolution_result.resolved_path}' with confidence {resolution_result.confidence}")
                
                field_processing_time = time.time() - field_start_time

                mapping_dict = {
                    "field_name": field_name,
                    "cadence_path": mapping_info['cadence_path'],
                    "confidence": mapping_info.get('confidence_score', 0.0),
                    "method": mapping_info.get('method'),
                    "metadata": {"field_value": field_value, **mapping_info.get('metadata', {})}
                }
                field_mappings_dicts.append(mapping_dict)

                mapping_obj = MappingResult(
                    field_name=field_name,
                    cadence_path=mapping_info['cadence_path'],
                    template=f"{{{{{mapping_info['cadence_path']}}}}}",
                    confidence=str(mapping_info.get('confidence_score', 0.0)),
                    field_type=FieldType.IDENTITY,
                    processing_time=field_processing_time,
                    metadata={"field_value": field_value, **mapping_info.get('metadata', {})}
                )
                mapping_results_objects.append(mapping_obj)

                if 'notes.additional_field' in mapping_dict['cadence_path']:
                    unmapped_fields.append(field_name)

            # --- STAGE 2: ADVANCED ANALYSIS ---
            cross_field_validation_results = []
            semantic_analysis_result = None
            completion_analysis_result = None

            if self.cross_field_validator:
                cross_field_validation_results = await self.cross_field_validator.validate_cross_fields(mapping_results_objects)

            if self.semantic_context_engine:
                semantic_analysis_result = await self.semantic_context_engine.analyze_semantic_context(field_data, mapping_results_objects, document_text=form_content)

            if self.form_completion_engine:
                completion_analysis_result = await self.form_completion_engine.analyze_form_completion(field_data, mapping_results_objects, form_type=detected_form)


            # --- STAGE 3: SERIALIZE ALL RESULTS ---
            conditional_rules_dicts = [asdict(rule) for rule in conditional_rules_objects]
            for rule_dict in conditional_rules_dicts:
                if isinstance(rule_dict.get('condition_type'), Enum):
                    rule_dict['condition_type'] = rule_dict['condition_type'].value
                if isinstance(rule_dict.get('confidence'), Enum):
                    rule_dict['confidence'] = rule_dict['confidence'].value

            validation_results_dict = [asdict(res) for res in cross_field_validation_results]
            if semantic_analysis_result:
                semantic_analysis_dict = asdict(semantic_analysis_result)
                # enum serialization for API
                def convert_enums_to_strings(obj):
                    if hasattr(obj, 'value'):  # It's an Enum
                        return obj.value
                    elif isinstance(obj, dict):
                        return {k: convert_enums_to_strings(v) for k, v in obj.items()}
                    elif isinstance(obj, list):
                        return [convert_enums_to_strings(item) for item in obj]
                    else:
                        return obj
                semantic_analysis_dict = convert_enums_to_strings(semantic_analysis_dict)
            else:
                semantic_analysis_dict = {}
            completion_analysis_dict = asdict(completion_analysis_result) if completion_analysis_result else {
                "overall_completion_score": 0.0,
                "form_readiness_assessment": "Analysis not performed",
                "critical_missing": [],
                "actionable_recommendations": []
            }

            quality_report = {
                "overall_score": 0.0, "quality_category": "critical", "mapping_quality": 0.0,
                "completeness_score": 0.0, "recommendations": [], "critical_issues": []
            }

            # --- STAGE 4: ASSEMBLE FINAL RESPONSE ---
            final_response = {
                "processing_metadata": { "processing_time": time.time() - start_time, "source": context.get("pdf_source", False) and "pdf" or "fields" },
                "document_analysis": {
                    "form_type": detected_form, "confidence": confidence, "category": detection_details.get("category", "unknown"),
                    "total_fields": len(field_data)
                },
                "subject_detection": subject_context_dict, ## DYNAMIC PATH RESOLUTION: Use the dictionary for the response
                "field_mappings": field_mappings_dicts,
                "conditional_logic_analysis": conditional_rules_dicts,
                "cross_field_validation": validation_results_dict,
                "semantic_context": semantic_analysis_dict,
                "completion_analysis": completion_analysis_dict,
                "quality_report": quality_report,
                "unmapped_fields": unmapped_fields
            }
            return final_response
        except Exception as e:
            logger.error(f"Enhanced form processing failed: {e}", exc_info=True)
            return {"error": f"{type(e).__name__}: {str(e)}", "processing_time": time.time() - start_time}


# All remaining functions and classes are kept
class CompleteEstateMapperAI(UniversalEstateMapper):
    def __init__(self, ollama_config=None): super().__init__(ollama_config)
async def process_universal_estate_form(field_data: Dict[str, str], **kwargs) -> Dict[str, Any]:
    mapper = UniversalEstateMapper(); return await mapper.process_form(field_data, **kwargs)
async def process_estate_document(source, **kwargs) -> Dict[str, Any]:
    mapper = UniversalEstateMapper()
    if isinstance(source, str) and source.lower().endswith('.pdf'): return await mapper.process_pdf_file(source, **kwargs)
    elif isinstance(source, dict): return await mapper.process_form(source, **kwargs)
    return {"error": "Invalid source type"}
def get_file_pattern_stats(filename: str, field_data: Dict[str, str], **kwargs) -> Dict[str, Any]:
    mapper = UniversalEstateMapper(); mapper.detect_form(field_data, **kwargs); return {}

__all__ = [
    'UniversalEstateMapper', 'CompleteEstateMapperAI', 'EstateSubjectDetector', 'PDFProcessor',
    'MappingResult', 'BatchProcessingResult', 'SubjectDetectionResult', 'SubjectEvidence',
    'ConditionalRule', 'SubjectRole', 'ConfidenceLevel', 'FieldType', 'ConditionalType',
    'PatternMatchingStats', 'PDFFieldExtraction', 'PDFFormInfo', 'ConditionalAnalysisResult',
    'process_universal_estate_form', 'process_estate_document', 'get_file_pattern_stats'
]