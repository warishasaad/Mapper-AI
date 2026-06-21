"""
Form Completion Intelligence Engine - Advanced Form Analysis

Provides intelligent form completion analysis with dynamic required field determination,
completion scoring, smart recommendations, and progressive disclosure logic.
REAL USER DATA ONLY - Integrates with existing MapperAI conditional logic and AI enhancement.
"""

import time
import logging
from typing import Dict, List, Optional, Tuple, Set, Any
from dataclasses import dataclass, field
from enum import Enum
from .models import (
    ConditionalLogic, FieldDependency, MappingResult, FieldType,
    ProvincialJurisdiction, ValidationSeverity
)

# ==================== FORM COMPLETION DATA MODELS ====================

class CompletionPriority(Enum):
    """Priority levels for field completion"""
    CRITICAL = "critical"      # Must complete to proceed
    HIGH = "high"             # Important for form accuracy
    MEDIUM = "medium"         # Helpful but not essential
    LOW = "low"              # Optional enhancement
    CONDITIONAL = "conditional"  # Only needed under certain conditions

class DisclosureState(Enum):
    """Field disclosure states for progressive forms"""
    HIDDEN = "hidden"         # Not shown to user
    AVAILABLE = "available"   # Can be shown if requested
    VISIBLE = "visible"       # Currently displayed
    REQUIRED = "required"     # Must be completed
    COMPLETED = "completed"   # Already filled

class CompletionBarrier(Enum):
    """Types of barriers preventing form completion"""
    MISSING_CRITICAL = "missing_critical"
    CONDITIONAL_UNFULFILLED = "conditional_unfulfilled"
    VALIDATION_ERRORS = "validation_errors"
    DEPENDENT_FIELDS = "dependent_fields"
    SUBJECT_UNCLEAR = "subject_unclear"
    INSUFFICIENT_DATA = "insufficient_data"

@dataclass
class FieldCompletionStatus:
    """Status of individual field completion"""
    field_name: str
    cadence_path: str
    is_filled: bool
    field_value: Optional[str] = None
    is_required: bool = False
    priority: CompletionPriority = CompletionPriority.MEDIUM
    disclosure_state: DisclosureState = DisclosureState.VISIBLE
    conditional_logic: Optional[ConditionalLogic] = None
    validation_errors: List[str] = field(default_factory=list)
    depends_on: List[str] = field(default_factory=list)
    blocks: List[str] = field(default_factory=list)  # Fields this blocks
    completion_score: float = 0.0
    ai_suggestion: Optional[str] = None

@dataclass
class SectionCompletionStatus:
    """Completion status for form sections"""
    section_name: str
    fields: List[FieldCompletionStatus]
    is_conditional: bool = False
    should_display: bool = True
    condition_met: bool = True
    completion_percentage: float = 0.0
    required_fields_count: int = 0
    completed_required_count: int = 0
    blocking_dependencies: List[str] = field(default_factory=list)

@dataclass
class FormCompletionAnalysis:
    """Comprehensive form completion analysis"""
    overall_completion_score: float
    sections: List[SectionCompletionStatus]
    critical_missing: List[FieldCompletionStatus]
    next_recommended_fields: List[FieldCompletionStatus]
    completion_barriers: List[CompletionBarrier]
    progressive_disclosure_suggestions: List[str]
    estimated_time_remaining: float
    form_readiness_assessment: str
    actionable_recommendations: List[str]
    ai_insights: List[str] = field(default_factory=list)
    processing_metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class SmartRecommendation:
    """AI-enhanced smart recommendation for form completion"""
    field_name: str
    recommendation_type: str  # 'fill_next', 'validate', 'conditional_check', 'ai_suggestion'
    priority: CompletionPriority
    reasoning: str
    suggested_value: Optional[str] = None
    confidence: float = 1.0
    ai_generated: bool = False

# ==================== FORM COMPLETION ENGINE ====================

class FormCompletionEngine:
    """Advanced form completion intelligence with AI enhancement"""
    
    def __init__(self, conditional_parser=None, ai_enhancer=None, dynamic_subject_engine=None):
        self.conditional_parser = conditional_parser  # from form_logic_parser
        self.ai_enhancer = ai_enhancer  # from ai_enhancer  
        self.dynamic_subject_engine = dynamic_subject_engine
        self.logger = logging.getLogger(__name__)
        
        # Form completion rules and patterns
        self.completion_rules = self._load_completion_rules()
        self.field_priorities = self._load_field_priorities()
        self.section_dependencies = self._load_section_dependencies()
        
        # Processing statistics
        self.stats = {
            "analyses_performed": 0,
            "ai_recommendations_generated": 0,
            "progressive_disclosures_applied": 0,
            "completion_scores_calculated": 0,
            "barriers_identified": 0,
            "smart_suggestions_made": 0
        }
        
        self.logger.info("Form Completion Engine initialized - Real data processing with AI enhancement")
    
    def _load_completion_rules(self) -> Dict[str, Dict]:
        """Load form completion rules for estate forms"""
        return {
            # Critical fields that must be completed
            "critical_fields": {
                "deceased.name": {
                    "priority": CompletionPriority.CRITICAL,
                    "reasoning": "Deceased identification is mandatory for all estate forms"
                },
                "deceased.date_of_death": {
                    "priority": CompletionPriority.CRITICAL,
                    "reasoning": "Date of death required for legal processing"
                },
                "applicant.name": {
                    "priority": CompletionPriority.CRITICAL,
                    "reasoning": "Applicant identification required"
                }
            },
            
            # Conditional completion rules
            "conditional_rules": {
                "spouse_section": {
                    "condition": "task_planner.b_has_spouse == 'yes'",
                    "required_fields": ["spouse.name", "spouse.date_of_birth"],
                    "priority": CompletionPriority.HIGH,
                    "reasoning": "Spouse information required when spouse exists"
                },
                "children_section": {
                    "condition": "task_planner.b_has_children == 'yes'",
                    "required_fields": ["children[*].name", "children[*].date_of_birth"],
                    "priority": CompletionPriority.HIGH,
                    "reasoning": "Children information required when children exist"
                },
                "will_section": {
                    "condition": "task_planner.b_will == 'yes'",
                    "required_fields": ["will.location_hint", "estate_reps[*].name"],
                    "priority": CompletionPriority.HIGH,
                    "reasoning": "Will details required when will exists"
                }
            },
            
            # Progressive disclosure rules
            "progressive_disclosure": {
                "basic_info_first": [
                    "deceased.name", "deceased.date_of_death", "applicant.name", "applicant.relationship"
                ],
                "then_relationship_specific": {
                    "spouse": ["spouse.*", "marriage.*"],
                    "child": ["children.*", "parent.*"],
                    "executor": ["will.*", "estate_reps.*"]
                },
                "finally_details": [
                    "financial.*", "insurance.*", "property.*"
                ]
            }
        }
    
    def _load_field_priorities(self) -> Dict[str, CompletionPriority]:
        """Load field priority mappings for estate forms"""
        return {
            # Critical priorities
            "deceased.name": CompletionPriority.CRITICAL,
            "deceased.date_of_death": CompletionPriority.CRITICAL,
            "deceased.social_insurance_number": CompletionPriority.CRITICAL,
            "applicant.name": CompletionPriority.CRITICAL,
            "applicant.relationship": CompletionPriority.CRITICAL,
            
            # High priorities
            "deceased.place_of_death": CompletionPriority.HIGH,
            "deceased.date_of_birth": CompletionPriority.HIGH,
            "applicant.contact.*": CompletionPriority.HIGH,
            "task_planner.b_has_spouse": CompletionPriority.HIGH,
            "task_planner.b_has_children": CompletionPriority.HIGH,
            "task_planner.b_will": CompletionPriority.HIGH,
            
            # Medium priorities
            "spouse.*": CompletionPriority.MEDIUM,
            "children.*": CompletionPriority.MEDIUM,
            "estate_reps.*": CompletionPriority.MEDIUM,
            "will.*": CompletionPriority.MEDIUM,
            
            # Low priorities  
            "financial.*": CompletionPriority.LOW,
            "insurance.*": CompletionPriority.LOW,
            "property.*": CompletionPriority.LOW,
            "contact.*": CompletionPriority.LOW
        }
    
    def _load_section_dependencies(self) -> Dict[str, List[str]]:
        """Load section dependency mappings"""
        return {
            "deceased_information": [],  # No dependencies
            "applicant_information": ["deceased_information"],
            "spouse_information": ["applicant_information", "task_planner.b_has_spouse"],
            "children_information": ["applicant_information", "task_planner.b_has_children"],
            "will_information": ["applicant_information", "task_planner.b_will"],
            "estate_representatives": ["will_information"],
            "financial_information": ["applicant_information"],
            "insurance_information": ["applicant_information"],
            "property_information": ["applicant_information"]
        }
    
    async def analyze_form_completion(self, field_data: Dict[str, str], 
                                    mapping_results: List[MappingResult],
                                    form_type: Optional[str] = None) -> FormCompletionAnalysis:
        """Comprehensive form completion analysis with AI enhancement"""
        start_time = time.time()
        self.stats["analyses_performed"] += 1
        
        if not field_data and not mapping_results:
            raise ValueError("No field data or mapping results provided for completion analysis")
        
        # Phase 1: Build field completion status
        field_statuses = await self._build_field_completion_status(field_data, mapping_results)
        
        # Phase 2: Analyze conditional requirements
        conditional_requirements = await self._analyze_conditional_requirements(field_statuses, field_data)
        
        # Phase 3: Calculate section completion
        section_statuses = await self._analyze_section_completion(field_statuses, conditional_requirements)
        
        # Phase 4: Identify completion barriers
        barriers = await self._identify_completion_barriers(field_statuses, section_statuses)
        
        # Phase 5: Generate smart recommendations with AI
        recommendations = await self._generate_smart_recommendations(
            field_statuses, barriers, field_data, form_type
        )
        
        # Phase 6: Progressive disclosure analysis
        disclosure_suggestions = await self._analyze_progressive_disclosure(
            field_statuses, section_statuses, field_data
        )
        
        # Phase 7: Calculate overall metrics
        overall_score = self._calculate_overall_completion_score(section_statuses)
        
        # Phase 8: Generate actionable insights
        actionable_recommendations = await self._generate_actionable_recommendations(
            recommendations, barriers, section_statuses
        )
        
        # Phase 9: AI-enhanced insights (if available)
        ai_insights = await self._generate_ai_insights(field_data, recommendations, form_type)
        
        processing_time = time.time() - start_time
        
        return FormCompletionAnalysis(
            overall_completion_score=overall_score,
            sections=section_statuses,
            critical_missing=self._get_critical_missing_fields(field_statuses),
            next_recommended_fields=self._get_next_recommended_fields(recommendations),
            completion_barriers=barriers,
            progressive_disclosure_suggestions=disclosure_suggestions,
            estimated_time_remaining=self._estimate_completion_time(field_statuses),
            form_readiness_assessment=self._assess_form_readiness(overall_score, barriers),
            actionable_recommendations=actionable_recommendations,
            ai_insights=ai_insights,
            processing_metadata={
                "processing_time": processing_time,
                "fields_analyzed": len(field_statuses),
                "ai_enhanced": self.ai_enhancer is not None,
                "form_type": form_type,
                "analysis_timestamp": time.time()
            }
        )
    
    async def _build_field_completion_status(self, field_data: Dict[str, str], 
                                           mapping_results: List[MappingResult]) -> List[FieldCompletionStatus]:
        """Build comprehensive field completion status"""
        field_statuses = []
        
        # Create a mapping of field names to their mapped paths
        field_to_path = {}
        path_to_result = {}
        
        for result in mapping_results:
            field_to_path[result.field_name] = result.cadence_path
            path_to_result[result.cadence_path] = result
        
        # Analyze each field
        for field_name, field_value in field_data.items():
            cadence_path = field_to_path.get(field_name, "unknown.field")
            mapping_result = path_to_result.get(cadence_path)
            
            # Determine if field is filled
            is_filled = bool(field_value and field_value.strip() and 
                           field_value.strip().lower() not in ['n/a', 'none', ''])
            
            # Get priority
            priority = self._determine_field_priority(cadence_path, field_name)
            
            # Check if required
            is_required = self._is_field_required(cadence_path, field_name, field_data)
            
            # Get conditional logic
            conditional_logic = mapping_result.conditional_logic if mapping_result else None
            
            # Get validation errors
            validation_errors = mapping_result.validation_errors if mapping_result else []
            
            # Create field status
            status = FieldCompletionStatus(
                field_name=field_name,
                cadence_path=cadence_path,
                is_filled=is_filled,
                field_value=field_value,
                is_required=is_required,
                priority=priority,
                conditional_logic=conditional_logic,
                validation_errors=validation_errors,
                completion_score=self._calculate_field_completion_score(
                    is_filled, is_required, priority, validation_errors
                )
            )
            
            field_statuses.append(status)
        
        # Add missing critical fields
        await self._add_missing_critical_fields(field_statuses, field_data)
        
        return field_statuses
    
    async def _analyze_conditional_requirements(self, field_statuses: List[FieldCompletionStatus], 
                                              field_data: Dict[str, str]) -> Dict[str, bool]:
        """Analyze conditional logic to determine dynamic requirements"""
        conditional_requirements = {}
        
        # Check task planner conditions
        has_spouse = field_data.get("task_planner.b_has_spouse", "").lower() == "yes"
        has_children = field_data.get("task_planner.b_has_children", "").lower() == "yes"
        has_will = field_data.get("task_planner.b_will", "").lower() == "yes"
        
        # Infer conditions from relationship information
        if not has_spouse:
            relationship = field_data.get("applicant.relationship", "").lower()
            has_spouse = any(term in relationship for term in ["spouse", "husband", "wife", "widow"])
        
        if not has_children:
            children_mentioned = any("child" in key.lower() or "child" in value.lower() 
                                   for key, value in field_data.items())
            has_children = children_mentioned
        
        if not has_will:
            will_mentioned = any("will" in key.lower() or "executor" in key.lower() 
                               for key in field_data.keys())
            has_will = will_mentioned
        
        conditional_requirements.update({
            "spouse_section_required": has_spouse,
            "children_section_required": has_children,
            "will_section_required": has_will
        })
        
        # Update field requirements based on conditions
        for status in field_statuses:
            if "spouse" in status.cadence_path and has_spouse:
                status.is_required = True
                status.priority = CompletionPriority.HIGH
            elif "children" in status.cadence_path and has_children:
                status.is_required = True
                status.priority = CompletionPriority.HIGH
            elif "will" in status.cadence_path or "estate_reps" in status.cadence_path:
                if has_will:
                    status.is_required = True
                    status.priority = CompletionPriority.HIGH
        
        return conditional_requirements
    
    async def _analyze_section_completion(self, field_statuses: List[FieldCompletionStatus], 
                                        conditional_requirements: Dict[str, bool]) -> List[SectionCompletionStatus]:
        """Analyze completion status by form sections"""
        
        # Group fields by section
        sections = {
            "deceased_information": [],
            "applicant_information": [],
            "spouse_information": [],
            "children_information": [],
            "will_information": [],
            "estate_representatives": [],
            "financial_information": [],
            "insurance_information": [],
            "property_information": []
        }
        
        # Classify fields into sections
        for status in field_statuses:
            path = status.cadence_path.lower()
            
            if path.startswith("deceased."):
                sections["deceased_information"].append(status)
            elif path.startswith("applicant."):
                sections["applicant_information"].append(status)
            elif path.startswith("spouse."):
                sections["spouse_information"].append(status)
            elif "children" in path:
                sections["children_information"].append(status)
            elif path.startswith("will.") or "executor" in path:
                sections["will_information"].append(status)
            elif path.startswith("estate_reps"):
                sections["estate_representatives"].append(status)
            elif "financial" in path or "estate_value" in path:
                sections["financial_information"].append(status)
            elif "insurance" in path:
                sections["insurance_information"].append(status)
            elif "property" in path:
                sections["property_information"].append(status)
        
        # Create section statuses
        section_statuses = []
        
        for section_name, fields in sections.items():
            if not fields:
                continue
            
            # Determine if section is conditional
            is_conditional = section_name in ["spouse_information", "children_information", "will_information"]
            
            # Check if condition is met
            condition_met = True
            should_display = True
            
            if section_name == "spouse_information":
                condition_met = conditional_requirements.get("spouse_section_required", False)
                should_display = condition_met
            elif section_name == "children_information":
                condition_met = conditional_requirements.get("children_section_required", False)
                should_display = condition_met
            elif section_name == "will_information":
                condition_met = conditional_requirements.get("will_section_required", False)
                should_display = condition_met
            
            # Calculate completion metrics
            required_fields = [f for f in fields if f.is_required and condition_met]
            completed_required = [f for f in required_fields if f.is_filled]
            
            completion_percentage = 0.0
            if required_fields:
                completion_percentage = (len(completed_required) / len(required_fields)) * 100
            elif fields:  # No required fields, check overall completion
                completed_all = [f for f in fields if f.is_filled]
                completion_percentage = (len(completed_all) / len(fields)) * 100
            
            section_status = SectionCompletionStatus(
                section_name=section_name,
                fields=fields,
                is_conditional=is_conditional,
                should_display=should_display,
                condition_met=condition_met,
                completion_percentage=completion_percentage,
                required_fields_count=len(required_fields),
                completed_required_count=len(completed_required)
            )
            
            section_statuses.append(section_status)
        
        return section_statuses
    
    async def _identify_completion_barriers(self, field_statuses: List[FieldCompletionStatus], 
                                          section_statuses: List[SectionCompletionStatus]) -> List[CompletionBarrier]:
        """Identify barriers preventing form completion"""
        barriers = []
        
        # Check for missing critical fields
        critical_missing = [f for f in field_statuses 
                          if f.priority == CompletionPriority.CRITICAL and not f.is_filled]
        if critical_missing:
            barriers.append(CompletionBarrier.MISSING_CRITICAL)
        
        # Check for validation errors
        fields_with_errors = [f for f in field_statuses if f.validation_errors]
        if fields_with_errors:
            barriers.append(CompletionBarrier.VALIDATION_ERRORS)
        
        # Check for unfulfilled conditional requirements
        conditional_sections = [s for s in section_statuses if s.is_conditional and s.should_display]
        incomplete_conditional = [s for s in conditional_sections if s.completion_percentage < 100]
        if incomplete_conditional:
            barriers.append(CompletionBarrier.CONDITIONAL_UNFULFILLED)
        
        # Check for subject role clarity (if subject engine available)
        if self.dynamic_subject_engine:
            # This would integrate with the existing subject detection
            barriers.append(CompletionBarrier.SUBJECT_UNCLEAR)  # Placeholder
        
        # Check for insufficient data overall
        total_required = sum(s.required_fields_count for s in section_statuses)
        total_completed = sum(s.completed_required_count for s in section_statuses)
        
        if total_required > 0 and (total_completed / total_required) < 0.7:
            barriers.append(CompletionBarrier.INSUFFICIENT_DATA)
        
        self.stats["barriers_identified"] += len(barriers)
        return barriers
    
    async def _generate_smart_recommendations(self, field_statuses: List[FieldCompletionStatus], 
                                            barriers: List[CompletionBarrier],
                                            field_data: Dict[str, str],
                                            form_type: Optional[str]) -> List[SmartRecommendation]:
        """Generate AI-enhanced smart recommendations"""
        recommendations = []
        
        # Priority 1: Address critical missing fields
        critical_missing = [f for f in field_statuses 
                          if f.priority == CompletionPriority.CRITICAL and not f.is_filled]
        
        for field in critical_missing:
            rec = SmartRecommendation(
                field_name=field.field_name,
                recommendation_type="fill_next",
                priority=CompletionPriority.CRITICAL,
                reasoning=f"Critical field required for form processing: {field.cadence_path}"
            )
            recommendations.append(rec)
        
        # Priority 2: Address validation errors
        fields_with_errors = [f for f in field_statuses if f.validation_errors]
        for field in fields_with_errors:
            rec = SmartRecommendation(
                field_name=field.field_name,
                recommendation_type="validate",
                priority=CompletionPriority.HIGH,
                reasoning=f"Validation errors: {'; '.join(field.validation_errors)}"
            )
            recommendations.append(rec)
        
        # Priority 3: Complete high-priority unfilled fields
        high_priority_missing = [f for f in field_statuses 
                               if f.priority == CompletionPriority.HIGH and not f.is_filled and f.is_required]
        
        for field in high_priority_missing:
            rec = SmartRecommendation(
                field_name=field.field_name,
                recommendation_type="fill_next",
                priority=CompletionPriority.HIGH,
                reasoning=f"High priority required field: {field.cadence_path}"
            )
            recommendations.append(rec)
        
        # Priority 4: AI-enhanced suggestions (if AI available)
        if self.ai_enhancer:
            ai_recommendations = await self._generate_ai_recommendations(
                field_data, field_statuses, form_type
            )
            recommendations.extend(ai_recommendations)
        
        # Priority 5: Conditional field checks
        conditional_recommendations = self._generate_conditional_recommendations(field_statuses)
        recommendations.extend(conditional_recommendations)
        
        self.stats["smart_suggestions_made"] += len(recommendations)
        return recommendations
    
    async def _generate_ai_recommendations(self, field_data: Dict[str, str], 
                                         field_statuses: List[FieldCompletionStatus],
                                         form_type: Optional[str]) -> List[SmartRecommendation]:
        """Generate AI-enhanced recommendations using Ollama"""
        ai_recommendations = []
        
        if not self.ai_enhancer:
            return ai_recommendations
        
        try:
            # Analyze missing fields with AI
            missing_fields = [f for f in field_statuses if not f.is_filled and f.is_required]
            
            for field in missing_fields[:5]:  # Limit to avoid overwhelming AI
                ai_result = await self.ai_enhancer.enhance_field_mapping(
                    field.field_name, "", 
                    f"Form type: {form_type}. Current data: {list(field_data.keys())}"
                )
                
                if ai_result.get("success"):
                    # Generate AI-based suggestion
                    rec = SmartRecommendation(
                        field_name=field.field_name,
                        recommendation_type="ai_suggestion",
                        priority=CompletionPriority.MEDIUM,
                        reasoning=f"AI suggests completing this field for better form accuracy",
                        confidence=0.8,
                        ai_generated=True
                    )
                    ai_recommendations.append(rec)
            
            self.stats["ai_recommendations_generated"] += len(ai_recommendations)
            
        except Exception as e:
            self.logger.warning(f"AI recommendation generation failed: {e}")
        
        return ai_recommendations
    
    def _generate_conditional_recommendations(self, field_statuses: List[FieldCompletionStatus]) -> List[SmartRecommendation]:
        """Generate recommendations for conditional logic completion"""
        recommendations = []
        
        # Check for task planner fields that could unlock sections
        task_planner_fields = [f for f in field_statuses 
                             if "task_planner.b_" in f.cadence_path and not f.is_filled]
        
        for field in task_planner_fields:
            rec = SmartRecommendation(
                field_name=field.field_name,
                recommendation_type="conditional_check",
                priority=CompletionPriority.MEDIUM,
                reasoning=f"Completing this field may unlock additional form sections"
            )
            recommendations.append(rec)
        
        return recommendations
    
    async def _analyze_progressive_disclosure(self, field_statuses: List[FieldCompletionStatus], 
                                            section_statuses: List[SectionCompletionStatus],
                                            field_data: Dict[str, str]) -> List[str]:
        """Analyze progressive disclosure recommendations"""
        suggestions = []
        
        # Basic info first strategy
        basic_fields = ["deceased.name", "deceased.date_of_death", "applicant.name"]
        basic_completed = sum(1 for f in field_statuses 
                            if f.cadence_path in basic_fields and f.is_filled)
        
        if basic_completed < len(basic_fields):
            suggestions.append("Complete basic deceased and applicant information first")
        
        # Relationship-specific disclosure
        relationship = field_data.get("applicant.relationship", "").lower()
        if relationship:
            if "spouse" in relationship:
                suggestions.append("Show spouse-specific fields based on detected relationship")
            elif "child" in relationship:
                suggestions.append("Show child-specific fields based on detected relationship")
            elif "executor" in relationship:
                suggestions.append("Show executor-specific fields based on detected relationship")
        
        # Section-based progressive disclosure
        completed_sections = [s for s in section_statuses if s.completion_percentage >= 80]
        incomplete_sections = [s for s in section_statuses if s.completion_percentage < 80 and s.should_display]
        
        if len(completed_sections) >= 2 and incomplete_sections:
            next_section = incomplete_sections[0]
            suggestions.append(f"Consider showing {next_section.section_name} section next")
        
        self.stats["progressive_disclosures_applied"] += len(suggestions)
        return suggestions
    
    async def _generate_actionable_recommendations(self, recommendations: List[SmartRecommendation], 
                                                 barriers: List[CompletionBarrier],
                                                 section_statuses: List[SectionCompletionStatus]) -> List[str]:
        """Generate actionable recommendations for users"""
        actionable = []
        
        # Address critical issues first
        critical_recs = [r for r in recommendations if r.priority == CompletionPriority.CRITICAL]
        if critical_recs:
            actionable.append(f"🚨 Complete {len(critical_recs)} critical fields before proceeding")
        
        # Address barriers
        if CompletionBarrier.MISSING_CRITICAL in barriers:
            actionable.append("📝 Provide deceased and applicant identification information")
        
        if CompletionBarrier.VALIDATION_ERRORS in barriers:
            actionable.append("⚠️ Fix validation errors in completed fields")
        
        if CompletionBarrier.CONDITIONAL_UNFULFILLED in barriers:
            actionable.append("🔄 Complete relationship-specific sections (spouse, children, will)")
        
        # Progress recommendations
        incomplete_sections = [s for s in section_statuses 
                             if s.should_display and s.completion_percentage < 100]
        
        if incomplete_sections:
            next_section = min(incomplete_sections, key=lambda s: s.completion_percentage)
            actionable.append(f"➡️ Focus on completing {next_section.section_name.replace('_', ' ')} section next")
        
        # AI recommendations
        ai_recs = [r for r in recommendations if r.ai_generated]
        if ai_recs:
            actionable.append("🤖 AI suggests reviewing recommended fields for completeness")
        
        return actionable
    
    async def _generate_ai_insights(self, field_data: Dict[str, str], 
                                   recommendations: List[SmartRecommendation],
                                   form_type: Optional[str]) -> List[str]:
        """Generate AI-powered insights about form completion"""
        insights = []
        
        if not self.ai_enhancer:
            return insights
        
        try:
            # Generate insight about form pattern
            insight_prompt = f"Analyze estate form completion pattern. Fields provided: {len(field_data)}. Form type: {form_type}."
            
            ai_result = await self.ai_enhancer.enhance_field_mapping("form_analysis", "", insight_prompt)
            
            if ai_result.get("success"):
                insights.append("🤖 AI analysis suggests this form follows standard estate administration patterns")
            
            # Additional contextual insights
            if len(field_data) < 5:
                insights.append("🤖 Consider providing more context fields for better AI assistance")
            
            if any("spouse" in key.lower() for key in field_data.keys()):
                insights.append("🤖 Spouse-related information detected - ensure spouse section completeness")
            
        except Exception as e:
            self.logger.warning(f"AI insight generation failed: {e}")
        
        return insights
    
    async def _add_missing_critical_fields(self, field_statuses: List[FieldCompletionStatus], 
                                         field_data: Dict[str, str]):
        """Add missing critical fields to analysis"""
        
        # Define critical fields that should always be present
        critical_paths = [
            "deceased.name", "deceased.date_of_death", "deceased.social_insurance_number",
            "applicant.name", "applicant.relationship"
        ]
        
        existing_paths = {status.cadence_path for status in field_statuses}
        
        for path in critical_paths:
            if path not in existing_paths:
                # Add missing critical field
                status = FieldCompletionStatus(
                    field_name=path.replace(".", "_").replace("[*]", ""),
                    cadence_path=path,
                    is_filled=False,
                    is_required=True,
                    priority=CompletionPriority.CRITICAL,
                    disclosure_state=DisclosureState.REQUIRED
                )
                field_statuses.append(status)
    
    def _determine_field_priority(self, cadence_path: str, field_name: str) -> CompletionPriority:
        """Determine field completion priority"""
        
        # Check exact path matches first
        if cadence_path in self.field_priorities:
            return self.field_priorities[cadence_path]
        
        # Check pattern matches
        path_lower = cadence_path.lower()
        
        # Critical fields
        if any(critical in path_lower for critical in ["deceased.name", "deceased.date_of_death", "applicant.name"]):
            return CompletionPriority.CRITICAL
        
        # High priority patterns
        if any(pattern in path_lower for pattern in ["task_planner.b_", "deceased.", "applicant.relationship"]):
            return CompletionPriority.HIGH
        
        # Medium priority patterns
        if any(pattern in path_lower for pattern in ["spouse.", "children", "will.", "estate_reps"]):
            return CompletionPriority.MEDIUM
        
        # Low priority (details)
        if any(pattern in path_lower for pattern in ["financial.", "insurance.", "property."]):
            return CompletionPriority.LOW
        
        return CompletionPriority.MEDIUM
    
    def _is_field_required(self, cadence_path: str, field_name: str, field_data: Dict[str, str]) -> bool:
        """Determine if field is required based on current form state"""
        
        # Critical fields are always required
        if cadence_path in ["deceased.name", "deceased.date_of_death", "applicant.name"]:
            return True
        
        # Task planner fields are generally required
        if cadence_path.startswith("task_planner.b_"):
            return True
        
        # Conditional requirements
        if "spouse" in cadence_path:
            return field_data.get("task_planner.b_has_spouse", "").lower() == "yes"
        
        if "children" in cadence_path:
            return field_data.get("task_planner.b_has_children", "").lower() == "yes"
        
        if "will" in cadence_path or "estate_reps" in cadence_path:
            return field_data.get("task_planner.b_will", "").lower() == "yes"
        
        return False
    
    def _calculate_field_completion_score(self, is_filled: bool, is_required: bool, 
                                        priority: CompletionPriority, validation_errors: List[str]) -> float:
        """Calculate completion score for individual field"""
        if not is_required:
            return 1.0 if is_filled else 0.5  # Optional fields
        
        if not is_filled:
            return 0.0  # Required but empty
        
        if validation_errors:
            return 0.3  # Filled but has errors
        
        # Priority-based scoring
        priority_scores = {
            CompletionPriority.CRITICAL: 1.0,
            CompletionPriority.HIGH: 0.9,
            CompletionPriority.MEDIUM: 0.8,
            CompletionPriority.LOW: 0.7,
            CompletionPriority.CONDITIONAL: 0.6
        }
        
        return priority_scores.get(priority, 0.5)
    
    def _calculate_overall_completion_score(self, section_statuses: List[SectionCompletionStatus]) -> float:
        """Calculate overall form completion score"""
        if not section_statuses:
            return 0.0
        
        # Weight sections by importance
        section_weights = {
            "deceased_information": 0.3,
            "applicant_information": 0.2,
            "spouse_information": 0.15,
            "children_information": 0.1,
            "will_information": 0.1,
            "estate_representatives": 0.05,
            "financial_information": 0.05,
            "insurance_information": 0.025,
            "property_information": 0.025
        }
        
        weighted_score = 0.0
        total_weight = 0.0
        
        for section in section_statuses:
            if section.should_display:
                weight = section_weights.get(section.section_name, 0.05)
                weighted_score += (section.completion_percentage / 100) * weight
                total_weight += weight
        
        self.stats["completion_scores_calculated"] += 1
        return (weighted_score / total_weight * 100) if total_weight > 0 else 0.0
    
    def _get_critical_missing_fields(self, field_statuses: List[FieldCompletionStatus]) -> List[FieldCompletionStatus]:
        """Get list of critical missing fields"""
        return [f for f in field_statuses 
                if f.priority == CompletionPriority.CRITICAL and not f.is_filled]
    
    def _get_next_recommended_fields(self, recommendations: List[SmartRecommendation]) -> List[FieldCompletionStatus]:
        """Get next recommended fields to complete"""
        # This would map recommendations back to field statuses
        # For now, return empty list as we're working with recommendation objects
        return []
    
    def _estimate_completion_time(self, field_statuses: List[FieldCompletionStatus]) -> float:
        """Estimate time to complete remaining fields"""
        remaining_required = [f for f in field_statuses if f.is_required and not f.is_filled]
        
        # Rough estimate: 30 seconds per required field
        return len(remaining_required) * 0.5  # minutes
    
    def _assess_form_readiness(self, completion_score: float, barriers: List[CompletionBarrier]) -> str:
        """Assess overall form readiness"""
        if CompletionBarrier.MISSING_CRITICAL in barriers:
            return "Not Ready - Missing Critical Information"
        
        if completion_score >= 90:
            return "Ready for Submission"
        elif completion_score >= 70:
            return "Nearly Complete - Minor Items Remaining"
        elif completion_score >= 50:
            return "In Progress - Significant Work Remaining"
        else:
            return "Getting Started - Major Sections Incomplete"
    
    def get_completion_statistics(self) -> Dict[str, Any]:
        """Get form completion engine statistics"""
        return {
            **self.stats,
            "ai_enhancement_available": self.ai_enhancer is not None,
            "conditional_parser_available": self.conditional_parser is not None,
            "subject_engine_available": self.dynamic_subject_engine is not None,
            "completion_rules_loaded": len(self.completion_rules),
            "field_priorities_loaded": len(self.field_priorities),
            "section_dependencies_loaded": len(self.section_dependencies)
        }

# ==================== INTEGRATION UTILITIES ====================

async def analyze_form_completion_with_mapper(mapper_ai, field_data: Dict[str, str], 
                                            form_type: Optional[str] = None) -> FormCompletionAnalysis:
    """Integrate form completion analysis with existing MapperAI system"""
    
    # Get mapping results from existing mapper
    mapping_results = []
    for field_name, field_value in field_data.items():
        result = await mapper_ai.analyze_field(field_name, field_value)
        mapping_results.append(result)
    
    # Create completion engine
    completion_engine = FormCompletionEngine(
        conditional_parser=getattr(mapper_ai, 'conditional_parser', None),
        ai_enhancer=getattr(mapper_ai, 'ai_enhancer', None),
        dynamic_subject_engine=getattr(mapper_ai, 'dynamic_subject_engine', None)
    )
    
    # Perform completion analysis
    return await completion_engine.analyze_form_completion(field_data, mapping_results, form_type)

def format_completion_analysis_for_display(analysis: FormCompletionAnalysis) -> str:
    """Format completion analysis for user display"""
    output = []
    
    output.append(f"📊 FORM COMPLETION ANALYSIS")
    output.append(f"=" * 50)
    output.append(f"Overall Completion: {analysis.overall_completion_score:.1f}%")
    output.append(f"Form Status: {analysis.form_readiness_assessment}")
    output.append(f"Estimated Time Remaining: {analysis.estimated_time_remaining:.1f} minutes")
    output.append("")
    
    if analysis.critical_missing:
        output.append(f"🚨 CRITICAL MISSING FIELDS ({len(analysis.critical_missing)}):")
        for field in analysis.critical_missing:
            output.append(f"  • {field.field_name} ({field.cadence_path})")
        output.append("")
    
    if analysis.completion_barriers:
        output.append(f"⚠️ COMPLETION BARRIERS:")
        for barrier in analysis.completion_barriers:
            output.append(f"  • {barrier.value.replace('_', ' ').title()}")
        output.append("")
    
    if analysis.actionable_recommendations:
        output.append(f"📝 RECOMMENDATIONS:")
        for rec in analysis.actionable_recommendations:
            output.append(f"  • {rec}")
        output.append("")
    
    if analysis.progressive_disclosure_suggestions:
        output.append(f"🔄 PROGRESSIVE DISCLOSURE:")
        for suggestion in analysis.progressive_disclosure_suggestions:
            output.append(f"  • {suggestion}")
        output.append("")
    
    if analysis.ai_insights:
        output.append(f"🤖 AI INSIGHTS:")
        for insight in analysis.ai_insights:
            output.append(f"  • {insight}")
        output.append("")
    
    # Section breakdown
    output.append(f"📋 SECTION BREAKDOWN:")
    for section in analysis.sections:
        status_emoji = "✅" if section.completion_percentage >= 100 else "🔄" if section.completion_percentage >= 50 else "❌"
        visibility = " (Conditional)" if section.is_conditional else ""
        output.append(f"  {status_emoji} {section.section_name.replace('_', ' ').title()}: {section.completion_percentage:.1f}%{visibility}")
    
    return "\n".join(output)
