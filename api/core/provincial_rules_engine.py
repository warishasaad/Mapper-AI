"""
Provincial Rules Engine for Canadian Estate Processing

Handles provincial-specific legal requirements, validation rules,
and processing variations across Canadian jurisdictions.
"""

import logging
import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime, date
from decimal import Decimal

from .models import (
    ProvincialJurisdiction, ProvincialRule, JurisdictionalContext,
    MappingResult, ValidationSeverity, FieldType
)

@dataclass
class ProvincialValidationResult:
    """Result of provincial validation"""
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    has_requirements: bool
    jurisdiction_specific_notes: List[str]
    legal_references: List[str]

class ProvincialRulesEngine:
    """Complete provincial rules engine for Canadian estate processing"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.rules_database = self._load_provincial_rules()
        self.form_requirements = self._load_form_requirements()
        self.fee_schedules = self._load_fee_schedules()
        self.court_registries = self._load_court_registries()
        self.processing_timelines = self._load_processing_timelines()
        
        self.logger.info("Provincial Rules Engine initialized for all Canadian jurisdictions")
    
    def _load_provincial_rules(self) -> Dict[ProvincialJurisdiction, List[ProvincialRule]]:
        """Load comprehensive provincial rules database"""
        
        rules = {}
        
        # Ontario Rules
        ontario_rules = [
            ProvincialRule(
                rule_id="ON_PROBATE_THRESHOLD",
                jurisdiction=ProvincialJurisdiction.ONTARIO,
                rule_type="estate_value_threshold",
                description="Probate required for estates over $50,000",
                applies_to_forms=["probate_application", "estate_certificate"],
                rule_logic="estate_value > 50000",
                validation_function="validate_ontario_probate_threshold",
                error_message="Estate value exceeds $50,000 - probate application required",
                legal_reference="Estate Administration Act, R.S.O. 1990, c. E.22, s. 2"
            ),
            ProvincialRule(
                rule_id="ON_ESTATE_TRUSTEE_REQUIREMENTS",
                jurisdiction=ProvincialJurisdiction.ONTARIO,
                rule_type="executor_requirements",
                description="Estate trustee must be 18+ and mentally capable",
                applies_to_forms=["probate_application"],
                rule_logic="executor_age >= 18 AND executor_mentally_capable == true",
                error_message="Estate trustee must be at least 18 years old and mentally capable",
                legal_reference="Estates Act, R.S.O. 1990, c. E.21, s. 29"
            ),
            ProvincialRule(
                rule_id="ON_SPOUSE_PREFERENTIAL_SHARE",
                jurisdiction=ProvincialJurisdiction.ONTARIO,
                rule_type="inheritance_rights",
                description="Surviving spouse entitled to preferential share",
                applies_to_forms=["estate_distribution"],
                rule_logic="has_surviving_spouse == true",
                error_message="Surviving spouse inheritance rights must be considered",
                legal_reference="Succession Law Reform Act, R.S.O. 1990, c. S.26, s. 44"
            ),
            ProvincialRule(
                rule_id="ON_FORMAL_PROOF_REQUIRED",
                jurisdiction=ProvincialJurisdiction.ONTARIO,
                rule_type="documentation",
                description="Formal proof of will required in contested cases",
                applies_to_forms=["probate_application"],
                rule_logic="will_contested == true",
                error_message="Formal proof of will required for contested estates"
            )
        ]
        
        # British Columbia Rules
        bc_rules = [
            ProvincialRule(
                rule_id="BC_PROBATE_THRESHOLD",
                jurisdiction=ProvincialJurisdiction.BRITISH_COLUMBIA,
                rule_type="estate_value_threshold",
                description="Probate required for estates over $25,000",
                applies_to_forms=["probate_application"],
                rule_logic="estate_value > 25000",
                error_message="Estate value exceeds $25,000 - probate application required",
                legal_reference="Wills, Estates and Succession Act, S.B.C. 2009, c. 13"
            ),
            ProvincialRule(
                rule_id="BC_REPRESENTATION_AGREEMENT",
                jurisdiction=ProvincialJurisdiction.BRITISH_COLUMBIA,
                rule_type="incapacity_planning",
                description="Representation agreements must be considered",
                applies_to_forms=["estate_administration"],
                rule_logic="deceased_had_representation_agreement == true",
                error_message="Check for valid representation agreements"
            ),
            ProvincialRule(
                rule_id="BC_SPOUSAL_PROPERTY_RIGHTS",
                jurisdiction=ProvincialJurisdiction.BRITISH_COLUMBIA,
                rule_type="property_rights",
                description="Family Property Act applies to spousal property",
                applies_to_forms=["estate_distribution"],
                rule_logic="has_surviving_spouse == true",
                error_message="BC Family Property Act considerations required"
            )
        ]
        
        # Alberta Rules
        alberta_rules = [
            ProvincialRule(
                rule_id="AB_PROBATE_THRESHOLD",
                jurisdiction=ProvincialJurisdiction.ALBERTA,
                rule_type="estate_value_threshold",
                description="No minimum threshold for probate in Alberta",
                applies_to_forms=["probate_application"],
                rule_logic="true",  # Always applicable
                error_message="",
                legal_reference="Wills and Succession Act, S.A. 2010, c. W-12.2"
            ),
            ProvincialRule(
                rule_id="AB_FAMILY_MAINTENANCE_SUPPORT",
                jurisdiction=ProvincialJurisdiction.ALBERTA,
                rule_type="family_support",
                description="Family maintenance and support obligations",
                applies_to_forms=["estate_distribution"],
                rule_logic="has_dependents == true",
                error_message="Family maintenance obligations must be considered"
            )
        ]
        
        # Quebec Rules (Civil Law System)
        quebec_rules = [
            ProvincialRule(
                rule_id="QC_NOTARIAL_WILL",
                jurisdiction=ProvincialJurisdiction.QUEBEC,
                rule_type="will_validation",
                description="Notarial wills have special status in Quebec",
                applies_to_forms=["probate_application"],
                rule_logic="will_type == 'notarial'",
                error_message="Notarial will procedures apply",
                legal_reference="Civil Code of Québec, art. 712-730"
            ),
            ProvincialRule(
                rule_id="QC_MATRIMONIAL_REGIME",
                jurisdiction=ProvincialJurisdiction.QUEBEC,
                rule_type="matrimonial_property",
                description="Matrimonial regime affects inheritance",
                applies_to_forms=["estate_distribution"],
                rule_logic="has_surviving_spouse == true",
                error_message="Quebec matrimonial regime must be determined"
            ),
            ProvincialRule(
                rule_id="QC_FRENCH_LANGUAGE_REQUIREMENT",
                jurisdiction=ProvincialJurisdiction.QUEBEC,
                rule_type="language_requirement",
                description="Documents may need French translation",
                applies_to_forms=["all"],
                rule_logic="document_language != 'french'",
                error_message="French translation may be required"
            )
        ]
        
        # Populate other provinces with basic rules
        manitoba_rules = self._create_basic_provincial_rules(ProvincialJurisdiction.MANITOBA, 10000)
        saskatchewan_rules = self._create_basic_provincial_rules(ProvincialJurisdiction.SASKATCHEWAN, 10000)
        nova_scotia_rules = self._create_basic_provincial_rules(ProvincialJurisdiction.NOVA_SCOTIA, 15000)
        new_brunswick_rules = self._create_basic_provincial_rules(ProvincialJurisdiction.NEW_BRUNSWICK, 15000)
        newfoundland_rules = self._create_basic_provincial_rules(ProvincialJurisdiction.NEWFOUNDLAND_LABRADOR, 1000)
        pei_rules = self._create_basic_provincial_rules(ProvincialJurisdiction.PRINCE_EDWARD_ISLAND, 10000)
        
        # Territory rules
        nwt_rules = self._create_basic_provincial_rules(ProvincialJurisdiction.NORTHWEST_TERRITORIES, 10000)
        nunavut_rules = self._create_basic_provincial_rules(ProvincialJurisdiction.NUNAVUT, 10000)
        yukon_rules = self._create_basic_provincial_rules(ProvincialJurisdiction.YUKON, 10000)
        
        rules.update({
            ProvincialJurisdiction.ONTARIO: ontario_rules,
            ProvincialJurisdiction.BRITISH_COLUMBIA: bc_rules,
            ProvincialJurisdiction.ALBERTA: alberta_rules,
            ProvincialJurisdiction.QUEBEC: quebec_rules,
            ProvincialJurisdiction.MANITOBA: manitoba_rules,
            ProvincialJurisdiction.SASKATCHEWAN: saskatchewan_rules,
            ProvincialJurisdiction.NOVA_SCOTIA: nova_scotia_rules,
            ProvincialJurisdiction.NEW_BRUNSWICK: new_brunswick_rules,
            ProvincialJurisdiction.NEWFOUNDLAND_LABRADOR: newfoundland_rules,
            ProvincialJurisdiction.PRINCE_EDWARD_ISLAND: pei_rules,
            ProvincialJurisdiction.NORTHWEST_TERRITORIES: nwt_rules,
            ProvincialJurisdiction.NUNAVUT: nunavut_rules,
            ProvincialJurisdiction.YUKON: yukon_rules
        })
        
        return rules
    
    def _create_basic_provincial_rules(self, jurisdiction: ProvincialJurisdiction, 
                                     probate_threshold: int) -> List[ProvincialRule]:
        """Create basic provincial rules template"""
        
        return [
            ProvincialRule(
                rule_id=f"{jurisdiction.value}_PROBATE_THRESHOLD",
                jurisdiction=jurisdiction,
                rule_type="estate_value_threshold",
                description=f"Probate threshold for {jurisdiction.value}",
                applies_to_forms=["probate_application"],
                rule_logic=f"estate_value > {probate_threshold}",
                error_message=f"Estate value exceeds ${probate_threshold:,} - probate may be required"
            ),
            ProvincialRule(
                rule_id=f"{jurisdiction.value}_EXECUTOR_CAPACITY",
                jurisdiction=jurisdiction,
                rule_type="executor_requirements",
                description="Executor capacity requirements",
                applies_to_forms=["probate_application"],
                rule_logic="executor_age >= 18",
                error_message="Executor must be at least 18 years old"
            )
        ]
    
    def _load_form_requirements(self) -> Dict[str, Dict[ProvincialJurisdiction, List[str]]]:
        """Load form-specific requirements by jurisdiction"""
        
        return {
            "probate_application": {
                ProvincialJurisdiction.ONTARIO: [
                    "Form 74.4 - Application for Certificate of Appointment of Estate Trustee with a Will",
                    "Original will or certified copy",
                    "Death certificate",
                    "Affidavit of execution (if required)",
                    "Estate administration tax calculation"
                ],
                ProvincialJurisdiction.BRITISH_COLUMBIA: [
                    "Form P2 - Petition for Probate",
                    "Original will",
                    "Death certificate", 
                    "Affidavit of attesting witness",
                    "Probate fee calculation"
                ],
                ProvincialJurisdiction.ALBERTA: [
                    "Form 74.4 - Application for Grant of Probate",
                    "Original will",
                    "Death certificate",
                    "Affidavit of executor",
                    "Court filing fee"
                ]
            },
            "administration_application": {
                ProvincialJurisdiction.ONTARIO: [
                    "Form 74.14 - Application for Certificate of Appointment of Estate Trustee without a Will",
                    "Death certificate",
                    "Bond (if required)",
                    "Consent of beneficiaries",
                    "Estate administration tax"
                ]
            }
        }
    
    def _load_fee_schedules(self) -> Dict[ProvincialJurisdiction, Dict[str, Any]]:
        """Load provincial fee schedules"""
        
        return {
            ProvincialJurisdiction.ONTARIO: {
                "estate_administration_tax": {
                    "calculation": "tiered",
                    "rates": [
                        {"threshold": 50000, "rate": 0.005},  # 0.5% on first $50k
                        {"threshold": float('inf'), "rate": 0.015}  # 1.5% on remainder
                    ]
                },
                "court_filing_fees": {"probate": 75, "administration": 75}
            },
            ProvincialJurisdiction.BRITISH_COLUMBIA: {
                "probate_fees": {
                    "calculation": "tiered",
                    "rates": [
                        {"threshold": 25000, "rate": 0},
                        {"threshold": 50000, "rate": 0.006},  # 0.6%
                        {"threshold": float('inf'), "rate": 0.014}  # 1.4%
                    ]
                }
            },
            ProvincialJurisdiction.ALBERTA: {
                "court_fees": {"probate": 135, "administration": 135},
                "surrogate_fees": {"probate": 35, "administration": 35}
            }
        }
    
    def _load_court_registries(self) -> Dict[ProvincialJurisdiction, List[Dict[str, str]]]:
        """Load court registry information"""
        
        return {
            ProvincialJurisdiction.ONTARIO: [
                {
                    "name": "Superior Court of Justice - Toronto",
                    "address": "393 University Avenue, Toronto, ON M5G 1E6",
                    "jurisdiction": "Central East Region"
                },
                {
                    "name": "Superior Court of Justice - Ottawa",
                    "address": "161 Elgin Street, Ottawa, ON K2P 2K1", 
                    "jurisdiction": "East Region"
                }
            ],
            ProvincialJurisdiction.BRITISH_COLUMBIA: [
                {
                    "name": "Supreme Court of BC - Vancouver Registry",
                    "address": "800 Smithe Street, Vancouver, BC V6Z 2E1",
                    "jurisdiction": "Vancouver"
                }
            ]
        }
    
    def _load_processing_timelines(self) -> Dict[ProvincialJurisdiction, Dict[str, int]]:
        """Load typical processing timelines by jurisdiction"""
        
        return {
            ProvincialJurisdiction.ONTARIO: {
                "probate_application": 30,  # days
                "administration_application": 45,
                "estate_certificate": 14
            },
            ProvincialJurisdiction.BRITISH_COLUMBIA: {
                "probate_application": 21,
                "administration_application": 30
            },
            ProvincialJurisdiction.ALBERTA: {
                "probate_application": 14,
                "administration_application": 21
            }
        }
    
    async def get_applicable_rules(self, jurisdiction: ProvincialJurisdiction, 
                                 form_type: str) -> List[ProvincialRule]:
        """Get applicable rules for jurisdiction and form type"""
        
        jurisdiction_rules = self.rules_database.get(jurisdiction, [])
        applicable_rules = []
        
        for rule in jurisdiction_rules:
            if form_type in rule.applies_to_forms or "all" in rule.applies_to_forms:
                # Check if rule is currently effective
                if self._is_rule_effective(rule):
                    applicable_rules.append(rule)
        
        self.logger.debug(f"Found {len(applicable_rules)} applicable rules for {jurisdiction.value} {form_type}")
        return applicable_rules
    
    def _is_rule_effective(self, rule: ProvincialRule) -> bool:
        """Check if rule is currently effective"""
        
        current_date = datetime.now().date()
        
        if rule.effective_date and current_date < rule.effective_date.date():
            return False
        
        if rule.expiry_date and current_date > rule.expiry_date.date():
            return False
        
        return True
    
    async def validate_field(self, mapping_result: MappingResult, 
                           jurisdiction: ProvincialJurisdiction,
                           applicable_rules: List[ProvincialRule]) -> ProvincialValidationResult:
        """Validate field against provincial rules"""
        
        errors = []
        warnings = []
        jurisdiction_notes = []
        legal_references = []
        has_requirements = False
        
        field_value = mapping_result.metadata.get("field_value", "") if mapping_result.metadata else ""
        
        for rule in applicable_rules:
            try:
                validation_result = await self._apply_validation_rule(
                    rule, mapping_result, field_value, jurisdiction
                )
                
                if not validation_result["is_valid"]:
                    has_requirements = True
                    
                    if rule.rule_type in ["estate_value_threshold", "executor_requirements"]:
                        errors.append(rule.error_message)
                    else:
                        warnings.append(rule.error_message)
                
                if rule.legal_reference:
                    legal_references.append(rule.legal_reference)
                
                # Add jurisdiction-specific notes
                if validation_result.get("notes"):
                    jurisdiction_notes.extend(validation_result["notes"])
                
            except Exception as e:
                self.logger.error(f"Error applying rule {rule.rule_id}: {e}")
                warnings.append(f"Unable to validate rule: {rule.description}")
        
        # Special validations by jurisdiction
        await self._apply_jurisdiction_specific_validations(
            mapping_result, jurisdiction, errors, warnings, jurisdiction_notes
        )
        
        return ProvincialValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            has_requirements=has_requirements,
            jurisdiction_specific_notes=jurisdiction_notes,
            legal_references=list(set(legal_references))
        )
    
    async def _apply_validation_rule(self, rule: ProvincialRule, mapping_result: MappingResult,
                                   field_value: str, jurisdiction: ProvincialJurisdiction) -> Dict[str, Any]:
        """Apply specific validation rule"""
        
        if rule.validation_function:
            # Call custom validation function
            return await self._call_custom_validation(rule, mapping_result, field_value)
        else:
            # Apply generic rule logic
            return await self._apply_generic_rule_logic(rule, mapping_result, field_value)
    
    async def _call_custom_validation(self, rule: ProvincialRule, mapping_result: MappingResult,
                                    field_value: str) -> Dict[str, Any]:
        """Call custom validation function"""
        
        # Map of custom validation functions
        validation_functions = {
            "validate_ontario_probate_threshold": self._validate_ontario_probate_threshold,
            "validate_bc_probate_threshold": self._validate_bc_probate_threshold,
            "validate_executor_capacity": self._validate_executor_capacity,
            "validate_quebec_language": self._validate_quebec_language
        }
        
        if rule.validation_function in validation_functions:
            return await validation_functions[rule.validation_function](mapping_result, field_value)
        else:
            return {"is_valid": True, "notes": []}
    
    async def _apply_generic_rule_logic(self, rule: ProvincialRule, mapping_result: MappingResult,
                                      field_value: str) -> Dict[str, Any]:
        """Apply generic rule logic"""
        
        # Simple rule evaluation
        if "estate_value" in rule.rule_logic and "estate" in mapping_result.cadence_path.lower():
            try:
                # Extract numeric value from field
                import re
                numeric_value = re.sub(r'[^\d.]', '', field_value)
                if numeric_value:
                    estate_value = float(numeric_value)
                    threshold = self._extract_threshold_from_rule(rule.rule_logic)
                    
                    if threshold and estate_value > threshold:
                        return {"is_valid": False, "notes": [f"Estate value ${estate_value:,.2f} exceeds threshold"]}
            except (ValueError, AttributeError):
                pass
        
        return {"is_valid": True, "notes": []}
    
    def _extract_threshold_from_rule(self, rule_logic: str) -> Optional[float]:
        """Extract numeric threshold from rule logic"""
        import re
        match = re.search(r'(\d+)', rule_logic)
        return float(match.group(1)) if match else None
    
    async def _validate_ontario_probate_threshold(self, mapping_result: MappingResult, 
                                                field_value: str) -> Dict[str, Any]:
        """Ontario-specific probate threshold validation"""
        
        if "estate" in mapping_result.cadence_path.lower() and "value" in mapping_result.cadence_path.lower():
            try:
                import re
                numeric_value = re.sub(r'[^\d.]', '', field_value)
                if numeric_value:
                    estate_value = float(numeric_value)
                    
                    if estate_value > 50000:
                        return {
                            "is_valid": False,
                            "notes": [
                                f"Estate value ${estate_value:,.2f} exceeds Ontario threshold of $50,000",
                                "Probate application required",
                                "Estate Administration Tax applies"
                            ]
                        }
                    elif estate_value > 1000:
                        return {
                            "is_valid": True,
                            "notes": [
                                f"Estate value ${estate_value:,.2f} may qualify for simplified process",
                                "Consider small estate certificate if applicable"
                            ]
                        }
            except ValueError:
                return {"is_valid": True, "notes": ["Unable to parse estate value"]}
        
        return {"is_valid": True, "notes": []}
    
    async def _validate_bc_probate_threshold(self, mapping_result: MappingResult,
                                           field_value: str) -> Dict[str, Any]:
        """BC-specific probate threshold validation"""
        
        if "estate" in mapping_result.cadence_path.lower() and "value" in mapping_result.cadence_path.lower():
            try:
                import re
                numeric_value = re.sub(r'[^\d.]', '', field_value)
                if numeric_value:
                    estate_value = float(numeric_value)
                    
                    if estate_value > 25000:
                        return {
                            "is_valid": False,
                            "notes": [
                                f"Estate value ${estate_value:,.2f} exceeds BC threshold of $25,000",
                                "Probate fees apply on tiered scale"
                            ]
                        }
            except ValueError:
                pass
        
        return {"is_valid": True, "notes": []}
    
    async def _validate_executor_capacity(self, mapping_result: MappingResult,
                                        field_value: str) -> Dict[str, Any]:
        """Validate executor capacity requirements"""
        
        if "executor" in mapping_result.cadence_path.lower() or "estate_rep" in mapping_result.cadence_path.lower():
            # Would implement age and capacity checks
            return {
                "is_valid": True,
                "notes": ["Verify executor is 18+ and mentally capable"]
            }
        
        return {"is_valid": True, "notes": []}
    
    async def _validate_quebec_language(self, mapping_result: MappingResult,
                                      field_value: str) -> Dict[str, Any]:
        """Quebec language requirement validation"""
        
        # Simple check for French characters or common French words
        french_indicators = ['québec', 'montreal', 'à', 'é', 'è', 'ç', 'notaire', 'testament']
        
        if any(indicator in field_value.lower() for indicator in french_indicators):
            return {
                "is_valid": True,
                "notes": ["Document appears to contain French content"]
            }
        else:
            return {
                "is_valid": False,
                "notes": ["Consider French translation requirements for Quebec"]
            }
    
    async def _apply_jurisdiction_specific_validations(self, mapping_result: MappingResult,
                                                     jurisdiction: ProvincialJurisdiction,
                                                     errors: List[str], warnings: List[str],
                                                     notes: List[str]):
        """Apply jurisdiction-specific validations"""
        
        if jurisdiction == ProvincialJurisdiction.QUEBEC:
            # Quebec Civil Law considerations
            if mapping_result.field_type == FieldType.LEGAL:
                notes.append("Quebec Civil Law applies - consult notary if needed")
        
        elif jurisdiction == ProvincialJurisdiction.ONTARIO:
            # Ontario-specific checks
            if "sin" in mapping_result.cadence_path.lower():
                notes.append("SIN verification required for Ontario estate tax purposes")
        
        elif jurisdiction == ProvincialJurisdiction.BRITISH_COLUMBIA:
            # BC-specific checks
            if mapping_result.field_type == FieldType.PROPERTY:
                notes.append("BC Property Transfer Tax may apply")
    
    def calculate_provincial_fees(self, jurisdiction: ProvincialJurisdiction,
                                form_type: str, estate_value: float) -> Dict[str, float]:
        """Calculate provincial fees for estate processing"""
        
        fee_schedule = self.fee_schedules.get(jurisdiction, {})
        fees = {}
        
        if jurisdiction == ProvincialJurisdiction.ONTARIO:
            if form_type in ["probate_application", "administration_application"]:
                # Estate Administration Tax
                if estate_value > 1000:
                    if estate_value <= 50000:
                        fees["estate_administration_tax"] = estate_value * 0.005
                    else:
                        fees["estate_administration_tax"] = (50000 * 0.005) + ((estate_value - 50000) * 0.015)
                
                fees["court_filing_fee"] = 75
        
        elif jurisdiction == ProvincialJurisdiction.BRITISH_COLUMBIA:
            if form_type == "probate_application":
                # BC Probate Fees
                if estate_value > 25000:
                    if estate_value <= 50000:
                        fees["probate_fee"] = (estate_value - 25000) * 0.006
                    else:
                        fees["probate_fee"] = (25000 * 0.006) + ((estate_value - 50000) * 0.014)
        
        elif jurisdiction == ProvincialJurisdiction.ALBERTA:
            fees["court_fee"] = 135
            fees["surrogate_fee"] = 35
        
        return fees
    
    def get_required_documents(self, jurisdiction: ProvincialJurisdiction,
                             form_type: str) -> List[str]:
        """Get required documents for jurisdiction and form type"""
        
        requirements = self.form_requirements.get(form_type, {})
        return requirements.get(jurisdiction, [])
    
    def get_processing_timeline(self, jurisdiction: ProvincialJurisdiction,
                              form_type: str) -> Optional[int]:
        """Get typical processing timeline in days"""
        
        timelines = self.processing_timelines.get(jurisdiction, {})
        return timelines.get(form_type)
    
    def get_court_registries(self, jurisdiction: ProvincialJurisdiction) -> List[Dict[str, str]]:
        """Get court registries for jurisdiction"""
        
        return self.court_registries.get(jurisdiction, [])
    
    def get_jurisdiction_summary(self, jurisdiction: ProvincialJurisdiction) -> Dict[str, Any]:
        """Get comprehensive jurisdiction summary"""
        
        rules = self.rules_database.get(jurisdiction, [])
        fees = self.fee_schedules.get(jurisdiction, {})
        registries = self.court_registries.get(jurisdiction, [])
        timelines = self.processing_timelines.get(jurisdiction, {})
        
        return {
            "jurisdiction": jurisdiction.value,
            "total_rules": len(rules),
            "rule_types": list(set(rule.rule_type for rule in rules)),
            "has_fee_schedule": bool(fees),
            "court_registries": len(registries),
            "processing_timelines": timelines,
            "special_considerations": self._get_special_considerations(jurisdiction)
        }
    
    def _get_special_considerations(self, jurisdiction: ProvincialJurisdiction) -> List[str]:
        """Get special considerations for jurisdiction"""
        
        considerations = {
            ProvincialJurisdiction.QUEBEC: [
                "Civil Law system applies",
                "French language requirements may apply",
                "Notarial wills have special status",
                "Matrimonial regime affects inheritance"
            ],
            ProvincialJurisdiction.ONTARIO: [
                "Estate Administration Tax applies",
                "Family Law Act affects spousal rights",
                "Succession Law Reform Act governs intestacy"
            ],
            ProvincialJurisdiction.BRITISH_COLUMBIA: [
                "Wills, Estates and Succession Act applies",
                "Family Property Act affects spousal property",
                "Representation agreements considered"
            ],
            ProvincialJurisdiction.ALBERTA: [
                "Wills and Succession Act governs",
                "Family maintenance obligations apply",
                "No minimum probate threshold"
            ]
        }
        
        return considerations.get(jurisdiction, ["Standard estate administration rules apply"])
