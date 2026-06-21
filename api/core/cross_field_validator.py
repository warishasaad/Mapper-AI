"""
Advanced Cross-Field Validation Engine

Handles validation rules that depend on multiple fields simultaneously,
estate-specific business rules, and cross-referential data consistency.
"""

import logging
import re
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

from .models import (
    MappingResult, ValidationSeverity, ProvincialJurisdiction,
    FieldType, ConditionalLogic, CrossFieldValidationRule, CrossFieldValidationResult
)

class CrossFieldValidator:
    """Advanced cross-field validation for estate forms"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.validation_rules = self._load_validation_rules()
        self.estate_business_rules = self._load_estate_business_rules()
        self.consistency_rules = self._load_consistency_rules()
        
        self.logger.info("Cross-Field Validator initialized")
    
    def _load_validation_rules(self) -> List[CrossFieldValidationRule]:
        """Load comprehensive cross-field validation rules"""
        
        return [
            # Deceased person consistency rules
            CrossFieldValidationRule(
                rule_id="DECEASED_DATE_CONSISTENCY",
                name="Deceased Date Consistency",
                description="Death date must be after birth date",
                source_fields=["deceased.date_of_birth", "deceased.date_of_death"],
                target_field="deceased.date_of_death",
                validation_logic="death_date > birth_date",
                error_message="Date of death cannot be before date of birth",
                severity=ValidationSeverity.ERROR
            ),
            
            CrossFieldValidationRule(
                rule_id="DECEASED_AGE_REASONABLE",
                name="Deceased Age Reasonableness",
                description="Age at death should be reasonable (0-120 years)",
                source_fields=["deceased.date_of_birth", "deceased.date_of_death"],
                target_field="deceased.date_of_death",
                validation_logic="0 <= age_at_death <= 120",
                error_message="Age at death appears unreasonable - please verify dates",
                severity=ValidationSeverity.WARNING
            ),
            
            # Spouse relationship rules
            CrossFieldValidationRule(
                rule_id="SPOUSE_CONSISTENCY",
                name="Spouse Information Consistency",
                description="If spouse exists, spouse information must be complete",
                source_fields=["task_planner.b_has_spouse"],
                target_field="spouse.name",
                validation_logic="has_spouse == 'yes' IMPLIES spouse_info_complete",
                error_message="Spouse information is incomplete but spouse was indicated",
                severity=ValidationSeverity.ERROR
            ),
            
            CrossFieldValidationRule(
                rule_id="MARRIAGE_DATE_CONSISTENCY",
                name="Marriage Date Consistency", 
                description="Marriage date should be reasonable relative to birth dates",
                source_fields=["spouse.date_of_marriage", "deceased.date_of_birth", "spouse.date_of_birth"],
                target_field="spouse.date_of_marriage",
                validation_logic="marriage_date >= max(deceased_birth + 16_years, spouse_birth + 16_years)",
                error_message="Marriage date seems early relative to birth dates",
                severity=ValidationSeverity.WARNING
            ),
            
            CrossFieldValidationRule(
                rule_id="EXECUTOR_IS_NOT_SPOUSE_UNLESS_SPECIFIED",
                name="Executor and Spouse Identity Check",
                description="Verifies that the executor and spouse are not the same person unless their roles overlap.",
                source_fields=["spouse.name", "estate_reps[*].name", "applicant.role"],
                target_field="estate_reps[*].name",
                validation_logic="spouse.name != estate_reps.name UNLESS applicant.role contains 'spouse' and 'executor'",
                error_message="The Executor and Spouse have the same name. Please confirm this is correct.",
                severity=ValidationSeverity.WARNING
            ),
            
            # Children relationship rules
            CrossFieldValidationRule(
                rule_id="CHILDREN_CONSISTENCY",
                name="Children Information Consistency",
                description="If children exist, at least one child must be specified",
                source_fields=["task_planner.b_has_children"],
                target_field="children[*].name",
                validation_logic="has_children == 'yes' IMPLIES children_count > 0",
                error_message="No children specified but children were indicated",
                severity=ValidationSeverity.ERROR
            ),
            
            CrossFieldValidationRule(
                rule_id="CHILD_BIRTH_DATE_CONSISTENCY",
                name="Child Birth Date Consistency",
                description="Child birth dates should be after parent birth dates",
                source_fields=["children[*].date_of_birth", "deceased.date_of_birth"],
                target_field="children[*].date_of_birth",
                validation_logic="child_birth >= parent_birth + 12_years",
                error_message="Child birth date seems early relative to parent age",
                severity=ValidationSeverity.WARNING
            ),
            
            # Estate value and probate rules
            CrossFieldValidationRule(
                rule_id="PROBATE_THRESHOLD_ONTARIO",
                name="Ontario Probate Threshold",
                description="Ontario estates over $50,000 require probate",
                source_fields=["estate.total_value", "task_planner.b_last_province_ca"],
                target_field="task_planner.b_probate_required",
                validation_logic="province == 'ON' AND estate_value > 50000 IMPLIES probate_required",
                error_message="Estate value exceeds Ontario probate threshold - probate required",
                severity=ValidationSeverity.ERROR,
                applies_to_jurisdictions=[ProvincialJurisdiction.ONTARIO]
            ),
            
            CrossFieldValidationRule(
                rule_id="PROBATE_THRESHOLD_BC",
                name="BC Probate Threshold",
                description="BC estates over $25,000 require probate",
                source_fields=["estate.total_value", "task_planner.b_last_province_ca"],
                target_field="task_planner.b_probate_required",
                validation_logic="province == 'BC' AND estate_value > 25000 IMPLIES probate_required",
                error_message="Estate value exceeds BC probate threshold - probate required",
                severity=ValidationSeverity.ERROR,
                applies_to_jurisdictions=[ProvincialJurisdiction.BRITISH_COLUMBIA]
            ),
            
            # Executor and will rules
            CrossFieldValidationRule(
                rule_id="EXECUTOR_WILL_CONSISTENCY",
                name="Executor and Will Consistency",
                description="If will exists, executor information should be provided",
                source_fields=["task_planner.b_will"],
                target_field="estate_reps[*].name",
                validation_logic="has_will == 'yes' IMPLIES executor_specified",
                error_message="Will exists but no executor information provided",
                severity=ValidationSeverity.WARNING
            ),
            
            # Contact information consistency
            CrossFieldValidationRule(
                rule_id="APPLICANT_CONTACT_COMPLETE",
                name="Applicant Contact Information",
                description="Applicant must have complete contact information",
                source_fields=["applicant.name"],
                target_field="applicant.phone",
                validation_logic="applicant_exists IMPLIES contact_info_complete",
                error_message="Applicant contact information is incomplete",
                severity=ValidationSeverity.ERROR
            ),
            
            # Address consistency rules
            CrossFieldValidationRule(
                rule_id="ADDRESS_PROVINCE_CONSISTENCY",
                name="Address Province Consistency",
                description="Address province should match last province of residence",
                source_fields=["deceased.home_address", "task_planner.b_last_province_ca"],
                target_field="deceased.home_address",
                validation_logic="address_province == last_province_residence",
                error_message="Address province doesn't match last province of residence",
                severity=ValidationSeverity.WARNING
            ),
            
            # Age-based validation rules
            CrossFieldValidationRule(
                rule_id="ADULT_CHILDREN_BENEFITS",
                name="Adult Children Benefits Eligibility",
                description="Children over 25 generally not eligible for benefits",
                source_fields=["children[*].date_of_birth", "deceased.date_of_death"],
                target_field="task_planner.b_has_children_18_25_full_time_school_ca",
                validation_logic="child_age_at_death <= 25 OR in_school",
                error_message="Children over 25 may not be eligible for survivor benefits",
                severity=ValidationSeverity.WARNING
            )
        ]
    
    def _load_estate_business_rules(self) -> List[CrossFieldValidationRule]:
        """Load estate-specific business rules"""
        
        return [
            # Estate administration rules
            CrossFieldValidationRule(
                rule_id="ESTATE_REP_AUTHORITY",
                name="Estate Representative Authority",
                description="Estate representative must have proper authority",
                source_fields=["estate_reps[*].relationship", "task_planner.b_will"],
                target_field="estate_reps[*].proof_of_authority",
                validation_logic="proper_authority_for_relationship",
                error_message="Estate representative may not have proper authority",
                severity=ValidationSeverity.WARNING
            ),
            
            # Insurance claim rules
            CrossFieldValidationRule(
                rule_id="INSURANCE_BENEFICIARY_CONSISTENCY",
                name="Insurance Beneficiary Consistency",
                description="Insurance beneficiary should match relationship",
                source_fields=["applicant.role", "insurance[*].beneficiary"],
                target_field="insurance[*].beneficiary",
                validation_logic="applicant_role_matches_beneficiary_status",
                error_message="Applicant role may not match insurance beneficiary status",
                severity=ValidationSeverity.WARNING
            ),
            
            # Financial consistency rules
            CrossFieldValidationRule(
                rule_id="FINANCIAL_ACCOUNTS_COMPLETE",
                name="Financial Accounts Completeness",
                description="Major financial institutions should be represented",
                source_fields=["financial_information[*].name"],
                target_field="deceased.employment.status",
                validation_logic="employed_person_has_financial_accounts",
                error_message="Consider checking for additional financial accounts",
                severity=ValidationSeverity.INFO
            )
        ]
    
    def _load_consistency_rules(self) -> List[CrossFieldValidationRule]:
        """Load data consistency rules"""
        
        return [
            # Name consistency
            CrossFieldValidationRule(
                rule_id="NAME_CONSISTENCY",
                name="Name Consistency Across Fields",
                description="Names should be consistent across related fields",
                source_fields=["deceased.name", "applicant.name"],
                target_field="spouse.name",
                validation_logic="name_variations_reasonable",
                error_message="Name variations detected - verify spelling consistency",
                severity=ValidationSeverity.INFO
            ),
            
            # Date format consistency
            CrossFieldValidationRule(
                rule_id="DATE_FORMAT_CONSISTENCY",
                name="Date Format Consistency",
                description="Dates should use consistent formatting",
                source_fields=["deceased.date_of_birth", "deceased.date_of_death"],
                target_field="spouse.date_of_birth",
                validation_logic="consistent_date_formats",
                error_message="Inconsistent date formats detected",
                severity=ValidationSeverity.INFO
            )
        ]
    
    async def validate_cross_fields(self, mapping_results: List[MappingResult], 
                                  context: Dict = None) -> List[CrossFieldValidationResult]:
        """Validate fields against cross-field rules"""
        
        validation_results = []
        
        # Extract field data from mapping results
        field_data = self._extract_field_data(mapping_results)
        
        # Get jurisdiction context
        jurisdiction = self._determine_jurisdiction(field_data, context)
        
        # Apply all validation rules
        all_rules = (self.validation_rules + 
                    self.estate_business_rules + 
                    self.consistency_rules)
        
        for rule in all_rules:
            # Skip jurisdiction-specific rules if not applicable
            if (hasattr(rule, 'applies_to_jurisdictions') and rule.applies_to_jurisdictions and 
                jurisdiction not in rule.applies_to_jurisdictions):
                continue
            
            # Check if we have the required fields
            if self._has_required_fields(rule, field_data):
                try:
                    result = await self._apply_validation_rule(rule, field_data, context)
                    if result:
                        validation_results.append(result)
                except Exception as e:
                    self.logger.error(f"Error applying validation rule {rule.rule_id}: {e}")
        
        return validation_results
    
    def _extract_field_data(self, mapping_results: List[MappingResult]) -> Dict[str, Any]:
        """Extract field data from mapping results"""
        
        field_data = {}
        
        for result in mapping_results:
            if result.cadence_path != "unknown.field":
                # Get field value from metadata
                field_value = result.metadata.get("field_value", "") if result.metadata else ""
                
                if field_value:
                    field_data[result.cadence_path] = field_value
        
        return field_data
    
    def _determine_jurisdiction(self, field_data: Dict[str, Any], 
                              context: Dict = None) -> Optional[ProvincialJurisdiction]:
        """Determine jurisdiction from field data"""
        
        # Check context first
        if context and "jurisdiction" in context:
            return context["jurisdiction"]
        
        # Check province field
        province_field = field_data.get("task_planner.b_last_province_ca", "")
        if province_field:
            province_mapping = {
                "ON": ProvincialJurisdiction.ONTARIO,
                "BC": ProvincialJurisdiction.BRITISH_COLUMBIA,
                "AB": ProvincialJurisdiction.ALBERTA,
                "QC": ProvincialJurisdiction.QUEBEC,
                "MB": ProvincialJurisdiction.MANITOBA,
                "SK": ProvincialJurisdiction.SASKATCHEWAN,
                "NS": ProvincialJurisdiction.NOVA_SCOTIA,
                "NB": ProvincialJurisdiction.NEW_BRUNSWICK,
                "PE": ProvincialJurisdiction.PRINCE_EDWARD_ISLAND,
                "NL": ProvincialJurisdiction.NEWFOUNDLAND_LABRADOR,
                "NT": ProvincialJurisdiction.NORTHWEST_TERRITORIES,
                "NU": ProvincialJurisdiction.NUNAVUT,
                "YT": ProvincialJurisdiction.YUKON
            }
            return province_mapping.get(province_field.upper())
        
        return None
    
    def _has_required_fields(self, rule: CrossFieldValidationRule, 
                           field_data: Dict[str, Any]) -> bool:
        """Check if we have the required fields for validation"""
        
        # Check source fields
        for field in rule.source_fields:
            if not self._field_exists_in_data(field, field_data):
                return False
        
        return True
    
    def _field_exists_in_data(self, field_pattern: str, field_data: Dict[str, Any]) -> bool:
        """Check if field pattern exists in data (handles arrays)"""
        
        if "[*]" in field_pattern:
            # Handle array patterns
            base_pattern = field_pattern.replace("[*]", "")
            return any(key.startswith(base_pattern) for key in field_data.keys())
        else:
            return field_pattern in field_data
    
    async def _apply_validation_rule(self, rule: CrossFieldValidationRule, 
                                   field_data: Dict[str, Any], 
                                   context: Dict = None) -> Optional[CrossFieldValidationResult]:
        """Apply specific validation rule"""
        
        try:
            if rule.rule_id == "DECEASED_DATE_CONSISTENCY":
                return self._validate_deceased_date_consistency(rule, field_data)
            elif rule.rule_id == "DECEASED_AGE_REASONABLE":
                return self._validate_deceased_age_reasonable(rule, field_data)
            elif rule.rule_id == "SPOUSE_CONSISTENCY":
                return self._validate_spouse_consistency(rule, field_data)
            elif rule.rule_id == "CHILDREN_CONSISTENCY":
                return self._validate_children_consistency(rule, field_data)
            elif rule.rule_id.startswith("PROBATE_THRESHOLD_"):
                return self._validate_probate_threshold(rule, field_data)
            elif rule.rule_id == "APPLICANT_CONTACT_COMPLETE":
                return self._validate_applicant_contact_complete(rule, field_data)
            else:
                # Generic validation
                return self._validate_generic_rule(rule, field_data)
        
        except Exception as e:
            self.logger.error(f"Error in validation rule {rule.rule_id}: {e}")
            return None
    
    def _validate_deceased_date_consistency(self, rule: CrossFieldValidationRule, 
                                          field_data: Dict[str, Any]) -> Optional[CrossFieldValidationResult]:
        """Validate deceased date consistency"""
        
        birth_date_str = field_data.get("deceased.date_of_birth")
        death_date_str = field_data.get("deceased.date_of_death")
        
        if not birth_date_str or not death_date_str:
            return None
        
        try:
            birth_date = self._parse_date(birth_date_str)
            death_date = self._parse_date(death_date_str)
            
            if birth_date and death_date:
                is_valid = death_date > birth_date
                
                return CrossFieldValidationResult(
                    rule_id=rule.rule_id,
                    is_valid=is_valid,
                    severity=rule.severity,
                    message=rule.error_message if not is_valid else "Date consistency valid",
                    affected_fields=rule.source_fields,
                    suggested_corrections=["Verify birth and death dates"] if not is_valid else []
                )
        except:
            pass
        
        return None
    
    def _validate_deceased_age_reasonable(self, rule: CrossFieldValidationRule, 
                                        field_data: Dict[str, Any]) -> Optional[CrossFieldValidationResult]:
        """Validate deceased age reasonableness"""
        
        birth_date_str = field_data.get("deceased.date_of_birth")
        death_date_str = field_data.get("deceased.date_of_death")
        
        if not birth_date_str or not death_date_str:
            return None
        
        try:
            birth_date = self._parse_date(birth_date_str)
            death_date = self._parse_date(death_date_str)
            
            if birth_date and death_date:
                age_at_death = relativedelta(death_date, birth_date).years
                is_valid = 0 <= age_at_death <= 120
                
                message = rule.error_message if not is_valid else "Age appears reasonable"
                if not is_valid:
                    message += f" (calculated age: {age_at_death})"
                
                return CrossFieldValidationResult(
                    rule_id=rule.rule_id,
                    is_valid=is_valid,
                    severity=rule.severity,
                    message=message,
                    affected_fields=rule.source_fields,
                    suggested_corrections=["Double-check birth and death dates"] if not is_valid else []
                )
        except:
            pass
        
        return None
    
    def _validate_spouse_consistency(self, rule: CrossFieldValidationRule, 
                                   field_data: Dict[str, Any]) -> Optional[CrossFieldValidationResult]:
        """Validate spouse information consistency"""
        
        has_spouse = field_data.get("task_planner.b_has_spouse", "").lower()
        spouse_name = field_data.get("spouse.name", "")
        
        if has_spouse == "yes":
            is_valid = bool(spouse_name and spouse_name.strip())
            
            return CrossFieldValidationResult(
                rule_id=rule.rule_id,
                is_valid=is_valid,
                severity=rule.severity,
                message=rule.error_message if not is_valid else "Spouse information consistent",
                affected_fields=rule.source_fields + [rule.target_field],
                suggested_corrections=["Complete spouse information"] if not is_valid else []
            )
        
        return None
    
    def _validate_children_consistency(self, rule: CrossFieldValidationRule, 
                                     field_data: Dict[str, Any]) -> Optional[CrossFieldValidationResult]:
        """Validate children information consistency"""
        
        has_children = field_data.get("task_planner.b_has_children", "").lower()
        
        if has_children == "yes":
            # Count children entries
            children_count = len([key for key in field_data.keys() 
                                if key.startswith("children[") and key.endswith("].name")])
            
            is_valid = children_count > 0
            
            return CrossFieldValidationResult(
                rule_id=rule.rule_id,
                is_valid=is_valid,
                severity=rule.severity,
                message=rule.error_message if not is_valid else "Children information consistent",
                affected_fields=rule.source_fields + [rule.target_field],
                suggested_corrections=["Add child information"] if not is_valid else []
            )
        
        return None
    
    def _validate_probate_threshold(self, rule: CrossFieldValidationRule, 
                                  field_data: Dict[str, Any]) -> Optional[CrossFieldValidationResult]:
        """Validate probate threshold requirements"""
        
        estate_value_str = field_data.get("estate.total_value", "")
        province = field_data.get("task_planner.b_last_province_ca", "")
        
        if not estate_value_str or not province:
            return None
        
        try:
            # Extract numeric value
            estate_value = float(re.sub(r'[^\d.]', '', estate_value_str))
            
            # Determine threshold based on rule
            threshold = 50000 if "ONTARIO" in rule.rule_id else 25000
            
            if estate_value > threshold:
                return CrossFieldValidationResult(
                    rule_id=rule.rule_id,
                    is_valid=False,
                    severity=rule.severity,
                    message=f"{rule.error_message} (Estate: ${estate_value:,.2f})",
                    affected_fields=rule.source_fields,
                    suggested_corrections=[f"Prepare probate application for {province}"]
                )
        except:
            pass
        
        return None
    
    def _validate_applicant_contact_complete(self, rule: CrossFieldValidationRule, 
                                           field_data: Dict[str, Any]) -> Optional[CrossFieldValidationResult]:
        """Validate applicant contact completeness"""
        
        applicant_name = field_data.get("applicant.name", "")
        
        if applicant_name:
            # Check for contact fields
            has_phone = bool(field_data.get("applicant.phone", ""))
            has_address = bool(field_data.get("applicant.address", ""))
            has_email = bool(field_data.get("applicant.email", ""))
            
            contact_complete = has_phone and has_address
            
            missing_fields = []
            if not has_phone:
                missing_fields.append("phone")
            if not has_address:
                missing_fields.append("address")
            
            suggested_corrections = []
            if missing_fields:
                suggested_corrections.append(f"Add applicant {', '.join(missing_fields)}")
            
            return CrossFieldValidationResult(
                rule_id=rule.rule_id,
                is_valid=contact_complete,
                severity=rule.severity,
                message=rule.error_message if not contact_complete else "Contact information complete",
                affected_fields=rule.source_fields + [rule.target_field],
                suggested_corrections=suggested_corrections
            )
        
        return None
    
    def _validate_generic_rule(self, rule: CrossFieldValidationRule, 
                             field_data: Dict[str, Any]) -> Optional[CrossFieldValidationResult]:
        """Generic validation for simpler rules"""
        
        return CrossFieldValidationResult(
            rule_id=rule.rule_id,
            is_valid=True,  
            severity=ValidationSeverity.INFO,
            message=f"Generic validation: {rule.description}",
            affected_fields=rule.source_fields,
            suggested_corrections=[]
        )
    
    def _parse_date(self, date_str: str) -> Optional[date]:
        """Parse date string into date object"""
        
        date_str = date_str.strip()
        
        # Common date formats
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
    
    def generate_validation_summary(self, validation_results: List[CrossFieldValidationResult]) -> Dict[str, Any]:
        """Generate summary of cross-field validation results"""
        
        total_validations = len(validation_results)
        errors = [r for r in validation_results if r.severity == ValidationSeverity.ERROR and not r.is_valid]
        warnings = [r for r in validation_results if r.severity == ValidationSeverity.WARNING and not r.is_valid]
        infos = [r for r in validation_results if r.severity == ValidationSeverity.INFO and not r.is_valid]
        
        return {
            "total_validations": total_validations,
            "total_errors": len(errors),
            "total_warnings": len(warnings),
            "total_infos": len(infos),
            "error_rate": len(errors) / total_validations if total_validations > 0 else 0,
            "overall_validity": len(errors) == 0,
            "critical_issues": [r.message for r in errors],
            "suggested_improvements": list(set([fix for r in validation_results for fix in r.suggested_corrections]))
        }