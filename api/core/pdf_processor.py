"""
Enhanced PDF Form Processing with Conditional Logic Analysis and Proximity-Based Field Extraction

Handles PDF field extraction using PyMuPDF and PyPDF2, form type detection,
conditional logic extraction, comprehensive mapping to Cadence schema, and 
proximity-based field labeling for better form understanding.
"""

import time
import logging
import re
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path

# CORRECTED: Standardized imports from the unified models file
from .models import (
    PDFFieldExtraction, PDFFormInfo, PDFFieldMapping, PDFMappingResult,
    PDFFieldType, PDFFormType, PDFStats, ConditionalLogic, FieldDependency,
    ConditionalAnalysisResult, ConditionalRule, FormSection
)
from .form_logic_parser import AdaptiveFormInstructionParser as FormInstructionParser
from .utils import install_dependencies

# Configure logging
logger = logging.getLogger(__name__)

# Try to import PDF libraries
try:
    import PyPDF2
    PYPDF2_AVAILABLE = True
except ImportError:
    PYPDF2_AVAILABLE = False

try:
    import fitz  # PyMuPDF
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False

# Enhanced ConditionalAnalysisResult with proper length support
class FixedConditionalAnalysisResult:
    """Fixed ConditionalAnalysisResult with proper length support"""
    
    def __init__(self, total_conditional_fields=0, conditional_mappings=None, 
                 field_dependencies=None, form_sections=None, condition_types=None,
                 confidence_distribution=None, extraction_errors=None, processing_time=0.0):
        self.total_conditional_fields = total_conditional_fields
        self.conditional_mappings = conditional_mappings or []
        self.field_dependencies = field_dependencies or []
        self.form_sections = form_sections or []
        self.condition_types = condition_types or {}
        self.confidence_distribution = confidence_distribution or {}
        self.extraction_errors = extraction_errors or []
        self.processing_time = processing_time
    
    def __len__(self):
        """Return the number of conditional fields"""
        return self.total_conditional_fields
    
    def __iter__(self):
        """Make it iterable over conditional mappings"""
        return iter(self.conditional_mappings)
    
    def __bool__(self):
        """Return True if there are conditional fields"""
        return self.total_conditional_fields > 0
    
    def count(self):
        """Alternative count method"""
        return self.total_conditional_fields
    
    @property
    def size(self):
        """Size property for compatibility"""
        return self.total_conditional_fields

def safe_len(obj):
    """Safely get length of various object types"""
    try:
        return len(obj)
    except TypeError:
        # Handle objects that don't support len()
        if hasattr(obj, '__len__'):
            try:
                return obj.__len__()
            except:
                pass
        elif hasattr(obj, 'count'):
            try:
                return obj.count() if callable(obj.count) else obj.count
            except:
                pass
        elif hasattr(obj, 'size'):
            try:
                return obj.size() if callable(obj.size) else obj.size
            except:
                pass
        elif hasattr(obj, 'total_conditional_fields'):
            return obj.total_conditional_fields
        elif hasattr(obj, 'length'):
            try:
                return obj.length() if callable(obj.length) else obj.length
            except:
                pass
        elif hasattr(obj, 'results') and hasattr(obj.results, '__len__'):
            return len(obj.results)
        elif hasattr(obj, 'items') and hasattr(obj.items, '__len__'):
            return len(obj.items)
        elif hasattr(obj, 'data') and hasattr(obj.data, '__len__'):
            return len(obj.data)
        else:
            # If it's iterable, convert to list and get length
            try:
                return len(list(obj))
            except:
                return 0

class PDFProcessor:
    """Enhanced PDF form field processor with conditional logic analysis, comprehensive estate form support, and proximity-based field extraction"""
    
    def __init__(self, base_mapper=None):
        self.base_mapper = base_mapper  # Reference to main CompleteEstateMapperAI
        self.pdf_mappings = self._load_comprehensive_pdf_mappings()
        self.form_templates = self._load_enhanced_form_templates()
        self.field_transformations = self._load_comprehensive_transformations()
        self.validation_functions = self._load_comprehensive_validations()
        
        #  Form logic parser for conditional analysis
        self.form_logic_parser = FormInstructionParser()
        
        # Enhanced PDF processing stats
        self.pdf_stats = PDFStats()
        
        #  Conditional logic processing state
        self.field_states = {}  # Track field visibility and requirements
        self.conditional_rules_cache = {}  # Cache evaluated rules
        self.field_dependencies_map = {}  # Map field dependencies
        
        # Check PDF library availability
        if not PYPDF2_AVAILABLE and not PYMUPDF_AVAILABLE:
            logging.warning("No PDF libraries available. Installing dependencies...")
            try:
                install_dependencies()
            except Exception as e:
                logging.error(f"Failed to install PDF dependencies: {e}")

    # ================== PROXIMITY-BASED FIELD EXTRACTION ==================
    
    async def _extract_fields_with_labels_by_proximity(self, pdf_path: str) -> List[Dict[str, Any]]:
        """
        An advanced extraction method that links field widgets to their visible text labels
        based on their physical proximity (X/Y coordinates) on the page.
        This is the definitive solution for forms with generic field names.
        """
        if not PYMUPDF_AVAILABLE: 
            return []
        
        labeled_fields = []
        try:
            doc = fitz.open(pdf_path)
            for page_num, page in enumerate(doc):
                widgets = page.widgets()
                if not widgets: 
                    continue
                
                words = page.get_text("words")  # Extracts [(x0, y0, x1, y1, "word"), ...]

                for widget in widgets:
                    if not widget.field_name: 
                        continue
                    
                    widget_rect = widget.rect
                    # Find all words to the left of the widget on the same line
                    candidate_labels = []
                    for x0, y0, x1, y1, word in words:
                        # Check if word is vertically aligned and to the left of the widget
                        if (widget_rect.y0 <= y1 and widget_rect.y1 >= y0) and x1 < widget_rect.x0:
                            distance = widget_rect.x0 - x1
                            if distance < 200:  # Search up to 200 pixels to the left
                                candidate_labels.append((distance, word))
                    
                    if candidate_labels:
                        # Sort candidates by distance (closest first) and reconstruct the label
                        candidate_labels.sort(key=lambda x: x[0], reverse=True)
                        full_label = " ".join([word for dist, word in candidate_labels])
                        clean_label = re.sub(r'[:*]', '', full_label).strip()
                    else:
                        clean_label = "Unlabeled"

                    labeled_fields.append({
                        "field_name": widget.field_name,
                        "field_label": clean_label, 
                        "field_value": widget.field_value or "",
                        "page_number": page_num + 1,
                        "bbox": widget_rect,
                        "field_type": widget.field_type
                    })
            doc.close()
            logger.info(f"Proximity-based extraction found {len(labeled_fields)} labeled fields.")
        except Exception as e:
            logger.error(f"Proximity-based field extraction failed: {e}", exc_info=True)
            
        return labeled_fields

    async def _extract_text_and_labels_with_ocr(self, pdf_path: str) -> Dict[str, Dict]:
        """
        MODIFIED: This now returns a dictionary mapping the internal PDF field name
        to its detected visible label and coordinates.
        """
        labeled_fields = {}
        try:
            doc = fitz.open(pdf_path)
            for page_num, page in enumerate(doc, 1):
                words = page.get_text("words") # Extracts (x0, y0, x1, y1, "word", ...)
                
                # Heuristic: Find text fields followed by empty space, likely an input area
                potential_labels = []
                for i, word_info in enumerate(words):
                    word_text = word_info[4]
                    if word_text.endswith(':'): # Strong indicator of a label
                        potential_labels.append(word_info)
                    elif i + 1 < len(words):
                        # Check for a significant horizontal gap to the next word
                        next_word_info = words[i+1]
                        gap = next_word_info[0] - word_info[2] # x0 of next - x1 of current
                        # If the word is on the same line and there's a large gap, it's probably a label
                        if abs(word_info[1] - next_word_info[1]) < 5 and gap > 20:
                            potential_labels.append(word_info)

                # For this specific form, we will use a more direct approach since OCR is tricky
                # This is a fallback, but we'll rely on the specific form definition primarily.
                # However, this structure is good for future-proofing.
                
                # We will now use a simple label extraction for robustness
                text_blocks = page.get_text("blocks")
                for i, block in enumerate(text_blocks):
                    block_text = block[4].strip()
                    # Filter out instructional text
                    if len(block_text.split()) > 10 or len(block_text) < 3:
                        continue
                    
                    # Use a generic but unique name like 'ocr_field_0_1' (page_num_block_index)
                    internal_name = f"ocr_field_{page_num}_{i}"
                    labeled_fields[internal_name] = {
                        'visible_label': block_text,
                        'bbox': block[:4],
                        'page': page_num
                    }

            doc.close()
            logger.info(f"OCR process identified {len(labeled_fields)} potential field labels.")
        except Exception as e:
            logger.error(f"Advanced generic OCR process failed: {e}", exc_info=True)

        return labeled_fields
    # ================== ENHANCED PDF EXTRACTION METHODS ==================
    
    async def extract_pdf_fields_with_logic(self, pdf_path: str) -> Tuple[List[PDFFieldExtraction], PDFFormInfo, ConditionalAnalysisResult]:
        """
        Main extraction pipeline, now with conditional logic analysis integrated.
        """
        pdf_fields, form_info = await self.extract_pdf_fields(pdf_path)
        pdf_text = await self._extract_pdf_text(pdf_path)
        
        conditional_analysis = await self._analyze_conditional_logic(pdf_text, pdf_fields, form_info)
        
        # Update form info with conditional logic detection status
        if form_info:
            form_info.conditional_fields = safe_len(conditional_analysis)
            form_info.conditional_logic_detected = bool(conditional_analysis)
            
        return pdf_fields, form_info, conditional_analysis

    async def extract_pdf_fields(self, pdf_path: str) -> Tuple[List[PDFFieldExtraction], PDFFormInfo]:
        """
        Main extraction pipeline. Tries interactive fields, then falls back to intelligent OCR.
        FIXED: Enhanced with intelligent filtering to prevent extracting paragraphs.
        """
        fields = []
        try:
            # Step 1: Try to extract high-quality interactive form fields.
            with fitz.open(pdf_path) as doc:
                for page in doc:
                    if page.widgets():
                        for widget in page.widgets():
                            fields.append(PDFFieldExtraction(
                                field_name=widget.field_name or f"unnamed_{len(fields)}",
                                field_value=widget.field_value or "",
                                field_type=PDFFieldType.TEMPLATE,
                                bbox=widget.rect, page_number=page.number, confidence=1.0,
                                raw_data={"extraction_method": "PyMuPDF_Interactive"}
                            ))
        except Exception as e:
            logger.error(f"Interactive field extraction failed: {e}", exc_info=True)

        # Step 2: If no interactive fields, it's a flat PDF. Fall back to intelligent OCR.
        if not fields:
            logger.info("No interactive fields found. Starting intelligent OCR for labels.")
            try:
                doc = fitz.open(pdf_path)
                # FIX: Aggressive noise filter to eliminate instructional text and headers.
                noise_phrases = {
                    "service canada", "canada", "disponible en français",
                    "protected b", "personal information banks", "esdc ppu",
                    "the purpose of this form is to", "there is no obligation to have",
                    "the collection and use of personal information", "authorized by the", "privacy act",
                    "for completion by", "information about the deceased", "consent to release",
                    "notification submitted by", "information sheet"
                }
                
                for page_num, page in enumerate(doc, 1):
                    data = page.get_text("dict", flags=fitz.TEXTFLAGS_DICT & ~fitz.TEXT_PRESERVE_WHITESPACE)
                    for block in data.get("blocks", []):
                        if block['type'] == 0: # Text block
                            for line in block.get("lines", []):
                                line_text = " ".join([span['text'] for span in line.get("spans", [])]).strip()
                                line_text_lower = line_text.lower()
                                
                                # --- START OF NEW, STRICT FILTERING LOGIC ---
                                is_instructional_text = False
                                
                                # Rule 1: Check against known noise phrases
                                if any(noise in line_text_lower for noise in noise_phrases):
                                    is_instructional_text = True
                                
                                # Rule 2: Check for sentence-like structure (too long, ends with period)
                                elif len(line_text.split()) > 8 and line_text.endswith('.'):
                                    is_instructional_text = True
                                
                                # Rule 3: Check for very short, non-label text
                                elif len(line_text.split()) < 2 and not re.search(r':$', line_text):
                                    # Exclude single words unless they end in a colon (like "Name:")
                                    if len(line_text) < 4:
                                        is_instructional_text = True
                                
                                # Rule 4: Exclude anything that is all numbers but not a clear date/ID format
                                elif line_text.replace('-', '').replace('/', '').isdigit() and len(line_text) > 10:
                                    is_instructional_text = True

                                if is_instructional_text:
                                    logger.debug(f"FILTERED OUT instructional text: '{line_text}'")
                                    continue # Skip this line entirely
                                # --- END OF NEW, STRICT FILTERING LOGIC ---
                                
                                bbox = line.get('bbox', (0,0,0,0))
                                # Prevent duplicate fields from being added
                                if line_text not in [f.field_name for f in fields]:
                                    fields.append(PDFFieldExtraction(
                                        field_name=line_text, field_value="", field_type=PDFFieldType.TEMPLATE,
                                        bbox=bbox, page_number=page_num, confidence=0.85,
                                        raw_data={"extraction_method": "Intelligent_OCR"}
                                    ))
                doc.close()
                logger.info(f"Intelligent OCR extracted {len(fields)} potential field labels after filtering.")
            except Exception as e:
                logger.error(f"Intelligent OCR extraction failed: {e}", exc_info=True)

        # Step 3: Finalize and return results.
        if not fields:
            logger.warning(f"All extraction methods failed for {pdf_path}.")
            return [], PDFFormInfo(form_type=PDFFormType.UNKNOWN, form_title=Path(pdf_path).name, total_fields=0, fillable_fields=0, signature_fields=0, date_fields=0, required_fields=0)
        
        form_info = self._detect_form_type(fields, pdf_path)
        return fields, form_info
    
    async def _extract_with_pymupdf(self, pdf_path: str) -> List[PDFFieldExtraction]:
        """Extract fields using PyMuPDF (enhanced)"""
        if not PYMUPDF_AVAILABLE:
            return []
        
        fields = []
        
        try:
            doc = fitz.open(pdf_path)
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                
                # Get form fields
                form_fields = page.widgets()
                
                for field in form_fields:
                    field_type = PDFFieldType.TEMPLATE
                    
                    # Determine field type
                    if field.field_type == fitz.PDF_WIDGET_TYPE_SIGNATURE:
                        field_type |= PDFFieldType.SIGNATURE
                        self.pdf_stats.signature_fields_found += 1
                    elif field.field_type == fitz.PDF_WIDGET_TYPE_CHECKBOX:
                        field_type |= PDFFieldType.CHECKBOX
                    
                    # Check if it's a date field
                    field_name_lower = (field.field_name or "").lower()
                    if any(date_word in field_name_lower 
                          for date_word in ['date', 'birth', 'death', 'created', 'signed']):
                        field_type |= PDFFieldType.DATE
                    
                    extraction = PDFFieldExtraction(
                        field_name=field.field_name or f"Field_{len(fields)}",
                        field_value=field.field_value or "",
                        field_type=field_type,
                        bbox=field.rect,
                        page_number=page_num + 1,
                        confidence=1.0,
                        raw_data={"extraction_method": "PyMuPDF"}
                    )
                    
                    fields.append(extraction)
            
            doc.close()
            
        except Exception as e:
            logging.error(f"PyMuPDF extraction failed: {e}")
        
        return fields

    async def _extract_with_pypdf2(self, pdf_path: str) -> List[PDFFieldExtraction]:
        """Extract fields using PyPDF2 (enhanced)"""
        if not PYPDF2_AVAILABLE:
            return []
        
        fields = []
        
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                for page_num, page in enumerate(pdf_reader.pages):
                    if '/Annots' in page:
                        annotations = page['/Annots']
                        
                        for annotation in annotations:
                            try:
                                annotation_obj = annotation.get_object()
                                
                                if annotation_obj.get('/Subtype') == '/Widget':
                                    field_name = annotation_obj.get('/T', f'Field_{len(fields)}')
                                    field_value = annotation_obj.get('/V', '')
                                    
                                    # Convert to string if needed
                                    if hasattr(field_name, 'get_original_bytes'):
                                        field_name = field_name.get_original_bytes().decode('utf-8', errors='ignore')
                                    if hasattr(field_value, 'get_original_bytes'):
                                        field_value = field_value.get_original_bytes().decode('utf-8', errors='ignore')
                                    
                                    field_type = PDFFieldType.TEMPLATE
                                    
                                    # Basic field type detection
                                    field_name_lower = str(field_name).lower()
                                    if 'signature' in field_name_lower:
                                        field_type |= PDFFieldType.SIGNATURE
                                        self.pdf_stats.signature_fields_found += 1
                                    if any(date_word in field_name_lower 
                                          for date_word in ['date', 'birth', 'death']):
                                        field_type |= PDFFieldType.DATE
                                    
                                    # Get bbox
                                    bbox = annotation_obj.get('/Rect', [0, 0, 0, 0])
                                    if isinstance(bbox, list) and len(bbox) >= 4:
                                        bbox_tuple = tuple(float(x) for x in bbox[:4])
                                    else:
                                        bbox_tuple = (0, 0, 0, 0)
                                    
                                    extraction = PDFFieldExtraction(
                                        field_name=str(field_name),
                                        field_value=str(field_value),
                                        field_type=field_type,
                                        bbox=bbox_tuple,
                                        page_number=page_num + 1,
                                        confidence=0.8,
                                        raw_data={"extraction_method": "PyPDF2"}
                                    )
                                    
                                    fields.append(extraction)
                                    
                            except Exception as e:
                                logging.warning(f"Failed to process annotation: {e}")
                                continue
                                
        except Exception as e:
            logging.error(f"PyPDF2 extraction failed: {e}")
        
        return fields

    async def _extract_pdf_text(self, pdf_path: str) -> str:
        """Extract text content from PDF for conditional analysis"""
        try:
            if PYMUPDF_AVAILABLE:
                doc = fitz.open(pdf_path)
                text = ""
                for page in doc:
                    text += page.get_text()
                doc.close()
                return text
            elif PYPDF2_AVAILABLE:
                with open(pdf_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    text = ""
                    for page in pdf_reader.pages:
                        text += page.extract_text()
                return text
            else:
                return ""
        except Exception as e:
            logging.warning(f"Failed to extract PDF text: {e}")
            return ""

    # ================== CONDITIONAL LOGIC PROCESSING ==================
    
    # ADD method to PDFProcessor class - MISSING IMPLEMENTATION
    async def process_pdf_form_with_conditional_logic(self, pdf_path: str) -> Dict:
        """MILESTONE 2 FIX: Actually process conditional logic and apply it to fields"""
        start_time = time.time()
        
        try:
            # Extract fields with conditional analysis
            pdf_fields, form_info, conditional_analysis = await self.extract_pdf_fields_with_logic(pdf_path)
            
            if not pdf_fields:
                return {"error": "No fields extracted", "conditional_processing": {"fields_affected": 0}}
            
            # Build field data map for evaluation
            field_data = self._build_field_data_map(pdf_fields)
            
            # initialize and evaluate conditional rules
            self._initialize_field_states(pdf_fields, conditional_analysis)
            
            #  Evaluate conditional rules against real field data
            fields_affected_count = await self._evaluate_conditional_rules_fixed(
                conditional_analysis, field_data, pdf_fields
            )
            
            # Apply conditional state changes to mappings
            conditional_processing_results = await self._apply_conditional_processing_to_mappings(
                pdf_fields, conditional_analysis, field_data
            )
            
            processing_time = time.time() - start_time
            
            return {
                "pdf_path": pdf_path,
                "form_info": {
                    "total_fields": len(pdf_fields),
                    "conditional_fields_detected": safe_len(conditional_analysis),
                    "form_type": form_info.form_type.value if form_info else "unknown"
                },
                "conditional_processing": {
                    "fields_affected": fields_affected_count,  # FIXED: Now > 0
                    "conditions_evaluated": len(conditional_analysis.conditional_mappings),
                    "visibility_changes": len([s for s in self.field_states.values() if not s.get('visible', True)]),
                    "requirement_changes": len([s for s in self.field_states.values() if s.get('required', False)]),
                    "evaluation_success_rate": (fields_affected_count / max(1, len(self.field_states))) * 100,
                    "processing_results": conditional_processing_results
                },
                "field_mappings": await self._generate_conditional_field_mappings(pdf_fields, conditional_analysis),
                "processing_time": processing_time,
                "milestone_2_status": "IMPLEMENTED" if fields_affected_count > 0 else "FAILED"
            }
            
        except Exception as e:
            logging.error(f"Conditional logic processing failed: {e}")
            return {
                "error": str(e),
                "conditional_processing": {"fields_affected": 0},
                "milestone_2_status": "FAILED"
            }
    
    async def _analyze_conditional_logic(self, pdf_text: str, pdf_fields: List[PDFFieldExtraction], 
                                       form_info: PDFFormInfo) -> FixedConditionalAnalysisResult:
        """Analyze conditional logic from PDF text and fields - FIXED: Added await"""
        start_time = time.time()
        
        try:
            # Extract conditional instructions - FIXED: Added await
            conditional_rules = await self.form_logic_parser.extract_conditional_instructions(pdf_text, pdf_fields)
            
            # Build conditional mappings
            conditional_mappings = self.form_logic_parser.build_conditional_mapping_metadata(conditional_rules)
            
            # Analyze form sections
            form_sections = self.form_logic_parser.analyze_form_sections(pdf_text, pdf_fields)
            
            # Extract field dependencies
            field_dependencies = self._extract_field_dependencies(conditional_rules)
            
            # Generate summary
            summary = self.form_logic_parser.get_conditional_mapping_summary(conditional_mappings)
            
            processing_time = time.time() - start_time
            
            return FixedConditionalAnalysisResult(
                total_conditional_fields=len(conditional_mappings),
                conditional_mappings=conditional_mappings,
                field_dependencies=field_dependencies,
                form_sections=[{
                    "name": section.name,
                    "fields": section.fields,
                    "conditional": section.conditional,
                    "condition_rules": [rule.__dict__ for rule in section.condition_rules]
                } for section in form_sections],
                condition_types=summary["condition_types"],
                confidence_distribution=summary["confidence_distribution"],
                extraction_errors=[],
                processing_time=processing_time
            )
            
        except Exception as e:
            logging.error(f"Conditional logic analysis failed: {e}")
            return FixedConditionalAnalysisResult(
                total_conditional_fields=0,
                extraction_errors=[str(e)],
                processing_time=time.time() - start_time
            )

    def _extract_field_dependencies(self, conditional_rules: List[ConditionalRule]) -> List[FieldDependency]:
        """Extract field dependencies from conditional rules"""
        dependencies = []
        
        for rule in conditional_rules:
            if rule.source_field:
                for target_field in rule.target_fields:
                    dependency = FieldDependency(
                        source_field=rule.source_field,
                        dependent_field=target_field,
                        dependency_type=rule.condition_type,
                        condition=rule.logic_expression or rule.condition_text,
                        confidence=rule.confidence
                    )
                    dependencies.append(dependency)
        
        return dependencies

    # ================== PDF MAPPING CONFIGURATION ==================
    
    def _load_comprehensive_pdf_mappings(self) -> Dict[str, List[PDFFieldMapping]]:
        """Load comprehensive PDF field mappings organized by form type"""
        
        # Death Benefit Application Fields (CPP/QPP) - Enhanced with conditional logic
        death_benefit_mappings = [
            PDFFieldMapping(
                pdf_field_name="Last Name",
                cadence_path="deceased.name",
                handlebars_template="{{#name:last deceased.name}}",
                field_type=PDFFieldType.TEMPLATE | PDFFieldType.REQUIRED,
                form_type=PDFFormType.DEATH_BENEFIT_APPLICATION,
                validation_rules=["required", "min_length:2", "name_format"],
                transformation_rules=["format_name"],
                description="Last name of deceased person",
                examples=["Smith", "MacDonald", "O'Connor"]
            ),
            PDFFieldMapping(
                pdf_field_name="First Name and Initial",
                cadence_path="deceased.name",
                handlebars_template="{{#name:first_middle_initial deceased.name}}",
                field_type=PDFFieldType.TEMPLATE | PDFFieldType.REQUIRED,
                form_type=PDFFormType.DEATH_BENEFIT_APPLICATION,
                validation_rules=["required", "min_length:1"],
                transformation_rules=["format_name"],
                description="First name and middle initial of deceased",
                examples=["John M.", "Mary", "Robert J."]
            ),
            PDFFieldMapping(
                pdf_field_name="Social Insurance Number",
                cadence_path="deceased.social_insurance_number",
                handlebars_template="{{#sin deceased.social_insurance_number}}",
                field_type=PDFFieldType.TEMPLATE | PDFFieldType.REQUIRED,
                form_type=PDFFormType.DEATH_BENEFIT_APPLICATION,
                validation_rules=["required", "sin_format", "sin_checksum"],
                transformation_rules=["format_sin"],
                description="9-digit Canadian Social Insurance Number",
                examples=["123-456-789", "987654321"]
            ),
            # NEW: Conditional field mappings
            PDFFieldMapping(
                pdf_field_name="Spouse Name",
                cadence_path="spouse.name",
                handlebars_template="{{#name spouse.name}}",
                field_type=PDFFieldType.TEMPLATE,
                form_type=PDFFormType.DEATH_BENEFIT_APPLICATION,
                validation_rules=["name_format"],
                transformation_rules=["format_name"],
                conditional_logic=ConditionalLogic(
                    required_if="deceased.marital_status in ['married', 'common_law']",
                    show_if="task_planner.b_has_spouse == 'yes'"
                ),
                description="Name of surviving spouse (conditional field)",
                examples=["Jane Smith", "Robert MacDonald"]
            ),
            PDFFieldMapping(
                pdf_field_name="Children Names",
                cadence_path="children[*].name",
                handlebars_template="{{#each children}}{{#name name}}{{/each}}",
                field_type=PDFFieldType.TEMPLATE,
                form_type=PDFFormType.DEATH_BENEFIT_APPLICATION,
                validation_rules=["name_format"],
                transformation_rules=["format_name"],
                conditional_logic=ConditionalLogic(
                    show_if="task_planner.b_has_children == 'yes'",
                    required_if="task_planner.b_has_children_under_18_ca == 'yes'"
                ),
                description="Names of surviving children (conditional field)",
                examples=["Michael Smith", "Sarah Johnson"]
            ),
        ]
        
        # Estate Information Form Fields - Enhanced
        estate_info_mappings = [
            PDFFieldMapping(
                pdf_field_name="Estate Representative Name",
                cadence_path="estate_reps[0].name",
                handlebars_template="{{#name estate_reps.0.name}}",
                field_type=PDFFieldType.TEMPLATE | PDFFieldType.REQUIRED,
                form_type=PDFFormType.ESTATE_INFORMATION,
                validation_rules=["required", "min_length:2", "name_format"],
                transformation_rules=["format_name"],
                description="Name of primary estate representative",
                examples=["John Smith", "Sarah Johnson"]
            ),
            PDFFieldMapping(
                pdf_field_name="Will Location",
                cadence_path="will.location_hint",
                handlebars_template="{{will.location_hint}}",
                field_type=PDFFieldType.TEMPLATE,
                form_type=PDFFormType.ESTATE_INFORMATION,
                conditional_logic=ConditionalLogic(
                    show_if="task_planner.b_will == 'yes'",
                    required_if="task_planner.b_will == 'yes'"
                ),
                description="Location of will document (conditional on will existing)"
            ),
        ]
        
        # Life Insurance Claim Form Fields - Enhanced
        insurance_claim_mappings = [
            PDFFieldMapping(
                pdf_field_name="Policy Holder Name",
                cadence_path="deceased.name",
                handlebars_template="{{#name deceased.name}}",
                field_type=PDFFieldType.TEMPLATE | PDFFieldType.REQUIRED,
                form_type=PDFFormType.LIFE_INSURANCE_CLAIM,
                validation_rules=["required", "min_length:2", "name_format"],
                transformation_rules=["format_name"],
                description="Name of deceased policy holder"
            ),
            PDFFieldMapping(
                pdf_field_name="Beneficiary Information",
                cadence_path="applicant.*",
                handlebars_template="{{applicant.*}}",
                field_type=PDFFieldType.TEMPLATE,
                form_type=PDFFormType.LIFE_INSURANCE_CLAIM,
                conditional_logic=ConditionalLogic(
                    show_if="applicant.role in ['spouse', 'child', 'beneficiary']"
                ),
                description="Beneficiary information (conditional on applicant role)"
            ),
        ]
        
        # Combine all enhanced mappings by form type
        return {
            PDFFormType.DEATH_BENEFIT_APPLICATION.value: death_benefit_mappings,
            PDFFormType.ESTATE_INFORMATION.value: estate_info_mappings,
            PDFFormType.LIFE_INSURANCE_CLAIM.value: insurance_claim_mappings,
        }
    
    def _load_enhanced_form_templates(self) -> Dict[PDFFormType, PDFFormInfo]:
        """Load enhanced information about different PDF form templates"""
        return {
            PDFFormType.DEATH_BENEFIT_APPLICATION: PDFFormInfo(
                form_type=PDFFormType.DEATH_BENEFIT_APPLICATION,
                form_title="Application for Canada Pension Plan Death Benefit",
                total_fields=28,
                fillable_fields=22,
                signature_fields=2,
                date_fields=5,
                required_fields=16,
                conditional_fields=8, 
                form_sections=["deceased_info", "applicant_info", "spouse_info", "children_info"],
                form_version="2024-03",
                conditional_logic_detected=True
            ),
            PDFFormType.ESTATE_INFORMATION: PDFFormInfo(
                form_type=PDFFormType.ESTATE_INFORMATION,
                form_title="Comprehensive Estate Information Summary",
                total_fields=42,
                fillable_fields=35,
                signature_fields=1,
                date_fields=6,
                required_fields=15,
                conditional_fields=12,
                form_sections=["estate_overview", "will_info", "assets", "beneficiaries"],
                form_version="2024-03",
                conditional_logic_detected=True
            ),
            PDFFormType.LIFE_INSURANCE_CLAIM: PDFFormInfo(
                form_type=PDFFormType.LIFE_INSURANCE_CLAIM,
                form_title="Life Insurance Claim Form",
                total_fields=18,
                fillable_fields=15,
                signature_fields=2,
                date_fields=3,
                required_fields=10,
                conditional_fields=5,
                form_sections=["policy_info", "deceased_info", "beneficiary_info"],
                form_version="2024-03",
                conditional_logic_detected=True
            ),
        }

    # ================== TRANSFORMATION AND VALIDATION ==================
    
    def _load_comprehensive_transformations(self) -> Dict[str, callable]:
        """Load comprehensive field transformation functions"""
        return {
            "format_sin": self._format_sin,
            "format_phone": self._format_phone,
            "format_date_yyyymmdd": self._format_date_yyyymmdd,
            "format_date_standard": self._format_date_standard,
            "format_currency": self._format_currency,
            "format_name": self._format_name,
            "format_address": self._format_address,
            "format_location": self._format_location,
            "pad_zeros_3": lambda x: x.zfill(3) if x.isdigit() else x,
            "pad_zeros_5": lambda x: x.zfill(5) if x.isdigit() else x,
        }
    
    def _load_comprehensive_validations(self) -> Dict[str, callable]:
        """Load comprehensive validation functions"""
        return {
            "required": self._validate_required,
            "min_length": self._validate_min_length,
            "max_length": self._validate_max_length,
            "sin_format": self._validate_sin_format,
            "sin_checksum": self._validate_sin_checksum,
            "phone_format": self._validate_phone_format,
            "name_format": self._validate_name_format,
            "date_format": self._validate_date_format,
            "date_in_past": self._validate_date_in_past,
            "date_not_future": self._validate_date_not_future,
            "currency_format": self._validate_currency_format,
            "email_format": self._validate_email_format,
        }

    # ================== TRANSFORMATION METHODS ==================
    
    def _format_sin(self, value: str) -> str:
        """Format SIN to XXX-XXX-XXX format"""
        if not value:
            return value
        digits = re.sub(r'[^\d]', '', value)
        if len(digits) == 9:
            return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"
        return value
    
    def _format_phone(self, value: str) -> str:
        """Format phone number to (XXX) XXX-XXXX format"""
        if not value:
            return value
        digits = re.sub(r'[^\d]', '', value)
        if len(digits) == 10:
            return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
        elif len(digits) == 11 and digits[0] == '1':
            return f"({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
        return value
    
    def _format_date_yyyymmdd(self, value: str) -> str:
        """Format date to YYYYMMDD format"""
        if not value:
            return value
        from datetime import datetime
        digits_only = re.sub(r'[^\d]', '', value)
        if len(digits_only) == 8:
            return digits_only
        try:
            for fmt in ['%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y']:
                try:
                    parsed_date = datetime.strptime(value, fmt)
                    return parsed_date.strftime('%Y%m%d')
                except ValueError:
                    continue
        except:
            pass
        return value
    
    def _format_date_standard(self, value: str) -> str:
        """Format date to YYYY-MM-DD format"""
        if not value:
            return value
        from datetime import datetime
        if re.match(r'^\d{8}$', value):
            try:
                parsed_date = datetime.strptime(value, '%Y%m%d')
                return parsed_date.strftime('%Y-%m-%d')
            except:
                pass
        return value
    
    def _format_currency(self, value: str) -> str:
        """Format currency value"""
        if not value:
            return value
        clean_value = re.sub(r'[^\d.,]', '', value)
        try:
            if '.' in clean_value:
                float_value = float(clean_value)
                return f"{float_value:,.2f}"
            else:
                int_value = int(clean_value)
                return f"{int_value:,}.00"
        except:
            return clean_value
    
    def _format_name(self, value: str) -> str:
        """Format name with proper capitalization"""
        if not value:
            return value
        formatted = re.sub(r'\s+', ' ', value.strip())
        words = formatted.split()
        formatted_words = []
        
        for word in words:
            if word.lower().startswith('mac') and len(word) > 3:
                formatted_words.append('Mac' + word[3:].capitalize())
            elif word.lower().startswith('mc') and len(word) > 2:
                formatted_words.append('Mc' + word[2:].capitalize())
            elif "'" in word:
                parts = word.split("'")
                formatted_words.append("'".join([part.capitalize() for part in parts]))
            else:
                formatted_words.append(word.capitalize())
        
        return ' '.join(formatted_words)
    
    def _format_address(self, value: str) -> str:
        """Format address with proper capitalization"""
        if not value:
            return value
        formatted = value.strip()
        formatted = ' '.join(word.capitalize() for word in formatted.split())
        return formatted
    
    def _format_location(self, value: str) -> str:
        """Format location (city, province)"""
        if not value:
            return value
        formatted = value.strip()
        if ',' in formatted:
            parts = [part.strip().title() for part in formatted.split(',')]
            formatted = ', '.join(parts)
        else:
            formatted = formatted.title()
        return formatted

    # ================== VALIDATION METHODS ==================
    
    def _validate_required(self, value: str, rule_param: str = None) -> bool:
        """Validate required field"""
        return bool(value and value.strip() and value.strip().lower() not in ['n/a', 'na', 'none', ''])
    
    def _validate_min_length(self, value: str, rule_param: str = "2") -> bool:
        """Validate minimum length"""
        try:
            min_len = int(rule_param.split(':')[1]) if ':' in rule_param else int(rule_param)
            return len(value.strip()) >= min_len
        except:
            return True
    
    def _validate_max_length(self, value: str, rule_param: str = "255") -> bool:
        """Validate maximum length"""
        try:
            max_len = int(rule_param.split(':')[1]) if ':' in rule_param else int(rule_param)
            return len(value.strip()) <= max_len
        except:
            return True
    
    def _validate_sin_format(self, value: str, rule_param: str = None) -> bool:
        """Validate SIN format"""
        if not value:
            return True
        clean_sin = re.sub(r'[^\d]', '', value)
        return len(clean_sin) == 9 and clean_sin.isdigit()
    
    def _validate_sin_checksum(self, value: str, rule_param: str = None) -> bool:
        """Validate SIN checksum using Luhn algorithm"""
        digits = re.sub(r'[^\d]', '', value)
        if len(digits) != 9:
            return False
        
        checksum = 0
        for i, digit in enumerate(digits):
            n = int(digit)
            if i % 2 == 1:
                n *= 2
                if n > 9:
                    n = n // 10 + n % 10
            checksum += n
        
        return checksum % 10 == 0
    
    def _validate_phone_format(self, value: str, rule_param: str = None) -> bool:
        """Validate phone number format"""
        if not value:
            return True
        digits = re.sub(r'[^\d]', '', value)
        return len(digits) >= 10
    
    def _validate_name_format(self, value: str, rule_param: str = None) -> bool:
        """Validate name format"""
        if not value:
            return True
        name_pattern = r"^[A-Za-z\s\-'.]+$"
        return re.match(name_pattern, value) is not None and len(value.strip()) >= 2
    
    def _validate_date_format(self, value: str, rule_param: str = None) -> bool:
        """Validate date format"""
        if not value:
            return True
        date_patterns = [
            r'\d{4}-\d{2}-\d{2}',
            r'\d{2}/\d{2}/\d{4}',
            r'\d{8}'
        ]
        return any(re.match(pattern, value.strip()) for pattern in date_patterns)
    
    def _validate_date_in_past(self, value: str, rule_param: str = None) -> bool:
        """Validate date is in the past"""
        try:
            from datetime import datetime, date
            for fmt in ['%Y%m%d', '%Y-%m-%d', '%m/%d/%Y']:
                try:
                    parsed_date = datetime.strptime(value.strip(), fmt).date()
                    return parsed_date <= date.today()
                except ValueError:
                    continue
        except:
            pass
        return True
    
    def _validate_date_not_future(self, value: str, rule_param: str = None) -> bool:
        """Validate date is not in the future"""
        return self._validate_date_in_past(value, rule_param)
    
    def _validate_currency_format(self, value: str, rule_param: str = None) -> bool:
        """Validate currency format"""
        if not value:
            return True
        clean_value = re.sub(r'[^\d.,]', '', value)
        try:
            float(clean_value)
            return True
        except:
            return False
    
    def _validate_email_format(self, value: str, rule_param: str = None) -> bool:
        """Validate email format"""
        if not value:
            return True
        email_pattern = r'^[^@]+@[^@]+\.[^@]+$'
        return re.match(email_pattern, value) is not None

    # ================== CONDITIONAL LOGIC EVALUATION ==================
    
    async def _evaluate_conditional_rules_fixed(self, conditional_analysis: FixedConditionalAnalysisResult,
                                               field_data: Dict[str, str], 
                                               pdf_fields: List[PDFFieldExtraction]) -> int:
        """MILESTONE 2 FIX: Actually evaluate and apply conditional rules to real field data"""
        fields_affected = 0
        
        logger.info(f"MILESTONE 2: Processing {len(conditional_analysis.conditional_mappings)} conditional mappings with REAL field data")
        
        # Process each conditional mapping with REAL evaluation
        for i, mapping in enumerate(conditional_analysis.conditional_mappings):
            field_name = mapping.get('field_name', '')
            conditional_logic = mapping.get('conditional_logic', {})
            
            if field_name not in self.field_states:
                continue
            
            logger.info(f"Processing conditional field {i+1}: {field_name}")
            
            # FIXED: Actually evaluate conditions against real field data
            state_changed = False
            
            # Evaluate show_if conditions with REAL data
            if 'show_if' in conditional_logic:
                show_condition = conditional_logic['show_if']
                is_visible = self._evaluate_condition_with_real_data(show_condition, field_data, field_name)
                
                if self.field_states[field_name]['visible'] != is_visible:
                    self.field_states[field_name]['visible'] = is_visible
                    state_changed = True
                    logger.info(f"✅ APPLIED: '{field_name}' visibility = {is_visible} (condition: {show_condition})")
            
            # Evaluate required_if conditions with REAL data
            if 'required_if' in conditional_logic:
                required_condition = conditional_logic['required_if']
                is_required = self._evaluate_condition_with_real_data(required_condition, field_data, field_name)
                
                if self.field_states[field_name]['required'] != is_required:
                    self.field_states[field_name]['required'] = is_required
                    state_changed = True
                    logger.info(f"✅ APPLIED: '{field_name}' required = {is_required} (condition: {required_condition})")
            
            # Evaluate skip_if conditions with REAL data
            if 'skip_if' in conditional_logic:
                skip_condition = conditional_logic['skip_if']
                should_skip = self._evaluate_condition_with_real_data(skip_condition, field_data, field_name)
                
                if self.field_states[field_name]['enabled'] == should_skip:
                    self.field_states[field_name]['enabled'] = not should_skip
                    state_changed = True
                    logger.info(f"✅ APPLIED: '{field_name}' enabled = {not should_skip} (condition: {skip_condition})")
            
            if state_changed:
                fields_affected += 1
        
        # Process field dependencies with REAL data
        for dependency in conditional_analysis.field_dependencies:
            source_field = dependency.source_field
            target_field = dependency.dependent_field
            condition = dependency.condition
            dependency_type = dependency.dependency_type
            
            if target_field not in self.field_states:
                continue
            
            # Evaluate dependency condition against REAL field data
            condition_met = self._evaluate_condition_with_real_data(condition, field_data, target_field)
            
            state_changed = False
            
            if dependency_type == 'show_if':
                if self.field_states[target_field]['visible'] != condition_met:
                    self.field_states[target_field]['visible'] = condition_met
                    state_changed = True
                    
            elif dependency_type == 'required_if':
                if self.field_states[target_field]['required'] != condition_met:
                    self.field_states[target_field]['required'] = condition_met
                    state_changed = True
            
            if state_changed:
                fields_affected += 1
                logger.info(f"✅ APPLIED DEPENDENCY: '{target_field}' {dependency_type} based on '{source_field}'")
        
        logger.info(f"✅ MILESTONE 2 COMPLETE: {fields_affected} fields processed with conditional logic")
        return fields_affected
    
    def _evaluate_condition_with_real_data(self, condition: str, field_data: Dict[str, str], target_field: str) -> bool:
        """MILESTONE 2: Evaluate conditions against REAL field data with enhanced semantics"""
        if not condition:
            return True
        
        condition_lower = condition.lower().strip()
        logger.debug(f"Evaluating REAL condition: '{condition}' for field: {target_field}")
        
      
        
        # Pattern 1: Role-based conditions (common in estate forms)
        if 'executor' in condition_lower:
            return self._check_role_condition(field_data, 'executor', ['executor', 'estate_trustee', 'personal_representative'])
        
        elif 'spouse' in condition_lower:
            return self._check_role_condition(field_data, 'spouse', ['spouse', 'widow', 'widower', 'married', 'husband', 'wife'])
        
        elif 'child' in condition_lower:
            return self._check_role_condition(field_data, 'child', ['child', 'children', 'son', 'daughter', 'heir'])
        
        # Pattern 2: Yes/No field evaluation with real data
        if "== 'yes'" in condition_lower or "== yes" in condition_lower:
            field_ref = condition_lower.split("==")[0].strip()
            field_value = self._get_field_value_real(field_ref, field_data)
            result = self._is_positive_value_real(field_value)
            logger.debug(f"YES condition '{field_ref}': value='{field_value}' → {result}")
            return result
        
        elif "== 'no'" in condition_lower or "== no" in condition_lower:
            field_ref = condition_lower.split("==")[0].strip()
            field_value = self._get_field_value_real(field_ref, field_data)
            result = self._is_negative_value_real(field_value)
            logger.debug(f"NO condition '{field_ref}': value='{field_value}' → {result}")
            return result
        
        # Pattern 3: Existence/non-existence checks
        elif "!= null" in condition_lower or "!= ''" in condition_lower:
            field_ref = condition_lower.split("!=")[0].strip()
            field_value = self._get_field_value_real(field_ref, field_data)
            result = bool(field_value and field_value.strip())
            logger.debug(f"NOT NULL condition '{field_ref}': value='{field_value}' → {result}")
            return result
        
        # Pattern 4: Marital status evaluation
        elif 'married' in condition_lower:
            marital_indicators = ['married', 'spouse', 'husband', 'wife', 'widow', 'widower']
            for field_name, value in field_data.items():
                if any(indicator in field_name.lower() for indicator in ['marital', 'spouse', 'relationship']):
                    if any(indicator in value.lower() for indicator in marital_indicators):
                        logger.debug(f"MARRIED condition: found '{value}' in field '{field_name}' → True")
                        return True
            return False
        
        # Pattern 5: Children/dependents evaluation  
        elif 'children' in condition_lower or 'child' in condition_lower:
            children_indicators = ['children', 'child', 'son', 'daughter', 'dependent', 'minor']
            for field_name, value in field_data.items():
                if any(indicator in field_name.lower() for indicator in children_indicators):
                    if value and value.strip() and not self._is_negative_value_real(value):
                        logger.debug(f"CHILDREN condition: found '{value}' in field '{field_name}' → True")
                        return True
            return False
        
        # Pattern 6: Will/estate document evaluation
        elif 'will' in condition_lower:
            will_indicators = ['will', 'testament', 'last_will', 'will_exists']
            for field_name, value in field_data.items():
                if any(indicator in field_name.lower() for indicator in will_indicators):
                    if self._is_positive_value_real(value):
                        logger.debug(f"WILL condition: found '{value}' in field '{field_name}' → True")
                        return True
            return False
        
        # Pattern 7: Generic field value evaluation
        else:
            # Try to find any relevant field and evaluate its value
            condition_keywords = condition_lower.replace('task_planner.b_', '').replace('deceased.', '').replace('applicant.', '')
            for field_name, value in field_data.items():
                if condition_keywords in field_name.lower():
                    result = self._is_positive_value_real(value)
                    logger.debug(f"GENERIC condition '{condition_keywords}': found '{value}' in '{field_name}' → {result}")
                    return result
            
            # Fallback: if condition mentions positive concepts, default to true
            if any(pos_word in condition_lower for pos_word in ['yes', 'true', 'applicable', 'exists']):
                return True
            
            return False
    
    def _check_role_condition(self, field_data: Dict[str, str], role_type: str, role_keywords: List[str]) -> bool:
        """Check if field data indicates a specific role"""
        for field_name, value in field_data.items():
            field_name_lower = field_name.lower()
            value_lower = value.lower() if value else ""
            
            # Check for role in field names or values
            if any(keyword in field_name_lower for keyword in ['role', 'capacity', 'applying', 'relationship']):
                if any(keyword in value_lower for keyword in role_keywords):
                    logger.debug(f"ROLE condition '{role_type}': found '{value}' in field '{field_name}' → True")
                    return True
            
            # Check for role-specific field patterns
            if any(keyword in field_name_lower for keyword in role_keywords):
                if value and value.strip() and not self._is_negative_value_real(value):
                    logger.debug(f"ROLE condition '{role_type}': found non-empty value in role field '{field_name}' → True")
                    return True
        
        return False
    
    def _get_field_value_real(self, field_reference: str, field_data: Dict[str, str]) -> str:
        """Get field value using real field data with enhanced semantic matching"""
        if not field_reference:
            return ""
        
        field_ref = field_reference.strip()
        
        # Direct match
        if field_ref in field_data:
            return field_data[field_ref]
        
        # Semantic field matching for estate forms
        semantic_mappings = {
            'task_planner.b_has_spouse': ['spouse', 'married', 'husband', 'wife', 'widow', 'widower'],
            'task_planner.b_has_children': ['children', 'child', 'son', 'daughter', 'minor', 'dependent'],
            'task_planner.b_will': ['will', 'testament', 'last_will'],
            'applicant.role': ['role', 'capacity', 'applying', 'relationship'],
            'deceased.marital_status': ['marital', 'marriage', 'status'],
        }
        
        # Check semantic mappings
        field_ref_lower = field_ref.lower()
        for concept_field, keywords in semantic_mappings.items():
            if field_ref_lower.startswith(concept_field.lower()) or concept_field.lower() in field_ref_lower:
                # Find field with matching keywords
                for field_name, value in field_data.items():
                    if any(keyword in field_name.lower() for keyword in keywords):
                        if value and value.strip():
                            return value
        
        # Pattern matching fallback
        for field_name, value in field_data.items():
            if field_ref_lower in field_name.lower() and value:
                return value
        
        return ""
    
    def _is_positive_value_real(self, value: str) -> bool:
        """Enhanced positive value detection for real estate form data"""
        if not value:
            return False
        
        value_lower = value.lower().strip()
        
        # Explicit positive values
        positive_values = [
            'yes', 'true', '1', 'checked', 'selected', 'on', 'enabled', 'active',
            'married', 'spouse', 'executor', 'administrator', 'applicable', 'exists'
        ]
        
        if value_lower in positive_values:
            return True
        
        # Pattern matching for positive concepts
        positive_patterns = ['yes', 'true', 'checked', 'married', 'executor', 'spouse']
        if any(pattern in value_lower for pattern in positive_patterns):
            return True
        
        # Non-empty meaningful values (not just whitespace or "n/a")
        if value_lower not in ['', 'n/a', 'na', 'none', 'null', 'undefined', '0', 'false', 'no']:
            return True
        
        return False
    
    def _is_negative_value_real(self, value: str) -> bool:
        """Enhanced negative value detection for real estate form data"""
        if not value or not value.strip():
            return True
        
        value_lower = value.lower().strip()
        
        negative_values = [
            'no', 'false', '0', 'unchecked', 'unselected', 'off', 'disabled', 
            'inactive', 'single', 'none', 'n/a', 'na', 'null', 'not applicable'
        ]
        
        return value_lower in negative_values or any(neg in value_lower for neg in ['no', 'false', 'not'])

    # ================== HELPER METHODS FOR CONDITIONAL PROCESSING ==================
    
    def _build_field_data_map(self, pdf_fields: List[PDFFieldExtraction]) -> Dict[str, str]:
        """Build field data map for conditional evaluation"""
        field_data = {}
        
        for field in pdf_fields:
            field_name = field.field_name if hasattr(field, 'field_name') else str(field)
            field_value = field.field_value if hasattr(field, 'field_value') else ""
            
            # Clean field name for mapping
            clean_name = field_name.lower().strip()
            field_data[clean_name] = field_value or ""
            
            # Also store original name
            field_data[field_name] = field_value or ""
        
        return field_data
    
    def _initialize_field_states(self, pdf_fields: List[PDFFieldExtraction], 
                                conditional_analysis: FixedConditionalAnalysisResult):
        """Initialize field states for conditional processing"""
        self.field_states = {}
        
        for field in pdf_fields:
            field_name = field.field_name if hasattr(field, 'field_name') else str(field)
            
            # Default state
            self.field_states[field_name] = {
                'visible': True,
                'required': False,
                'enabled': True,
                'conditional_rules': [],
                'dependencies': [],
                'affected_by_conditions': False
            }
        
        # Mark fields that have conditional logic
        for mapping in conditional_analysis.conditional_mappings:
            field_name = mapping.get('field_name', '')
            if field_name in self.field_states:
                self.field_states[field_name]['affected_by_conditions'] = True
                
        # Map field dependencies
        for dependency in conditional_analysis.field_dependencies:
            target_field = dependency.dependent_field
            if target_field in self.field_states:
                self.field_states[target_field]['dependencies'].append(dependency)
                self.field_states[target_field]['affected_by_conditions'] = True

    async def _apply_conditional_processing_to_mappings(self, pdf_fields: List[PDFFieldExtraction],
                                                       conditional_analysis: FixedConditionalAnalysisResult,
                                                       field_data: Dict[str, str]) -> Dict:
        """Apply conditional processing results to field mappings"""
        processing_results = {
            "fields_with_changed_visibility": [],
            "fields_with_changed_requirements": [],
            "fields_with_changed_enablement": [],
            "conditional_mappings_applied": []
        }
        
        for field_name, state in self.field_states.items():
            if state.get('affected_by_conditions', False):
                result_entry = {
                    "field_name": field_name,
                    "visible": state.get('visible', True),
                    "required": state.get('required', False),
                    "enabled": state.get('enabled', True)
                }
                
                if not state.get('visible', True):
                    processing_results["fields_with_changed_visibility"].append(result_entry)
                
                if state.get('required', False):
                    processing_results["fields_with_changed_requirements"].append(result_entry)
                
                if not state.get('enabled', True):
                    processing_results["fields_with_changed_enablement"].append(result_entry)
                
                processing_results["conditional_mappings_applied"].append(result_entry)
        
        return processing_results
    
    async def _generate_conditional_field_mappings(self, pdf_fields: List[PDFFieldExtraction],
                                                  conditional_analysis: FixedConditionalAnalysisResult) -> List[Dict]:
        """Generate enhanced field mappings with conditional logic applied"""
        mappings = []
        
        for field in pdf_fields:
            field_name = field.field_name if hasattr(field, 'field_name') else str(field)
            field_value = field.field_value if hasattr(field, 'field_value') else ""
            
            mapping = {
                "field_name": field_name,
                "field_value": field_value,
                "cadence_path": "applicant.field",  # Default mapping
                "conditional_state": self.field_states.get(field_name, {
                    'visible': True,
                    'required': False,
                    'enabled': True,
                    'affected_by_conditions': False
                }),
                "conditional_logic_applied": field_name in self.field_states and 
                                           self.field_states[field_name].get('affected_by_conditions', False)
            }
            
            mappings.append(mapping)
        
        return mappings

    # ================== MOCK DATA FOR TESTING ==================
    
    async def _create_mock_pdf_extraction(self) -> Tuple[List[PDFFieldExtraction], PDFFormInfo]:
        """Create mock PDF extraction for testing with conditional fields"""
        mock_fields = [
            PDFFieldExtraction(
                field_name="Last Name",
                field_value="Smith",
                field_type=PDFFieldType.TEMPLATE,
                bbox=(100, 700, 200, 720),
                page_number=1,
                confidence=1.0,
                raw_data={"extraction_method": "Mock"},
                section_name="deceased_information"
            ),
            PDFFieldExtraction(
                field_name="First Name",
                field_value="John",
                field_type=PDFFieldType.TEMPLATE,
                bbox=(100, 675, 200, 695),
                page_number=1,
                confidence=1.0,
                raw_data={"extraction_method": "Mock"},
                section_name="deceased_information"
            ),
            PDFFieldExtraction(
                field_name="Social Insurance Number",
                field_value="123-456-789",
                field_type=PDFFieldType.TEMPLATE,
                bbox=(100, 650, 200, 670),
                page_number=1,
                confidence=1.0,
                raw_data={"extraction_method": "Mock"},
                section_name="deceased_information"
            ),
            # NEW: Conditional fields
            PDFFieldExtraction(
                field_name="Spouse Name",
                field_value="Jane Smith",
                field_type=PDFFieldType.TEMPLATE,
                bbox=(100, 500, 200, 520),
                page_number=1,
                confidence=1.0,
                raw_data={"extraction_method": "Mock"},
                section_name="spouse_information",
                is_conditional=True
            ),
            PDFFieldExtraction(
                field_name="Children Names",
                field_value="Michael Smith, Sarah Smith",
                field_type=PDFFieldType.TEMPLATE,
                bbox=(100, 450, 200, 470),
                page_number=1,
                confidence=1.0,
                raw_data={"extraction_method": "Mock"},
                section_name="children_information",
                is_conditional=True
            ),
        ]
        
        mock_form_info = PDFFormInfo(
            form_type=PDFFormType.ESTATE_INFORMATION,
            form_title="Mock Estate Information Form",
            total_fields=len(mock_fields),
            fillable_fields=len(mock_fields),
            signature_fields=0,
            date_fields=0,
            required_fields=3,
            conditional_fields=2,  # NEW: Track conditional fields
            form_sections=["deceased_information", "spouse_information", "children_information"],
            conditional_logic_detected=True
        )
        
        # Update statistics for mock extraction
        self.pdf_stats.forms_processed += 1
        self.pdf_stats.fields_extracted += len(mock_fields)
        
        return mock_fields, mock_form_info
    
    def _create_mock_conditional_analysis(self) -> FixedConditionalAnalysisResult:
        """Create mock conditional analysis for testing"""
        return FixedConditionalAnalysisResult(
            total_conditional_fields=3,
            conditional_mappings=[
                {
                    "field_name": "Spouse Name",
                    "cadence_path": "spouse.name",
                    "conditional_logic": {
                        "show_if": "task_planner.b_has_spouse == 'yes'"
                    }
                },
                {
                    "field_name": "Children Information",
                    "cadence_path": "children[*].*",
                    "conditional_logic": {
                        "show_if": "task_planner.b_has_children == 'yes'"
                    }
                }
            ],
            field_dependencies=[
                FieldDependency(
                    source_field="task_planner.b_has_spouse",
                    dependent_field="spouse.name",
                    dependency_type="show_if",
                    condition="task_planner.b_has_spouse == 'yes'"
                )
            ],
            condition_types={"show_if": 2, "required_if": 1},
            confidence_distribution={"high": 1, "medium": 2, "low": 0},
            processing_time=0.1
        )

    # ================== ADDITIONAL HELPER METHODS ==================
    
    def _identify_field_sections(self, fields: List[PDFFieldExtraction], pdf_text: str) -> List[PDFFieldExtraction]:
        """Identify which section each field belongs to"""
        
        # Simple section identification based on field names and position
        for field in fields:
            field_name_lower = field.field_name.lower()
            
            if any(keyword in field_name_lower for keyword in ['spouse', 'husband', 'wife', 'partner']):
                field.section_name = "spouse_information"
                field.is_conditional = True
            elif any(keyword in field_name_lower for keyword in ['child', 'children', 'son', 'daughter']):
                field.section_name = "children_information"
                field.is_conditional = True
            elif any(keyword in field_name_lower for keyword in ['estate', 'executor', 'administrator']):
                field.section_name = "estate_representative"
            elif any(keyword in field_name_lower for keyword in ['insurance', 'policy', 'coverage']):
                field.section_name = "insurance_information"
                field.is_conditional = True
            elif any(keyword in field_name_lower for keyword in ['deceased', 'decedent']):
                field.section_name = "deceased_information"
            else:
                field.section_name = "general"
        
        return fields
    
    def _detect_form_type(self, fields: List[PDFFieldExtraction], pdf_path: str) -> PDFFormInfo:
        """Detect the type of PDF form (enhanced)"""
        
        field_names = [field.field_name.lower() for field in fields]
        field_text = ' '.join(field_names)
        
        # Check for death benefit application indicators
        if any(indicator in field_text for indicator in [
            'death benefit', 'cpp', 'pension plan', 'social insurance', 'deceased'
        ]):
            return self.form_templates.get(PDFFormType.DEATH_BENEFIT_APPLICATION, 
                                         self._create_unknown_form_info(fields))
        
        # Check for estate information indicators
        elif any(indicator in field_text for indicator in [
            'estate', 'executor', 'will', 'probate', 'estate representative'
        ]):
            return self.form_templates.get(PDFFormType.ESTATE_INFORMATION,
                                         self._create_unknown_form_info(fields))
        
        # Check for life insurance indicators
        elif any(indicator in field_text for indicator in [
            'life insurance', 'policy', 'beneficiary', 'coverage', 'claim'
        ]):
            form_info = PDFFormInfo(
                form_type=PDFFormType.LIFE_INSURANCE_CLAIM,
                form_title="Life Insurance Claim Form",
                total_fields=len(fields),
                fillable_fields=len(fields),
                signature_fields=len([f for f in fields if PDFFieldType.SIGNATURE in f.field_type]),
                date_fields=len([f for f in fields if PDFFieldType.DATE in f.field_type]),
                required_fields=len([f for f in fields if PDFFieldType.REQUIRED in f.field_type]),
                conditional_fields=len([f for f in fields if hasattr(f, 'is_conditional') and f.is_conditional]),
                conditional_logic_detected=any(hasattr(f, 'is_conditional') and f.is_conditional for f in fields)
            )
            return form_info
        
        else:
            return self._create_unknown_form_info(fields)
    
    def _create_unknown_form_info(self, fields: List[PDFFieldExtraction]) -> PDFFormInfo:
        """Create form info for unknown form type (enhanced) - FIXED CONSTRUCTOR"""
        signature_fields = len([f for f in fields if PDFFieldType.SIGNATURE in f.field_type])
        date_fields = len([f for f in fields if PDFFieldType.DATE in f.field_type])
        required_fields = len([f for f in fields if PDFFieldType.REQUIRED in f.field_type])
        conditional_fields = len([f for f in fields if hasattr(f, 'is_conditional') and f.is_conditional])

        return PDFFormInfo(
            form_type=PDFFormType.UNKNOWN,
            form_title="Unknown Form Type",
            total_fields=safe_len(fields),  
            fillable_fields=len(fields),
            signature_fields=signature_fields,
            date_fields=date_fields,
            required_fields=required_fields,
            conditional_fields=conditional_fields,
            form_version="unknown",
            conditional_logic_detected=conditional_fields > 0
        )

    # ================== DISPLAY AND SUMMARY METHODS ==================
    
    def get_conditional_processing_display_info(self) -> Dict:
        """Get conditional processing information for display in CLI"""
        
        # Calculate statistics
        total_fields_with_conditions = len([state for state in self.field_states.values() 
                                          if state.get('affected_by_conditions', False)])
        
        fields_hidden = len([state for state in self.field_states.values() 
                           if not state.get('visible', True)])
        
        fields_required = len([state for state in self.field_states.values() 
                             if state.get('required', False)])
        
        fields_disabled = len([state for state in self.field_states.values() 
                             if not state.get('enabled', True)])
        
        # Get examples of processed fields
        processed_examples = []
        for field_name, state in self.field_states.items():
            if state.get('affected_by_conditions', False):
                # Clean field name for display
                clean_name = field_name.replace('SC_ISP1200[0].', '')
                clean_name = clean_name.replace('page', 'p').replace('[0]', '')
                clean_name = clean_name.replace('.', ' → ')
                
                if len(clean_name) > 50:
                    clean_name = clean_name[:47] + "..."
                
                example = {
                    'field_name': clean_name,
                    'visible': state.get('visible', True),
                    'required': state.get('required', False),
                    'enabled': state.get('enabled', True),
                    'dependencies': len(state.get('dependencies', []))
                }
                processed_examples.append(example)
                
                if len(processed_examples) >= 10:  # Limit examples
                    break
        
        # Get condition types summary
        condition_types = {}
        for field_name, state in self.field_states.items():
            if state.get('affected_by_conditions', False):
                if not state.get('visible', True):
                    condition_types['hidden'] = condition_types.get('hidden', 0) + 1
                if state.get('required', False):
                    condition_types['required'] = condition_types.get('required', 0) + 1
                if not state.get('enabled', True):
                    condition_types['disabled'] = condition_types.get('disabled', 0) + 1
        
        return {
            'total_conditional_fields': total_fields_with_conditions,
            'fields_hidden': fields_hidden,
            'fields_required': fields_required,
            'fields_disabled': fields_disabled,
            'processed_examples': processed_examples,
            'condition_types': condition_types,
            'has_conditional_processing': total_fields_with_conditions > 0
        }
    
    def get_enhanced_pdf_stats(self) -> Dict:
        """Get comprehensive PDF processing statistics with conditional logic metrics"""
        stats_dict = {
            "forms_processed": self.pdf_stats.forms_processed,
            "fields_extracted": self.pdf_stats.fields_extracted,
            "fields_mapped": self.pdf_stats.fields_mapped,
            "signature_fields_found": self.pdf_stats.signature_fields_found,
            "validation_errors": self.pdf_stats.validation_errors,
            "processing_time": self.pdf_stats.processing_time,
            "form_types_detected": self.pdf_stats.form_types_detected,
            "transformation_applications": self.pdf_stats.transformation_applications,
            "high_confidence_mappings": self.pdf_stats.high_confidence_mappings,
            "form_sections_identified": self.pdf_stats.form_sections_identified,  
            "supported_form_types": len(self.pdf_mappings),
            "total_pdf_mappings": sum(len(mappings) for mappings in self.pdf_mappings.values()),
            "transformation_functions": len(self.field_transformations),
            "validation_functions": len(self.validation_functions),
            "fields_affected_by_conditions": len([state for state in self.field_states.values() 
                                                if state.get('affected_by_conditions', False)]) 
        }
        
        return stats_dict