from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from typing import Dict, Any, Optional, List # <--- Added List here
import logging
import os
import sys
import uuid # <--- Added for unique batch IDs and filenames
import asyncio # <--- Added for parallel processing

# ==============================================================================
# CORRECTED: The project structure is now standard, so sys.path manipulation
# is no longer needed. Imports from the 'api' package will work correctly
# when `uvicorn main:app` is run from the project root.
# ==============================================================================

# Now, these absolute imports will work reliably.
from api.core.estate_mapper import UniversalEstateMapper
from api.core.models import OllamaConfig
from api.models_schema import DocumentProcessingResponse, ProcessFieldsRequest
from api.core.utils import install_dependencies

# --- App Initialization ---
app = FastAPI(
    title="MapperAI API",
    description="Automated document field extraction and contextualization for estate settlement.",
    version="1.0.0"
)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- System Initialization ---
@app.on_event("startup")
async def startup_event():
    logger.info("Starting up MapperAI API...")
    install_dependencies()
    logger.info("🏛️ Estate Mapper AI System Initialized and Ready.")

# --- Dependency Injection ---
ollama_conf = OllamaConfig()
universal_mapper = UniversalEstateMapper(ollama_config=ollama_conf)

def get_mapper():
    return universal_mapper

# --- API Endpoints ---

@app.get("/api/v1/status", tags=["System"])
async def get_status():
    return {"status": "ok", "version": "1.0.0"}

@app.post("/api/v1/process/document", response_model=DocumentProcessingResponse, tags=["Processing"])
async def process_document_endpoint(
    file: UploadFile = File(...),
    mapper: UniversalEstateMapper = Depends(get_mapper)
):
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF is supported.")

    temp_dir = "/tmp/mapper_uploads"
    os.makedirs(temp_dir, exist_ok=True)
    # Use a unique filename to prevent conflicts
    temp_file_path = os.path.join(temp_dir, f"{uuid.uuid4()}-{file.filename}")

    try:
        with open(temp_file_path, "wb") as buffer:
            buffer.write(await file.read())
        logger.info(f"Processing document: {file.filename}")
        
        # Get the result from mapper
        result = await mapper.process_pdf_file(temp_file_path)
        
        if "error" in result:
             raise HTTPException(status_code=500, detail=result["error"])
        
        return result
        
    except Exception as e:
        logger.error(f"Error processing document {file.filename}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An internal error occurred: {e}")
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

# ==============================================================================
# START OF NEWLY ADDED ENDPOINT
# ==============================================================================
@app.post("/api/v1/process/document/batch", tags=["Processing"])
async def process_document_batch_endpoint(
    files: List[UploadFile] = File(...),
    mapper: UniversalEstateMapper = Depends(get_mapper)
):
    """
    Process a batch of PDF documents concurrently.
    """
    temp_dir = "/tmp/mapper_uploads"
    os.makedirs(temp_dir, exist_ok=True)
    
    tasks = []
    temp_files = []

    for file in files:
        if not file.filename.lower().endswith('.pdf'):
            logger.warning(f"Skipping non-PDF file in batch: {file.filename}")
            continue

        # Save each file temporarily with a unique name
        temp_file_path = os.path.join(temp_dir, f"{uuid.uuid4()}-{file.filename}")
        temp_files.append(temp_file_path)
        
        try:
            with open(temp_file_path, "wb") as buffer:
                buffer.write(await file.read())
            # Create a processing task for each valid file
            tasks.append(mapper.process_pdf_file(temp_file_path))
        except Exception as e:
            logger.error(f"Failed to save file for batch processing: {file.filename}, Error: {e}")

    if not tasks:
        raise HTTPException(status_code=400, detail="No valid PDF files found in the batch.")

    logger.info(f"Processing a batch of {len(tasks)} documents concurrently.")
    
    # Run all processing tasks in parallel
    batch_results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Clean up all temporary files
    for temp_file in temp_files:
        if os.path.exists(temp_file):
            os.remove(temp_file)

    # Structure the final response
    processed_results = []
    for i, result in enumerate(batch_results):
        original_filename = files[i].filename
        if isinstance(result, Exception):
            processed_results.append({"filename": original_filename, "error": str(result)})
        else:
            processed_results.append({"filename": original_filename, "data": result})

    return {"batch_id": str(uuid.uuid4()), "results": processed_results}
# ==============================================================================
# END OF NEWLY ADDED ENDPOINT
# ==============================================================================

@app.post("/api/v1/process/fields", response_model=DocumentProcessingResponse, tags=["Processing"])
async def process_fields_endpoint(
    request: ProcessFieldsRequest,
    mapper: UniversalEstateMapper = Depends(get_mapper)
):
    try:
        logger.info(f"Processing {len(request.field_data)} fields.")
        result = await mapper.process_form(
            field_data=request.field_data,
            context=request.form_context
        )
        if "error" in result:
             raise HTTPException(status_code=500, detail=result["error"])
        return result
    except Exception as e:
        logger.error(f"Error processing fields: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An internal error occurred: {e}")

@app.get("/")
async def root():
    return {"message": "Welcome to the MapperAI API. Visit /docs for documentation."}