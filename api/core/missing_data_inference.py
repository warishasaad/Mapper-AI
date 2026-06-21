"""
Missing Data Inference Engine

Intelligent inference of missing required data from available information
using logical rules, Canadian estate law requirements, and AI assistance.
"""

import logging
import re
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

from .models import (
    DataInference, MissingDataAnalysis, ProvincialJurisdiction,
    FieldType, MappingResult
)

@dataclass
class InferenceRule:
    """Rule for data inference"""
    rule_id: str
    source_fields: List[str]
    target_field: str
    inference_logic: str
    confidence_level: float
    requires_validation: bool = True
    description: str = ""

@dataclass
class RequiredFieldSpec:
    """Specification for required field"""
    field_name: str
    cadence_path: str
    required_for_forms: List[str]
    required_for_jurisdictions: List[ProvincialJurisdiction]
    criticality: str  # 'critical', 'important', 'helpful'
    validation_rules: List[str]

class MissingDataInferenceEngine:
    """Engine for intelligent missing data inference"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.inference_rules = self._load_inference_rules()
        self.required_fields = self._load_required_fields()
        self.relationship_inference = self._load_relationship_inference()
        self.estate_requirements = self._load_estate_requirements()
        
        self.logger.info("Missing Data Inference Engine initialized")
    
    def _load_inference_rules(self) -> List[InferenceRule]:
        """Load comprehensive inference rules"""
        
        return [
            # Age and date calculations
            InferenceRule(
                rule_id="AGE_FROM_BIRTH_DEATH",
                source_fields=["deceased.date_of_birth", "deceased.date_of_death"],
                target_field="deceased.age_at_death",
                inference_logic="calculate_age(birth_date, death_date)",
                confidence_level=0.95,
                description="Calculate age at death from birth and death dates"
            ),
            
            # Relationship inferences
            InferenceRule(
                rule_id="SPOUSE_ADDRESS_SAME",
                source_fields=["deceased.home_address", "applicant.relationship_to_deceased"],
                target_field="spouse.address",
                inference_logic="relationship == 'spouse' AND same_address_likely",
                confidence_level=0.7,
                description="Infer spouse address same as deceased if living together"
            ),
            
            InferenceRule(
                rule_id="CHILD_LAST_NAME",
                source_fields=["deceased.name", "applicant.relationship_to_deceased"],
                target_field="children[*].name",
                inference_logic="relationship == 'child' AND same_last_name_likely",
                confidence_level=0.6,
                description="Infer child may have same last name as deceased parent"
            ),
            
            # Estate value inferences
            InferenceRule(
                rule_id="ESTATE_VALUE_FROM_ASSETS",
                source_fields=["property[*].estimated_value", "financial_information[*].balance"],
                target_field="estate.total_value",
                inference_logic="sum_all_assets()",
                confidence_level=0.8,
                description="Calculate estate value from sum of known assets"
            ),
            
            # Tax and benefit eligibility
            InferenceRule(
                rule_id="CPP_ELIGIBILITY_AGE",
                source_fields=["deceased.age_at_death", "deceased.employment.status"],
                target_field="task_planner.b_cpp_eligible",
                inference_logic="age >= 60 OR (age >= 18 AND employed)",
                confidence_level=0.9,
                description="Infer CPP death benefit eligibility from age and employment"
            ),
            
            # Provincial requirements
            InferenceRule(
                rule_id="PROBATE_REQUIRED_ON",
                source_fields=["estate.total_value", "deceased.last_province"],
                target_field="task_planner.b_probate_required",
                inference_logic="province == 'ON' AND estate_value > 50000",
                confidence_level=0.95,
                description="Infer probate requirement for Ontario estates over $50k"
            ),
            
            InferenceRule(
                rule_id="PROBATE_REQUIRED_BC",
                source_fields=["estate.total_value", "deceased.last_province"],
                target_field="task_planner.b_probate_required", 
                inference_logic="province == 'BC' AND estate_value > 25000",
                confidence_level=0.95,
                description="Infer probate requirement for BC estates over $25k"
            ),
            
            # Document requirements
            InferenceRule(
                rule_id="DEATH_CERTIFICATE_REQUIRED",
                source_fields=["task_planner.b_probate_required", "task_planner.b_cpp_application"],
                target_field="required_documents.death_certificate",
                inference_logic="probate_required OR cpp_application",
                confidence_level=1.0,
                description="Death certificate required for probate or CPP applications"
            ),
            
            # Contact information
            InferenceRule(
                rule_id="PHONE_FROM_EMERGENCY_CONTACT",
                source_fields=["contact[*].phone.phone_number", "applicant.relationship_to_deceased"],
                target_field="applicant.phone",
                inference_logic="emergency_contact_is_applicant",
                confidence_level=0.8,
                description="Use emergency contact phone if same person as applicant"
            ),
            
            # Address standardization
            InferenceRule(
                rule_id="POSTAL_CODE_FROM_ADDRESS",
                source_fields=["deceased.home_address"],
                target_field="deceased.postal_code",
                inference_logic="extract_postal_code(address)",
                confidence_level=0.9,
                description="Extract postal code from full address"
            ),
            
            # Marriage and family status
            InferenceRule(
                rule_id="MARRIAGE_STATUS_FROM_SPOUSE",
                source_fields=["spouse.name", "spouse.date_of_birth"],
                target_field="deceased.marital_status",
                inference_logic="spouse_exists == True",
                confidence_level=0.8,
                description="Infer married status if spouse information provided"
            ),
            
            # Employment and pension inferences
            InferenceRule(
                rule_id="PENSION_FROM_EMPLOYMENT",
                source_fields=["deceased.employment.employer", "deceased.employment.years_service"],
                target_field="deceased.pension_plans[*]",
                inference_logic="long_term_employer(years >= 5)",
                confidence_level=0.6,
                description="Infer possible pension if long-term employment"
            ),
            
            # Will and executor inferences
            InferenceRule(
                rule_id="EXECUTOR_IS_SPOUSE",
                source_fields=["spouse.name", "applicant.name", "applicant.relationship_to_deceased"],
                target_field="estate_reps[*].name",
                inference_logic="applicant_is_spouse AND no_other_executor",
                confidence_level=0.7,
                description="Infer spouse as executor if applying and no other executor named"
            ),
            
            # Insurance inferences
            InferenceRule(
                rule_id="LIFE_INSURANCE_FROM_EMPLOYMENT",
                source_fields=["deceased.employment.status", "deceased.employment.employer"],
                target_field="insurance__life[*].name",
                inference_logic="employed_full_time AND large_employer",
                confidence_level=0.5,
                description="Possible employer life insurance for full-time employees"
            ),
            
            # Asset inferences
            InferenceRule(
                rule_id="HOME_OWNERSHIP_FROM_ADDRESS",
                source_fields=["deceased.home_address", "deceased.age_at_death"],
                target_field="property[*].type",
                inference_logic="stable_address AND age > 30",
                confidence_level=0.4,
                description="Possible home ownership for older adults with stable address"
            ),
            
            # Banking and financial
            InferenceRule(
                rule_id="BANK_ACCOUNT_REQUIRED",
                source_fields=["deceased.employment.status", "spouse.name"],
                target_field="financial_information[*].type",
                inference_logic="employed OR married",
                confidence_level=0.9,
                description="Bank account highly likely if employed or married"
            ),
            
            # Age-based inferences
            InferenceRule(
                rule_id="RETIREMENT_SAVINGS_OLDER",
                source_fields=["deceased.age_at_death", "deceased.employment.status"],
                target_field="financial_information[*].type",
                inference_logic="age >= 40 AND employed_history",
                confidence_level=0.6,
                description="RRSP/pension likely for older employed individuals"
            ),
            
            # Geographic inferences
            InferenceRule(
                rule_id="HEALTHCARE_NUMBER_PROVINCE",
                source_fields=["deceased.last_province", "deceased.home_address"],
                target_field="deceased.health_care_number",
                inference_logic="resident_of_province(address, province)",
                confidence_level=0.8,
                description="Health card number expected for provincial residents"
            )
        ]
    
    def _load_required_fields(self) -> List[RequiredFieldSpec]:
        """Load required field specifications"""
        
        return [
            # Critical identity fields
            RequiredFieldSpec(
                field_name="Deceased Full Name",
                cadence_path="deceased.name",
                required_for_forms=["all"],
                required_for_jurisdictions=list(ProvincialJurisdiction),
                criticality="critical",
                validation_rules=["required", "min_length:2"]
            ),
            
            RequiredFieldSpec(
                field_name="Date of Death",
                cadence_path="deceased.date_of_death",
                required_for_forms=["all"],
                required_for_jurisdictions=list(ProvincialJurisdiction),
                criticality="critical",
                validation_rules=["required", "date_format", "date_in_past"]
            ),
            
            RequiredFieldSpec(
                field_name="Social Insurance Number",
                cadence_path="deceased.social_insurance_number",
                required_for_forms=["probate_application", "death_benefit_application", "tax_clearance"],
                required_for_jurisdictions=list(ProvincialJurisdiction),
                criticality="critical",
                validation_rules=["required", "sin_format", "sin_checksum"]
            ),
            
            # Applicant information
            RequiredFieldSpec(
                field_name="Applicant Name",
                cadence_path="applicant.name",
                required_for_forms=["all"],
                required_for_jurisdictions=list(ProvincialJurisdiction),
                criticality="critical",
                validation_rules=["required", "min_length:2"]
            ),
            
            RequiredFieldSpec(
                field_name="Applicant Address",
                cadence_path="applicant.address",
                required_for_forms=["all"],
                required_for_jurisdictions=list(ProvincialJurisdiction),
                criticality="important",
                validation_rules=["required", "min_length:10"]
            ),
            
            RequiredFieldSpec(
                field_name="Relationship to Deceased",
                cadence_path="applicant.role",
                required_for_forms=["all"],
                required_for_jurisdictions=list(ProvincialJurisdiction),
                criticality="critical",
                validation_rules=["required"]
            ),
            
            # Estate-specific fields
            RequiredFieldSpec(
                field_name="Estate Value",
                cadence_path="estate.total_value",
                required_for_forms=["probate_application", "estate_information"],
                required_for_jurisdictions=list(ProvincialJurisdiction),
                criticality="important",
                validation_rules=["required", "currency_format"]
            ),
            
            # Spouse information (conditional)
            RequiredFieldSpec(
                field_name="Spouse Name",
                cadence_path="spouse.name",
                required_for_forms=["death_benefit_application"],
                required_for_jurisdictions=list(ProvincialJurisdiction),
                criticality="important",
                validation_rules=["conditional_required"]
            ),
            
            # Will information
            RequiredFieldSpec(
                field_name="Will Existence",
                cadence_path="task_planner.b_will",
                required_for_forms=["probate_application", "estate_information"],
                required_for_jurisdictions=list(ProvincialJurisdiction),
                criticality="critical",
                validation_rules=["required"]
            ),
            
            # Executor information
            RequiredFieldSpec(
                field_name="Executor Name",
                cadence_path="estate_reps[*].name",
                required_for_forms=["probate_application"],
                required_for_jurisdictions=list(ProvincialJurisdiction),
                criticality="critical",
                validation_rules=["conditional_required"]
            ),
            
            # Provincial-specific requirements
            RequiredFieldSpec(
                field_name="Last Province of Residence",
                cadence_path="task_planner.b_last_province_ca",
                required_for_forms=["death_benefit_application"],
                required_for_jurisdictions=list(ProvincialJurisdiction),
                criticality="important",
                validation_rules=["required"]
            )
        ]
    
    def _load_relationship_inference(self) -> Dict[str, List[str]]:
        """Load relationship-based inference patterns"""
        
        return {
            "spouse": [
                "same_address_likely",
                "shared_financial_accounts",
                "beneficiary_of_insurance",
                "next_of_kin",
                "emergency_contact"
            ],
            "child": [
                "possible_same_last_name",
                "beneficiary_status",
                "emergency_contact",
                "dependent_status_if_minor"
            ],
            "executor": [
                "access_to_estate_documents",
                "knowledge_of_assets",
                "close_relationship",
                "trustworthy_status"
            ],
            "parent": [
                "emergency_contact",
                "next_of_kin_if_no_spouse",
                "beneficiary_if_no_will"
            ]
        }
    
    def _load_estate_requirements(self) -> Dict[str, Dict[str, Any]]:
        """Load estate processing requirements by form type"""
        
        return {
            "probate_application": {
                "required_fields": [
                    "deceased.name", "deceased.date_of_death", "deceased.social_insurance_number",
                    "applicant.name", "applicant.relationship_to_deceased", "estate.total_value",
                    "will.location_hint", "estate_reps[*].name"
                ],
                "conditional_fields": {
                    "spouse.name": "has_surviving_spouse",
                    "children[*].name": "has_children",
                    "will.date_created": "will_exists"
                }
            },
            "death_benefit_application": {
                "required_fields": [
                    "deceased.name", "deceased.date_of_death", "deceased.social_insurance_number",
                    "applicant.name", "applicant.relationship_to_deceased"
                ],
                "conditional_fields": {
                    "spouse.name": "applicant_is_spouse",
                    "children[*].name": "applicant_is_child_or_has_children",
                    "spouse.date_of_birth": "applying_for_spouse_benefits"
                }
            },
            "estate_information": {
                "required_fields": [
                    "deceased.name", "deceased.date_of_death", "estate.total_value",
                    "applicant.name", "applicant.relationship_to_deceased"
                ],
                "helpful_fields": [
                    "property[*].name", "financial_information[*].name",
                    "insurance[*].name", "will.location_hint"
                ]
            }
        }
    
    async def analyze_missing_data(self, extraction_result) -> MissingDataAnalysis:
        """Analyze missing data and generate inferences"""
        
        # Extract available data
        available_data = self._extract_available_data(extraction_result.field_results)
        
        # Determine form type and requirements
        form_type = self._determine_form_type(extraction_result)
        required_fields = self._get_required_fields_for_form(form_type)
        
        # Identify missing fields
        missing_fields = self._identify_missing_fields(available_data, required_fields)
        
        # Categorize missing fields by criticality
        critical_missing = self._categorize_critical_missing(missing_fields)
        
        # Generate inferences for missing data
        inferences = await self._generate_inferences(available_data, missing_fields)
        
        # Generate data collection suggestions
        suggestions = self._generate_collection_suggestions(missing_fields, available_data)
        
        # Calculate completion percentage
        completion_percentage = self._calculate_completion_percentage(
            available_data, required_fields, inferences
        )
        
        # Identify blocking issues
        blocking_issues = self._identify_blocking_issues(critical_missing, inferences)
        
        return MissingDataAnalysis(
            missing_fields=missing_fields,
            critical_missing=critical_missing,
            inferable_fields=inferences,
            data_collection_suggestions=suggestions,
            form_completion_percentage=completion_percentage,
            blocking_issues=blocking_issues
        )
    
    def _extract_available_data(self, field_results: List[MappingResult]) -> Dict[str, Any]:
        """Extract available data from field mapping results"""
        
        available_data = {}
        
        for result in field_results:
            if result.cadence_path != "unknown.field":
                field_value = result.metadata.get("field_value", "") if result.metadata else ""
                if field_value and field_value.strip():
                    available_data[result.cadence_path] = field_value.strip()
        
        return available_data
    
    def _determine_form_type(self, extraction_result) -> str:
        """Determine the most likely form type"""
        
        if hasattr(extraction_result, 'form_info') and extraction_result.form_info:
            return extraction_result.form_info.form_type.value
        
        # Analyze field patterns to infer form type
        field_paths = [r.cadence_path for r in extraction_result.field_results]
        
        if any("estate_reps" in path for path in field_paths):
            return "probate_application"
        elif any("spouse" in path for path in field_paths):
            return "death_benefit_application"
        else:
            return "estate_information"
    
    def _get_required_fields_for_form(self, form_type: str) -> List[RequiredFieldSpec]:
        """Get required fields for specific form type"""
        
        relevant_fields = []
        
        for field_spec in self.required_fields:
            if form_type in field_spec.required_for_forms or "all" in field_spec.required_for_forms:
                relevant_fields.append(field_spec)
        
        return relevant_fields
    
    def _identify_missing_fields(self, available_data: Dict[str, Any],
                               required_fields: List[RequiredFieldSpec]) -> List[str]:
        """Identify missing required fields"""
        
        missing_fields = []
        
        for field_spec in required_fields:
            if field_spec.cadence_path not in available_data:
                # Check if it's an array field with any populated entries
                if "[*]" in field_spec.cadence_path:
                    base_path = field_spec.cadence_path.replace("[*]", "")
                    has_any_entry = any(path.startswith(base_path) for path in available_data.keys())
                    if not has_any_entry:
                        missing_fields.append(field_spec.cadence_path)
                else:
                    missing_fields.append(field_spec.cadence_path)
        
        return missing_fields
    
    def _categorize_critical_missing(self, missing_fields: List[str]) -> List[str]:
        """Categorize missing fields by criticality"""
        
        critical_missing = []
        
        for field_path in missing_fields:
            # Find the field spec
            field_spec = next(
                (spec for spec in self.required_fields if spec.cadence_path == field_path),
                None
            )
            
            if field_spec and field_spec.criticality == "critical":
                critical_missing.append(field_path)
        
        return critical_missing
    
    async def _generate_inferences(self, available_data: Dict[str, Any],
                                 missing_fields: List[str]) -> List[DataInference]:
        """Generate inferences for missing data"""
        
        inferences = []
        
        for missing_field in missing_fields:
            # Find applicable inference rules
            applicable_rules = [
                rule for rule in self.inference_rules
                if rule.target_field == missing_field or missing_field.startswith(rule.target_field.replace("[*]", ""))
            ]
            
            for rule in applicable_rules:
                # Check if we have the required source fields
                if self._has_required_source_fields(rule, available_data):
                    # Generate inference
                    inference = await self._apply_inference_rule(rule, available_data)
                    if inference:
                        inferences.append(inference)
        
        return inferences
    
    def _has_required_source_fields(self, rule: InferenceRule, available_data: Dict[str, Any]) -> bool:
        """Check if we have the required source fields for inference"""
        
        for source_field in rule.source_fields:
            if "[*]" in source_field:
                # Check if any array entry exists
                base_path = source_field.replace("[*]", "")
                if not any(path.startswith(base_path) for path in available_data.keys()):
                    return False
            else:
                if source_field not in available_data:
                    return False
        
        return True
    
    async def _apply_inference_rule(self, rule: InferenceRule, available_data: Dict[str, Any]) -> Optional[DataInference]:
        """Apply inference rule to generate missing data"""
        
        try:
            # Apply rule-specific logic
            if rule.rule_id == "AGE_FROM_BIRTH_DEATH":
                return self._infer_age_from_dates(rule, available_data)
            elif rule.rule_id == "SPOUSE_ADDRESS_SAME":
                return self._infer_spouse_address(rule, available_data)
            elif rule.rule_id == "ESTATE_VALUE_FROM_ASSETS":
                return self._infer_estate_value(rule, available_data)
            elif rule.rule_id.startswith("PROBATE_REQUIRED_"):
                return self._infer_probate_requirement(rule, available_data)
            elif rule.rule_id == "MARRIAGE_STATUS_FROM_SPOUSE":
                return self._infer_marital_status(rule, available_data)
            elif rule.rule_id == "POSTAL_CODE_FROM_ADDRESS":
                return self._infer_postal_code(rule, available_data)
            elif rule.rule_id == "CPP_ELIGIBILITY_AGE":
                return self._infer_cpp_eligibility(rule, available_data)
            else:
                # Generic inference
                return self._apply_generic_inference(rule, available_data)
        
        except Exception as e:
            self.logger.error(f"Error applying inference rule {rule.rule_id}: {e}")
            return None
    
    def _infer_age_from_dates(self, rule: InferenceRule, available_data: Dict[str, Any]) -> Optional[DataInference]:
        """Infer age from birth and death dates"""
        
        birth_date_str = available_data.get("deceased.date_of_birth")
        death_date_str = available_data.get("deceased.date_of_death")
        
        if not birth_date_str or not death_date_str:
            return None
        
        try:
            birth_date = self._parse_date(birth_date_str)
            death_date = self._parse_date(death_date_str)
            
            if birth_date and death_date:
                age = relativedelta(death_date, birth_date).years
                
                return DataInference(
                    inferred_field="deceased.age_at_death",
                    inferred_value=str(age),
                    inference_method="date_calculation",
                    confidence=0.95,
                    source_fields=["deceased.date_of_birth", "deceased.date_of_death"],
                    reasoning=f"Calculated age as {age} years from birth date {birth_date_str} to death date {death_date_str}"
                )
        except:
            pass
        
        return None
    
    def _infer_spouse_address(self, rule: InferenceRule, available_data: Dict[str, Any]) -> Optional[DataInference]:
        """Infer spouse address from deceased address"""
        
        deceased_address = available_data.get("deceased.home_address")
        relationship = available_data.get("applicant.role", "").lower()
        
        if deceased_address and "spouse" in relationship:
            return DataInference(
                inferred_field="spouse.address",
                inferred_value=deceased_address,
                inference_method="relationship_logic",
                confidence=0.7,
                source_fields=["deceased.home_address", "applicant.role"],
                reasoning="Spouse likely lived at same address as deceased"
            )
        
        return None
    
    def _infer_estate_value(self, rule: InferenceRule, available_data: Dict[str, Any]) -> Optional[DataInference]:
        """Infer estate value from asset information"""
        
        total_value = 0
        source_fields = []
        
        # Sum property values
        for field_path, value in available_data.items():
            if "property" in field_path and "value" in field_path:
                try:
                    numeric_value = float(re.sub(r'[^\d.]', '', value))
                    total_value += numeric_value
                    source_fields.append(field_path)
                except:
                    continue
        
        # Sum financial account balances
        for field_path, value in available_data.items():
            if "financial_information" in field_path and ("balance" in field_path or "value" in field_path):
                try:
                    numeric_value = float(re.sub(r'[^\d.]', '', value))
                    total_value += numeric_value
                    source_fields.append(field_path)
                except:
                    continue
        
        if total_value > 0 and source_fields:
            return DataInference(
                inferred_field="estate.total_value",
                inferred_value=f"${total_value:,.2f}",
                inference_method="asset_summation",
                confidence=0.8,
                source_fields=source_fields,
                reasoning=f"Calculated minimum estate value of ${total_value:,.2f} from known assets"
            )
        
        return None
    
    def _infer_probate_requirement(self, rule: InferenceRule, available_data: Dict[str, Any]) -> Optional[DataInference]:
        """Infer probate requirement based on estate value and jurisdiction"""
        
        estate_value_str = available_data.get("estate.total_value")
        province = available_data.get("task_planner.b_last_province_ca")
        
        if not estate_value_str or not province:
            return None
        
        try:
            estate_value = float(re.sub(r'[^\d.]', '', estate_value_str))
            
            # Apply provincial thresholds
            probate_required = False
            threshold = 0
            
            if province == "ON":
                threshold = 50000
                probate_required = estate_value > threshold
            elif province == "BC":
                threshold = 25000
                probate_required = estate_value > threshold
            elif province in ["AB", "SK", "MB"]:
                # These provinces have lower or no thresholds
                threshold = 10000
                probate_required = estate_value > threshold
            
            if threshold > 0:
                return DataInference(
                    inferred_field="task_planner.b_probate_required",
                    inferred_value="yes" if probate_required else "no",
                    inference_method="provincial_threshold",
                    confidence=0.95,
                    source_fields=["estate.total_value", "task_planner.b_last_province_ca"],
                    reasoning=f"Estate value ${estate_value:,.2f} {'exceeds' if probate_required else 'is below'} {province} threshold of ${threshold:,.2f}",
                    provincial_specific=True
                )
        except:
            pass
        
        return None
    
    def _infer_marital_status(self, rule: InferenceRule, available_data: Dict[str, Any]) -> Optional[DataInference]:
        """Infer marital status from spouse information"""
        
        spouse_name = available_data.get("spouse.name")
        spouse_dob = available_data.get("spouse.date_of_birth")
        
        if spouse_name and spouse_name.strip():
            return DataInference(
                inferred_field="deceased.marital_status",
                inferred_value="married",
                inference_method="spouse_existence",
                confidence=0.8,
                source_fields=["spouse.name"],
                reasoning="Spouse information provided indicates deceased was married"
            )
        
        return None
    
    def _infer_postal_code(self, rule: InferenceRule, available_data: Dict[str, Any]) -> Optional[DataInference]:
        """Extract postal code from address"""
        
        address = available_data.get("deceased.home_address")
        
        if address:
            # Canadian postal code pattern
            postal_pattern = r'([A-Za-z]\d[A-Za-z]\s?\d[A-Za-z]\d)'
            match = re.search(postal_pattern, address)
            
            if match:
                postal_code = match.group(1)
                # Format consistently
                if len(postal_code) == 6:
                    postal_code = f"{postal_code[:3]} {postal_code[3:]}"
                
                return DataInference(
                    inferred_field="deceased.postal_code",
                    inferred_value=postal_code.upper(),
                    inference_method="pattern_extraction",
                    confidence=0.9,
                    source_fields=["deceased.home_address"],
                    reasoning=f"Extracted postal code {postal_code} from address"
                )
        
        return None
    
    def _infer_cpp_eligibility(self, rule: InferenceRule, available_data: Dict[str, Any]) -> Optional[DataInference]:
        """Infer CPP death benefit eligibility"""
        
        # Calculate age if we have birth/death dates
        age_at_death = None
        if "deceased.date_of_birth" in available_data and "deceased.date_of_death" in available_data:
            birth_date = self._parse_date(available_data["deceased.date_of_birth"])
            death_date = self._parse_date(available_data["deceased.date_of_death"])
            if birth_date and death_date:
                age_at_death = relativedelta(death_date, birth_date).years
        
        employment_status = available_data.get("deceased.employment.status[*]", "").lower()
        
        # CPP eligibility rules
        eligible = False
        reasoning = ""
        
        if age_at_death:
            if age_at_death >= 60:
                eligible = True
                reasoning = f"Age {age_at_death} meets CPP minimum age requirement"
            elif age_at_death >= 18 and "employ" in employment_status:
                eligible = True
                reasoning = f"Age {age_at_death} with employment history likely qualifies for CPP"
        
        if eligible:
            return DataInference(
                inferred_field="task_planner.b_cpp_eligible",
                inferred_value="yes",
                inference_method="age_employment_analysis",
                confidence=0.8,
                source_fields=["deceased.date_of_birth", "deceased.date_of_death", "deceased.employment.status"],
                reasoning=reasoning
            )
        
        return None
    
    def _apply_generic_inference(self, rule: InferenceRule, available_data: Dict[str, Any]) -> Optional[DataInference]:
        """Apply generic inference logic"""
        
        # Simple rule evaluation for other cases
        return DataInference(
            inferred_field=rule.target_field,
            inferred_value="inferred_value",
            inference_method="generic_rule",
            confidence=rule.confidence_level,
            source_fields=rule.source_fields,
            reasoning=rule.description
        )
    
    def _parse_date(self, date_str: str) -> Optional[date]:
        """Parse date string into date object"""
        
        date_str = date_str.strip()
        
        # Try common date formats
        formats = [
            "%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y", "%Y/%m/%d",
            "%B %d, %Y", "%d %B %Y", "%Y%m%d"
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt).date()
            except ValueError:
                continue
        
        return None
    
    def _generate_collection_suggestions(self, missing_fields: List[str], 
                                       available_data: Dict[str, Any]) -> List[str]:
        """Generate suggestions for collecting missing data"""
        
        suggestions = []
        
        for field_path in missing_fields:
            # Find the field spec
            field_spec = next(
                (spec for spec in self.required_fields if spec.cadence_path == field_path),
                None
            )
            
            if field_spec:
                if field_spec.criticality == "critical":
                    suggestions.append(f"🔴 CRITICAL: Collect {field_spec.field_name}")
                elif field_spec.criticality == "important":
                    suggestions.append(f"🟡 IMPORTANT: Obtain {field_spec.field_name}")
                else:
                    suggestions.append(f"ℹ️ HELPFUL: Consider gathering {field_spec.field_name}")
        
        # Add relationship-specific suggestions
        relationship = available_data.get("applicant.role", "").lower()
        if "spouse" in relationship:
            suggestions.append("📋 As spouse, you may need marriage certificate")
            suggestions.append("💰 Check for joint financial accounts and insurance policies")
        elif "child" in relationship:
            suggestions.append("👨‍👩‍👧‍👦 Gather information about other siblings/beneficiaries")
            suggestions.append("📜 Locate will or estate planning documents")
        
        return suggestions
    
    def _calculate_completion_percentage(self, available_data: Dict[str, Any],
                                       required_fields: List[RequiredFieldSpec],
                                       inferences: List[DataInference]) -> float:
        """Calculate form completion percentage"""
        
        total_required = len(required_fields)
        if total_required == 0:
            return 100.0
        
        completed = 0
        
        for field_spec in required_fields:
            # Check if we have the data directly
            if field_spec.cadence_path in available_data:
                completed += 1
            # Check if we can infer it
            elif any(inf.inferred_field == field_spec.cadence_path for inf in inferences):
                completed += 0.8  # Inferences count as 80% completion
        
        return min(100.0, (completed / total_required) * 100)
    
    def _identify_blocking_issues(self, critical_missing: List[str], 
                                inferences: List[DataInference]) -> List[str]:
        """Identify issues that block form processing"""
        
        blocking_issues = []
        
        # Check for critical missing fields that can't be inferred
        for critical_field in critical_missing:
            can_infer = any(inf.inferred_field == critical_field for inf in inferences)
            if not can_infer:
                field_spec = next(
                    (spec for spec in self.required_fields if spec.cadence_path == critical_field),
                    None
                )
                if field_spec:
                    blocking_issues.append(f"Missing critical field: {field_spec.field_name}")
        
        return blocking_issues
