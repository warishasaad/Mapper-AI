import re
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from .models import SubjectRole, SubjectDetectionResult

@dataclass
class PathResolutionResult:
    original_path: str
    resolved_path: str
    confidence: float
    resolution_method: str
    metadata: Dict[str, Any]

class DynamicPathResolver:
    """Resolves applicant.* paths to subject-specific schema paths"""
    
    def __init__(self, schema_config: Dict):
        self.logger = logging.getLogger(__name__)
        self.schema_config = schema_config
        self.path_mappings = self._build_path_mappings()
        self.alias_manager = FieldAliasManager() 
        self.statistics = {
            'resolutions': 0,
            'successful_resolutions': 0,
            'fallback_resolutions': 0
        }
    
    def resolve_path(self, field_path: str, subject_result: SubjectDetectionResult,
                    context: Dict = None) -> PathResolutionResult:
        """Main path resolution method"""
        self.statistics['resolutions'] += 1
        
        if field_path.startswith('applicant.'):
            return self._resolve_applicant_path(field_path, subject_result, context)
        
        return PathResolutionResult(
            original_path=field_path,
            resolved_path=field_path,
            confidence=1.0,
            resolution_method='no_op',
            metadata={'reason': 'Path does not start with applicant.'}
        )
    
    def _resolve_applicant_path(self, field_path: str, subject_result: SubjectDetectionResult,
                               context: Dict) -> PathResolutionResult:
        """Resolve applicant.* paths to subject-specific paths"""
        
        field_component = field_path.split('.', 1)[1] if '.' in field_path else ''
        subject_role = subject_result.role
        
        # --- START: NEW AND FINAL LOGIC ---
       
        specific_prefix_map = {
            SubjectRole.SPOUSE: 'spouse',
            SubjectRole.CHILD: 'child',
            SubjectRole.EXECUTOR: 'executor',
            SubjectRole.ADMINISTRATOR: 'administrator',
            SubjectRole.TRUSTEE: 'trustee'
        }
        target_prefix = specific_prefix_map.get(subject_role)
        
        if target_prefix:
            resolved_path = f"{target_prefix}.{field_component}"
            if self._validate_schema_path(resolved_path):
                self.statistics['successful_resolutions'] += 1
                return PathResolutionResult(
                    original_path=field_path,
                    resolved_path=resolved_path,
                    confidence=subject_result.confidence,
                    resolution_method='subject_role_mapping',
                    metadata={'subject_role': subject_role.value}
                )

        if self._validate_schema_path(field_path):
            self.statistics['successful_resolutions'] += 1
            return PathResolutionResult(
                original_path=field_path,
                resolved_path=field_path, 
                confidence=0.95,         
                resolution_method='applicant_path_confirmed',
                metadata={'subject_role': subject_role.value, 'reason': 'Generic role matches a valid applicant path.'}
            )
            
      
        return PathResolutionResult(
            original_path=field_path,
            resolved_path=field_path,
            confidence=0.3,
            resolution_method='no_resolution',
            metadata={'reason': 'No valid specific or generic schema path found.'}
        )
    
    def _validate_schema_path(self, path: str) -> bool:
        """Validate that a path or its prefix exists in the Cadence schema."""
        known_paths = self.schema_config.get('paths', {})
        if path in known_paths: return True
        if any(known_path.startswith(path + '.') for known_path in known_paths): return True
        if path == "applicant.full_name" and "applicant.name.first" in known_paths: return True
        if path == "applicant.signature": return True
        return False
    
    def _get_role_prefix(self, role: SubjectRole) -> str:
        """Get schema prefix for a subject role"""
        role_prefixes = {
            SubjectRole.SPOUSE: 'spouse', SubjectRole.CHILD: 'child', SubjectRole.EXECUTOR: 'executor',
            SubjectRole.ADMINISTRATOR: 'administrator', SubjectRole.TRUSTEE: 'trustee',
            SubjectRole.BENEFICIARY: 'beneficiary', SubjectRole.GUARDIAN: 'guardian', SubjectRole.ATTORNEY: 'attorney'
        }
        return role_prefixes.get(role, 'person')
    
    def _build_path_mappings(self) -> Dict:
        """Build comprehensive path mapping configurations"""
        return {
            'common_fields': ['name', 'firstName', 'lastName', 'middleName', 'address', 'city', 'province', 'postalCode', 'phone', 'email', 'dateOfBirth', 'socialInsuranceNumber'],
            'legal_fields': ['relationship', 'capacity', 'authority', 'appointmentDate', 'bondRequired', 'residency'],
            'financial_fields': ['compensation', 'expenses', 'bondAmount', 'estateClaim', 'debtOwed']
        }

class FieldAliasManager:
    """Manages field aliases and synonyms for path resolution"""
    
    def __init__(self):
        self.aliases = self._build_aliases()
    
    def normalize_field_name(self, field_name: str) -> str:
        """Normalize field name using aliases"""
        canonical = field_name.lower().replace(' ', '_')
        for canonical_name, aliases in self.aliases.items():
            if canonical in aliases:
                return canonical_name
        return canonical
    
    def _build_aliases(self) -> Dict[str, List[str]]:
        """Build comprehensive field alias mappings"""
        return {
            'name': ['full_name', 'fullName', 'legal_name', 'applicant_name'],
            'firstName': ['first_name', 'given_name', 'forename'],
            'lastName': ['last_name', 'surname', 'family_name'],
            'dateOfBirth': ['dob', 'birth_date', 'birthDate', 'date_born'],
            'socialInsuranceNumber': ['sin', 'ssn', 'social_security', 'tax_id'],
            'address': ['street_address', 'mailing_address', 'home_address'],
            'postalCode': ['postal_code', 'zip_code', 'zip'],
            'phone': ['telephone', 'phone_number', 'contact_number'],
            'email': ['email_address', 'electronic_mail']
        }