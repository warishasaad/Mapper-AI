"""
AI Enhancement Module - DYNAMIC Schema Integration

"""

import asyncio
import logging
import time
import json
import re
from typing import Dict, Optional, List, Any
from .models import OllamaConfig, MappingResult, FieldType, AIEnhancementError

# Import the actual schema 
try:
    from .schema import cadence_schema
    SCHEMA_AVAILABLE = True
    print(f"✅ Schema imported: {len(cadence_schema.get_schema_paths())} paths available")
except ImportError:
    SCHEMA_AVAILABLE = False
    print("⚠️ Schema not available - using fallback")

# to import httpx for Ollama communication
try:
    import httpx
    HTTPX_AVAILABLE = True
except ImportError:
    try:
        import subprocess
        import sys
        print("Installing httpx for Ollama integration...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "httpx"])
        import httpx
        HTTPX_AVAILABLE = True
        print("✅ httpx installed successfully")
    except Exception as e:
        HTTPX_AVAILABLE = False
        logging.warning(f"httpx not available - AI enhancement will be disabled: {e}")

class DynamicSchemaManager:
    """Manages dynamic schema loading for AI prompts - NO HARDCODED PATHS"""
    
    def __init__(self, schema):
        self.schema = schema
        self.all_paths = schema.get_schema_paths() if schema else []
        self.categorized_paths = self._categorize_all_paths()
        
        print(f"Dynamic Schema Manager initialized")
        print(f"Total paths: {len(self.all_paths)}")
        print(f"Categories: {list(self.categorized_paths.keys())}")
        for category, paths in self.categorized_paths.items():
            if paths:
                print(f"   • {category}: {len(paths)} paths")
    
    def _categorize_all_paths(self) -> Dict[str, List[str]]:
        """Categorize ALL schema paths dynamically - NO HARDCODING"""
        categories = {
            'deceased': [], 'applicant': [], 'spouse': [], 'estate_reps': [], 'children': [],
            'contact': [], 'financial': [], 'property': [], 'insurance': [], 'task_planner': [],
            'payment': [], 'will': [], 'documents': [], 'final_wishes': [], 'utility': [],
            'account': [], 'business': [], 'farm': [], 'other': []
        }
        
        for path in self.all_paths:
            categorized = False
            if path.startswith('deceased.'): categories['deceased'].append(path); categorized = True
            elif path.startswith('applicant.'): categories['applicant'].append(path); categorized = True
            elif path.startswith('spouse.'): categories['spouse'].append(path); categorized = True
            elif path.startswith('estate_reps'): categories['estate_reps'].append(path); categorized = True
            elif path.startswith('children'): categories['children'].append(path); categorized = True
            elif path.startswith('contact'): categories['contact'].append(path); categorized = True
            elif path.startswith('will.'): categories['will'].append(path); categorized = True
            elif path.startswith('payment.'): categories['payment'].append(path); categorized = True
            elif path.startswith('task_planner'): categories['task_planner'].append(path); categorized = True
            elif path.startswith('final_wishes'): categories['final_wishes'].append(path); categorized = True
            elif path.startswith('business_documents'): categories['business'].append(path); categorized = True
            elif path.startswith('farm_documents'): categories['farm'].append(path); categorized = True
            
            if not categorized:
                if any(term in path for term in ['financial', 'bank', 'account', 'investment']): categories['financial'].append(path)
                elif any(term in path for term in ['property', 'real_estate', 'vehicle', 'farm']): categories['property'].append(path)
                elif 'insurance' in path: categories['insurance'].append(path)
                elif any(term in path for term in ['document', 'id_document', 'key_document']): categories['documents'].append(path)
                elif 'utility' in path: categories['utility'].append(path)
                elif 'account' in path: categories['account'].append(path)
                else: categories['other'].append(path)
        
        for category in categories:
            categories[category].sort()
        
        return categories
    
    def get_representative_paths(self, category: str, max_paths: int = 8) -> List[str]:
        """Get representative paths from a category for AI prompt"""
        paths = self.categorized_paths.get(category, [])
        if not paths or len(paths) <= max_paths:
            return paths
        
        representative = []
        priority_patterns = {
            'deceased': ['name', 'date_of_death', 'date_of_birth', 'social_insurance'],
            'applicant': ['name', 'address', 'phone', 'email'],
            'spouse': ['name', 'date_of_birth', 'date_of_marriage'],
            'estate_reps': ['name', 'role', 'address', 'phone'],
            'children': ['name', 'date_of_birth'],
            'financial': ['account_number', 'balance', 'total_estate_value'],
            'property': ['address', 'estimated_value', 'vin', 'vehicles'],
            'insurance': ['policy_number', 'coverage_amount', 'beneficiary'],
            'task_planner': ['b_will', 'b_has_spouse', 'b_has_children']
        }
        
        patterns = priority_patterns.get(category, [])
        for pattern in patterns:
            for path in paths:
                if pattern in path and len(representative) < max_paths and path not in representative:
                    representative.append(path)
        
        for path in paths:
            if path not in representative and len(representative) < max_paths:
                representative.append(path)
        
        return representative[:max_paths]
    
    def generate_schema_summary(self) -> str:
        """Generate dynamic schema summary for AI prompt"""
        summary_parts = []
        for category, paths in self.categorized_paths.items():
            if not paths: continue
            representative = self.get_representative_paths(category)
            if not representative: continue
            
            category_title = category.upper().replace('_', ' ')
            summary_parts.append(f"\n# {category_title} (Examples)")
            summary_parts.extend([f"- {path}" for path in representative])
            if len(paths) > len(representative):
                summary_parts.append(f"- ... and {len(paths) - len(representative)} more")
        
        return '\n'.join(summary_parts)

class OllamaAIEnhancer:
    """AI enhancement using Ollama with DYNAMIC schema integration"""
    
    def __init__(self, config: OllamaConfig):
        self.config = config
        self.client = None
        self.logger = logging.getLogger(__name__)
        
        if SCHEMA_AVAILABLE:
            self.schema_manager = DynamicSchemaManager(cadence_schema)
        else:
            self.schema_manager = None
        
        if self.config.enabled and HTTPX_AVAILABLE:
            self.client = self._init_client()
        
        self.stats = {
            "total_calls": 0, "successful_calls": 0, "failed_calls": 0,
            "average_response_time": 0.0, "total_response_time": 0.0,
            "cache_hits": 0, "enhanced_mappings": 0, "validation_calls": 0,
            "form_detection_calls": 0, "connection_errors": 0, "timeout_errors": 0,
            "json_parse_errors": 0, "invalid_path_responses": 0, "extracted_valid_paths": 0
        }
        
        self.cache = {}
        self.cache_max_size = 500
        self.prompts = self._load_dynamic_prompts()
        self.last_call_time = 0
        self.min_call_interval = 0.1
        self.connection_tested = False
        self.connection_healthy = False
        
        self.logger.info("Dynamic Ollama AI Enhancer initialized for real estate data processing")
        
        if self.client:
            asyncio.create_task(self._test_initial_connection())
    
    def _init_client(self) -> Optional[httpx.AsyncClient]:
        """Initialize Ollama HTTP client with optimized configuration"""
        try:
            return httpx.AsyncClient(
                timeout=httpx.Timeout(connect=10.0, read=self.config.timeout, write=10.0, pool=15.0),
                limits=httpx.Limits(max_connections=20, max_keepalive_connections=10),
                follow_redirects=True, verify=False,
                headers={'Content-Type': 'application/json', 'Accept': 'application/json'}
            )
        except Exception as e:
            self.logger.error(f"Failed to initialize Ollama client: {e}")
            return None

    def _load_dynamic_prompts(self) -> Dict[str, str]:
        """Load prompts with DYNAMIC schema paths and the final Chain-of-Thought instructions."""
        
        if not self.schema_manager:
            return { "field_mapping": "Schema not available. Respond with best guess." }

        return {
            "field_mapping": f"""You are a precise field mapping system. Your only task is to find the best schema path for the given field.

# Relevant Schema Paths
{{{{focused_schema_summary}}}}

# Field to Map
- Name: "{{{{field_name}}}}"
- Context: {{{{context}}}}

# Rules
- You MUST select a path from the 'Relevant Schema Paths' list.
- If no logical path exists in the RELEVANT paths, you MUST respond with `unknown.field`.
- **CRITICAL RULE:** Do NOT map a field that is clearly about a person's address (like City, State, ZIP) to a vehicle path. A person's address belongs to an `applicant` or `deceased` path. A vehicle's registration location belongs to a `property.vehicles` path.
- Your response MUST contain ONLY the schema path and nothing else.

# Your Response
""",
            "field_validation": """Validate Canadian estate form data:

FIELD: {field_name}
VALUE: {field_value}
TYPE: {field_type}

Canadian requirements:
- SIN: 9 digits, valid format
- Phone: Valid Canadian format
- Postal: A1A 1A1 format
- Dates: Reasonable for estate processing

Respond with exactly "VALID" or "INVALID: reason":""",
            "form_type_detection": """Identify Canadian estate form type:

FIELDS: {field_list}

Form types:
death_benefit_application, estate_information, life_insurance_claim, 
probate_application, bank_account_closure, vehicle_transfer, 
tax_clearance, property_transfer

Respond with exactly one form type:"""
        }

    
    async def _test_initial_connection(self):
        """Test initial connection to Ollama"""
        try:
            self.logger.info("Testing initial Ollama connection...")
            health = await self.health_check()
            self.connection_tested = True
            self.connection_healthy = health.get("healthy", False)
            if self.connection_healthy:
                self.logger.info("✅ Ollama connection successful - Dynamic AI enhancement ready")
            else:
                self.logger.warning(f"⚠️ Ollama connection failed: {health.get('reason', 'Unknown')}")
        except Exception as e:
            self.logger.error(f"Initial connection test failed: {e}")
            self.connection_tested = True
            self.connection_healthy = False
    
    # =========================================================================
    # START OF CHANGE 2: This is the updated mapping method
    # =========================================================================
    async def enhance_field_mapping(self, field_name: str, field_value: str = "", 
                                  context: str = "") -> Dict[str, Any]:
        """Enhance field mapping using dynamic and context-aware AI analysis"""
        
        if not self._is_available():
            return {"success": False, "reason": "AI enhancement unavailable"}
        
        if not field_name or not field_name.strip():
            return {"success": False, "reason": "No field name provided"}
        
        cache_key = f"mapping:{field_name.lower().strip()}:{field_value[:50] if field_value else ''}"
        if cache_key in self.cache:
            self.stats["cache_hits"] += 1
            return self.cache[cache_key]
        
        await self._apply_rate_limit()
        start_time = time.time()
        self.stats["total_calls"] += 1
        
        try:
            context_info = context.strip() if context else "No additional context provided."
            
            # Dynamically select relevant schema categories
            relevant_categories = ['deceased', 'applicant']
            field_lower = field_name.lower()
            if any(kw in field_lower for kw in ['vin', 'vehicle', 'model', 'make', 'plate', 'year', 'body type']):
                relevant_categories.extend(['property', 'documents'])
            elif any(kw in field_lower for kw in ['address', 'city', 'state', 'zip', 'po']):
                relevant_categories.extend(['applicant', 'deceased'])
            
            # Build a focused schema summary
            focused_schema_summary = ""
            for category in set(relevant_categories):
                paths = self.schema_manager.get_representative_paths(category, max_paths=10)
                if paths:
                    focused_schema_summary += f"\n# {category.upper().replace('_', ' ')} (Examples)\n"
                    focused_schema_summary += "\n".join([f"- {path}" for path in paths])

            # Get the base prompt template
            prompt_template = self.prompts["field_mapping"]
            
            # Manually replace the placeholders to avoid f-string conflicts
            prompt = prompt_template.replace("{{focused_schema_summary}}", focused_schema_summary)
            prompt = prompt.replace("{{field_name}}", field_name.strip())
            prompt = prompt.replace("{{context}}", context_info)
            
            response = await self._call_ollama(prompt)
            
            if response["success"]:
                mapped_path = response["content"].strip()
                mapped_path = re.sub(r"[`'\"]", "", mapped_path)
                
                final_path = mapped_path if self._is_valid_schema_path(mapped_path) else self._try_extract_valid_path(mapped_path)
                
                if final_path and final_path != 'unknown.field':
                    # Final sanity check for vehicle-related fields
                    is_vehicle_field = any(kw in field_lower for kw in ['vin', 'vehicle', 'plate', 'make', 'model'])
                    is_vehicle_path = 'property.vehicles' in final_path

                    if is_vehicle_field and not is_vehicle_path:
                        self.logger.warning(f"AI Mismatch: AI mapped a clear vehicle field '{field_name}' to a non-vehicle path '{final_path}'. Rejecting.")
                        final_path = None # Reject the illogical mapping
                
                if final_path:
                    result = {
                        "success": True, "path": final_path,
                        "confidence": self._determine_ai_confidence(response["content"], field_name),
                        "method": "ollama_context_aware", "response_time": time.time() - start_time,
                        "model": response.get("model", self.config.model),
                        "raw_response": response.get("raw_content", mapped_path), "schema_validated": True
                    }
                    self.stats["successful_calls"] += 1; self.stats["enhanced_mappings"] += 1
                    if len(self.cache) < self.cache_max_size: self.cache[cache_key] = result
                    return result
                else:
                    self.stats["failed_calls"] += 1; self.stats["invalid_path_responses"] += 1
                    # Correctly format the f-string to show the actual value of mapped_path
                    self.logger.warning(f"❌ AI suggested path not found in schema or was rejected for '{field_name}': '{mapped_path}'")
                    return {"success": False, "reason": f"AI returned invalid/rejected path: {mapped_path[:100]}"}
            else:
                self.stats["failed_calls"] += 1
                return {"success": False, "reason": response.get("error", "Unknown AI error")}
        except Exception as e:
            self.stats["failed_calls"] += 1
            self.logger.error(f"AI enhancement exception for '{field_name}': {e}", exc_info=True)
            return {"success": False, "reason": f"AI processing error: {str(e)}"}
        finally:
            response_time = time.time() - start_time
            self.stats["total_response_time"] += response_time
            if self.stats["total_calls"] > 0:
                self.stats["average_response_time"] = self.stats["total_response_time"] / self.stats["total_calls"]


    async def _call_ollama(self, prompt: str) -> Dict[str, Any]:
        """Make API call to Ollama with optimized settings"""
        if not self.client: return {"success": False, "error": "Ollama client not initialized"}
        
        try:
            payload = {
                "model": self.config.model, "prompt": prompt, "stream": False,
                "options": {
                    "temperature": 0.1, "num_predict": 100,
                    "stop": ["\n\n", "---", "```", "EXAMPLE:", "Based on"],
                    "top_k": 10, "top_p": 0.5, "repeat_penalty": 1.1
                }
            }
            response = await self.client.post(f"{self.config.base_url}/api/generate", json=payload, timeout=self.config.timeout)
            
            if response.status_code == 200:
                data = response.json()
                raw_content = data.get("response", "").strip()
                cleaned_content = self._clean_ai_response(raw_content)
                if not cleaned_content: return {"success": False, "error": "Empty response from Ollama"}
                return {
                    "success": True, "content": cleaned_content, "raw_content": raw_content,
                    "model": data.get("model", self.config.model)
                }
            else:
                return {"success": False, "error": f"HTTP {response.status_code}: {response.text[:200]}"}
        except asyncio.TimeoutError:
            self.stats["timeout_errors"] += 1; return {"success": False, "error": "Request timeout"}
        except httpx.ConnectError as e:
            self.stats["connection_errors"] += 1; return {"success": False, "error": f"Cannot connect to Ollama: {e}"}
        except Exception as e:
            self.stats["connection_errors"] += 1; return {"success": False, "error": f"Unexpected error: {e}"}
    
    def _clean_ai_response(self, raw_response: str) -> str:
        """Clean and extract the final schema path from a Chain-of-Thought response."""
        if not raw_response: return ""
        
        if "final answer" in raw_response.lower():
            parts = re.split(r'## Final Answer\s*', raw_response, flags=re.IGNORECASE)
            if len(parts) > 1:
                return parts[-1].strip().split('\n')[0].strip()

        lines = raw_response.strip().split('\n')
        for line in reversed(lines):
            line = line.strip()
            if self._looks_like_schema_path(line): return line
        
        for line in reversed(lines):
            if line: return line
        
        return ""
    
    def _looks_like_schema_path(self, text: str) -> bool:
        """Check if text looks like a valid schema path"""
        return text and len(text) <= 100 and '.' in text and (' ' not in text or '[*]' in text) and \
               not any(word in text.lower().split() for word in ['the', 'is', 'based', 'on'] if len(word) > 2)
    
    def _is_valid_schema_path(self, path: str) -> bool:
        """Validate path against actual schema"""
        if not path or path == "unknown.field": return True
        clean_path = path.strip().replace('"', '').replace("'", "")
        if not self.schema_manager or not self.schema_manager.all_paths: return '.' in clean_path
        if clean_path in self.schema_manager.all_paths: return True
        for actual_path in self.schema_manager.all_paths:
            if clean_path.lower().replace('[0]', '[*]') == actual_path.lower().replace('[0]', '[*]'): return True
        return False
    
    def _try_extract_valid_path(self, invalid_response: str) -> Optional[str]:
        """Try to extract valid schema path from invalid AI response"""
        if not self.schema_manager or not self.schema_manager.all_paths: return None
        for actual_path in self.schema_manager.all_paths:
            if actual_path.lower() in invalid_response.lower():
                self.stats["extracted_valid_paths"] += 1; return actual_path
        
        matches = re.findall(r'\b(deceased|applicant|spouse|estate_reps|children|financial|property|task_planner|contact)\.[\w\[\*\]\.]+\b', invalid_response, re.IGNORECASE)
        for match in matches:
            if self._is_valid_schema_path(match.strip().rstrip('.,!?')):
                self.stats["extracted_valid_paths"] += 1; return match.strip().rstrip('.,!?')
        return None
    
    def _determine_ai_confidence(self, response: str, field_name: str) -> float:
        """Determine confidence level based on AI response quality"""
        if "unknown.field" in response: return 0.3
        if any(indicator in response.lower() for indicator in ["clearly", "obviously"]): return 0.95
        if any(indicator in response.lower() for indicator in ["maybe", "possibly"]): return 0.5
        return 0.8
    
    async def _apply_rate_limit(self):
        """Apply rate limiting between API calls"""
        time_since_last = time.time() - self.last_call_time
        if time_since_last < self.min_call_interval: await asyncio.sleep(self.min_call_interval - time_since_last)
        self.last_call_time = time.time()
    
    def _is_available(self) -> bool:
        """Check if AI enhancement is available"""
        return self.config.enabled and self.client is not None and HTTPX_AVAILABLE
    
    def _get_availability_details(self) -> Dict[str, Any]:
        """Get detailed availability information"""
        return {
            "config_enabled": self.config.enabled, "httpx_available": HTTPX_AVAILABLE,
            "client_initialized": self.client is not None, "schema_available": SCHEMA_AVAILABLE,
            "schema_paths_loaded": len(self.schema_manager.all_paths) if self.schema_manager else 0,
            "base_url": self.config.base_url, "model": self.config.model,
            "connection_tested": self.connection_tested, "connection_healthy": self.connection_healthy
        }
    
    async def health_check(self) -> Dict[str, Any]:
        """Comprehensive health check for dynamic AI system"""
        if not self._is_available(): return {"healthy": False, "reason": "AI not available"}
        try:
            response = await self.client.get(f"{self.config.base_url}/api/tags", timeout=10.0)
            if response.status_code != 200: return {"healthy": False, "reason": f"HTTP {response.status_code}"}
            models_data = response.json()
            available_models = [model.get('name', '') for model in models_data.get('models', [])]
            if self.config.model not in available_models:
                return {"healthy": False, "reason": f"Model '{self.config.model}' not available"}
            return {"healthy": True, "model": self.config.model, "schema_paths_available": len(self.schema_manager.all_paths) if self.schema_manager else 0}
        except Exception as e:
            return {"healthy": False, "reason": f"Health check failed: {e}"}
    
    def get_stats(self) -> Dict[str, Any]:
        """Get comprehensive AI enhancement statistics"""
        total_calls = self.stats["total_calls"]
        return {
            **self.stats,
            "cache_efficiency": round((self.stats["cache_hits"] / max(1, total_calls + self.stats["cache_hits"])) * 100, 1),
            "success_rate": round((self.stats["successful_calls"] / max(1, total_calls)) * 100, 1),
            "average_response_time_ms": round(self.stats["average_response_time"] * 1000),
            "is_available": self._is_available(), "connection_healthy": self.connection_healthy,
        }
    
    async def cleanup(self):
        """Cleanup AI enhancement resources"""
        if self.client: await self.client.aclose()

class AIEnhancementManager:
    """Manager for AI enhancement features - Dynamic Schema Integration"""
    def __init__(self, config: OllamaConfig):
        self.config = config
        self.enhancer = OllamaAIEnhancer(config)
        self.logger = logging.getLogger(__name__)
        self.enabled_features = {"field_mapping": True, "field_validation": True, "form_detection": True}
        
    async def enhance_field_mapping(self, mapping_result, field_value: str = None):
        """Enhanced field mapping with dynamic schema"""
        if not self.config.enabled or (hasattr(mapping_result, 'confidence') and float(mapping_result.confidence) >= 0.9):
            return mapping_result
        try:
            ai_result = await self.enhancer.enhance_field_mapping(mapping_result.field_name, field_value or "")
            if ai_result.get("success") and ai_result.get("path") != "unknown.field":
                mapping_result.cadence_path = ai_result["path"]
                mapping_result.template = f"{{{{{ai_result['path']}}}}}"
                mapping_result.confidence = ai_result.get("confidence", 0.7)
                if not hasattr(mapping_result, 'metadata'): mapping_result.metadata = {}
                mapping_result.metadata.update({'ai_enhanced': True, 'ai_model': self.config.model})
                self.logger.info(f"✅ AI enhanced: {mapping_result.field_name} → {ai_result['path']}")
            else:
                self.logger.warning(f"⚠️ AI enhancement failed: {ai_result.get('reason', 'Unknown')}")
            return mapping_result
        except Exception as e:
            self.logger.error(f"AI enhancement failed: {e}")
            return mapping_result
    
    async def test_connection(self) -> Dict[str, Any]:
        """Test AI connection"""
        return await self.enhancer.health_check()
    
    async def get_system_status(self) -> Dict[str, Any]:
        """Get AI system status"""
        return {"health": await self.enhancer.health_check(), "statistics": self.enhancer.get_stats()}
    
    async def cleanup(self):
        """Cleanup AI resources"""
        await self.enhancer.cleanup()