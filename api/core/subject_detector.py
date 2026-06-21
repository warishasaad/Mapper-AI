import re
import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

class SubjectRole(Enum):
    SPOUSE = "spouse"
    CHILD = "child"
    EXECUTOR = "executor"
    ADMINISTRATOR = "administrator"
    TRUSTEE = "trustee"
    BENEFICIARY = "beneficiary"
    GUARDIAN = "guardian"
    ATTORNEY = "attorney"
    UNKNOWN = "unknown"

@dataclass
class SubjectDetectionResult:
    role: SubjectRole
    confidence: float
    evidence: List[str]
    metadata: Dict[str, any]
    fallback_roles: List[SubjectRole]

@dataclass
class DetectionRule:
    rule_id: str
    role: SubjectRole
    field_patterns: List[str]
    value_patterns: List[str]
    weight: float
    context_requirements: List[str]

class EstateSubjectDetector:
    """Intelligent subject role detection for estate forms"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.logger = logging.getLogger(__name__)
        self.detection_rules = self._load_detection_rules(config_path)
        self.relationship_patterns = self._build_relationship_patterns()
        self.form_type_indicators = self._build_form_indicators()
        self.statistics = {'detections': 0, 'successes': 0, 'failures': 0}
        
        self.logger.info("Estate Subject Detector initialized")
    
    def _load_detection_rules(self, config_path: Optional[str] = None) -> List[DetectionRule]:
        """Load detection rules for subject role identification"""
        
        return [
            # Spouse detection rules
            DetectionRule(
                rule_id="SPOUSE_RELATIONSHIP_FIELD",
                role=SubjectRole.SPOUSE,
                field_patterns=["relationship", "applicant_relationship", "relationship_to_deceased"],
                value_patterns=[r"spouse", r"husband", r"wife", r"widow", r"widower", r"surviving spouse"],
                weight=0.9,
                context_requirements=[]
            ),
            
            DetectionRule(
                rule_id="SPOUSE_MARITAL_STATUS",
                role=SubjectRole.SPOUSE,
                field_patterns=["marital_status", "spouse_name", "marriage_date"],
                value_patterns=[r"married", r"common.?law", r"\.+"],  # non-empty for name fields
                weight=0.8,
                context_requirements=[]
            ),
            
            # Child detection rules
            DetectionRule(
                rule_id="CHILD_RELATIONSHIP_FIELD",
                role=SubjectRole.CHILD,
                field_patterns=["relationship", "applicant_relationship", "relationship_to_deceased"],
                value_patterns=[r"child", r"son", r"daughter", r"heir", r"offspring", r"adult child"],
                weight=0.9,
                context_requirements=[]
            ),
            
            DetectionRule(
                rule_id="CHILD_FAMILY_INDICATORS",
                role=SubjectRole.CHILD,
                field_patterns=["parent_name", "deceased_parent", "inheritance_share"],
                value_patterns=[r"\.+"],  # non-empty
                weight=0.7,
                context_requirements=[]
            ),
            
            # Executor detection rules
            DetectionRule(
                rule_id="EXECUTOR_RELATIONSHIP_FIELD",
                role=SubjectRole.EXECUTOR,
                field_patterns=["relationship", "applicant_relationship", "capacity", "authority_basis"],
                value_patterns=[r"executor", r"executrix", r"estate trustee", r"personal representative"],
                weight=0.95,
                context_requirements=[]
            ),
            
            DetectionRule(
                rule_id="EXECUTOR_WILL_INDICATORS",
                role=SubjectRole.EXECUTOR,
                field_patterns=["will_dated", "executor_appointment", "estate_value", "probate_application"],
                value_patterns=[r"\.+"],  # non-empty
                weight=0.8,
                context_requirements=["has_will"]
            ),
            
            # Administrator detection rules
            DetectionRule(
                rule_id="ADMINISTRATOR_RELATIONSHIP_FIELD",
                role=SubjectRole.ADMINISTRATOR,
                field_patterns=["relationship", "applicant_relationship", "capacity"],
                value_patterns=[r"administrator", r"administratrix", r"estate administrator"],
                weight=0.95,
                context_requirements=[]
            ),
            
            DetectionRule(
                rule_id="ADMINISTRATOR_INTESTATE_INDICATORS",
                role=SubjectRole.ADMINISTRATOR,
                field_patterns=["will_exists", "intestate", "no_will"],
                value_patterns=[r"no", r"false", r"intestate", r"without will"],
                weight=0.8,
                context_requirements=["no_will"]
            ),
            
            # Trustee detection rules
            DetectionRule(
                rule_id="TRUSTEE_PROFESSIONAL_INDICATORS",
                role=SubjectRole.TRUSTEE,
                field_patterns=["law_firm", "trust_company", "professional_capacity", "corporate_trustee"],
                value_patterns=[r"trust company", r"law firm", r"professional", r"corporate"],
                weight=0.9,
                context_requirements=[]
            ),
            
            DetectionRule(
                rule_id="TRUSTEE_RELATIONSHIP_FIELD",
                role=SubjectRole.TRUSTEE,
                field_patterns=["relationship", "capacity", "trustee_type"],
                value_patterns=[r"trustee", r"professional trustee", r"corporate trustee"],
                weight=0.8,
                context_requirements=[]
            ),
            
            # Beneficiary detection rules
            DetectionRule(
                rule_id="BENEFICIARY_RELATIONSHIP_FIELD",
                role=SubjectRole.BENEFICIARY,
                field_patterns=["relationship", "beneficiary_status", "inheritance_claim"],
                value_patterns=[r"beneficiary", r"heir", r"entitled", r"inherit"],
                weight=0.7,
                context_requirements=[]
            ),
            
            # Guardian detection rules
            DetectionRule(
                rule_id="GUARDIAN_MINOR_INDICATORS",
                role=SubjectRole.GUARDIAN,
                field_patterns=["guardian", "minor_children", "custody"],
                value_patterns=[r"guardian", r"custody", r"minor"],
                weight=0.8,
                context_requirements=["has_minor_children"]
            ),
            
            # Attorney detection rules
            DetectionRule(
                rule_id="ATTORNEY_PROFESSIONAL_INDICATORS",
                role=SubjectRole.ATTORNEY,
                field_patterns=["law_firm", "lawyer", "attorney", "legal_counsel"],
                value_patterns=[r"lawyer", r"attorney", r"counsel", r"barrister", r"solicitor"],
                weight=0.9,
                context_requirements=[]
            )
        ]
    
    def detect_subject_role(self, form_data: Dict, context: Dict = None) -> SubjectDetectionResult:
        """Main detection method that analyzes form data to determine subject role"""
        self.statistics['detections'] += 1
        
        # Multi-factor detection approach
        relationship_score = self._analyze_relationship_fields(form_data)
        form_type_score = self._analyze_form_type(form_data, context)
        field_pattern_score = self._analyze_field_patterns(form_data)
        declaration_score = self._analyze_declarations(form_data)
        rule_based_score = self._analyze_detection_rules(form_data, context)
        
        # Combine scores using weighted ensemble
        final_scores = self._combine_detection_scores(
            relationship_score, form_type_score, field_pattern_score, declaration_score, rule_based_score
        )
        
        # Determine primary role with confidence
        primary_role, confidence = self._determine_primary_role(final_scores)
        
        # Generate evidence trail
        evidence = self._generate_evidence(form_data, primary_role)
        
        # Identify fallback roles
        fallback_roles = self._identify_fallback_roles(final_scores, primary_role)
        
        result = SubjectDetectionResult(
            role=primary_role,
            confidence=confidence,
            evidence=evidence,
            metadata={
                'detection_scores': final_scores,
                'form_type': context.get('form_type') if context else None,
                'province': context.get('province') if context else None
            },
            fallback_roles=fallback_roles
        )
        
        if confidence > 0.7:
            self.statistics['successes'] += 1
        else:
            self.statistics['failures'] += 1
            
        self.logger.info(f"Subject detection: {primary_role.value} (confidence: {confidence:.2f})")
        return result
    
    def _analyze_detection_rules(self, form_data: Dict, context: Dict = None) -> Dict[SubjectRole, float]:
        """Analyze form data using detection rules"""
        scores = {role: 0.0 for role in SubjectRole}
        
        for rule in self.detection_rules:
            # Check context requirements
            if not self._check_context_requirements(rule, form_data, context):
                continue
            
            # Check field patterns
            field_match = False
            for field_pattern in rule.field_patterns:
                matching_fields = [k for k in form_data.keys() if re.search(field_pattern, k, re.IGNORECASE)]
                if matching_fields:
                    field_match = True
                    break
            
            if not field_match:
                continue
            
            # Check value patterns
            value_match = False
            for field_key, field_value in form_data.items():
                if any(re.search(fp, field_key, re.IGNORECASE) for fp in rule.field_patterns):
                    str_value = str(field_value).lower()
                    for value_pattern in rule.value_patterns:
                        if re.search(value_pattern, str_value, re.IGNORECASE):
                            value_match = True
                            break
                    if value_match:
                        break
            
            if value_match:
                scores[rule.role] += rule.weight
        
        return scores
    
    def _check_context_requirements(self, rule: DetectionRule, form_data: Dict, context: Dict = None) -> bool:
        """Check if context requirements are met for a rule"""
        
        for requirement in rule.context_requirements:
            if requirement == "has_will":
                will_indicators = ["will_dated", "will_exists", "executor_appointment"]
                if not any(indicator in form_data for indicator in will_indicators):
                    return False
            elif requirement == "no_will":
                no_will_indicators = ["no_will", "intestate"]
                will_exists = any(indicator in form_data for indicator in ["will_dated", "will_exists"])
                no_will_stated = any(indicator in form_data for indicator in no_will_indicators)
                if will_exists and not no_will_stated:
                    return False
            elif requirement == "has_minor_children":
                minor_indicators = ["minor_children", "guardian", "custody"]
                if not any(indicator in form_data for indicator in minor_indicators):
                    return False
        
        return True
    
    def _analyze_relationship_fields(self, form_data: Dict) -> Dict[SubjectRole, float]:
        """Analyze relationship fields to determine subject role"""
        scores = {role: 0.0 for role in SubjectRole}
        
        relationship_fields = [
            'relationship_to_deceased', 'applicant_relationship', 'relationship',
            'applicant_type', 'capacity', 'authority_basis'
        ]
        
        for field in relationship_fields:
            if field in form_data:
                value = str(form_data[field]).lower()
                for role, patterns in self.relationship_patterns.items():
                    for pattern in patterns:
                        if re.search(pattern, value, re.IGNORECASE):
                            scores[role] += 0.8
                            break
        
        return scores
    
    def _analyze_form_type(self, form_data: Dict, context: Dict) -> Dict[SubjectRole, float]:
        """Analyze form type to infer likely subject roles"""
        scores = {role: 0.0 for role in SubjectRole}
        
        form_type = context.get('form_type') if context else None
        if not form_type:
            # Attempt to detect form type from data
            form_type = self._detect_form_type(form_data)
        
        if form_type in self.form_type_indicators:
            for role, weight in self.form_type_indicators[form_type].items():
                scores[role] += weight
        
        return scores
    
    def _detect_form_type(self, form_data: Dict) -> str:
        """Detect form type from field patterns"""
        
        # Probate application indicators
        probate_indicators = ['probate', 'executor', 'will_dated', 'estate_value', 'letters_probate']
        if any(indicator in str(form_data.keys()).lower() for indicator in probate_indicators):
            return 'probate_application'
        
        # Administration application indicators
        admin_indicators = ['administrator', 'intestate', 'no_will', 'letters_administration']
        if any(indicator in str(form_data.keys()).lower() for indicator in admin_indicators):
            return 'administration_application'
        
        # Death benefit indicators
        benefit_indicators = ['cpp', 'death_benefit', 'survivor_benefit', 'pension']
        if any(indicator in str(form_data.keys()).lower() for indicator in benefit_indicators):
            return 'death_benefit_application'
        
        # Small estate indicators
        small_estate_indicators = ['small_estate', 'estate_certificate', 'summary_administration']
        if any(indicator in str(form_data.keys()).lower() for indicator in small_estate_indicators):
            return 'small_estate_certificate'
        
        return 'estate_information'
    
    def _analyze_field_patterns(self, form_data: Dict) -> Dict[SubjectRole, float]:
        """Analyze field naming patterns and presence to determine role"""
        scores = {role: 0.0 for role in SubjectRole}
        
        # Spouse indicators
        spouse_fields = ['spouse_name', 'surviving_spouse', 'widow', 'widower', 'marriage_date']
        if any(field in form_data for field in spouse_fields):
            scores[SubjectRole.SPOUSE] += 0.6
        
        # Child indicators
        child_fields = ['parent_name', 'deceased_parent', 'inheritance_share']
        if any(field in form_data for field in child_fields):
            scores[SubjectRole.CHILD] += 0.5
        
        # Executor indicators
        executor_fields = ['will_dated', 'executor_appointment', 'estate_value', 'probate']
        if any(field in form_data for field in executor_fields):
            scores[SubjectRole.EXECUTOR] += 0.7
        
        # Professional indicators
        professional_fields = ['law_firm', 'trust_company', 'professional_capacity']
        if any(field in form_data for field in professional_fields):
            scores[SubjectRole.TRUSTEE] += 0.8
        
        return scores
    
    def _analyze_declarations(self, form_data: Dict) -> Dict[SubjectRole, float]:
        """Analyze declaration text to determine role"""
        scores = {role: 0.0 for role in SubjectRole}
        
        declaration_fields = ['declaration', 'oath', 'attestation', 'affirmation']
        declaration_text = ""
        
        for field in declaration_fields:
            if field in form_data:
                declaration_text += str(form_data[field]).lower() + " "
        
        if declaration_text:
            # Spouse declarations
            if re.search(r'surviving spouse|widow|widower|married to', declaration_text):
                scores[SubjectRole.SPOUSE] += 0.9
            
            # Executor declarations
            if re.search(r'executor|estate trustee|named in will|appointed', declaration_text):
                scores[SubjectRole.EXECUTOR] += 0.9
            
            # Child declarations
            if re.search(r'child of|heir|entitled to inherit', declaration_text):
                scores[SubjectRole.CHILD] += 0.8
        
        return scores
    
    def _combine_detection_scores(self, *score_dicts) -> Dict[SubjectRole, float]:
        """Combine multiple scoring methods using weighted ensemble"""
        combined = {role: 0.0 for role in SubjectRole}
        weights = [0.25, 0.2, 0.2, 0.15, 0.2]  # relationship, form_type, field_pattern, declaration, rule_based
        
        for i, score_dict in enumerate(score_dicts):
            weight = weights[i] if i < len(weights) else 0.1
            for role, score in score_dict.items():
                combined[role] += score * weight
        
        return combined
    
    def _determine_primary_role(self, scores: Dict[SubjectRole, float]) -> Tuple[SubjectRole, float]:
        """Determine primary role and confidence from combined scores"""
        # Remove unknown role from consideration
        filtered_scores = {k: v for k, v in scores.items() if k != SubjectRole.UNKNOWN}
        
        if not filtered_scores or max(filtered_scores.values()) == 0:
            return SubjectRole.UNKNOWN, 0.0
        
        primary_role = max(filtered_scores.keys(), key=lambda k: filtered_scores[k])
        max_score = filtered_scores[primary_role]
        
        # Calculate confidence based on score separation
        sorted_scores = sorted(filtered_scores.values(), reverse=True)
        if len(sorted_scores) > 1:
            confidence = min(1.0, max_score / (sorted_scores[1] + 0.1))
        else:
            confidence = min(1.0, max_score)
        
        return primary_role, confidence
    
    def _generate_evidence(self, form_data: Dict, primary_role: SubjectRole) -> List[str]:
        """Generate evidence trail for the detected role"""
        evidence = []
        
        # Look for direct relationship indicators
        relationship_fields = ['relationship_to_deceased', 'applicant_relationship', 'relationship']
        for field in relationship_fields:
            if field in form_data:
                value = str(form_data[field])
                if value and primary_role.value.lower() in value.lower():
                    evidence.append(f"Relationship field '{field}' contains '{value}'")
        
        # Look for role-specific field patterns
        role_fields = {
            SubjectRole.SPOUSE: ['spouse_name', 'marriage_date', 'widow', 'widower'],
            SubjectRole.CHILD: ['parent_name', 'inheritance_share'],
            SubjectRole.EXECUTOR: ['executor_appointment', 'will_dated', 'probate'],
            SubjectRole.ADMINISTRATOR: ['intestate', 'no_will'],
            SubjectRole.TRUSTEE: ['trust_company', 'professional_capacity']
        }
        
        if primary_role in role_fields:
            for field in role_fields[primary_role]:
                if field in form_data and form_data[field]:
                    evidence.append(f"Field '{field}' present with value")
        
        # Look for declaration evidence
        declaration_fields = ['declaration', 'oath', 'attestation']
        for field in declaration_fields:
            if field in form_data:
                value = str(form_data[field]).lower()
                if primary_role.value in value:
                    evidence.append(f"Declaration contains reference to {primary_role.value}")
        
        return evidence
    
    def _identify_fallback_roles(self, scores: Dict[SubjectRole, float], 
                                primary_role: SubjectRole) -> List[SubjectRole]:
        """Identify alternative roles based on scores"""
        
        # Sort roles by score, excluding primary role and unknown
        sorted_roles = sorted(
            [(role, score) for role, score in scores.items() 
             if role != primary_role and role != SubjectRole.UNKNOWN and score > 0],
            key=lambda x: x[1], reverse=True
        )
        
        # Return top 2 alternative roles
        return [role for role, score in sorted_roles[:2]]
    
    def _build_relationship_patterns(self) -> Dict[SubjectRole, List[str]]:
        """Build regex patterns for relationship detection"""
        return {
            SubjectRole.SPOUSE: [
                r'spouse', r'husband', r'wife', r'widow', r'widower',
                r'surviving spouse', r'married to', r'common.?law'
            ],
            SubjectRole.CHILD: [
                r'child', r'son', r'daughter', r'heir', r'offspring',
                r'adult child', r'next of kin'
            ],
            SubjectRole.EXECUTOR: [
                r'executor', r'executrix', r'estate trustee', r'personal representative',
                r'named in will', r'appointed by will'
            ],
            SubjectRole.ADMINISTRATOR: [
                r'administrator', r'administratrix', r'estate administrator',
                r'without will', r'intestate'
            ],
            SubjectRole.TRUSTEE: [
                r'trustee', r'trust company', r'professional trustee',
                r'corporate trustee'
            ],
            SubjectRole.BENEFICIARY: [
                r'beneficiary', r'heir', r'entitled', r'inherit'
            ],
            SubjectRole.GUARDIAN: [
                r'guardian', r'custody', r'minor'
            ],
            SubjectRole.ATTORNEY: [
                r'lawyer', r'attorney', r'counsel', r'barrister', r'solicitor'
            ]
        }
    
    def _build_form_indicators(self) -> Dict[str, Dict[SubjectRole, float]]:
        """Build form type indicators for role likelihood"""
        return {
            'probate_application': {
                SubjectRole.EXECUTOR: 0.8,
                SubjectRole.SPOUSE: 0.3,
                SubjectRole.CHILD: 0.2
            },
            'administration_application': {
                SubjectRole.ADMINISTRATOR: 0.8,
                SubjectRole.SPOUSE: 0.6,
                SubjectRole.CHILD: 0.5
            },
            'estate_certificate': {
                SubjectRole.SPOUSE: 0.7,
                SubjectRole.CHILD: 0.6,
                SubjectRole.EXECUTOR: 0.4
            },
            'small_estate_certificate': {
                SubjectRole.SPOUSE: 0.8,
                SubjectRole.CHILD: 0.7
            },
            'death_benefit_application': {
                SubjectRole.SPOUSE: 0.9,
                SubjectRole.CHILD: 0.7,
                SubjectRole.BENEFICIARY: 0.5
            },
            'estate_information': {
                SubjectRole.SPOUSE: 0.5,
                SubjectRole.CHILD: 0.5,
                SubjectRole.EXECUTOR: 0.4,
                SubjectRole.BENEFICIARY: 0.3
            }
        }
    
    def get_statistics(self) -> Dict:
        """Return detection statistics"""
        return self.statistics.copy()
    
    def reset_statistics(self):
        """Reset detection statistics"""
        self.statistics = {'detections': 0, 'successes': 0, 'failures': 0}
    
    def get_detection_summary(self) -> Dict:
        """Get summary of detection capabilities"""
        return {
            'supported_roles': [role.value for role in SubjectRole],
            'detection_rules_count': len(self.detection_rules),
            'relationship_patterns_count': sum(len(patterns) for patterns in self.relationship_patterns.values()),
            'form_types_supported': list(self.form_type_indicators.keys()),
            'statistics': self.get_statistics()
        }