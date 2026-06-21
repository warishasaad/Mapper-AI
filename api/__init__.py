"""
Estate Mapper System - Comprehensive Estate Form Processing with Conditional Logic

This package initializes the core components of the MapperAI system, making them
available for use by the main application (e.g., the FastAPI server).

Author: AI Assistant
Version: 3.0 Production Ready with Conditional Logic
"""

import sys
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ==============================================================================
# 1. CORE MODULE IMPORTS - ALL PRESERVED WITH FIXED PATHS
# ==============================================================================
# We use try/except blocks to provide helpful error messages if a module is missing
# and to allow the system to function in different environments.

try:
    # --- Data Models (Single Source of Truth) ---
    from .core.models import (
        FieldType, PDFFieldType, PDFFormType, OllamaConfig, MappingResult,
        PDFFieldMapping, PDFFormInfo, PDFFieldExtraction, PDFMappingResult,
        ConditionalLogic, FieldDependency, ConditionalAnalysisResult,
        ConditionalRule, FormSection, SubjectRole, ConfidenceLevel,
        BatchProcessingResult, PatternMatchingStats, QualityCategory,
        FormIntent, ContextualConfidence, LegalDocumentType, ConditionalType,
        ProvincialJurisdiction, ValidationSeverity, SubjectDetectionResult,
        SubjectEvidence
    )
    logger.info("✅ Successfully imported data models from core.models")
except ImportError as e:
    logger.error(f"❌ CRITICAL: Failed to import data models: {e}")
    print(f"FATAL ERROR: Data models are missing from core/models.py. Error: {e}")
    sys.exit(1)

try:
    # --- Core Processing Engines ---
    from .core.estate_mapper import UniversalEstateMapper, CompleteEstateMapperAI
    logger.info("✅ Successfully imported estate mapper")
except ImportError as e:
    logger.error(f"❌ CRITICAL: Failed to import estate mapper: {e}")
    print(f"FATAL ERROR: Estate mapper is missing. Error: {e}")
    sys.exit(1)

# --- Optional Imports (with graceful fallback) ---
try:
    from .core.pdf_processor import PDFProcessor 
    PDF_PROCESSOR_AVAILABLE = True
    logger.info("✅ PDF processor available")
except ImportError as e:
    logger.warning(f"⚠️  PDF processor not available: {e}")
    PDF_PROCESSOR_AVAILABLE = False
    EnhancedPDFMapperAI = None

try:
    from .core.ai_enhancer import OllamaAIEnhancer
    AI_ENHANCER_AVAILABLE = True
    logger.info("✅ AI enhancer available")
except ImportError as e:
    logger.warning(f"⚠️  AI enhancer not available: {e}")
    AI_ENHANCER_AVAILABLE = False
    OllamaAIEnhancer = None

try:
    from .core.form_logic_parser import AdaptiveFormInstructionParser as FormInstructionParser
    CONDITIONAL_LOGIC_AVAILABLE = True
    logger.info("✅ Conditional logic engine available")
except ImportError as e:
    logger.warning(f"⚠️  Conditional logic engine not available: {e}")
    CONDITIONAL_LOGIC_AVAILABLE = False
    FormInstructionParser = None

# --- Advanced Engines (Optional) ---
try:
    from .core.cross_field_validator import CrossFieldValidator
    from .core.semantic_context_engine import SemanticContextEngine
    from .core.form_completion_engine import FormCompletionEngine
    from .core.quality_assurance import QualityAssuranceEngine
    from .core.dynamic_path_resolver import DynamicPathResolver
    ADVANCED_ENGINES_AVAILABLE = True
    logger.info("✅ Advanced engines available")
except ImportError as e:
    logger.warning(f"⚠️  Advanced engines not available: {e}")
    ADVANCED_ENGINES_AVAILABLE = False
    CrossFieldValidator = None
    SemanticContextEngine = None
    FormCompletionEngine = None
    QualityAssuranceEngine = None
    DynamicPathResolver = None

try:
    # --- Utility Functions ---
    from .core.utils import install_dependencies, format_time, calculate_confidence
    UTILS_AVAILABLE = True
    logger.info("✅ Utility functions available")
except ImportError as e:
    logger.warning(f"⚠️  Utility functions not available: {e}")
    UTILS_AVAILABLE = False
    # Provide basic fallbacks
    def install_dependencies():
        logger.warning("install_dependencies function not available")
        pass
    
    def format_time(seconds):
        return f"{seconds:.2f}s"
    
    def calculate_confidence(*args):
        return 0.5

# ==============================================================================
# 2. PUBLIC API DEFINITION (`__all__`) - ALL PRESERVED
# ==============================================================================
# This list defines which components are exposed when a user does `from api import *`.

__version__ = "3.0.0"
__author__ = "AI Assistant"

# Build __all__ dynamically based on what's available
__all__ = [
    # Always available
    "UniversalEstateMapper",
    "CompleteEstateMapperAI",
    
    # Data Models (always required)
    "FieldType", "PDFFieldType", "PDFFormType", "OllamaConfig", "MappingResult",
    "PDFFieldMapping", "PDFFormInfo", "PDFFieldExtraction", "PDFMappingResult",
    "ConditionalLogic", "FieldDependency", "ConditionalAnalysisResult",
    "ConditionalRule", "FormSection", "SubjectRole", "ConfidenceLevel",
    "BatchProcessingResult", "PatternMatchingStats", "QualityCategory",
    "FormIntent", "ContextualConfidence", "LegalDocumentType", "ConditionalType",
    "ProvincialJurisdiction", "ValidationSeverity", "SubjectDetectionResult",
    "SubjectEvidence",
    
    # Utilities (with fallbacks)
    "install_dependencies", "format_time", "calculate_confidence"
]

# Add optional components if available
if PDF_PROCESSOR_AVAILABLE:
    __all__.append("EnhancedPDFMapperAI")

if AI_ENHANCER_AVAILABLE:
    __all__.append("OllamaAIEnhancer")

if CONDITIONAL_LOGIC_AVAILABLE:
    __all__.append("FormInstructionParser")

if ADVANCED_ENGINES_AVAILABLE:
    __all__.extend([
        "CrossFieldValidator",
        "SemanticContextEngine", 
        "FormCompletionEngine",
        "QualityAssuranceEngine",
        "DynamicPathResolver"
    ])

# ==============================================================================
# 3. INITIALIZATION & DEPENDENCY CHECK - ALL PRESERVED
# ==============================================================================

def _run_initialization_checks():
    """
    Private function to run initial system checks and print status messages.
    """
    print("\n" + "="*60)
    print("🏛️  Estate Mapper AI System v3.0 Initializing...")
    print("="*60)
    
    # Core components
    print("✅ Core mapping engine: Ready")
    print("✅ Data models: Loaded")
    
    # Optional components
    if PDF_PROCESSOR_AVAILABLE:
        print("✅ PDF processing: Ready")
    else:
        print("⚠️  PDF processing: Limited (some modules missing)")
    
    if AI_ENHANCER_AVAILABLE:
        print("✅ AI enhancement: Available")
    else:
        print("⚠️  AI enhancement: Not available")
    
    if CONDITIONAL_LOGIC_AVAILABLE:
        print("✅ Conditional logic: Enabled")
    else:
        print("⚠️  Conditional logic: Disabled")
    
    if ADVANCED_ENGINES_AVAILABLE:
        print("✅ Advanced form analysis: Ready")
        print("✅ Field dependency detection: Ready")
    else:
        print("⚠️  Advanced analysis engines: Limited")
    
    # Ensure dependencies are available (if utils are available)
    if UTILS_AVAILABLE:
        try:
            install_dependencies()
            print("✅ Dependencies: Checked")
        except Exception as e:
            print(f"⚠️  Dependency check failed: {e}")
            print("   Core functionality will still work, but some features might be limited.")
    else:
        print("⚠️  Dependency checker: Not available")
    
    print("="*60)
    print("🚀 System initialization complete!")
    print("="*60 + "\n")

# Run the initialization checks only once when the package is first imported.
if not hasattr(sys, '_mapper_ai_initialized'):
    _run_initialization_checks()
    sys._mapper_ai_initialized = True

# ==============================================================================
# 4. SYSTEM STATUS FUNCTIONS - ALL PRESERVED
# ==============================================================================

def get_system_status():
    """Get the current system status and available components."""
    return {
        "version": __version__,
        "core_available": True,
        "pdf_processor_available": PDF_PROCESSOR_AVAILABLE,
        "ai_enhancer_available": AI_ENHANCER_AVAILABLE,
        "conditional_logic_available": CONDITIONAL_LOGIC_AVAILABLE,
        "advanced_engines_available": ADVANCED_ENGINES_AVAILABLE,
        "utils_available": UTILS_AVAILABLE,
        "available_components": __all__
    }

def print_system_status():
    """Print a detailed system status report."""
    status = get_system_status()
    print(f"Estate Mapper AI System v{status['version']}")
    print("-" * 40)
    for component, available in status.items():
        if component not in ['version', 'available_components']:
            status_icon = "✅" if available else "❌"
            print(f"{status_icon} {component.replace('_', ' ').title()}: {available}")
    print(f"\nTotal Available Components: {len(status['available_components'])}")

# Add status functions to __all__
__all__.extend(["get_system_status", "print_system_status"])

logger.info("✅ Core package initialized successfully.")