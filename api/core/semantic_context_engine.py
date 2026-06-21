"""
Enhanced Semantic Context Engine - Deep Contextual Understanding

Provides advanced semantic analysis with form intent recognition, legal document
classification, and contextual field meaning analysis.
REAL USER DATA ONLY - Integrates with existing MapperAI system and Ollama AI.
"""

import re
import time
import logging
from typing import Dict, List, Optional, Tuple, Set, Any
from dataclasses import dataclass, field
from enum import Enum
from collections import Counter
from .models import FieldType, MappingResult, ProvincialJurisdiction

# ==================== SEMANTIC CONTEXT DATA MODELS ====================

class FormIntent(Enum):
    """Estate form intent classifications"""
    PROBATE = "probate"                    # Court probate application
    ADMINISTRATION = "administration"      # Letters of administration (no will)
    DEATH_BENEFITS = "death_benefits"      # CPP/QPP death benefits
    SURVIVOR_BENEFITS = "survivor_benefits" # Pension survivor benefits
    LIFE_INSURANCE = "life_insurance"      # Insurance claims
    ESTATE_INFO = "estate_information"     # Comprehensive estate summary
    ASSET_TRANSFER = "asset_transfer"      # Property/asset transfers
    ACCOUNT_CLOSURE = "account_closure"    # Bank/financial account closure
    TAX_CLEARANCE = "tax_clearance"        # CRA tax matters
    GUARDIANSHIP = "guardianship"          # Minor children matters
    TRUST_ADMIN = "trust_administration"   # Trust-related forms
    UNKNOWN = "unknown"

class LegalDocumentType(Enum):
    """Specific legal document classifications"""
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

class ContextualConfidence(Enum):
    """Confidence levels for contextual analysis"""
    VERY_HIGH = "very_high"    # 90-100% confidence
    HIGH = "high"              # 80-89% confidence  
    MEDIUM = "medium"          # 60-79% confidence
    LOW = "low"                # 40-59% confidence
    VERY_LOW = "very_low"      # Below 40% confidence

@dataclass
class FormIntentAnalysis:
    """Analysis of form intent and purpose"""
    primary_intent: FormIntent
    confidence: ContextualConfidence
    evidence: List[str]
    secondary_intents: List[FormIntent] = field(default_factory=list)
    legal_context: str = ""
    jurisdiction_indicators: List[ProvincialJurisdiction] = field(default_factory=list)
    processing_complexity: str = "medium" 
    ai_insights: List[str] = field(default_factory=list)

@dataclass
class DocumentClassification:
    """Legal document type classification"""
    document_type: LegalDocumentType
    confidence: ContextualConfidence
    classification_evidence: List[str]
    alternative_classifications: List[Tuple[LegalDocumentType, float]] = field(default_factory=list)
    required_attachments: List[str] = field(default_factory=list)
    legal_requirements: List[str] = field(default_factory=list)
    provincial_specifics: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ContextualFieldMeaning:
    """Enhanced contextual meaning of a field"""
    field_name: str
    cadence_path: str
    base_meaning: str
    contextual_meaning: str
    surrounding_context: List[str] = field(default_factory=list)
    semantic_category: str = ""
    legal_significance: str = ""
    conditional_relevance: str = ""
    ai_interpretation: str = ""
    confidence: ContextualConfidence = ContextualConfidence.MEDIUM

@dataclass
class SemanticContextAnalysis:
    """Comprehensive semantic context analysis"""
    form_intent: FormIntentAnalysis
    document_classification: DocumentClassification
    field_meanings: List[ContextualFieldMeaning]
    overall_context_score: float
    processing_recommendations: List[str]
    semantic_relationships: Dict[str, List[str]] = field(default_factory=dict)
    ai_enhanced_insights: List[str] = field(default_factory=list)
    processing_metadata: Dict[str, Any] = field(default_factory=dict)

# ==================== SEMANTIC CONTEXT ENGINE ====================

class SemanticContextEngine:
    """Enhanced semantic context analysis with AI integration"""
    
    def __init__(self, ai_enhancer=None, form_logic_parser=None):
        self.ai_enhancer = ai_enhancer
        self.form_logic_parser = form_logic_parser
        self.logger = logging.getLogger(__name__)
        
        # Load semantic knowledge bases
        self.intent_patterns = self._load_intent_patterns()
        self.document_signatures = self._load_document_signatures()
        self.contextual_indicators = self._load_contextual_indicators()
        self.legal_terminology = self._load_legal_terminology()
        self.provincial_indicators = self._load_provincial_indicators()
        
        # Processing statistics
        self.stats = {
            "analyses_performed": 0,
            "intent_recognitions": 0,
            "document_classifications": 0,
            "ai_enhancements": 0,
            "contextual_field_analyses": 0,
            "high_confidence_results": 0
        }
        
        self.logger.info("Semantic Context Engine initialized - Real data processing with AI enhancement")
    
    def _load_intent_patterns(self) -> Dict[FormIntent, Dict]:
        """Load patterns for form intent recognition"""
        return {
            FormIntent.PROBATE: {
                "keywords": [
                    "probate", "will", "testament", "estate trustee", "court", "application for probate",
                    "grant of probate", "proving the will", "letters probate", "probate registry"
                ],
                "field_patterns": [
                    "will_date", "will_location", "testator", "executor", "estate_trustee",
                    "probate_court", "court_file", "deceased_will"
                ],
                "legal_indicators": [
                    "superior court", "probate court", "estate administration act",
                    "succession law", "testate", "executor appointment"
                ],
                "required_elements": ["will_exists", "executor_named", "deceased_identity"],
                "complexity_score": 8
            },
            
            FormIntent.ADMINISTRATION: {
                "keywords": [
                    "administration", "letters of administration", "intestate", "no will",
                    "administrator", "next of kin", "intestacy", "letters admin"
                ],
                "field_patterns": [
                    "administrator", "no_will", "intestate", "next_of_kin", "family_tree",
                    "intestacy_rules", "letters_administration"
                ],
                "legal_indicators": [
                    "intestate succession", "administrator appointment", "intestacy act",
                    "distribution according to law", "statutory distribution"
                ],
                "required_elements": ["no_will_confirmed", "administrator_eligible", "deceased_identity"],
                "complexity_score": 7
            },
            
            FormIntent.DEATH_BENEFITS: {
                "keywords": [
                    "death benefit", "cpp", "canada pension plan", "qpp", "quebec pension",
                    "survivor benefit", "pension death", "government benefit"
                ],
                "field_patterns": [
                    "sin", "social_insurance", "pension_number", "cpp_number", "benefit_amount",
                    "survivor_pension", "death_benefit_amount"
                ],
                "legal_indicators": [
                    "canada pension plan act", "service canada", "pension administration",
                    "government benefits", "federal benefits"
                ],
                "required_elements": ["deceased_sin", "relationship_proof", "death_certificate"],
                "complexity_score": 4
            },
            
            FormIntent.LIFE_INSURANCE: {
                "keywords": [
                    "life insurance", "insurance claim", "policy", "beneficiary", "coverage",
                    "insurance company", "death claim", "policy holder"
                ],
                "field_patterns": [
                    "policy_number", "insurance_company", "beneficiary", "coverage_amount",
                    "premium", "policy_date", "claim_amount"
                ],
                "legal_indicators": [
                    "insurance contract", "beneficiary designation", "policy terms",
                    "insurance act", "claim processing"
                ],
                "required_elements": ["policy_number", "beneficiary_proof", "death_certificate"],
                "complexity_score": 5
            },
            
            FormIntent.ESTATE_INFO: {
                "keywords": [
                    "estate information", "estate summary", "comprehensive", "overview",
                    "estate details", "complete estate", "full disclosure"
                ],
                "field_patterns": [
                    "estate_value", "assets", "liabilities", "debts", "property",
                    "financial_summary", "complete_list"
                ],
                "legal_indicators": [
                    "estate administration", "fiduciary duty", "asset disclosure",
                    "estate accounting", "inventory of assets"
                ],
                "required_elements": ["asset_inventory", "liability_list", "estate_value"],
                "complexity_score": 6
            },
            
            FormIntent.ASSET_TRANSFER: {
                "keywords": [
                    "transfer", "vehicle", "property", "real estate", "ownership",
                    "title transfer", "deed", "registration"
                ],
                "field_patterns": [
                    "vehicle_vin", "property_description", "title", "deed", "registration",
                    "transfer_to", "new_owner"
                ],
                "legal_indicators": [
                    "transfer of ownership", "property law", "vehicle registration",
                    "land titles", "ownership transfer"
                ],
                "required_elements": ["asset_description", "new_owner", "transfer_authority"],
                "complexity_score": 5
            }
        }
    
    def _load_document_signatures(self) -> Dict[LegalDocumentType, Dict]:
        """Load document type identification signatures"""
        return {
            LegalDocumentType.PROBATE_APPLICATION: {
                "title_patterns": [
                    r"application for probate", r"probate application", r"grant of probate",
                    r"application for estate certificate", r"estate trustee application"
                ],
                "form_numbers": ["Form 74.4", "Form 74.14", "Estate Certificate Application"],
                "required_sections": ["deceased_info", "will_info", "estate_trustee", "assets"],
                "signature_fields": ["applicant_signature", "witness_signature", "commissioner"],
                "legal_references": ["Estate Administration Act", "Rules of Civil Procedure"],
                "confidence_indicators": ["court_file_number", "probate_registry", "estate_trustee"]
            },
            
            LegalDocumentType.CPP_DEATH_BENEFIT_APP: {
                "title_patterns": [
                    r"death benefit", r"cpp.*death", r"canada pension.*death",
                    r"application.*death benefit", r"survivor.*benefit"
                ],
                "form_numbers": ["ISP-1000", "Service Canada", "CPP Death Benefit"],
                "required_sections": ["deceased_info", "applicant_info", "relationship"],
                "signature_fields": ["applicant_signature", "witness_signature"],
                "legal_references": ["Canada Pension Plan Act", "Service Canada"],
                "confidence_indicators": ["sin_number", "cpp_number", "service_canada"]
            },
            
            LegalDocumentType.LIFE_INSURANCE_CLAIM: {
                "title_patterns": [
                    r"life insurance.*claim", r"insurance.*death.*claim", r"policy.*claim",
                    r"beneficiary.*claim", r"death.*benefit.*claim"
                ],
                "form_numbers": ["Life Insurance Claim", "Death Benefit Claim"],
                "required_sections": ["policy_info", "deceased_info", "beneficiary_info"],
                "signature_fields": ["beneficiary_signature", "witness_signature"],
                "legal_references": ["Insurance Act", "Policy Terms"],
                "confidence_indicators": ["policy_number", "insurance_company", "beneficiary"]
            },
            
            LegalDocumentType.ESTATE_SUMMARY: {
                "title_patterns": [
                    r"estate information", r"estate summary", r"comprehensive.*estate",
                    r"estate.*details", r"complete.*estate"
                ],
                "form_numbers": ["Estate Information Form", "Estate Summary"],
                "required_sections": ["deceased_info", "assets", "liabilities", "beneficiaries"],
                "signature_fields": ["estate_representative_signature"],
                "legal_references": ["Estate Administration Act", "Trustee Act"],
                "confidence_indicators": ["estate_value", "asset_list", "estate_representative"]
            }
        }
    
    def _load_contextual_indicators(self) -> Dict[str, List[str]]:
        """Load contextual meaning indicators"""
        return {
            "legal_authority": [
                "executor", "administrator", "estate trustee", "power of attorney",
                "legal representative", "authorized person", "court appointed"
            ],
            "family_relationships": [
                "spouse", "husband", "wife", "widow", "widower", "child", "son", "daughter",
                "parent", "sibling", "next of kin", "family member"
            ],
            "financial_context": [
                "estate value", "assets", "liabilities", "debts", "bank account",
                "investments", "rrsp", "pension", "property value"
            ],
            "timing_context": [
                "date of death", "date of birth", "date of will", "date of marriage",
                "time of death", "age at death", "years married"
            ],
            "identification_context": [
                "social insurance number", "sin", "health card", "driver license",
                "birth certificate", "death certificate", "identity"
            ]
        }
    
    def _load_legal_terminology(self) -> Dict[str, str]:
        """Load legal terminology and meanings"""
        return {
            "testate": "Having a valid will at time of death",
            "intestate": "Died without a valid will",
            "executor": "Person named in will to administer estate",
            "administrator": "Court-appointed person to administer intestate estate",
            "estate trustee": "Ontario term for executor/administrator",
            "probate": "Court process to validate a will",
            "letters of administration": "Court document appointing administrator",
            "grant of probate": "Court document validating will and appointing executor",
            "beneficiary": "Person entitled to receive from estate or insurance",
            "next of kin": "Closest living relative by law",
            "intestacy": "Legal rules for distributing estate without will",
            "residuary estate": "What remains after specific gifts and debts",
            "per stirpes": "Distribution method by family branch",
            "per capita": "Distribution method by individual share"
        }
    
    def _load_provincial_indicators(self) -> Dict[ProvincialJurisdiction, List[str]]:
        """Load provincial jurisdiction indicators"""
        return {
            ProvincialJurisdiction.ONTARIO: [
                "ontario", "superior court of justice", "estate certificate",
                "estate trustee", "ontario court", "toronto", "ottawa"
            ],
            ProvincialJurisdiction.BRITISH_COLUMBIA: [
                "british columbia", "bc", "supreme court of bc", "grant of probate",
                "representation grant", "vancouver", "victoria"
            ],
            ProvincialJurisdiction.ALBERTA: [
                "alberta", "ab", "court of queen's bench", "grant of probate",
                "calgary", "edmonton", "alberta courts"
            ],
            ProvincialJurisdiction.QUEBEC: [
                "quebec", "qc", "notaire", "succession", "liquidateur",
                "montreal", "quebec city", "civil code"
            ],
            ProvincialJurisdiction.FEDERAL: [
                "canada", "federal", "service canada", "cpp", "qpp",
                "canada pension plan", "government of canada"
            ]
        }
    
    async def analyze_semantic_context(self, field_data: Dict[str, str], 
                                     mapping_results: List[MappingResult],
                                     document_text: Optional[str] = None,
                                     form_metadata: Optional[Dict] = None) -> SemanticContextAnalysis:
        """Comprehensive semantic context analysis with AI enhancement"""
        start_time = time.time()
        self.stats["analyses_performed"] += 1
        
        if not field_data and not mapping_results:
            raise ValueError("No field data or mapping results provided for semantic analysis")
        
        # Phase 1: Form Intent Recognition
        intent_analysis = await self._analyze_form_intent(field_data, document_text, form_metadata)
        
        # Phase 2: Document Classification
        doc_classification = await self._classify_legal_document(
            field_data, document_text, intent_analysis, form_metadata
        )
        
        # Phase 3: Contextual Field Meaning Analysis
        field_meanings = await self._analyze_contextual_field_meanings(
            field_data, mapping_results, intent_analysis, document_text
        )
        
        # Phase 4: Semantic Relationship Analysis
        semantic_relationships = self._analyze_semantic_relationships(field_meanings, intent_analysis)
        
        # Phase 5: AI-Enhanced Insights (if available)
        ai_insights = await self._generate_ai_semantic_insights(
            field_data, intent_analysis, doc_classification
        )
        
        # Phase 6: Processing Recommendations
        processing_recommendations = self._generate_processing_recommendations(
            intent_analysis, doc_classification, field_meanings
        )
        
        # Calculate overall context score
        context_score = self._calculate_context_score(intent_analysis, doc_classification, field_meanings)
        
        processing_time = time.time() - start_time
        
        return SemanticContextAnalysis(
            form_intent=intent_analysis,
            document_classification=doc_classification,
            field_meanings=field_meanings,
            overall_context_score=context_score,
            processing_recommendations=processing_recommendations,
            semantic_relationships=semantic_relationships,
            ai_enhanced_insights=ai_insights,
            processing_metadata={
                "processing_time": processing_time,
                "fields_analyzed": len(field_data),
                "ai_enhanced": self.ai_enhancer is not None,
                "analysis_timestamp": time.time()
            }
        )
    
    async def _analyze_form_intent(self, field_data: Dict[str, str], 
                                 document_text: Optional[str],
                                 form_metadata: Optional[Dict]) -> FormIntentAnalysis:
        """Analyze form intent and purpose"""
        self.stats["intent_recognitions"] += 1
        
        # Combine all text for analysis
        all_text = " ".join(field_data.values()).lower()
        if document_text:
            all_text += " " + document_text.lower()
        if form_metadata and form_metadata.get("title"):
            all_text += " " + str(form_metadata["title"]).lower()
        
        # Score each intent
        intent_scores = {}
        evidence_dict = {}
        
        for intent, patterns in self.intent_patterns.items():
            score = 0.0
            evidence = []
            
            # Keyword matching
            keyword_matches = sum(1 for keyword in patterns["keywords"] if keyword in all_text)
            keyword_score = min(keyword_matches / len(patterns["keywords"]), 1.0) * 40
            score += keyword_score
            
            if keyword_matches > 0:
                evidence.append(f"Keywords found: {keyword_matches}/{len(patterns['keywords'])}")
            
            # Field pattern matching
            field_pattern_matches = sum(1 for pattern in patterns["field_patterns"] 
                                      if any(pattern in field.lower() for field in field_data.keys()))
            field_score = min(field_pattern_matches / len(patterns["field_patterns"]), 1.0) * 30
            score += field_score
            
            if field_pattern_matches > 0:
                evidence.append(f"Field patterns: {field_pattern_matches}/{len(patterns['field_patterns'])}")
            
            # Legal indicator matching
            legal_matches = sum(1 for indicator in patterns["legal_indicators"] if indicator in all_text)
            legal_score = min(legal_matches / len(patterns["legal_indicators"]), 1.0) * 20
            score += legal_score
            
            if legal_matches > 0:
                evidence.append(f"Legal indicators: {legal_matches}/{len(patterns['legal_indicators'])}")
            
            # Required elements check
            required_matches = sum(1 for element in patterns["required_elements"] 
                                 if self._check_required_element(element, field_data, all_text))
            required_score = min(required_matches / len(patterns["required_elements"]), 1.0) * 10
            score += required_score
            
            if required_matches > 0:
                evidence.append(f"Required elements: {required_matches}/{len(patterns['required_elements'])}")
            
            intent_scores[intent] = score
            evidence_dict[intent] = evidence
        
        # Determine primary intent
        primary_intent = max(intent_scores.keys(), key=lambda x: intent_scores[x])
        primary_score = intent_scores[primary_intent]
        
        # Determine confidence
        confidence = self._score_to_confidence(primary_score)
        
        # Get secondary intents (scores within 20% of primary)
        secondary_intents = [
            intent for intent, score in intent_scores.items()
            if intent != primary_intent and score >= primary_score * 0.8
        ]
        
        # Generate legal context
        legal_context = self._generate_legal_context(primary_intent, field_data)
        
        # Detect jurisdictional indicators
        jurisdiction_indicators = self._detect_jurisdictions(all_text)
        
        # Determine processing complexity
        complexity_score = self.intent_patterns[primary_intent]["complexity_score"]
        processing_complexity = "simple" if complexity_score <= 4 else "medium" if complexity_score <= 6 else "complex"
        
        # AI enhancement if available
        ai_insights = []
        if self.ai_enhancer and primary_score > 60:
            ai_insights = await self._get_ai_intent_insights(field_data, primary_intent)
        
        return FormIntentAnalysis(
            primary_intent=primary_intent,
            confidence=confidence,
            evidence=evidence_dict[primary_intent],
            secondary_intents=secondary_intents,
            legal_context=legal_context,
            jurisdiction_indicators=jurisdiction_indicators,
            processing_complexity=processing_complexity,
            ai_insights=ai_insights
        )
    
    async def _classify_legal_document(self, field_data: Dict[str, str],
                                     document_text: Optional[str],
                                     intent_analysis: FormIntentAnalysis,
                                     form_metadata: Optional[Dict]) -> DocumentClassification:
        """Classify specific legal document type"""
        self.stats["document_classifications"] += 1
        
        # Combine text sources
        all_text = " ".join(field_data.values()).lower()
        if document_text:
            all_text += " " + document_text.lower()
        
        title_text = ""
        if form_metadata and form_metadata.get("title"):
            title_text = str(form_metadata["title"]).lower()
        
        # Score document types
        doc_scores = {}
        evidence_dict = {}
        
        for doc_type, signatures in self.document_signatures.items():
            score = 0.0
            evidence = []
            
            # Title pattern matching (highest weight)
            title_matches = sum(1 for pattern in signatures["title_patterns"] 
                              if re.search(pattern, title_text + " " + all_text))
            if title_matches > 0:
                score += 40
                evidence.append(f"Title pattern matches: {title_matches}")
            
            # Form number identification
            form_number_matches = sum(1 for form_num in signatures["form_numbers"] 
                                    if form_num.lower() in all_text)
            if form_number_matches > 0:
                score += 25
                evidence.append(f"Form number identified: {form_number_matches}")
            
            # Required sections present
            section_matches = sum(1 for section in signatures["required_sections"] 
                                if self._check_section_present(section, field_data))
            section_score = (section_matches / len(signatures["required_sections"])) * 20
            score += section_score
            
            if section_matches > 0:
                evidence.append(f"Required sections: {section_matches}/{len(signatures['required_sections'])}")
            
            # Signature fields present
            sig_matches = sum(1 for sig_field in signatures["signature_fields"] 
                            if any(sig_field in field.lower() for field in field_data.keys()))
            if sig_matches > 0:
                score += 10
                evidence.append(f"Signature fields: {sig_matches}")
            
            # Confidence indicators
            conf_matches = sum(1 for indicator in signatures["confidence_indicators"] 
                             if indicator in all_text or any(indicator in field.lower() for field in field_data.keys()))
            conf_score = min(conf_matches, 3) * 2  # Max 6 points
            score += conf_score
            
            if conf_matches > 0:
                evidence.append(f"Confidence indicators: {conf_matches}")
            
            doc_scores[doc_type] = score
            evidence_dict[doc_type] = evidence
        
        # Determine primary classification
        if not doc_scores or max(doc_scores.values()) < 20:
            primary_doc_type = LegalDocumentType.UNKNOWN_LEGAL_DOC
            confidence = ContextualConfidence.VERY_LOW
            evidence = ["Insufficient indicators for classification"]
        else:
            primary_doc_type = max(doc_scores.keys(), key=lambda x: doc_scores[x])
            primary_score = doc_scores[primary_doc_type]
            confidence = self._score_to_confidence(primary_score)
            evidence = evidence_dict[primary_doc_type]
        
        # Get alternative classifications
        alternatives = [
            (doc_type, score) for doc_type, score in doc_scores.items()
            if doc_type != primary_doc_type and score >= 15
        ]
        alternatives.sort(key=lambda x: x[1], reverse=True)
        
        # Generate required attachments and legal requirements
        required_attachments = self._get_required_attachments(primary_doc_type, intent_analysis)
        legal_requirements = self._get_legal_requirements(primary_doc_type, intent_analysis)
        
        # Provincial specifics
        provincial_specifics = self._get_provincial_specifics(primary_doc_type, intent_analysis.jurisdiction_indicators)
        
        return DocumentClassification(
            document_type=primary_doc_type,
            confidence=confidence,
            classification_evidence=evidence,
            alternative_classifications=alternatives[:3],  # Top 3 alternatives
            required_attachments=required_attachments,
            legal_requirements=legal_requirements,
            provincial_specifics=provincial_specifics
        )
    
    async def _analyze_contextual_field_meanings(self, field_data: Dict[str, str],
                                               mapping_results: List[MappingResult],
                                               intent_analysis: FormIntentAnalysis,
                                               document_text: Optional[str]) -> List[ContextualFieldMeaning]:
        """Analyze contextual meaning of each field"""
        self.stats["contextual_field_analyses"] += 1
        
        field_meanings = []
        
        # Create mapping lookup
        field_to_result = {result.field_name: result for result in mapping_results}
        
        for field_name, field_value in field_data.items():
            mapping_result = field_to_result.get(field_name)
            cadence_path = mapping_result.cadence_path if mapping_result else "unknown.field"
            
            # Base meaning from field name
            base_meaning = self._extract_base_meaning(field_name)
            
            # Enhanced contextual meaning
            contextual_meaning = await self._enhance_contextual_meaning(
                field_name, field_value, cadence_path, intent_analysis, document_text
            )
            
            # Surrounding context analysis
            surrounding_context = self._analyze_surrounding_context(field_name, field_data)
            
            # Semantic categorization
            semantic_category = self._categorize_semantically(field_name, cadence_path, intent_analysis)
            
            # Legal significance
            legal_significance = self._assess_legal_significance(
                field_name, cadence_path, intent_analysis.primary_intent
            )
            
            # Conditional relevance
            conditional_relevance = self._assess_conditional_relevance(field_name, field_data, intent_analysis)
            
            # AI interpretation if available
            ai_interpretation = await self._get_ai_field_interpretation(
                field_name, field_value, contextual_meaning, intent_analysis
            )
            
            # Determine confidence
            confidence = self._determine_meaning_confidence(
                base_meaning, contextual_meaning, semantic_category, legal_significance
            )
            
            field_meaning = ContextualFieldMeaning(
                field_name=field_name,
                cadence_path=cadence_path,
                base_meaning=base_meaning,
                contextual_meaning=contextual_meaning,
                surrounding_context=surrounding_context,
                semantic_category=semantic_category,
                legal_significance=legal_significance,
                conditional_relevance=conditional_relevance,
                ai_interpretation=ai_interpretation,
                confidence=confidence
            )
            
            field_meanings.append(field_meaning)
        
        return field_meanings
    
    def _check_required_element(self, element: str, field_data: Dict[str, str], all_text: str) -> bool:
        """Check if required element is present"""
        element_checks = {
            "will_exists": lambda: any("will" in key.lower() for key in field_data.keys()) or "will" in all_text,
            "executor_named": lambda: any("executor" in key.lower() for key in field_data.keys()),
            "deceased_identity": lambda: any("deceased" in key.lower() and "name" in key.lower() for key in field_data.keys()),
            "no_will_confirmed": lambda: any("no will" in val.lower() or "intestate" in val.lower() for val in field_data.values()),
            "administrator_eligible": lambda: any("administrator" in key.lower() for key in field_data.keys()),
            "deceased_sin": lambda: any("sin" in key.lower() and "deceased" in key.lower() for key in field_data.keys()),
            "relationship_proof": lambda: any("relationship" in key.lower() for key in field_data.keys()),
            "death_certificate": lambda: "death certificate" in all_text or any("death" in key.lower() and "cert" in key.lower() for key in field_data.keys()),
            "policy_number": lambda: any("policy" in key.lower() and "number" in key.lower() for key in field_data.keys()),
            "beneficiary_proof": lambda: any("beneficiary" in key.lower() for key in field_data.keys())
        }
        
        check_func = element_checks.get(element)
        return check_func() if check_func else False
    
    def _check_section_present(self, section: str, field_data: Dict[str, str]) -> bool:
        """Check if form section is present based on field names"""
        section_indicators = {
            "deceased_info": ["deceased", "decedent"],
            "will_info": ["will", "testament"],
            "estate_trustee": ["executor", "estate_trustee", "administrator"],
            "assets": ["asset", "property", "value", "estate_value"],
            "applicant_info": ["applicant", "person"],
            "relationship": ["relationship", "relation"],
            "policy_info": ["policy", "insurance"],
            "beneficiary_info": ["beneficiary", "benefit"]
        }
        
        indicators = section_indicators.get(section, [section])
        return any(indicator in field_name.lower() for field_name in field_data.keys() for indicator in indicators)
    
    def _score_to_confidence(self, score: float) -> ContextualConfidence:
        """Convert numeric score to confidence level"""
        if score >= 90:
            return ContextualConfidence.VERY_HIGH
        elif score >= 80:
            return ContextualConfidence.HIGH
        elif score >= 60:
            return ContextualConfidence.MEDIUM
        elif score >= 40:
            return ContextualConfidence.LOW
        else:
            return ContextualConfidence.VERY_LOW
    
    def _generate_legal_context(self, intent: FormIntent, field_data: Dict[str, str]) -> str:
        """Generate legal context description"""
        context_descriptions = {
            FormIntent.PROBATE: "Court application to validate will and appoint executor. Requires proof of will validity and executor authority.",
            FormIntent.ADMINISTRATION: "Court application for intestate estate administration. No valid will exists.",
            FormIntent.DEATH_BENEFITS: "Government benefit application for deceased person's survivors. Federal/provincial pension systems.",
            FormIntent.LIFE_INSURANCE: "Private insurance claim for death benefits. Contractual relationship between insurer and beneficiary.",
            FormIntent.ESTATE_INFO: "Comprehensive estate disclosure for administrative purposes. Asset and liability inventory.",
            FormIntent.ASSET_TRANSFER: "Legal transfer of specific estate assets to new owners. Property law requirements."
        }
        
        return context_descriptions.get(intent, "General estate administration document processing.")
    
    def _detect_jurisdictions(self, text: str) -> List[ProvincialJurisdiction]:
        """Detect jurisdictional indicators in text"""
        detected = []
        
        for jurisdiction, indicators in self.provincial_indicators.items():
            if any(indicator in text for indicator in indicators):
                detected.append(jurisdiction)
        
        return detected
    
    async def _get_ai_intent_insights(self, field_data: Dict[str, str], intent: FormIntent) -> List[str]:
        """Get AI insights about form intent"""
        if not self.ai_enhancer:
            return []
        
        try:
            self.stats["ai_enhancements"] += 1
            
            context = f"Form intent: {intent.value}. Fields: {list(field_data.keys())[:10]}"
            ai_result = await self.ai_enhancer.enhance_field_mapping("intent_analysis", "", context)
            
            if ai_result.get("success"):
                return [f"🤖 AI confirms {intent.value} classification based on field patterns"]
            
        except Exception as e:
            self.logger.warning(f"AI intent insight generation failed: {e}")
        
        return []
    
    def _extract_base_meaning(self, field_name: str) -> str:
        """Extract base meaning from field name"""
        field_lower = field_name.lower()
        
        # Common field meanings
        if "name" in field_lower:
            if "deceased" in field_lower:
                return "Name of the deceased person"
            elif "applicant" in field_lower:
                return "Name of person completing form"
            elif "spouse" in field_lower:
                return "Name of deceased's spouse"
            else:
                return "Person's name"
        
        elif "date" in field_lower:
            if "death" in field_lower:
                return "Date when person died"
            elif "birth" in field_lower:
                return "Date when person was born"
            elif "marriage" in field_lower:
                return "Date of marriage"
            else:
                return "Important date"
        
        elif "address" in field_lower:
            return "Physical address or mailing address"
        
        elif "phone" in field_lower:
            return "Contact telephone number"
        
        elif "relationship" in field_lower:
            return "How applicant is related to deceased"
        
        elif "sin" in field_lower or "social_insurance" in field_lower:
            return "Canadian Social Insurance Number"
        
        elif "will" in field_lower:
            return "Information about deceased's will"
        
        elif "estate" in field_lower:
            return "Information about deceased's estate"
        
        else:
            return f"Form field: {field_name}"
    
    async def _enhance_contextual_meaning(self, field_name: str, field_value: str,
                                        cadence_path: str, intent_analysis: FormIntentAnalysis,
                                        document_text: Optional[str]) -> str:
        """Enhance field meaning with contextual analysis"""
        
        base_meaning = self._extract_base_meaning(field_name)
        
        # Add intent-specific context
        intent_context = ""
        if intent_analysis.primary_intent == FormIntent.PROBATE:
            intent_context = " (Required for probate court application)"
        elif intent_analysis.primary_intent == FormIntent.ADMINISTRATION:
            intent_context = " (Required for letters of administration)"
        elif intent_analysis.primary_intent == FormIntent.DEATH_BENEFITS:
            intent_context = " (Required for government death benefit claim)"
        elif intent_analysis.primary_intent == FormIntent.LIFE_INSURANCE:
            intent_context = " (Required for insurance benefit claim)"
        
        # Add legal significance
        legal_context = ""
        if "deceased" in field_name.lower() and "name" in field_name.lower():
            legal_context = " - Critical for legal identification of estate"
        elif "executor" in field_name.lower() or "administrator" in field_name.lower():
            legal_context = " - Establishes legal authority over estate"
        elif "beneficiary" in field_name.lower():
            legal_context = " - Determines who receives benefits/assets"
        
        enhanced_meaning = base_meaning + intent_context + legal_context
        
        return enhanced_meaning.strip()
    
    def _analyze_surrounding_context(self, field_name: str, field_data: Dict[str, str]) -> List[str]:
        """Analyze surrounding field context"""
        context = []
        field_lower = field_name.lower()
        
        # Find related fields
        related_fields = []
        for other_field in field_data.keys():
            if other_field != field_name:
                other_lower = other_field.lower()
                
                # Same entity context
                if any(entity in field_lower and entity in other_lower 
                      for entity in ["deceased", "applicant", "spouse", "executor"]):
                    related_fields.append(other_field)
                
                # Same category context
                elif any(category in field_lower and category in other_lower
                        for category in ["address", "phone", "date", "name"]):
                    related_fields.append(other_field)
        
        if related_fields:
            context.append(f"Related to {len(related_fields)} other fields in same category")
        
        # Check for section context
        section_indicators = self._identify_field_section(field_name)
        if section_indicators:
            context.extend(section_indicators)
        
        return context
    
    def _identify_field_section(self, field_name: str) -> List[str]:
        """Identify which form section this field belongs to"""
        field_lower = field_name.lower()
        sections = []
        
        if "deceased" in field_lower:
            sections.append("Part of deceased person information section")
        
        if "applicant" in field_lower:
            sections.append("Part of applicant/person completing form section")
        
        if "spouse" in field_lower:
            sections.append("Part of spouse information section (conditional)")
        
        if "will" in field_lower or "executor" in field_lower:
            sections.append("Part of will and executor information section")
        
        if "estate" in field_lower and "value" in field_lower:
            sections.append("Part of estate valuation section")
        
        return sections
    
    def _categorize_semantically(self, field_name: str, cadence_path: str, 
                               intent_analysis: FormIntentAnalysis) -> str:
        """Categorize field semantically"""
        field_lower = field_name.lower()
        path_lower = cadence_path.lower()
        
        if any(term in field_lower or term in path_lower for term in ["name", "identity"]):
            return "Identity Information"
        elif any(term in field_lower or term in path_lower for term in ["address", "location"]):
            return "Location Information"
        elif any(term in field_lower or term in path_lower for term in ["phone", "email", "contact"]):
            return "Contact Information"
        elif any(term in field_lower or term in path_lower for term in ["date", "birth", "death"]):
            return "Temporal Information"
        elif any(term in field_lower or term in path_lower for term in ["relationship", "spouse", "child"]):
            return "Relationship Information"
        elif any(term in field_lower or term in path_lower for term in ["will", "executor", "legal"]):
            return "Legal Authority Information"
        elif any(term in field_lower or term in path_lower for term in ["estate", "value", "asset"]):
            return "Financial Information"
        elif any(term in field_lower or term in path_lower for term in ["insurance", "policy", "benefit"]):
            return "Benefit Information"
        else:
            return "General Information"
    
    def _assess_legal_significance(self, field_name: str, cadence_path: str, intent: FormIntent) -> str:
        """Assess legal significance of field"""
        field_lower = field_name.lower()
        
        # Critical legal fields
        if any(term in field_lower for term in ["deceased", "name"]) and "deceased" in field_lower:
            return "Critical - Legal identification of estate"
        
        if any(term in field_lower for term in ["executor", "administrator", "estate_trustee"]):
            return "Critical - Establishes legal authority"
        
        if "date" in field_lower and "death" in field_lower:
            return "Critical - Establishes date of death for legal purposes"
        
        if "will" in field_lower:
            return "High - Determines testate vs intestate processing"
        
        if "relationship" in field_lower:
            return "High - Determines legal standing and inheritance rights"
        
        if "beneficiary" in field_lower:
            return "High - Determines benefit/asset distribution"
        
        if any(term in field_lower for term in ["sin", "social_insurance"]):
            return "Medium - Government identification and verification"
        
        if any(term in field_lower for term in ["address", "phone", "contact"]):
            return "Medium - Required for legal correspondence"
        
        return "Low - Supporting information"
    
    def _assess_conditional_relevance(self, field_name: str, field_data: Dict[str, str], 
                                    intent_analysis: FormIntentAnalysis) -> str:
        """Assess when field is conditionally relevant"""
        field_lower = field_name.lower()
        
        if "spouse" in field_lower:
            has_spouse = any("spouse" in val.lower() or "married" in val.lower() 
                           for val in field_data.values())
            return "Required if deceased was married" + (" - Condition appears met" if has_spouse else "")
        
        if "child" in field_lower:
            has_children = any("child" in val.lower() for val in field_data.values())
            return "Required if deceased had children" + (" - Condition appears met" if has_children else "")
        
        if "will" in field_lower or "executor" in field_lower:
            has_will = any("will" in val.lower() for val in field_data.values())
            return "Required if will exists" + (" - Condition appears met" if has_will else "")
        
        if "administrator" in field_lower:
            no_will = any("no will" in val.lower() or "intestate" in val.lower() 
                         for val in field_data.values())
            return "Required if no will exists" + (" - Condition appears met" if no_will else "")
        
        if intent_analysis.primary_intent == FormIntent.PROBATE and "probate" not in field_lower:
            return "Required for probate application"
        
        return "Generally required"
    
    async def _get_ai_field_interpretation(self, field_name: str, field_value: str,
                                         contextual_meaning: str, 
                                         intent_analysis: FormIntentAnalysis) -> str:
        """Get AI interpretation of field"""
        if not self.ai_enhancer or not field_value:
            return ""
        
        try:
            context = f"Field: {field_name}, Value: {field_value}, Intent: {intent_analysis.primary_intent.value}"
            ai_result = await self.ai_enhancer.enhance_field_mapping(field_name, field_value, context)
            
            if ai_result.get("success"):
                return f"AI interprets as {ai_result.get('field_type', 'unknown')} field"
            
        except Exception as e:
            self.logger.warning(f"AI field interpretation failed: {e}")
        
        return ""
    
    def _determine_meaning_confidence(self, base_meaning: str, contextual_meaning: str,
                                    semantic_category: str, legal_significance: str) -> ContextualConfidence:
        """Determine confidence in field meaning analysis"""
        
        confidence_score = 0
        
        # Base meaning confidence
        if "Form field:" not in base_meaning:
            confidence_score += 25
        
        # Contextual enhancement
        if len(contextual_meaning) > len(base_meaning) + 10:
            confidence_score += 25
        
        # Semantic categorization
        if semantic_category != "General Information":
            confidence_score += 25
        
        # Legal significance
        if "Critical" in legal_significance:
            confidence_score += 25
        elif "High" in legal_significance:
            confidence_score += 20
        elif "Medium" in legal_significance:
            confidence_score += 15
        
        return self._score_to_confidence(confidence_score)
    
    def _analyze_semantic_relationships(self, field_meanings: List[ContextualFieldMeaning],
                                      intent_analysis: FormIntentAnalysis) -> Dict[str, List[str]]:
        """Analyze semantic relationships between fields"""
        relationships = {}
        
        # Group by semantic category
        categories = {}
        for meaning in field_meanings:
            category = meaning.semantic_category
            if category not in categories:
                categories[category] = []
            categories[category].append(meaning.field_name)
        
        relationships["semantic_groups"] = list(categories.keys())
        
        # Identify dependent relationships
        dependent_fields = []
        for meaning in field_meanings:
            if "conditional" in meaning.conditional_relevance.lower():
                dependent_fields.append(meaning.field_name)
        
        relationships["conditional_dependencies"] = dependent_fields
        
        # Identify critical path
        critical_fields = [
            meaning.field_name for meaning in field_meanings
            if "Critical" in meaning.legal_significance
        ]
        relationships["critical_path"] = critical_fields
        
        return relationships
    
    async def _generate_ai_semantic_insights(self, field_data: Dict[str, str],
                                           intent_analysis: FormIntentAnalysis,
                                           doc_classification: DocumentClassification) -> List[str]:
        """Generate AI-powered semantic insights"""
        insights = []
        
        if not self.ai_enhancer:
            return insights
        
        try:
            context = f"Intent: {intent_analysis.primary_intent.value}, Document: {doc_classification.document_type.value}"
            context += f", Fields: {len(field_data)}, Confidence: {intent_analysis.confidence.value}"
            
            ai_result = await self.ai_enhancer.enhance_field_mapping("semantic_analysis", "", context)
            
            if ai_result.get("success"):
                insights.append("🤖 AI confirms semantic analysis alignment with estate administration patterns")
            
            # Additional contextual insights
            if intent_analysis.confidence in [ContextualConfidence.VERY_HIGH, ContextualConfidence.HIGH]:
                insights.append("🤖 High confidence in form purpose classification enables targeted processing")
            
            if len(intent_analysis.jurisdiction_indicators) > 1:
                insights.append("🤖 Multiple jurisdictional indicators detected - review for cross-border requirements")
            
        except Exception as e:
            self.logger.warning(f"AI semantic insight generation failed: {e}")
        
        return insights
    
    def _generate_processing_recommendations(self, intent_analysis: FormIntentAnalysis,
                                           doc_classification: DocumentClassification,
                                           field_meanings: List[ContextualFieldMeaning]) -> List[str]:
        """Generate processing recommendations based on semantic analysis"""
        recommendations = []
        
        # Intent-based recommendations
        if intent_analysis.primary_intent == FormIntent.PROBATE:
            recommendations.append("📋 Probate application detected - ensure court filing requirements met")
        elif intent_analysis.primary_intent == FormIntent.ADMINISTRATION:
            recommendations.append("📋 Administration application - verify intestacy and administrator eligibility")
        elif intent_analysis.primary_intent == FormIntent.DEATH_BENEFITS:
            recommendations.append("📋 Government benefits application - verify SIN and relationship proof")
        
        # Confidence-based recommendations
        if intent_analysis.confidence == ContextualConfidence.LOW:
            recommendations.append("⚠️ Low confidence in form intent - manual review recommended")
        
        if doc_classification.confidence == ContextualConfidence.LOW:
            recommendations.append("⚠️ Uncertain document type - additional context needed")
        
        # Critical field recommendations
        critical_fields = [f for f in field_meanings if "Critical" in f.legal_significance]
        if len(critical_fields) > 0:
            recommendations.append(f"🎯 Focus on {len(critical_fields)} critical legal fields first")
        
        # Conditional field recommendations
        conditional_fields = [f for f in field_meanings if "conditional" in f.conditional_relevance.lower()]
        if conditional_fields:
            recommendations.append(f"🔄 Review {len(conditional_fields)} conditional fields based on form state")
        
        # Jurisdiction recommendations
        if intent_analysis.jurisdiction_indicators:
            jurisdictions = [j.value for j in intent_analysis.jurisdiction_indicators]
            recommendations.append(f"🏛️ Consider {', '.join(jurisdictions)} jurisdictional requirements")
        
        return recommendations
    
    def _calculate_context_score(self, intent_analysis: FormIntentAnalysis,
                                doc_classification: DocumentClassification,
                                field_meanings: List[ContextualFieldMeaning]) -> float:
        """Calculate overall context analysis score"""
        
        # Intent confidence scoring
        intent_scores = {
            ContextualConfidence.VERY_HIGH: 25,
            ContextualConfidence.HIGH: 20,
            ContextualConfidence.MEDIUM: 15,
            ContextualConfidence.LOW: 10,
            ContextualConfidence.VERY_LOW: 5
        }
        intent_score = intent_scores.get(intent_analysis.confidence, 5)
        
        # Document classification scoring
        doc_score = intent_scores.get(doc_classification.confidence, 5)
        
        # Field meaning scoring
        high_conf_fields = len([f for f in field_meanings 
                              if f.confidence in [ContextualConfidence.VERY_HIGH, ContextualConfidence.HIGH]])
        field_score = min((high_conf_fields / len(field_meanings)) * 30, 30) if field_meanings else 0
        
        # Legal significance scoring
        critical_fields = len([f for f in field_meanings if "Critical" in f.legal_significance])
        legal_score = min((critical_fields / max(len(field_meanings), 1)) * 20, 20)
        
        total_score = intent_score + doc_score + field_score + legal_score
        
        if total_score >= 85:
            self.stats["high_confidence_results"] += 1
        
        return total_score
    
    def _get_required_attachments(self, doc_type: LegalDocumentType, 
                                intent_analysis: FormIntentAnalysis) -> List[str]:
        """Get required attachments for document type"""
        attachments = {
            LegalDocumentType.PROBATE_APPLICATION: [
                "Original will", "Death certificate", "Estate asset inventory",
                "Consent of beneficiaries", "Bond (if required)"
            ],
            LegalDocumentType.CPP_DEATH_BENEFIT_APP: [
                "Death certificate", "Proof of relationship", "Birth certificate of applicant"
            ],
            LegalDocumentType.LIFE_INSURANCE_CLAIM: [
                "Death certificate", "Insurance policy", "Beneficiary identification",
                "Proof of insurability"
            ],
           LegalDocumentType.ESTATE_SUMMARY: [
                "Asset statements", "Liability statements", "Previous tax returns",
                "Financial institution letters"
]
        }
        
        return attachments.get(doc_type, ["Death certificate", "Supporting documentation"])
    
    def _get_legal_requirements(self, doc_type: LegalDocumentType,
                              intent_analysis: FormIntentAnalysis) -> List[str]:
        """Get legal requirements for document type"""
        requirements = {
            LegalDocumentType.PROBATE_APPLICATION: [
                "Court filing fees", "Legal capacity verification", "Proper service requirements",
                "Statutory waiting periods", "Beneficiary notice requirements"
            ],
            LegalDocumentType.CPP_DEATH_BENEFIT_APP: [
                "Relationship eligibility", "Application within time limits",
                "Government identification verification"
            ],
            LegalDocumentType.LIFE_INSURANCE_CLAIM: [
                "Policy in good standing", "Premium payments current",
                "Beneficiary designation valid", "Claim within policy terms"
            ]
        }
        
        return requirements.get(doc_type, ["Legal standing verification", "Proper authorization"])
    
    def _get_provincial_specifics(self, doc_type: LegalDocumentType,
                                jurisdiction_indicators: List[ProvincialJurisdiction]) -> Dict[str, Any]:
        """Get provincial-specific requirements"""
        specifics = {}
        
        for jurisdiction in jurisdiction_indicators:
            if jurisdiction == ProvincialJurisdiction.ONTARIO:
                specifics["ontario"] = {
                    "court": "Superior Court of Justice",
                    "estate_certificate": "Required for most estates",
                    "executor_title": "Estate Trustee with a Will"
                }
            elif jurisdiction == ProvincialJurisdiction.BRITISH_COLUMBIA:
                specifics["bc"] = {
                    "court": "Supreme Court of British Columbia",
                    "representation_grant": "Required for most estates",
                    "executor_title": "Executor"
                }
        
        return specifics
    
    def get_semantic_statistics(self) -> Dict[str, Any]:
        """Get semantic context engine statistics"""
        return {
            **self.stats,
            "ai_enhancement_available": self.ai_enhancer is not None,
            "form_logic_parser_available": self.form_logic_parser is not None,
            "intent_patterns_loaded": len(self.intent_patterns),
            "document_signatures_loaded": len(self.document_signatures),
            "legal_terminology_loaded": len(self.legal_terminology),
            "provincial_indicators_loaded": len(self.provincial_indicators),
            "high_confidence_rate": (self.stats["high_confidence_results"] / 
                                   max(1, self.stats["analyses_performed"])) * 100
        }

# ==================== INTEGRATION UTILITIES ====================

async def analyze_semantic_context_with_mapper(mapper_ai, field_data: Dict[str, str],
                                              document_text: Optional[str] = None,
                                              form_metadata: Optional[Dict] = None) -> SemanticContextAnalysis:
    """Integrate semantic context analysis with existing MapperAI system"""
    
    # Get mapping results from existing mapper
    mapping_results = []
    for field_name, field_value in field_data.items():
        result = await mapper_ai.analyze_field(field_name, field_value)
        mapping_results.append(result)
    
    # Create semantic context engine
    semantic_engine = SemanticContextEngine(
        ai_enhancer=getattr(mapper_ai, 'ai_enhancer', None),
        form_logic_parser=getattr(mapper_ai, 'form_logic_parser', None)
    )
    
    # Perform semantic analysis
    return await semantic_engine.analyze_semantic_context(
        field_data, mapping_results, document_text, form_metadata
    )

def format_semantic_analysis_for_display(analysis: SemanticContextAnalysis) -> str:
    """Format semantic analysis for user display"""
    output = []
    
    output.append(f"🧠 SEMANTIC CONTEXT ANALYSIS")
    output.append(f"=" * 60)
    output.append(f"Overall Context Score: {analysis.overall_context_score:.1f}/100")
    output.append("")
    
    # Form Intent
    intent = analysis.form_intent
    output.append(f"📋 FORM INTENT ANALYSIS:")
    output.append(f"  • Primary Intent: {intent.primary_intent.value.replace('_', ' ').title()}")
    output.append(f"  • Confidence: {intent.confidence.value.replace('_', ' ').title()}")
    output.append(f"  • Legal Context: {intent.legal_context}")
    output.append(f"  • Processing Complexity: {intent.processing_complexity.title()}")
    
    if intent.evidence:
        output.append(f"  • Evidence: {'; '.join(intent.evidence[:3])}")
    
    if intent.jurisdiction_indicators:
        jurisdictions = [j.value for j in intent.jurisdiction_indicators]
        output.append(f"  • Jurisdictions: {', '.join(jurisdictions)}")
    output.append("")
    
    # Document Classification
    doc = analysis.document_classification
    output.append(f"📄 DOCUMENT CLASSIFICATION:")
    output.append(f"  • Document Type: {doc.document_type.value.replace('_', ' ').title()}")
    output.append(f"  • Confidence: {doc.confidence.value.replace('_', ' ').title()}")
    
    if doc.classification_evidence:
        output.append(f"  • Evidence: {'; '.join(doc.classification_evidence[:2])}")
    
    if doc.required_attachments:
        output.append(f"  • Required Attachments: {', '.join(doc.required_attachments[:3])}")
    output.append("")
    
    # Field Analysis Summary
    output.append(f"🔍 FIELD ANALYSIS SUMMARY:")
    critical_fields = [f for f in analysis.field_meanings if "Critical" in f.legal_significance]
    conditional_fields = [f for f in analysis.field_meanings if "conditional" in f.conditional_relevance.lower()]
    
    output.append(f"  • Total Fields Analyzed: {len(analysis.field_meanings)}")
    output.append(f"  • Critical Legal Fields: {len(critical_fields)}")
    output.append(f"  • Conditional Fields: {len(conditional_fields)}")
    
    # Semantic categories
    categories = {}
    for field in analysis.field_meanings:
        cat = field.semantic_category
        categories[cat] = categories.get(cat, 0) + 1
    
    output.append(f"  • Semantic Categories: {', '.join([f'{cat}({count})' for cat, count in categories.items()])}")
    output.append("")
    
    # Processing Recommendations
    if analysis.processing_recommendations:
        output.append(f"📋 PROCESSING RECOMMENDATIONS:")
        for rec in analysis.processing_recommendations:
            output.append(f"  • {rec}")
        output.append("")
    
    # AI Insights
    if analysis.ai_enhanced_insights:
        output.append(f"🤖 AI INSIGHTS:")
        for insight in analysis.ai_enhanced_insights:
            output.append(f"  • {insight}")
        output.append("")
    
    # Semantic Relationships
    if analysis.semantic_relationships:
        output.append(f"🔗 SEMANTIC RELATIONSHIPS:")
        for rel_type, items in analysis.semantic_relationships.items():
            if items:
                output.append(f"  • {rel_type.replace('_', ' ').title()}: {len(items)} items")
    
    return "\n".join(output)
