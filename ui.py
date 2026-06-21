import streamlit as st
import requests
import json
import pandas as pd
import io
import tempfile
import os
from typing import Dict, List, Any, Optional
from datetime import datetime

# ============================================================================
# PDF GENERATION LIBRARIES - Install with: pip install PyPDFForm fillpdf pdfrw2 reportlab
# ============================================================================
try:
    from PyPDFForm import PdfWrapper
    from fillpdf import fillpdfs
    import pdfrw
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    PDF_GENERATION_AVAILABLE = True
except ImportError:
    PDF_GENERATION_AVAILABLE = False
    print("Install PDF libraries for full functionality: pip install PyPDFForm fillpdf pdfrw2 reportlab")

# ============================================================================
# 1. CONFIGURATION
# ============================================================================
API_SINGLE_URL = "http://api:8000/api/v1/process/document"
API_BATCH_URL = "http://api:8000/api/v1/process/document/batch"
st.set_page_config(layout="wide", page_title="MapperAI Admin Tool")

# ============================================================================
# 2. CLEAN WHITE CSS
# ============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
    
    /* Global clean white theme */
    .stApp { 
        background-color: #ffffff; 
        font-family: 'Inter', sans-serif; 
        color: #2c3e50;
    }
    header, footer { display: none !important; }
    .main .block-container { padding-top: 1rem; }
    
    /* Force all text to be readable */
    .stMarkdown, .stText, p, div, span, h1, h2, h3, h4, h5, h6 {
        color: #2c3e50 !important;
        background-color: transparent !important;
    }
    
    /* Logo container in top left corner */
    .cadence-logo-container {
        position: fixed !important;
        top: 1rem !important;
        left: 1rem !important;
        z-index: 1000 !important;
    }
    
    /* Logo image styling */
    .cadence-logo-container img {
        height: 40px !important;
        width: auto !important;
        max-width: 160px !important;
    }
    
    /* Adjust main content to account for logo */
    .main .block-container { 
        padding-top: 1rem; 
        padding-left: 1rem;
        margin-top: 4rem !important; /* Add space for fixed logo */
    }
    
    /* Simple header without logo */
    .admin-header { 
        background-color: #ffffff;
        color: #2c3e50; 
        padding: 1.5rem 0; 
        margin-bottom: 2rem; 
        display: flex; 
        justify-content: center; /* Center the header content */
        align-items: center; 
        border-bottom: 2px solid #ecf0f1;
        margin-top: 0rem; /* Remove extra margin since we have it on main container */
    }
    .admin-header h1 { 
        color: #2c3e50 !important; 
        margin: 0; 
        font-size: 1.8rem; 
        font-weight: 600;
    }
    .user-info { 
        display: flex; 
        align-items: center; 
        gap: 1rem; 
        color: #2c3e50;
        font-weight: 500;
    }
    
    /* Simple cards with minimal styling */
    .card { 
        background-color: #ffffff; 
        border: none; 
        border-radius: 8px; 
        padding: 1.5rem; 
        margin-bottom: 1.5rem;
    }
    .card h3 { 
        font-size: 1.2rem; 
        font-weight: 600; 
        margin-bottom: 1rem; 
        color: #2c3e50;
    }
    
    /* Clean workflow steps */
    .workflow-steps { 
        display: flex; 
        justify-content: space-between; 
        gap: 1rem; 
        margin-bottom: 2rem; 
        background: #ffffff;
        border: none;
        border-radius: 8px;
        padding: 1rem;
    }
    .step { 
        padding: 0.75rem 1rem; 
        border-radius: 6px; 
        font-weight: 500; 
        font-size: 0.9rem; 
        color: #2c3e50;
        border: none;
        background-color: #f8f9fa;
    }
    .step-completed { 
        background-color: #d5f4e6; 
        color: #27ae60; 
        border-color: #27ae60;
    }
    .step-active { 
        background-color: #fff4e6; 
        color: #f39c12; 
        border-color: #f39c12;
    }
    .step-pending { 
        background-color: #f8f9fa; 
        color: #7f8c8d; 
        border-color: #bdc3c7;
    }
    
    /* Simple metrics */
    .analysis-summary { 
        display: grid; 
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); 
        gap: 1rem; 
    }
    .summary-item { 
        text-align: center; 
        padding: 1rem; 
        background-color: #ffffff;
        border: none; 
        border-radius: 6px; 
    }
    .summary-value { 
        font-size: 2rem; 
        font-weight: 600; 
        color: #2c3e50;
    }
    .summary-label { 
        font-size: 0.9rem; 
        color: #7f8c8d; 
        margin-top: 0.5rem;
        font-weight: 500;
    }

    /* Simple preview area */
    .pdf-preview { 
        border: none; 
        border-radius: 8px; 
        height: 200px; 
        background-color: #f8f9fa;
        display: flex; 
        flex-direction: column;
        align-items: center; 
        justify-content: center; 
        color: #7f8c8d; 
    }
    
    /* File list styling */
    .file-list-item {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
        background-color: #f8f9fa;
        border: none;
        border-radius: 6px;
    }
    
    .file-info {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        flex-grow: 1;
    }
    
    .file-icon {
        font-size: 1.2rem;
        color: #e74c3c;
    }
    
    .file-name {
        font-weight: 500;
        color: #2c3e50;
    }
    
    .file-size {
        font-size: 0.8rem;
        color: #7f8c8d;
    }
    
    /* Override global button styling for file management - using more specific selectors */
    .clear-all-btn .stButton > button,
    .clear-all-btn .stButton button,
    div.clear-all-btn button {
        background-color: #e74c3c !important;
        color: white !important;
        border: none !important;
        border-radius: 4px !important;
        padding: 0.4rem 0.8rem !important;
        font-size: 0.8rem !important;
        font-weight: 500 !important;
        width: auto !important;
        min-width: 120px !important;
        max-width: 140px !important;
        height: 32px !important;
    }
    
    .clear-all-btn .stButton > button:hover,
    .clear-all-btn .stButton button:hover,
    div.clear-all-btn button:hover {
        background-color: #c0392b !important;
    }
    
    .remove-file-btn .stButton > button,
    .remove-file-btn .stButton button,
    div.remove-file-btn button {
        background-color: #f8f9fa !important;
        color: #000000 !important;
        border: 1px solid #ecf0f1 !important;
        border-radius: 4px !important;
        padding: 0.25rem !important;
        font-size: 0.9rem !important;
        width: 36px !important;
        min-width: 36px !important;
        max-width: 36px !important;
        height: 32px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    
    .remove-file-btn .stButton > button:hover,
    .remove-file-btn .stButton button:hover,
    div.remove-file-btn button:hover {
        background-color: #fdeaea !important;
        border-color: #e74c3c !important;
    }
    
    /* Force override on all nested elements */
    .clear-all-btn button *,
    .remove-file-btn button * {
        color: inherit !important;
    }
    
    /* Clean buttons matching Cadence logo purple with white text - FORCE WHITE TEXT */
    .stButton > button, .stDownloadButton > button,
    .stButton > button *, .stDownloadButton > button *,
    .stButton button, .stDownloadButton button,
    .stButton button *, .stDownloadButton button * {
        background-color: #5B2C6F !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 0.5rem 1rem !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        width: 100% !important;
    }
    
    /* OVERRIDE for file management buttons - very specific targeting */
    div[data-testid="column"]:has(button[title*="Clear All Files"]) .stButton > button,
    div[data-testid="column"]:has(button[title*="Remove"]) .stButton > button,
    button[title*="Clear All Files"],
    button[title*="Remove"] {
        background-color: #e74c3c !important;
        color: white !important;
        padding: 0.4rem 0.8rem !important;
        font-size: 0.8rem !important;
        width: auto !important;
        min-width: 120px !important;
        max-width: 140px !important;
        height: 32px !important;
    }
    
    /* Individual remove buttons */
    button[title*="Remove"]:not([title*="Clear"]) {
        background-color: #f8f9fa !important;
        color: #e74c3c !important;
        border: 1px solid #ecf0f1 !important;
        padding: 0.25rem !important;
        width: 36px !important;
        min-width: 36px !important;
        max-width: 36px !important;
        height: 32px !important;
    }
    
    button[title*="Remove"]:not([title*="Clear"]):hover {
        background-color: #fdeaea !important;
        border-color: #000000 !important;
    }
    
    button[title*="Clear All Files"]:hover {
        background-color: #c0392b !important;
    }
    .stButton > button:hover, .stDownloadButton > button:hover,
    .stButton > button:active, .stDownloadButton > button:active,
    .stButton > button:visited, .stDownloadButton > button:visited,
    .stButton > button:focus, .stDownloadButton > button:focus {
        background-color: #4A235A !important;
        color: white !important;
        border: none !important;
    }
    /* Additional force for any nested elements */
    .stButton button span, .stDownloadButton button span,
    .stButton button div, .stDownloadButton button div {
        color: white !important;
    }
    
    /* Ensure button alignment */
    .stButton, .stDownloadButton {
        text-align: center !important;
        width: 100% !important;
    }
    
    /* Column alignment */
    .stColumn {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
    }
    
    /* Clean dataframe */
    .stDataFrame {
        background-color: #ffffff !important;
        border: 1px solid #ecf0f1 !important;
        border-radius: 6px !important;
    }
    
    /* Simple tabs */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #ffffff;
        border-bottom: 1px solid #ecf0f1;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 0.75rem 1rem;
        background-color: transparent;
        color: #2c3e50 !important;
        font-weight: 500;
        border-bottom: 2px solid transparent;
    }
    
    .stTabs [aria-selected="true"] {
        color: #3498db !important;
        border-bottom-color: #3498db !important;
    }
    
    /* Clean metrics */
    .stMetric {
        background-color: #ffffff !important;
        padding: 1rem !important;
        border: none !important;
        border-radius: 6px !important;
    }
    
    /* Clean alerts */
    .stSuccess {
        background-color: #d5f4e6 !important;
        border: 1px solid #27ae60 !important;
        color: #27ae60 !important;
    }
    
    .stWarning {
        background-color: #fff4e6 !important;
        border: 1px solid #f39c12 !important;
        color: #f39c12 !important;
    }
    
    .stInfo {
        background-color: #e8f4f8 !important;
        border: 1px solid #3498db !important;
        color: #3498db !important;
    }
    
    .stError {
        background-color: #fdeaea !important;
        border: 1px solid #e74c3c !important;
        color: #e74c3c !important;
    }
    
    .stFileUploader label, .stFileUploader small {
        color: white !important; /* Force text to be white */
    }
    /* Target the "Browse files" button text specifically */
    .stFileUploader button {
        color: white !important; /* Force button text to be white */
    }
    
    /* Remove all gradients and complex backgrounds */
    .element-container, .stContainer, .block-container {
        background-color: #ffffff !important;
    }
    
    /* Clean code blocks */
    .stCode, code, pre {
        background-color: #f8f9fa !important;
        border: 1px solid #ecf0f1 !important;
        color: #2c3e50 !important;
    }
    
    /* Clean expander - comprehensive targeting */
    .streamlit-expanderContent {
        background-color: #ffffff !important;
        border: 1px solid #ecf0f1 !important;
    }
    
    /* Remove black highlight from all possible expander header selectors */
    .streamlit-expanderHeader,
    [data-testid="stExpander"] summary,
    [data-testid="stExpander"] > div:first-child,
    [data-testid="stExpander"] > div[role="button"],
    .stExpander > div:first-child,
    .stExpander summary {
        background-color: #ffffff !important;
        background: #ffffff !important;
        color: #2c3e50 !important;
        border: 1px solid #ecf0f1 !important;
        border-radius: 6px !important;
    }
    
    /* Hover states */
    .streamlit-expanderHeader:hover,
    [data-testid="stExpander"] summary:hover,
    [data-testid="stExpander"] > div:first-child:hover,
    [data-testid="stExpander"] > div[role="button"]:hover,
    .stExpander > div:first-child:hover,
    .stExpander summary:hover {
        background-color: #f8f9fa !important;
        background: #f8f9fa !important;
        color: #2c3e50 !important;
    }
    
    /* Target nested elements within expander headers */
    .streamlit-expanderHeader *,
    [data-testid="stExpander"] summary *,
    [data-testid="stExpander"] > div:first-child *,
    .stExpander > div:first-child * {
        background-color: transparent !important;
        background: transparent !important;
        color: #2c3e50 !important;
    }
    
    /* Force override any dark backgrounds */
    div[data-testid="stExpander"] {
        background-color: #ffffff !important;
    }
    
    div[data-testid="stExpander"] > div {
        background-color: #ffffff !important;
        color: #2c3e50 !important;
    }

    /* ========================================================================= */
    /* === ULTRA HIGH SPECIFICITY TRANSPARENT TRASH BUTTON =================== */
    /* ========================================================================= */

    /* Maximum specificity selectors to force transparent trash button */
    div.remove-result-btn-container .stButton > button,
    div.remove-result-btn-container .stButton button,
    div.remove-result-btn-container button,
    .remove-result-btn-container .stButton > button,
    .remove-result-btn-container .stButton button,
    .remove-result-btn-container button,
    div[class="remove-result-btn-container"] .stButton > button,
    div[class="remove-result-btn-container"] .stButton button,
    div[class="remove-result-btn-container"] button {
        /* FORCE TRANSPARENT BACKGROUND */
        background: transparent !important;
        background-color: transparent !important;
        background-image: none !important;
        border: none !important;
        box-shadow: none !important;
        outline: none !important;
        
        /* MAKE ICON SEMI-TRANSPARENT */
        color: rgba(150, 150, 150, 0.5) !important; /* Light gray, very transparent */
        opacity: 0.3 !important; /* Extra transparency */
        
        /* SIZE AND POSITIONING */
        padding: 0 !important;
        margin: 0 !important;
        font-size: 1.2rem !important;
        width: 40px !important;
        min-width: 40px !important;
        max-width: 40px !important;
        height: 40px !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        border-radius: 8px !important;
        transition: all 0.2s ease !important;
    }

    /* Hover effect - becomes visible */
    div.remove-result-btn-container .stButton > button:hover,
    div.remove-result-btn-container .stButton button:hover,
    div.remove-result-btn-container button:hover,
    .remove-result-btn-container .stButton > button:hover,
    .remove-result-btn-container .stButton button:hover,
    .remove-result-btn-container button:hover,
    div[class="remove-result-btn-container"] .stButton > button:hover,
    div[class="remove-result-btn-container"] .stButton button:hover,
    div[class="remove-result-btn-container"] button:hover {
        background-color: rgba(253, 234, 234, 0.8) !important; /* Light red background */
        color: rgba(231, 76, 60, 0.9) !important; /* More visible red on hover */
        opacity: 1 !important; /* Full opacity on hover */
        border: none !important;
    }

    /* Force override ALL nested elements */
    div.remove-result-btn-container .stButton > button *,
    div.remove-result-btn-container .stButton button *,
    div.remove-result-btn-container button *,
    .remove-result-btn-container .stButton > button *,
    .remove-result-btn-container .stButton button *,
    .remove-result-btn-container button *,
    div[class="remove-result-btn-container"] .stButton > button *,
    div[class="remove-result-btn-container"] .stButton button *,
    div[class="remove-result-btn-container"] button * {
        background: transparent !important;
        background-color: transparent !important;
        color: inherit !important;
        border: none !important;
        opacity: inherit !important;
    }

    /* Nuclear option - catch any remaining button elements */
    [class*="remove-result-btn"] button,
    [class*="remove-result-btn"] .stButton button,
    [class*="remove-result-btn"] .stButton > button {
        background: transparent !important;
        background-color: transparent !important;
        color: rgba(150, 150, 150, 0.5) !important;
        opacity: 0.3 !important;
        border: none !important;
        padding: 0 !important;
        width: 40px !important;
        height: 40px !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# 3. SESSION STATE MANAGEMENT
# ============================================================================
if 'selected_field' not in st.session_state:
    st.session_state.selected_field = None
if 'bulk_actions' not in st.session_state:
    st.session_state.bulk_actions = []
if 'filter_status' not in st.session_state:
    st.session_state.filter_status = "All"
if 'sort_by' not in st.session_state:
    st.session_state.sort_by = "confidence"
if 'uploaded_files_list' not in st.session_state:
    st.session_state.uploaded_files_list = []

# ============================================================================
# 4. FILE MANAGEMENT FUNCTIONS
# ============================================================================

def add_files_to_session(new_files):
    """Add new files to session state, avoiding duplicates."""
    if not new_files:
        return
    
    existing_names = {f['name'] for f in st.session_state.uploaded_files_list}
    
    for file in new_files:
        if file.name not in existing_names:
            file_data = {
                'name': file.name,
                'size': file.size,
                'type': file.type,
                'data': file.getvalue(),
                'timestamp': datetime.now().isoformat()
            }
            st.session_state.uploaded_files_list.append(file_data)

def handle_file_upload():
    """Callback to add newly uploaded files to the session state AND clear the uploader."""
    new_files = st.session_state.get("file_uploader", [])
    if new_files:
        add_files_to_session(new_files)
        st.session_state.file_uploader = []

def remove_file_from_session(file_index: int):
    """Remove a file from the session state list by its index."""
    if 0 <= file_index < len(st.session_state.uploaded_files_list):
        st.session_state.uploaded_files_list.pop(file_index)

def clear_all_files():
    """Clear all uploaded files from the session state list."""
    st.session_state.uploaded_files_list = []

def remove_result_from_session(result_index: int):
    """Remove a specific result dictionary from the session state list."""
    if 'api_response_data' in st.session_state and st.session_state.api_response_data:
        if 0 <= result_index < len(st.session_state.api_response_data):
            st.session_state.api_response_data.pop(result_index)

def format_file_size(size_bytes: int) -> str:
    """Format file size in a human-readable format."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.1f} MB"

def create_file_objects_from_session() -> List[io.BytesIO]:
    """Create file-like objects from session state data for API submission."""
    file_objects = []
    for file_data in st.session_state.uploaded_files_list:
        file_obj = io.BytesIO(file_data['data'])
        file_obj.name = file_data['name']
        file_obj.size = file_data['size']
        file_objects.append(file_obj)
    return file_objects

# ============================================================================
# 5. PDF GENERATION FUNCTIONS
# ============================================================================

def generate_auto_fillable_pdf(original_pdf_bytes: bytes, mappings: List[Dict[str, Any]], file_name: str) -> bytes:
    """Generate a real auto-fillable PDF from the original PDF and field mappings"""
    if not PDF_GENERATION_AVAILABLE:
        raise Exception("PDF generation libraries not installed. Run: pip install PyPDFForm fillpdf pdfrw2 reportlab")
    
    try:
        # Method 1: Try PyPDFForm first (most robust for interactive forms)
        return generate_with_pypdfform(original_pdf_bytes, mappings)
    except Exception as e:
        print(f"PyPDFForm failed: {e}")
        try:
            # Method 2: Fall back to fillpdf
            return generate_with_fillpdf(original_pdf_bytes, mappings)
        except Exception as e2:
            print(f"fillpdf failed: {e2}")
            # Method 3: Create overlay with ReportLab
            return generate_overlay_pdf(mappings, file_name)

def generate_with_pypdfform(pdf_bytes: bytes, mappings: List[Dict[str, Any]]) -> bytes:
    """Use PyPDFForm to create auto-fillable PDF"""
    
    form_data = {}
    for mapping in mappings:
        if mapping.get('confidence', 0.0) >= 70: # Use a confidence threshold
         
            field_name_for_pdf = mapping.get('pdf_internal_name') or mapping.get('field_name', '')
            # -----------------------------------------------------------

            cadence_path = mapping.get('cadence_path', '')
            
            if field_name_for_pdf: # Ensure we have a key
                form_data[field_name_for_pdf] = f"{{{{{cadence_path}}}}}"
    
    # Create temporary file-like object
    input_stream = io.BytesIO(pdf_bytes)
    
    # Fill the PDF
    filled_pdf = PdfWrapper(input_stream).fill(form_data)
    
    # Return as bytes
    output_stream = io.BytesIO()
    filled_pdf.write(output_stream)
    return output_stream.getvalue()

def generate_with_fillpdf(pdf_bytes: bytes, mappings: List[Dict[str, Any]]) -> bytes:
    """Use fillpdf library as fallback"""
    
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_input:
        temp_input.write(pdf_bytes)
        temp_input_path = temp_input.name
    
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_output:
        temp_output_path = temp_output.name
    
    try:
        # Create fillpdf data dictionary
        data_dict = {}
        for mapping in mappings:
            if mapping.get('confidence', 0.0) >= 0.7:
                field_name = mapping.get('field_name', '')
                cadence_path = mapping.get('cadence_path', '')
                data_dict[field_name] = f"{{{{{cadence_path}}}}}"
        
        # Fill the PDF
        fillpdfs.write_fillable_pdf(temp_input_path, temp_output_path, data_dict)
        
        # Read the result
        with open(temp_output_path, 'rb') as f:
            result_bytes = f.read()
        
        return result_bytes
        
    finally:
        # Cleanup
        os.unlink(temp_input_path)
        if os.path.exists(temp_output_path):
            os.unlink(temp_output_path)

def generate_overlay_pdf(mappings: List[Dict[str, Any]], file_name: str) -> bytes:
    """Create a new PDF with form fields as fallback"""
    
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    # Add title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, f"Auto-Fillable Template: {file_name}")
    
    # Add field mappings
    y_position = height - 100
    c.setFont("Helvetica", 10)
    
    c.drawString(50, y_position, "Auto-Fillable Fields (Ready for Cadence Integration):")
    y_position -= 30
    
    for i, mapping in enumerate(mappings):
        if mapping.get('confidence', 0.0) >= 0.7:  # Only high-confidence
            field_name = mapping.get('field_name', 'Unknown')
            cadence_path = mapping.get('cadence_path', 'unknown')
            confidence = mapping.get('confidence', 0.0)
            
            # Create a text field representation
            field_text = f"• {field_name}: {{{{{cadence_path}}}}} ({confidence:.0%})"
            c.drawString(70, y_position, field_text)
            y_position -= 20
            
            # Create new page if needed
            if y_position < 100:
                c.showPage()
                y_position = height - 50
                c.setFont("Helvetica", 10)
    
    # Add instructions
    y_position -= 30
    c.drawString(50, y_position, "Integration Instructions:")
    y_position -= 20
    c.drawString(70, y_position, "1. Upload this PDF to your Cadence document templates")
    y_position -= 15
    c.drawString(70, y_position, "2. Cadence will automatically populate the {{}} fields")
    y_position -= 15
    c.drawString(70, y_position, "3. Users only fill remaining unmapped fields manually")
    
    c.save()
    return buffer.getvalue()

def create_template_file(mappings: List[Dict[str, Any]], file_name: str) -> str:
    """Create JavaScript template file content"""
    
    template_content = f"""// Auto-fillable template for {file_name}
// Generated by MapperAI - Ready for Cadence Integration

const autoFillData = {{
"""
    
    for mapping in mappings:
        if mapping.get('confidence', 0.0) >= 0.7:  # Only high-confidence mappings
            field_name = mapping.get('field_name', 'Unknown')
            cadence_path = mapping.get('cadence_path', 'unknown')
            template_content += f'  "{field_name}": {{{{{cadence_path}}}}},\n'
    
    template_content += """}};

// Usage Instructions:
// 1. This data structure shows how PDF fields map to Cadence paths
// 2. When integrated with Cadence, these {{}} placeholders become real data
// 3. Example: {{applicant.full_name}} becomes "John Smith" automatically

export default autoFillData;
"""
    
    return template_content

# ============================================================================
# 6. API CALL FUNCTION - FIXED TO PRESERVE PDF BYTES
# ============================================================================
def call_api(uploaded_files: List[io.BytesIO]):
    """
    Make API call to process one or more documents.
    Handles both single and batch uploads.
    """
    if not uploaded_files:
        return {"success": False, "error": "No files were uploaded."}

    try:
        # If only one file is uploaded, use the single file endpoint
        if len(uploaded_files) == 1:
            uploaded_file = uploaded_files[0]
            original_pdf_bytes = uploaded_file.getvalue()
            files_payload = {'file': (uploaded_file.name, original_pdf_bytes, 'application/pdf')}
            response = requests.post(API_SINGLE_URL, files=files_payload, timeout=1200) # Use a long timeout
            
            if response.status_code == 200:
                response_json = response.json()
                # Wrap the single result in a list to match the batch format for consistent UI handling
                return {
                    "success": True, 
                    "data": [{
                        "filename": uploaded_file.name,
                        "data": response_json,
                        "original_pdf_bytes": original_pdf_bytes
                    }]
                }
            else:
                error_detail = response.json().get('detail', response.text)
                return {"success": False, "error": f"API Error (Code {response.status_code}): {error_detail}"}

        # If multiple files are uploaded, use the batch endpoint
        else:
            files_payload = []
            original_bytes_map = {}
            for uploaded_file in uploaded_files:
                original_pdf_bytes = uploaded_file.getvalue()
                files_payload.append(('files', (uploaded_file.name, original_pdf_bytes, 'application/pdf')))
                original_bytes_map[uploaded_file.name] = original_pdf_bytes
            
            response = requests.post(API_BATCH_URL, files=files_payload, timeout=1200) # Use a long timeout

            if response.status_code == 200:
                batch_response = response.json()
                # Combine the API response with the original PDF bytes for each file
                for result in batch_response.get("results", []):
                    if "error" not in result:
                        result["original_pdf_bytes"] = original_bytes_map.get(result["filename"])
                return {"success": True, "data": batch_response.get("results", [])}
            else:
                error_detail = response.json().get('detail', response.text)
                return {"success": False, "error": f"API Error (Code {response.status_code}): {error_detail}"}

    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "Connection Error: Could not connect to the MapperAI API. Is the backend running?"}
    except Exception as e:
        return {"success": False, "error": f"An unexpected error occurred: {e}"}
    
# ============================================================================
# 7. HELPER FUNCTIONS
# ============================================================================
def get_confidence_class(confidence: float) -> str:
    """Get CSS class based on confidence score"""
    if confidence >= 0.9: 
        return "High"
    elif confidence >= 0.7: 
        return "Medium"
    else: 
        return "Low"

def get_row_class(mapping: Dict[str, Any]) -> str:
    """Determine row class based on mapping status"""
    confidence = mapping.get('confidence', 0.0)
    cadence_path = str(mapping.get('cadence_path', ''))
    
    if not cadence_path or cadence_path.lower() in ['none', 'null', '']:
        return "Manual Required"
    elif confidence >= 0.95:
        return "Approved"
    else:
        return "Needs Review"

def create_export_data(mappings: List[Dict[str, Any]], unmapped: List[str], quality_report: Dict[str, Any], file_name: str) -> str:
    """Create export data as JSON string"""
    export_data = {
        "document_info": {
            "file_name": file_name,
            "export_timestamp": pd.Timestamp.now().isoformat(),
            "total_fields": len(mappings) + len(unmapped),
            "mapped_fields": len(mappings),
            "unmapped_fields": len(unmapped)
        },
        "field_mappings": mappings,
        "unmapped_fields": unmapped,
        "quality_report": quality_report,
        "statistics": {
            "high_confidence_count": len([m for m in mappings if m.get('confidence', 0.0) >= 0.9]),
            "medium_confidence_count": len([m for m in mappings if 0.7 <= m.get('confidence', 0.0) < 0.9]),
            "low_confidence_count": len([m for m in mappings if m.get('confidence', 0.0) < 0.7]),
            "average_confidence": sum(m.get('confidence', 0.0) for m in mappings) / len(mappings) if mappings else 0.0
        }
    }
    return json.dumps(export_data, indent=2)

def get_handlebars_template(mapping: Dict[str, Any]) -> str:
    """Generate Handlebars template based on mapping schema"""
    cadence_path = str(mapping.get('cadence_path', ''))
    
    if not cadence_path or cadence_path.lower() in ['none', 'null', '']:
        return "Template generation failed"
    else:
        return f"{{{{{cadence_path}}}}}"

# ============================================================================
# 8. UI RENDERING FUNCTIONS
# ============================================================================
def render_header():
    """Render clean header with Cadence logo image in top left corner"""
    # Cadence logo in top left corner - using the uploaded image
    st.markdown("""
    <div class="cadence-logo-container">
    </div>
    """, unsafe_allow_html=True)
    
    # Display the logo image in a container with fixed positioning
    # Note: You'll need to save your uploaded image to a file and reference it here
    # For now, using a placeholder approach
    logo_col1, logo_col2, logo_col3 = st.columns([1, 8, 1])
    with logo_col1:
        # Place your Cadence logo image file in the same directory as this script
        # and reference it here. For example:
        try:
            st.image("cadence_logo.png", width=160)
        except:
            # Fallback to text if image not found
            st.markdown("""
            <div style="position: fixed; top: 1rem; left: 1rem; z-index: 1000; background: white; padding: 0.5rem 1rem; border-radius: 8px; box-shadow: 0 2px 12px rgba(0,0,0,0.1); border: 1px solid #f0f0f0;">
                <span style="color: #6b46c1; font-weight: 600; font-size: 1.1rem;">Cadence</span>
            </div>
            """, unsafe_allow_html=True)
    
    # Main header centered
    st.markdown("""
    <div class="admin-header">
        <h1 style="margin: 0; text-align: center; width: 100%;">MapperAI Admin Tool</h1>
    </div>
    """, unsafe_allow_html=True)

def render_document_info(api_response: Dict[str, Any], file_name: str):
    """Render document information with enhanced form type and subject detection"""
    doc_analysis = api_response.get('document_analysis', {})
    processing_metadata = api_response.get('processing_metadata', {})
    mappings = api_response.get('field_mappings', [])
    unmapped = api_response.get('unmapped_fields', [])
    logic = api_response.get('conditional_logic_analysis', [])
    subject_detection = api_response.get('subject_detection', {})
    
    total_fields = len(mappings) + len(unmapped)
    mapped_count = len(mappings)
    
    # Extract form type information
    form_type = doc_analysis.get('form_type', 'unknown')
    category = doc_analysis.get('category', 'unknown')
    confidence = doc_analysis.get('confidence', 0.0)
    processing_time = processing_metadata.get('processing_time', processing_metadata.get('duration', 'Unknown'))
    
    # Create enhanced form type display
    if form_type and form_type != 'unknown':
        # Convert form_type to readable format
        form_display = form_type.replace('_', ' ').title()
        if category and category != 'unknown':
            category_display = category.replace('_', ' ').upper()
            enhanced_form_type = f"{category_display} ({form_display})"
        else:
            enhanced_form_type = form_display
    else:
        enhanced_form_type = subject_detection.get('primary_subject', 'Document').replace('_', ' ').title()

    # Extract subject detection information
    primary_subject = subject_detection.get('primary_subject', 'unknown')
    subject_confidence = subject_detection.get('confidence', 0.0)
    
    # Create enhanced subject display
    if primary_subject and primary_subject != 'unknown':
        subject_display = primary_subject.replace('_', ' ').title()
        enhanced_subject = f"SUBJECT ROLE ({subject_display})"
    else:
        enhanced_subject = "SUBJECT ROLE (Unknown)"

    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"""
        <div class="card">
            <h3>Document Analysis: {enhanced_form_type}</h3>
            <div class="pdf-preview">
                <div style="text-align: center;">
                    <div style="font-size: 1.1rem; font-weight: 600; color: #2c3e50;">{file_name}</div>
                    <div style="font-size: 0.9rem; color: #7f8c8d; margin-top: 0.5rem;">Analysis Complete</div>
                    <div style="font-size: 0.85rem; color: #27ae60; margin-top: 0.25rem;">Processing Time: {processing_time}</div>
                    <div style="font-size: 0.8rem; color: #6b46c1; margin-top: 0.25rem;">Detection Confidence: {confidence:.1%}</div>
                    <div style="font-size: 0.8rem; color: #e67e22; margin-top: 0.25rem; font-weight: 600;">{enhanced_subject}</div>
                    <div style="font-size: 0.75rem; color: #e67e22; margin-top: 0.1rem;">Subject Confidence: {subject_confidence:.1%}</div>
                    <div style="font-size: 0.75rem; color: #e67e22; margin-top: 0.1rem;">Conditional Logic: {'Detected' if len(logic) > 0 else 'None Found'}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="card">
            <h3>Processing Results</h3>
            <div class="analysis-summary">
                <div class="summary-item">
                    <div class="summary-value">{total_fields}</div>
                    <div class="summary-label">Total Fields</div>
                </div>
                <div class="summary-item">
                    <div class="summary-value">{mapped_count}</div>
                    <div class="summary-label">Mapped</div>
                </div>
                <div class="summary-item">
                    <div class="summary-value">{len(unmapped)}</div>
                    <div class="summary-label">Unmapped</div>
                </div>
                <div class="summary-item">
                    <div class="summary-value">{len(logic)}</div>
                    <div class="summary-label">Logic Rules</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_enhanced_mapping_table(mappings: List[Dict[str, Any]], unmapped: List[str], file_name: str, original_pdf_bytes: bytes = None, quality_report: Dict[str, Any] = None, doc_index: int = 0):
    """Render clean mapping table with auto-fill generation buttons"""
    
    # Create unique key suffix for this document
    key_suffix = f"_{doc_index}_{file_name.replace('.pdf', '').replace(' ', '_')}"
    
    # Calculate auto-fill readiness
    high_confidence_mappings = [m for m in mappings if m.get('confidence', 0.0) >= 0.7]
    fillable_count = len(high_confidence_mappings)
    total_count = len(mappings) + len(unmapped)
    
    # Quick transformation overview
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Fields", total_count)
    with col2:
        st.metric("Auto-Fillable", fillable_count, delta=f"{(fillable_count/total_count*100):.0f}% ready" if total_count > 0 else "0% ready")
    with col3:
        avg_confidence = sum(m.get('confidence', 0.0) for m in mappings) / len(mappings) if mappings else 0.0
        st.metric("Avg Confidence", f"{avg_confidence:.0f}%")
    
    # Apply filters
    filtered_mappings = mappings
    if st.session_state.filter_status != "All":
        filtered_mappings = [m for m in mappings if get_row_class(m) == st.session_state.filter_status]
    
    # Create table data
    table_data = []
    
    for i, mapping in enumerate(filtered_mappings):
        confidence = mapping.get('confidence', 0.0)
        status = get_row_class(mapping)
        
        table_data.append({
            'ID': i,
            'PDF Field': mapping.get('field_name', 'Unknown'),
            'Cadence Path': mapping.get('cadence_path', 'No path'),
            'Template': get_handlebars_template(mapping),
            'Confidence': confidence,  # Keep as is - already in 0-100 format
            'Status': status
        })
    
    # Add unmapped fields
    for field in unmapped:
        table_data.append({
            'ID': len(table_data),
            'PDF Field': field,
            'Cadence Path': 'No Cadence Field Found',
            'Template': 'Template generation failed',
            'Confidence': 0.0,  # Already 0, no need to multiply by 100
            'Status': 'Manual Required'
        })
    
    if table_data:
        df = pd.DataFrame(table_data)
        
        edited_df = st.data_editor(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "ID": st.column_config.NumberColumn("ID", width="small"),
                "PDF Field": st.column_config.TextColumn("PDF Field", width="large"),
                "Cadence Path": st.column_config.TextColumn("Cadence Path", width="medium"),
                "Template": st.column_config.TextColumn("Handlebars Template", width="medium"),
                "Confidence": st.column_config.NumberColumn("AI Confidence (%)", width="small", min_value=0, max_value=100, format="%.0f"),
                "Status": st.column_config.SelectboxColumn(
                    "Status", 
                    width="small",
                    options=["Approved", "Needs Review", "Manual Required"]
                )
            },
            key=f"mapping_table{key_suffix}"  # FIXED: Unique key for each document
        )
        
        if not edited_df.equals(df):
            st.info("Table has been modified. Changes detected!")
            if st.button("Save Changes", key=f"save_table_changes{key_suffix}"):  # FIXED: Unique key
                st.success("Changes saved!")
                st.rerun()
    else:
        st.info("No mappings available")
    
    # AUTO-FILL GENERATION BUTTONS (moved from auto-fill preview tab) - ALL IN ONE LINE
    st.markdown("---")
    st.markdown("#### Generate Auto-Fillable PDF")
    
    action_col1, action_col2, action_col3, action_col4 = st.columns(4)
    
    with action_col1:
        if st.button("Generate Auto-Fillable PDF", key=f"generate_pdf{key_suffix}"):  # FIXED: Unique key
            with st.spinner("Generating auto-fillable PDF..."):
                try:
                    if original_pdf_bytes and PDF_GENERATION_AVAILABLE:
                        # Generate real auto-fillable PDF
                        auto_fill_pdf_bytes = generate_auto_fillable_pdf(
                            original_pdf_bytes, mappings, file_name
                        )
                        
                        st.success("Auto-fillable PDF generated successfully!")
                        #st.balloons()
                        
                        # Real download button with actual PDF
                        st.download_button(
                            label="Download Auto-Fillable PDF",
                            data=auto_fill_pdf_bytes,
                            file_name=f"{file_name.replace('.pdf', '')}_auto_fillable.pdf",
                            mime="application/pdf",
                            key=f"download_auto_pdf{key_suffix}"  # FIXED: Unique key
                        )
                    elif original_pdf_bytes:
                        # Fallback to template PDF
                        fallback_pdf = generate_overlay_pdf(mappings, file_name)
                        st.warning("Generated template PDF (install PDF libraries for full functionality)")
                        st.info("Run: pip install PyPDFForm fillpdf pdfrw2 reportlab")
                        
                        st.download_button(
                            label="Download Template PDF",
                            data=fallback_pdf,
                            file_name=f"{file_name.replace('.pdf', '')}_template.pdf",
                            mime="application/pdf",
                            key=f"download_template_pdf{key_suffix}"  # FIXED: Unique key
                        )
                    else:
                        st.error("Original PDF data not available")
                        
                except Exception as e:
                    st.error(f"PDF generation failed: {str(e)}")
                    st.info("Install PDF libraries: pip install PyPDFForm fillpdf pdfrw2 reportlab")
    
    with action_col2:
        if st.button("Export Template Code", key=f"export_template{key_suffix}"):  # FIXED: Unique key
            # Create real template file
            template_content = create_template_file(mappings, file_name)
            
            st.download_button(
                label="Download Template",
                data=template_content,
                file_name=f"{file_name.replace('.pdf', '')}_template.js",
                mime="text/javascript",
                key=f"download_template{key_suffix}"  # FIXED: Unique key
            )
    
    with action_col3:
        # Create export data - fix quality_report reference
        if quality_report is None:
            quality_report = {}
        export_json = create_export_data(mappings, unmapped, quality_report, file_name)
        
        st.download_button(
            label="Export Results",
            data=export_json,
            file_name=f"{file_name.replace('.pdf', '')}_mapping_results.json",
            mime="application/json",
            key=f"export_results_mapping{key_suffix}"  # FIXED: Unique key
        )
    
    with action_col4:
        # Show auto-fill readiness metric
        auto_fill_ready = len([m for m in mappings if m.get('confidence', 0.0) >= 0.7])
        total_count = len(mappings) + len(unmapped)
        readiness_percent = (auto_fill_ready / total_count * 100) if total_count > 0 else 0
        
        st.metric(
            label="Auto-Fill Ready", 
            value=f"{readiness_percent:.0f}%",
            delta=f"{auto_fill_ready}/{total_count} fields"
        )

def render_quality_report(quality_report: Dict[str, Any], mappings: List[Dict[str, Any]], unmapped: List[str]):
    """Render clean quality report"""
    
    # Calculate metrics from actual data if quality_report is empty
    if not quality_report or all(v == 0.0 for v in [quality_report.get('overall_score', 0), quality_report.get('mapping_quality', 0), quality_report.get('completeness_score', 0)]):
        total_fields = len(mappings) + len(unmapped)
        mapped_fields = len(mappings)
        high_confidence = len([m for m in mappings if m.get('confidence', 0.0) >= 70])  # Use 70 instead of 0.7
        medium_confidence = len([m for m in mappings if 70 <= m.get('confidence', 0.0) < 90])  # Use 70-90 instead of 0.7-0.9
        low_confidence = len([m for m in mappings if m.get('confidence', 0.0) < 70])  # Use 70 instead of 0.7
        
        mapping_coverage = (mapped_fields / total_fields) if total_fields > 0 else 0.0
        # FIX: Ensure confidence values are in 0-1 scale for calculation
        raw_confidences = [m.get('confidence', 0.0) for m in mappings]
        # Convert to 0-1 scale if they're in 0-100 scale
        normalized_confidences = [c/100 if c > 1 else c for c in raw_confidences]
        avg_confidence = sum(normalized_confidences) / len(mappings) if mappings else 0.0
        overall_score = (mapping_coverage * 0.4) + (avg_confidence * 0.6)
        
        overall_score = max(0.0, min(1.0, overall_score))
        mapping_coverage = max(0.0, min(1.0, mapping_coverage))
        avg_confidence = max(0.0, min(1.0, avg_confidence))
        
        quality_category = "EXCELLENT" if overall_score >= 0.9 else "GOOD" if overall_score >= 0.8 else "ACCEPTABLE" if overall_score >= 0.6 else "POOR" if overall_score >= 0.4 else "CRITICAL"
        
        recommendations = []
        if len(unmapped) > 0:
            recommendations.append(f"Map {len(unmapped)} unmapped fields to improve coverage")
        if low_confidence > 0:
            recommendations.append(f"Review {low_confidence} low-confidence mappings")
        if avg_confidence < 0.8:
            recommendations.append("Consider retraining AI model for better accuracy")
        
        critical_issues = []
        if mapping_coverage < 0.5:
            critical_issues.append(f"Low mapping coverage: Only {mapping_coverage:.1%} of fields mapped")
        if avg_confidence < 0.6:
            critical_issues.append(f"Low average confidence: {avg_confidence:.1%}")
    else:
        overall_score = max(0.0, min(1.0, quality_report.get('overall_score', 0.0)))
        quality_category = quality_report.get('quality_category', 'unknown')
        mapping_coverage = max(0.0, min(1.0, quality_report.get('mapping_quality', 0.0)))
        avg_confidence = max(0.0, min(1.0, quality_report.get('completeness_score', 0.0)))
        recommendations = quality_report.get('recommendations', [])
        critical_issues = quality_report.get('critical_issues', [])
        
        high_confidence = len([m for m in mappings if m.get('confidence', 0.0) >= 70])  # Use 70 instead of 0.7
        medium_confidence = len([m for m in mappings if 70 <= m.get('confidence', 0.0) < 90])  # Use 70-90 instead of 0.7-0.9
        low_confidence = len([m for m in mappings if m.get('confidence', 0.0) < 70])  # Use 70 instead of 0.7
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Overall Score", f"{overall_score:.1%}")
    with col2:
        st.metric("Mapping Coverage", f"{mapping_coverage:.1%}")
    with col3:
        st.metric("Avg Confidence", f"{avg_confidence:.1%}")
    with col4:
        st.metric("Quality Category", quality_category.upper())
    
    # Progress visualization
    st.markdown("### Quality Breakdown")
    progress_col1, progress_col2 = st.columns(2)
    
    with progress_col1:
        st.markdown("**Overall Quality**")
        st.progress(overall_score)
        
    with progress_col2:
        st.markdown("**Mapping Coverage**")
        st.progress(mapping_coverage)
    
    # Confidence breakdown
    st.markdown("### Confidence Distribution")
    conf_col1, conf_col2, conf_col3 = st.columns(3)
    with conf_col1:
        st.metric("High Confidence", high_confidence, help="90%+ confidence")
    with conf_col2:
        st.metric("Medium Confidence", medium_confidence, help="70-89% confidence")
    with conf_col3:
        st.metric("Low Confidence", low_confidence, help="<70% confidence")
    
    # Recommendations
    if recommendations:
        st.markdown("### Recommendations")
        for rec in recommendations:
            st.info(f"{rec}")
    
    # Critical issues
    if critical_issues:
        st.markdown("### Critical Issues")
        for issue in critical_issues:
            st.error(f"{issue}")
    else:
        st.success("No critical issues detected!")

def render_conditional_logic(logic_rules: List[Dict[str, Any]], doc_index: int = 0):
    """Render conditional logic with robust data handling for the UI."""
   
    if not logic_rules:
        st.info("No conditional logic rules detected.")
        return

    st.metric("Total Rules Detected", len(logic_rules))
    st.markdown("---")
    st.subheader(f"Conditional Rule Details ({len(logic_rules)} Found)")
    
    for i, rule in enumerate(logic_rules):
        rule_name = rule.get('rule_name', f'Rule {i+1}').replace('_', ' ').title()
            
        # --- START OF THE ROBUST UI FIX ---
        # Safely get and normalize the confidence value from the API response
        raw_confidence = rule.get('confidence', 0.0)
        
        # This logic handles values like 0.9 (float) or 90 (int/float) correctly
        compare_confidence = 0.0
        if isinstance(raw_confidence, (int, float)):
            compare_confidence = raw_confidence if raw_confidence <= 1.0 else raw_confidence / 100.0
        
        # Always create a display percentage from the normalized value
        display_confidence_pct = compare_confidence * 100

        # Determine display properties based on the reliable normalized value
        if compare_confidence >= 0.9:
            conf_color, conf_label, conf_icon = "#27ae60", "HIGH", "🟢"
        elif compare_confidence >= 0.7:
            conf_color, conf_label, conf_icon = "#f39c12", "MEDIUM", "🟡"
        else:
            conf_color, conf_label, conf_icon = "#e74c3c", "LOW", "🔴"
        # --- END OF THE ROBUST UI FIX ---

        # Use a red circle icon to match your latest UI screenshot for low confidence
        if conf_label == "LOW":
             conf_icon = "🔴"

        with st.expander(f"{conf_icon} {rule_name}", expanded=(i == 0)): # Expand the first rule by default
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**IF this field is filled:** `{rule.get('source_field', 'N/A')}`")
                st.markdown(f"**THEN this happens:** `{rule.get('condition_type', 'unknown').replace('_', ' ').title()}`")
            with col2:
                st.markdown(f"**Confidence:** <span style='color:{conf_color};'>{display_confidence_pct:.0f}% ({conf_label})</span>", unsafe_allow_html=True)
                

            # Clean up the description text to be more user-friendly
            description_text = rule.get('condition_text', 'No description available.')
            # Remove the technical jargon by keeping only the part before the first hyphen
            clean_description = description_text.split('-')[0].strip()

            st.markdown(f"**Description:** {clean_description}")
            
            target_fields = rule.get('target_fields', [])
            if target_fields:
                st.markdown(f"**Fields that this rule affects:** {', '.join(target_fields)}")
            
            # FIXED: Make checkbox key unique for each document
            unique_key = f"debug_{doc_index}_{rule.get('rule_id', i)}_{i}"
            if st.checkbox("Show technical details", key=unique_key):
                st.json(rule)

def render_validation_issues(mappings: List[Dict[str, Any]], unmapped: List[str], quality_report: Dict[str, Any]):
    """Render validation issues with clean styling"""
    issues = []
    
    for field in unmapped:
        issues.append({
            'type': 'Unmapped Field',
            'severity': 'High',
            'description': f"No Cadence path could be found for the PDF field '{field}'.",
            'action': 'Manual mapping required.'
        })
    
    # Issue Type 2: Low Confidence Mappings
    # Use the same confidence threshold as the tab count (e.g., < 70%)
    low_confidence_mappings = [m for m in mappings if m.get('confidence', 0.0) < 70]
    for mapping in low_confidence_mappings:
        issues.append({
            'type': 'Low Confidence',
            'severity': 'Medium',
            'description': f"Field '{mapping.get('field_name')}' was mapped with low confidence ({mapping.get('confidence', 0.0):.0f}%).",
            'action': 'Please review and confirm the mapping.'
        })

    # Issue Type 3: Critical Issues from Quality Report
    critical_issues = quality_report.get('critical_issues', [])
    for issue in critical_issues:
        issues.append({
            'type': 'Critical Issue',
            'severity': 'Critical',
            'description': issue,
            'action': 'Immediate attention required.'
        })
    
    if not issues:
        st.success("No validation issues detected. All mappings look excellent!")
        return
    
    st.warning(f"{len(issues)} Validation Issues Detected")
    
    if issues:
        issues_df = pd.DataFrame(issues)
        st.dataframe(
            issues_df,
            use_container_width=True,
            column_config={
                "type": "Issue Type",
                "severity": st.column_config.SelectboxColumn(
                    "Severity",
                    options=["Low", "Medium", "High", "Critical"],
                ),
                "description": "Description",
                "action": "Recommended Action"
            }
        )

# ============================================================================
# 9. MAIN UI RENDERING FUNCTION
# ============================================================================
def render_complete_ui(api_results: List[Dict[str, Any]]):
    """Render complete clean UI with an icon-only remove button for each result."""
    render_header()
    
    if len(api_results) > 1:
        st.success(f"Successfully processed a batch of {len(api_results)} documents.")

    for i, result in enumerate(api_results):
        file_name = result.get("filename", f"Document {i+1}")
        api_response = result.get("data", {})
        original_pdf_bytes = result.get("original_pdf_bytes")

        # --- FILENAME AND REMOVE BUTTON ON SAME LINE ---
        title_col, button_col = st.columns([0.85, 0.15])
        with title_col:
            expander_title = f"Results for: {file_name}" if not ("error" in result or not api_response) else f"❌ Error processing: {file_name}"
            st.markdown(f"### {expander_title}")
        with button_col:
            if st.button("Remove", key=f"remove_result_{i}", help=f"Remove results for {file_name}"):
                remove_result_from_session(i)
                st.rerun()
        
        # --- CONTENT BELOW ---
        with st.expander("Show Details", expanded=(i == 0)):
            if "error" in result or not api_response:
                st.error(f"Could not process this document. Error: {result.get('error', 'Unknown API error')}")
                continue

            # Existing rendering logic for the result content
            render_document_info(api_response, file_name)
            
            mappings = api_response.get('field_mappings', [])
            unmapped = api_response.get('unmapped_fields', [])
            logic_rules = api_response.get('conditional_logic_analysis', [])
            quality_report = api_response.get('quality_report', {})
            
            total_mappings = len(mappings) + len(unmapped)
            validation_issues_count = len(unmapped) + len([m for m in mappings if m.get('confidence', 0.0) < 70]) + len(quality_report.get('critical_issues', []))
            
            tab1, tab2, tab3, tab4 = st.tabs([
                f"Field Mappings ({total_mappings})",
                f"Conditional Logic ({len(logic_rules)})",
                f"Quality Report",
                f"Validation Issues ({validation_issues_count})"
            ])
            
            with tab1:
                render_enhanced_mapping_table(mappings, unmapped, file_name, original_pdf_bytes, quality_report, doc_index=i)
            with tab2:
                render_conditional_logic(logic_rules, doc_index=i)
            with tab3:
                render_quality_report(quality_report, mappings, unmapped)
            with tab4:
                render_validation_issues(mappings, unmapped, quality_report)

# ============================================================================
# 10. MAIN APPLICATION LOGIC
# ============================================================================
# Initialize session state keys if they don't exist
if 'api_response_data' not in st.session_state:
    st.session_state.api_response_data = None
if 'api_error' not in st.session_state:
    st.session_state.api_error = None

st.markdown("### Upload Document(s) for Analysis")

# The file_uploader widget will now be the SINGLE SOURCE OF TRUTH.
# Its state is managed by Streamlit and accessed via its key.
# We remove the on_change callback as it is no longer needed for this logic.
uploaded_files = st.file_uploader(
    "Choose one or more PDF files for bulk processing",
    type="pdf",
    help="Upload one or more estate-related PDF forms for AI analysis.",
    accept_multiple_files=True,
    key="file_uploader"
)

# The "Process" button's logic is now directly tied to the uploader's state.
if uploaded_files:
    num_files = len(uploaded_files)
    button_label = f"Process {num_files} Document"
    if num_files > 1:
        button_label += "s"

    if st.button(button_label, use_container_width=True):
        st.session_state.api_response_data = None
        st.session_state.api_error = None

        # We can use the 'uploaded_files' variable directly from the widget
        with st.spinner(f"Processing {num_files} document{'s' if num_files > 1 else ''}..."):
            api_result = call_api(uploaded_files)

        if api_result.get("success"):
            st.session_state['api_response_data'] = api_result["data"]
        else:
            st.session_state['api_error'] = api_result.get('error', 'An unknown error occurred.')

        # Rerun to display results
        st.rerun()

# Display results or errors from the API call.
if st.session_state.api_response_data:
    render_complete_ui(st.session_state.api_response_data)
elif st.session_state.api_error:
    st.error(st.session_state.api_error)
# Show the welcome message only if no files are uploaded AND no results are present.
elif not uploaded_files:
    st.info("Please upload one or more PDF documents to begin.")
    
    with st.expander("What does MapperAI do?", expanded=False):
        st.markdown("""
        **MapperAI** automatically analyzes PDF forms and creates auto-fillable versions connected to your Cadence data:
        
        **INPUT:** Static PDF form (e.g., "Canadian_Government_Form.pdf")  
        **ANALYSIS:** AI detects fields and maps them to Cadence paths  
        **OUTPUT:** That SAME PDF becomes auto-fillable with Cadence data  
        
        **Key Features:**
        - **Field Detection** - Identifies all form fields in your PDF  
        - **Smart Mapping** - Maps fields to appropriate Cadence paths  
        - **Auto-Fill Generation** - Creates fillable PDFs connected to your data  
        - **Logic Analysis** - Detects conditional rules and relationships  
        - **Quality Assessment** - Provides confidence scores and recommendations  
        - **Admin Review** - Allows you to approve, edit, or reject mappings  
        
        **Requirements:**
        - Install PDF libraries: `pip install PyPDFForm fillpdf pdfrw2 reportlab`
        - Ensure MapperAI backend is running on port 8000
        - Upload interactive PDF forms (not scanned images)
        
        **Result:** Transform static forms into intelligent, auto-fillable documents!
        """)
        
    # Show PDF generation status
    if PDF_GENERATION_AVAILABLE:
        st.success("PDF generation libraries are installed and ready!")
    else:
        st.warning("PDF generation libraries not found. Install with: `pip install PyPDFForm fillpdf pdfrw2 reportlab`")
