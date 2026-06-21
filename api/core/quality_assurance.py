
"""
Quality Assurance Engine - Complete Implementation

Provides comprehensive quality scoring, confidence metrics,
and validation for the entire mapping process.
"""

import time
import statistics
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum


from .models import MappingResult, ProcessingMetrics, ValidationSeverity, FieldType, QualityCategory

@dataclass
class QualityReport:
    """Comprehensive quality assessment report"""
    overall_score: float
    mapping_quality: float
    template_quality: float
    conditional_logic_quality: float
    completeness_score: float
    confidence_distribution: Dict[str, int]
    recommendations: List[str]
    critical_issues: List[str]
    quality_category: QualityCategory
    processing_efficiency: float
    error_analysis: Dict[str, Any]
    improvement_opportunities: List[str]

@dataclass
class QualityMetric:
    """Individual quality metric"""
    metric_name: str
    score: float
    weight: float
    description: str
    status: str  # 'pass', 'warning', 'fail'

class QualityAssuranceEngine:
    """Comprehensive quality assurance for estate form processing"""
    
    def __init__(self):
        self.quality_thresholds = self._load_quality_thresholds()
        self.scoring_weights = self._load_scoring_weights()
        self.validation_rules = self._load_validation_rules()
        self.benchmarks = self._load_performance_benchmarks()
        
    def _load_quality_thresholds(self) -> Dict[str, Dict[str, float]]:
        """Load quality assessment thresholds"""
        return {
            'mapping_quality': {
                'excellent': 0.95,
                'good': 0.85,
                'acceptable': 0.70,
                'poor': 0.50,
                'critical': 0.30
            },
            'confidence_distribution': {
                'high_confidence_min': 0.60,  
                'low_confidence_max': 0.20,   
                'unknown_fields_max': 0.15    
            },
            'template_quality': {
                'syntax_errors_max': 0,
                'helper_errors_max': 1,
                'schema_compliance_min': 0.95
            },
            'processing_efficiency': {
                'fields_per_second_min': 5.0,
                'processing_time_max': 300.0,  # 5 minutes max
                'memory_usage_max': 512  # MB
            },
            'completeness': {
                'required_fields_min': 0.90,
                'critical_fields_min': 1.0,
                'data_coverage_min': 0.75
            }
        }
    
    def _load_scoring_weights(self) -> Dict[str, float]:
        """Load scoring weights for different quality aspects"""
        return {
            'mapping_accuracy': 0.30,
            'confidence_distribution': 0.20,
            'template_quality': 0.15,
            'conditional_logic': 0.15,
            'completeness': 0.10,
            'processing_efficiency': 0.10
        }
    
    def _load_validation_rules(self) -> Dict[str, List[str]]:
        """Load validation rules for quality assessment"""
        return {
            'critical_requirements': [
                'deceased_name_present',
                'applicant_name_present',
                'basic_contact_info',
                'no_critical_errors'
            ],
            'mapping_requirements': [
                'high_confidence_majority',
                'low_unknown_percentage',
                'schema_compliance',
                'template_validity'
            ],
            'efficiency_requirements': [
                'reasonable_processing_time',
                'acceptable_throughput',
                'error_rate_acceptable'
            ]
        }
    
    def _load_performance_benchmarks(self) -> Dict[str, float]:
        """Load performance benchmarks for comparison"""
        return {
            'fields_per_second_target': 10.0,
            'mapping_accuracy_target': 0.85,
            'high_confidence_target': 0.70,
            'processing_time_target': 60.0,  # seconds
            'error_rate_target': 0.05  # 5% max error rate
        }
    
    async def generate_quality_report(self, mapping_results: List[MappingResult],
                                    processing_metrics: ProcessingMetrics = None,
                                    form_analysis: Dict = None) -> QualityReport:
        """Generate comprehensive quality report"""
        
        start_time = time.time()
        
        # Calculate individual quality scores
        mapping_quality = self._calculate_mapping_quality(mapping_results)
        template_quality = self._calculate_template_quality(mapping_results)
        conditional_quality = self._calculate_conditional_logic_quality(mapping_results)
        completeness = self._calculate_completeness_score(mapping_results, form_analysis)
        efficiency = self._calculate_processing_efficiency(mapping_results, processing_metrics)
        
        # Analyze confidence distribution
        confidence_dist = self._analyze_confidence_distribution(mapping_results)
        confidence_score = self._score_confidence_distribution(confidence_dist)
        
        # Calculate overall score using weighted average
        overall_score = self._calculate_overall_score({
            'mapping_quality': mapping_quality,
            'template_quality': template_quality,
            'conditional_logic': conditional_quality,
            'completeness': completeness,
            'efficiency': efficiency,
            'confidence_distribution': confidence_score
        })
        
        # Determine quality category
        quality_category = self._determine_quality_category(overall_score)
        
        # Generate comprehensive analysis
        recommendations = self._generate_recommendations(
            mapping_results, overall_score, mapping_quality, template_quality
        )
        
        critical_issues = self._identify_critical_issues(mapping_results)
        error_analysis = self._analyze_errors(mapping_results)
        improvement_opportunities = self._identify_improvement_opportunities(
            mapping_results, overall_score
        )
        
        report_generation_time = time.time() - start_time
        
        return QualityReport(
            overall_score=overall_score,
            mapping_quality=mapping_quality,
            template_quality=template_quality,
            conditional_logic_quality=conditional_quality,
            completeness_score=completeness,
            confidence_distribution=confidence_dist,
            recommendations=recommendations,
            critical_issues=critical_issues,
            quality_category=quality_category,
            processing_efficiency=efficiency,
            error_analysis=error_analysis,
            improvement_opportunities=improvement_opportunities
        )
    
    def _calculate_mapping_quality(self, mapping_results: List[MappingResult]) -> float:
        """Calculate mapping quality score"""
        
        if not mapping_results:
            return 0.0
        
        total_fields = len(mapping_results)
        successful_mappings = len([r for r in mapping_results if "unmapped." not in r.cadence_path])
        
        # Convert confidence values to categories for scoring
        high_confidence = 0
        medium_confidence = 0
        
        for result in mapping_results:
            try:
             
                conf_value = float(result.confidence)
                if conf_value > 1.0: # Handle cases where it might be 0-100
                    conf_value /= 100.0

                if conf_value >= 0.9:
                    high_confidence += 1
                elif conf_value >= 0.6:
                    medium_confidence += 1
            except (ValueError, TypeError):
                # Handle string confidence values
                if str(result.confidence).lower() == "high":
                    high_confidence += 1
                elif str(result.confidence).lower() == "medium":
                    medium_confidence += 1
        
        # Calculate sub-scores
        mapping_success_rate = successful_mappings / total_fields
        confidence_quality = (high_confidence * 1.0 + medium_confidence * 0.7) / total_fields
        
        # Penalty for validation errors
        error_penalty = 0
        for result in mapping_results:
            if hasattr(result, 'validation_errors') and result.validation_errors:
                error_penalty += len(result.validation_errors) * 0.05
        
        error_penalty = min(error_penalty, 0.5)  # Cap penalty at 50%
        
        # Combined mapping quality score
        mapping_quality = (mapping_success_rate * 0.6 + confidence_quality * 0.4) - error_penalty
        
        return max(0.0, min(1.0, mapping_quality))
    
    def _calculate_template_quality(self, mapping_results: List[MappingResult]) -> float:
        """Calculate template quality score"""
        
        if not mapping_results:
            return 0.0
        
        total_templates = 0
        valid_templates = 0
        syntax_errors = 0
        helper_errors = 0
        
        for result in mapping_results:
            if result.template and result.template != "{{unknown.field}}":
                total_templates += 1
                
                # Basic template validation
                template_valid = self._validate_template_basic(result.template)
                if template_valid['is_valid']:
                    valid_templates += 1
                
                syntax_errors += len(template_valid.get('syntax_errors', []))
                helper_errors += len(template_valid.get('helper_errors', []))
        
        if total_templates == 0:
            return 1.0  # No templates to validate
        
        # Calculate template quality components
        validity_score = valid_templates / total_templates
        syntax_quality = max(0, 1.0 - (syntax_errors / total_templates * 0.2))
        helper_quality = max(0, 1.0 - (helper_errors / total_templates * 0.1))
        
        # Combined template quality
        template_quality = validity_score * 0.5 + syntax_quality * 0.3 + helper_quality * 0.2
        
        return max(0.0, min(1.0, template_quality))
    
    def _validate_template_basic(self, template: str) -> Dict[str, Any]:
        """Basic template validation"""
        
        syntax_errors = []
        helper_errors = []
        
        # Check balanced handlebars
        if template.count('{{') != template.count('}}'):
            syntax_errors.append("Unbalanced handlebars")
        
        # Check for empty expressions
        if '{{}}' in template:
            syntax_errors.append("Empty expressions found")
        
        # Check for unknown helpers (basic check)
        known_helpers = ['name', 'date', 'phone', 'sin', 'currency', 'location', 'checkbox', 'postal_code']
        helper_pattern = r'\{\{#(\w+)(?::(\w+))?\s'
        
        import re
        for match in re.finditer(helper_pattern, template):
            helper_name = match.group(1)
            if helper_name not in known_helpers:
                helper_errors.append(f"Unknown helper: {helper_name}")
        
        return {
            'is_valid': len(syntax_errors) == 0 and len(helper_errors) == 0,
            'syntax_errors': syntax_errors,
            'helper_errors': helper_errors
        }
    
    def _calculate_conditional_logic_quality(self, mapping_results: List[MappingResult]) -> float:
        """Calculate conditional logic quality score"""
        
        total_fields = len(mapping_results)
        if total_fields == 0:
            return 1.0
        
        conditional_fields = len([r for r in mapping_results if hasattr(r, 'conditional_logic') and r.conditional_logic])
        dependency_fields = len([r for r in mapping_results if hasattr(r, 'field_dependencies') and r.field_dependencies])
        
        # Quality indicators
        has_conditional_logic = conditional_fields > 0
        has_dependencies = dependency_fields > 0
        conditional_coverage = conditional_fields / total_fields
        
        # Score based on presence and coverage of conditional logic
        if conditional_coverage > 0.3:
            return 1.0  # Excellent conditional logic coverage
        elif conditional_coverage > 0.1:
            return 0.8  # Good conditional logic coverage
        elif has_conditional_logic or has_dependencies:
            return 0.6  # Some conditional logic present
        else:
            return 0.4  # No conditional logic detected
    
    def _calculate_completeness_score(self, mapping_results: List[MappingResult], 
                                    form_analysis: Dict = None) -> float:
        """Calculate data completeness score"""
        
        if not mapping_results:
            return 0.0
        
        total_fields = len(mapping_results)
        mapped_fields = len([r for r in mapping_results if "unmapped." not in r.cadence_path])
        
        # Basic completeness
        basic_completeness = mapped_fields / total_fields
        
        # Check for critical field coverage
        critical_fields = self._identify_critical_fields(mapping_results)
        critical_coverage = len(critical_fields) / max(1, self._get_expected_critical_fields_count())
        
        # Check for required field types
        field_type_coverage = self._calculate_field_type_coverage(mapping_results)
        
        # Combined completeness score
        completeness = (
            basic_completeness * 0.5 +
            critical_coverage * 0.3 +
            field_type_coverage * 0.2
        )
        
        return max(0.0, min(1.0, completeness))
    
    def _identify_critical_fields(self, mapping_results: List[MappingResult]) -> List[str]:
        """Identify critical fields that are mapped"""
        
        critical_patterns = [
            'deceased.name', 'deceased.date_of_death', 'deceased.social_insurance_number',
            'applicant.name', 'applicant.phone', 'applicant.address'
        ]
        
        mapped_critical = []
        for result in mapping_results:
            if any(pattern in result.cadence_path for pattern in critical_patterns):
                mapped_critical.append(result.cadence_path)
        
        return mapped_critical
    
    def _get_expected_critical_fields_count(self) -> int:
        """Get expected number of critical fields"""
        return 6  
    
    def _calculate_field_type_coverage(self, mapping_results: List[MappingResult]) -> float:
        """Calculate coverage across different field types"""
        
        required_types = [
            FieldType.IDENTITY, FieldType.DATE, FieldType.CONTACT, 
            FieldType.ADDRESS, FieldType.RELATIONSHIP
        ]
        
        present_types = set()
        for result in mapping_results:
            if "unmapped." not in result.cadence_path:
                present_types.add(result.field_type)
        
        coverage = len(present_types.intersection(required_types)) / len(required_types)
        return coverage
    
    def _calculate_processing_efficiency(self, mapping_results: List[MappingResult],
                                       processing_metrics: ProcessingMetrics = None) -> float:
        """Calculate processing efficiency score"""
        
        if not mapping_results:
            return 0.0
        
        # Calculate fields per second
        total_processing_time = sum(r.processing_time for r in mapping_results)
        if total_processing_time > 0:
            fields_per_second = len(mapping_results) / total_processing_time
        else:
            fields_per_second = float('inf')
        
        # Score against benchmark
        target_fps = self.benchmarks['fields_per_second_target']
        fps_score = min(1.0, fields_per_second / target_fps)
        
        # Processing time score
        avg_processing_time = total_processing_time / len(mapping_results)
        time_score = max(0, 1.0 - (avg_processing_time / 1.0))  # 1 second per field threshold
        
        # Combined efficiency score
        efficiency = fps_score * 0.6 + time_score * 0.4
        
        return max(0.0, min(1.0, efficiency))
    
    def _analyze_confidence_distribution(self, mapping_results: List[MappingResult]) -> Dict[str, int]:
        """Analyze distribution of confidence levels, handling various score types."""
        distribution = {"high": 0, "medium": 0, "low": 0, "unknown": 0}
        
        for result in mapping_results:
            if "unmapped." in result.cadence_path or result.cadence_path == "unknown.field":
                distribution["unknown"] += 1
            else:
                try:
                    # Standardize confidence to a float between 0.0 and 1.0
                    conf_value = float(result.confidence)
                    if conf_value > 1.0: # Handle cases where it might be 0-100
                        conf_value /= 100.0
                    
                    # Categorize the float value
                    if conf_value >= 0.9:
                        distribution["high"] += 1
                    elif conf_value >= 0.7:
                        distribution["medium"] += 1
                    else:
                        distribution["low"] += 1
                except (ValueError, TypeError):
                    # Handle string confidence values
                    confidence_str = str(result.confidence).lower()
                    if confidence_str in distribution:
                        distribution[confidence_str] += 1
                    else:
                        distribution["low"] += 1
        
        return distribution
    
    def _score_confidence_distribution(self, distribution: Dict[str, int]) -> float:
        """Score confidence distribution quality"""
        
        total = sum(distribution.values())
        if total == 0:
            return 0.0
        
        # Calculate percentages
        high_pct = distribution["high"] / total
        medium_pct = distribution["medium"] / total
        low_pct = distribution["low"] / total
        unknown_pct = distribution["unknown"] / total
        
        # Score based on thresholds
        thresholds = self.quality_thresholds['confidence_distribution']
        
        score = 0.0
        
        # High confidence bonus
        if high_pct >= thresholds['high_confidence_min']:
            score += 0.4
        else:
            score += 0.4 * (high_pct / thresholds['high_confidence_min'])
        
        # Medium confidence contribution
        score += 0.3 * medium_pct
        
        # Low confidence penalty
        if low_pct <= thresholds['low_confidence_max']:
            score += 0.2
        else:
            score += 0.2 * (1 - (low_pct - thresholds['low_confidence_max']))
        
        # Unknown fields penalty
        if unknown_pct <= thresholds['unknown_fields_max']:
            score += 0.1
        else:
            score += 0.1 * (1 - (unknown_pct - thresholds['unknown_fields_max']))
        
        return max(0.0, min(1.0, score))
    
    def _calculate_overall_score(self, component_scores: Dict[str, float]) -> float:
        """Calculate weighted overall quality score"""
        
        weighted_sum = 0.0
        total_weight = 0.0
        
        for component, score in component_scores.items():
            if component in self.scoring_weights:
                weight = self.scoring_weights[component]
                weighted_sum += score * weight
                total_weight += weight
        
        if total_weight > 0:
            return weighted_sum / total_weight
        else:
            return 0.0
    
    def _determine_quality_category(self, overall_score: float) -> QualityCategory:
        """Determine quality category from overall score"""
        
        if overall_score >= 0.90:
            return QualityCategory.EXCELLENT
        elif overall_score >= 0.70:
            return QualityCategory.GOOD
        elif overall_score >= 0.50:
            return QualityCategory.ACCEPTABLE
        elif overall_score >= 0.30:
            return QualityCategory.POOR
        else:
            return QualityCategory.CRITICAL
    
    def _generate_recommendations(self, mapping_results: List[MappingResult],
                                overall_score: float, mapping_quality: float,
                                template_quality: float) -> List[str]:
        """Generate actionable recommendations"""
        
        recommendations = []
        
        # Overall score recommendations
        if overall_score < 0.5:
            recommendations.append("🔴 Overall quality is below acceptable levels - comprehensive review needed")
        elif overall_score < 0.7:
            recommendations.append("🟡 Overall quality needs improvement - focus on key areas")
        else:
            recommendations.append("✅ Good overall quality - minor optimizations possible")
        
        # Mapping-specific recommendations
        if mapping_quality < 0.6:
            recommendations.append("📊 Low mapping accuracy - review field matching algorithms")
        
        unknown_count = len([r for r in mapping_results if "unmapped." in r.cadence_path])
        if unknown_count > len(mapping_results) * 0.2:
            recommendations.append("❓ High number of unknown fields - expand mapping patterns")
        
        # Template recommendations
        if template_quality < 0.7:
            recommendations.append("🔧 Template quality issues detected - review template syntax")
        
        # Confidence recommendations
        confidence_dist = self._analyze_confidence_distribution(mapping_results)
        high_confidence_pct = confidence_dist["high"] / sum(confidence_dist.values()) if sum(confidence_dist.values()) > 0 else 0
        
        if high_confidence_pct < 0.5:
            recommendations.append("📈 Low high-confidence mappings - improve pattern matching")
        
        # Processing efficiency recommendations
        avg_processing_time = sum(r.processing_time for r in mapping_results) / len(mapping_results) if mapping_results else 0
        if avg_processing_time > 0.5:  # 500ms per field
            recommendations.append("⚡ Slow processing detected - optimize algorithms")
        
        # Validation error recommendations
        error_count = sum(len(getattr(r, 'validation_errors', [])) for r in mapping_results)
        if error_count > 0:
            recommendations.append(f"⚠️ {error_count} validation errors found - review data quality")
        
        return recommendations
    
    def _identify_critical_issues(self, mapping_results: List[MappingResult]) -> List[str]:
        """Identify critical issues that need immediate attention"""
        
        critical_issues = []
        
        # Check for complete mapping failure
        successful_mappings = len([r for r in mapping_results if "unmapped." not in r.cadence_path])
        if successful_mappings == 0:
            critical_issues.append("🚨 CRITICAL: No successful field mappings found")
        
        # Check for missing critical fields
        critical_field_patterns = ['deceased.name', 'applicant.name']
        missing_critical = []
        
        for pattern in critical_field_patterns:
            if not any(pattern in r.cadence_path for r in mapping_results):
                missing_critical.append(pattern)
        
        if missing_critical:
            critical_issues.append(f"🚨 CRITICAL: Missing essential fields: {', '.join(missing_critical)}")
        
        # Check for severe validation errors
        severe_errors = []
        for result in mapping_results:
            validation_errors = getattr(result, 'validation_errors', [])
            if validation_errors:
                for error in validation_errors:
                    if any(term in error.lower() for term in ['invalid', 'required', 'missing']):
                        severe_errors.append(f"{result.field_name}: {error}")
        
        if severe_errors:
            critical_issues.append(f"🚨 CRITICAL: Severe validation errors in {len(severe_errors)} fields")
        
        return critical_issues
    
    def _analyze_errors(self, mapping_results: List[MappingResult]) -> Dict[str, Any]:
        """Analyze errors and validation issues"""
        
        error_analysis = {
            'total_validation_errors': 0,
            'total_warnings': 0,
            'error_types': {},
            'most_common_errors': [],
            'fields_with_errors': []
        }
        
        all_errors = []
        all_warnings = []
        
        for result in mapping_results:
            # Collect validation errors
            validation_errors = getattr(result, 'validation_errors', [])
            if validation_errors:
                error_analysis['total_validation_errors'] += len(validation_errors)
                all_errors.extend(validation_errors)
                error_analysis['fields_with_errors'].append(result.field_name)
            
            # Collect warnings
            warnings = getattr(result, 'warnings', [])
            if warnings:
                error_analysis['total_warnings'] += len(warnings)
                all_warnings.extend(warnings)
        
        # Categorize errors
        error_categories = {
            'format_errors': ['format', 'invalid format', 'pattern'],
            'required_errors': ['required', 'missing', 'empty'],
            'type_errors': ['type', 'expected', 'incorrect type'],
            'validation_errors': ['validation', 'check', 'verify']
        }
        
        for category, keywords in error_categories.items():
            count = 0
            for error in all_errors:
                if any(keyword in error.lower() for keyword in keywords):
                    count += 1
            error_analysis['error_types'][category] = count
        
        # Find most common errors
        from collections import Counter
        error_counter = Counter(all_errors)
        error_analysis['most_common_errors'] = error_counter.most_common(5)
        
        return error_analysis
    
    def _identify_improvement_opportunities(self, mapping_results: List[MappingResult],
                                          overall_score: float) -> List[str]:
        """Identify specific improvement opportunities"""
        
        opportunities = []
        
        # Mapping accuracy improvements
        unknown_fields = [r for r in mapping_results if "unmapped." in r.cadence_path]
        if unknown_fields:
            # Analyze patterns in unknown fields
            field_patterns = self._analyze_unknown_field_patterns(unknown_fields)
            if field_patterns:
                opportunities.append(f"📊 Add mapping patterns for: {', '.join(field_patterns[:3])}")
        
        # Confidence improvements
        low_confidence_count = 0
        for result in mapping_results:
            try:
                conf_value = float(result.confidence)
                if conf_value < 0.6:
                    low_confidence_count += 1
            except (ValueError, TypeError):
                if str(result.confidence).lower() == "low":
                    low_confidence_count += 1
        
        if low_confidence_count > len(mapping_results) * 0.3:
            opportunities.append("📈 Improve confidence scoring algorithms")
        
        # Template improvements
        template_issues = self._identify_template_improvement_areas(mapping_results)
        if template_issues:
            opportunities.extend(template_issues)
        
        # Processing efficiency improvements
        slow_fields = [r for r in mapping_results if r.processing_time > 0.1]
        if len(slow_fields) > len(mapping_results) * 0.2:
            opportunities.append("⚡ Optimize processing for slow fields")
        
        # Conditional logic improvements
        conditional_fields = [r for r in mapping_results if hasattr(r, 'conditional_logic') and r.conditional_logic]
        if len(conditional_fields) < len(mapping_results) * 0.1:
            opportunities.append("🔀 Enhance conditional logic detection")
        
        return opportunities
    
    def _analyze_unknown_field_patterns(self, unknown_fields: List[MappingResult]) -> List[str]:
        """Analyze patterns in unknown fields to suggest new mappings"""
        
        patterns = []
        field_names = [r.field_name.lower() for r in unknown_fields]
        
        # Common word analysis
        from collections import Counter
        all_words = []
        for name in field_names:
            all_words.extend(name.split())
        
        common_words = Counter(all_words).most_common(5)
        patterns = [word for word, count in common_words if count > 1 and len(word) > 3]
        
        return patterns
    
    def _identify_template_improvement_areas(self, mapping_results: List[MappingResult]) -> List[str]:
        """Identify template improvement opportunities"""
        
        improvements = []
        
        # Count template types
        template_types = {}
        for result in mapping_results:
            if result.template and result.template != "{{unknown.field}}":
                # Extract helper type
                if result.template.startswith('{{#'):
                    helper = result.template.split()[0][3:]  # Remove {{#
                    template_types[helper] = template_types.get(helper, 0) + 1
        
        # Suggest missing helper types
        common_helpers = ['name', 'date', 'phone', 'currency', 'location']
        missing_helpers = [h for h in common_helpers if h not in template_types]
        
        if missing_helpers:
            improvements.append(f"🔧 Consider adding templates with helpers: {', '.join(missing_helpers)}")
        
        return improvements
    
    def generate_quality_metrics_summary(self, mapping_results: List[MappingResult]) -> List[QualityMetric]:
        """Generate detailed quality metrics"""
        
        metrics = []
        
        # Mapping accuracy metric
        successful = len([r for r in mapping_results if "unmapped." not in r.cadence_path])
        total = len(mapping_results)
        mapping_score = successful / total if total > 0 else 0
        
        metrics.append(QualityMetric(
            metric_name="Mapping Accuracy",
            score=mapping_score,
            weight=0.30,
            description=f"{successful}/{total} fields successfully mapped",
            status="pass" if mapping_score >= 0.7 else "warning" if mapping_score >= 0.5 else "fail"
        ))
        
        # Confidence distribution metric
        confidence_dist = self._analyze_confidence_distribution(mapping_results)
        high_confidence_ratio = confidence_dist["high"] / total if total > 0 else 0
        
        metrics.append(QualityMetric(
            metric_name="High Confidence Ratio",
            score=high_confidence_ratio,
            weight=0.20,
            description=f"{confidence_dist['high']}/{total} fields with high confidence",
            status="pass" if high_confidence_ratio >= 0.6 else "warning" if high_confidence_ratio >= 0.4 else "fail"
        ))
        
        # Error rate metric
        error_count = sum(len(getattr(r, 'validation_errors', [])) for r in mapping_results)
        error_rate = error_count / total if total > 0 else 0
        
        metrics.append(QualityMetric(
            metric_name="Error Rate",
            score=max(0, 1.0 - error_rate),
            weight=0.15,
            description=f"{error_count} validation errors across {total} fields",
            status="pass" if error_rate <= 0.05 else "warning" if error_rate <= 0.15 else "fail"
        ))
        
        # Processing efficiency metric
        avg_time = sum(r.processing_time for r in mapping_results) / total if total > 0 else 0
        efficiency_score = max(0, 1.0 - (avg_time / 0.5))  # 500ms threshold
        
        metrics.append(QualityMetric(
            metric_name="Processing Efficiency",
            score=efficiency_score,
            weight=0.10,
            description=f"Average processing time: {avg_time:.3f}s per field",
            status="pass" if avg_time <= 0.1 else "warning" if avg_time <= 0.5 else "fail"
        ))
        
        return metrics
    
    def export_quality_report(self, quality_report: QualityReport) -> Dict[str, Any]:
        """Export comprehensive quality report for external use"""
        
        return {
            'report_summary': {
                'overall_score': quality_report.overall_score,
                'quality_category': quality_report.quality_category.value,
                'timestamp': time.time()
            },
            'detailed_scores': {
                'mapping_quality': quality_report.mapping_quality,
                'template_quality': quality_report.template_quality,
                'conditional_logic_quality': quality_report.conditional_logic_quality,
                'completeness_score': quality_report.completeness_score,
                'processing_efficiency': quality_report.processing_efficiency
            },
            'confidence_analysis': quality_report.confidence_distribution,
            'issues_and_recommendations': {
                'critical_issues': quality_report.critical_issues,
                'recommendations': quality_report.recommendations,
                'improvement_opportunities': quality_report.improvement_opportunities
            },
            'error_analysis': quality_report.error_analysis,
            'quality_thresholds': self.quality_thresholds,
            'benchmarks_comparison': {
                'meets_mapping_target': quality_report.mapping_quality >= self.benchmarks['mapping_accuracy_target'],
                'meets_efficiency_target': quality_report.processing_efficiency >= 0.7
            }
        }
