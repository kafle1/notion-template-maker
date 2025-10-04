"""
Template generation routes
Handles AI-powered template creation
"""

from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import sys
import os
import uuid

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))

from backend.services.session_manager import SessionManager
from backend.services.template_generator import TemplateGenerator
from backend.services.template_validator import TemplateValidator
from backend.clients.openrouter_client import OpenRouterClient
from backend.clients.notion_client import NotionClient

router = APIRouter()
session_manager = SessionManager()
template_validator = TemplateValidator()


def ensure_session_exists(session_id: str) -> str:
    """
    Ensure session exists, create if it doesn't.
    Returns the session ID.
    """
    # Check if session exists
    if session_id not in session_manager._sessions:
        print(f"[TEMPLATES] Session {session_id} not found, creating new one with same ID")
        # Manually create session with the provided ID
        session_manager._sessions[session_id] = {
            "session_id": session_id,
            "user_id": "web_user",
            "created_at": datetime.now().isoformat(),
            "expires_at": (
                datetime.now() + timedelta(hours=24)
            ).isoformat(),
            "user_data": {},
            "api_keys": {},
            "preferences": {},
        }
    return session_id


class TemplateRequest(BaseModel):
    """Request model for template generation"""
    template_type: str = Field(..., description="Type of template to generate")
    title: str = Field(..., min_length=1, max_length=100, description="Template title")
    description: str = Field(..., min_length=1, max_length=1000, description="Template description")
    features: Optional[List[str]] = Field(default=[], description="Additional features")
    complexity: Optional[str] = Field(default="medium", description="Complexity level")
    include_database: Optional[bool] = Field(default=True, description="Include databases")
    include_pages: Optional[bool] = Field(default=True, description="Include sample pages")


class TemplateResponse(BaseModel):
    """Response model for generated templates"""
    template_id: str
    template_data: Dict[str, Any]
    metadata: Dict[str, Any]
    validation_errors: List[str] = []


@router.post("/generate", response_model=TemplateResponse)
async def generate_template(
    request: TemplateRequest,
    session_id: str = Header(..., alias="X-Session-ID")
):
    """Generate a new Notion template using AI"""
    try:
        # Ensure session exists (create if backend restarted)
        ensure_session_exists(session_id)
        
        # Validate input
        user_input = request.dict()
        validation_errors = template_validator.validate_user_input(user_input)
        
        if validation_errors:
            raise HTTPException(
                status_code=400,
                detail={"message": "Validation failed", "errors": validation_errors}
            )
        
        # Get API keys from session
        openrouter_key = session_manager.get_api_key(session_id, "openrouter")
        if not openrouter_key:
            raise HTTPException(status_code=401, detail="OpenRouter API key not configured")
        
        notion_key = session_manager.get_api_key(session_id, "notion")
        
        # Get AI model preference from session (default to deepseek if not set)
        ai_model = session_manager.get_preference(session_id, "ai_model") or "deepseek/deepseek-chat-v3.1:free"
        
        # Initialize clients
        openrouter_client = OpenRouterClient(openrouter_key, model=ai_model)
        notion_client = NotionClient(notion_key) if notion_key else None
        
        # Initialize generator
        generator = TemplateGenerator(openrouter_client, notion_client)
        
        # Generate template
        template_data = generator.generate_template(user_input)
        
        # Validate generated template
        template_errors = template_validator.validate_template_data(template_data)
        
        # Generate template ID
        template_id = str(uuid.uuid4())
        
        return TemplateResponse(
            template_id=template_id,
            template_data=template_data,
            metadata=template_data.get("metadata", {}),
            validation_errors=template_errors
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/types")
async def list_template_types():
    """List available template types"""
    return {
        "types": [
            {"id": "general", "name": "General", "description": "General purpose template"},
            {"id": "project_management", "name": "Project Management", "description": "Manage projects and tasks"},
            {"id": "knowledge_base", "name": "Knowledge Base", "description": "Organize knowledge and notes"},
            {"id": "personal", "name": "Personal", "description": "Personal productivity"},
            {"id": "business", "name": "Business", "description": "Business operations"},
            {"id": "education", "name": "Education", "description": "Learning and education"},
            {"id": "health", "name": "Health", "description": "Health and wellness tracking"},
            {"id": "finance", "name": "Finance", "description": "Financial management"},
        ]
    }


@router.get("/features")
async def list_available_features():
    """List available template features"""
    return {
        "features": [
            "Calendar Integration",
            "Progress Tracking",
            "File Attachments",
            "Tags/Categories",
            "Priority Levels",
            "Due Dates",
            "Status Tracking",
            "Custom Properties",
            "Formulas",
            "Relations",
        ]
    }
