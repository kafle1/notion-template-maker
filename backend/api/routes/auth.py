"""
Authentication routes
Handles API key management and session tokens
"""

from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timedelta
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))

from backend.services.session_manager import SessionManager

router = APIRouter()
session_manager = SessionManager()


def ensure_session_exists(session_id: str) -> str:
    """
    Ensure session exists, create if it doesn't.
    Returns the session ID.
    """
    # Check if session exists
    if session_id not in session_manager._sessions:
        print(f"[AUTH] Session {session_id} not found, creating new one with same ID")
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


class APIKeysRequest(BaseModel):
    """Request model for storing API keys"""
    openrouter_key: str = Field(..., min_length=10, description="OpenRouter API key")
    notion_token: str = Field(..., min_length=10, description="Notion integration token (required for importing templates)")
    ai_model: Optional[str] = Field(None, description="AI model to use for template generation")


class SessionResponse(BaseModel):
    """Response model for session creation"""
    session_id: str
    message: str


@router.post("/session", response_model=SessionResponse)
async def create_session():
    """Create a new session"""
    try:
        session_id = session_manager.create_session(user_id="web_user")
        return SessionResponse(
            session_id=session_id,
            message="Session created successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/keys")
async def store_api_keys(
    keys: APIKeysRequest,
    session_id: str = Header(..., alias="X-Session-ID")
):
    """Store API keys in session"""
    try:
        print(f"[AUTH] Storing keys for session: {session_id}")
        
        # Ensure session exists (create if backend restarted)
        ensure_session_exists(session_id)
        
        # Store keys directly without validation
        or_result = session_manager.store_api_key(session_id, "openrouter", keys.openrouter_key)
        notion_result = session_manager.store_api_key(session_id, "notion", keys.notion_token)
        
        print(f"[AUTH] OpenRouter storage result: {or_result}")
        print(f"[AUTH] Notion storage result: {notion_result}")
        
        # Store AI model preference
        if keys.ai_model:
            session_manager.store_preference(session_id, "ai_model", keys.ai_model)
        
        # Verify keys were stored
        or_key = session_manager.get_api_key(session_id, "openrouter")
        notion_key = session_manager.get_api_key(session_id, "notion")
        print(f"[AUTH] Verification - OpenRouter key exists: {bool(or_key)}")
        print(f"[AUTH] Verification - Notion key exists: {bool(notion_key)}")
        
        return {
            "message": "API keys stored successfully",
            "openrouter_configured": True,
            "notion_configured": True
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/keys/status")
async def get_keys_status(session_id: str = Header(..., alias="X-Session-ID")):
    """Check which API keys are configured"""
    try:
        print(f"[AUTH] Checking keys status for session: {session_id}")
        
        # Ensure session exists (create if backend restarted)
        ensure_session_exists(session_id)
        
        openrouter_key = session_manager.get_api_key(session_id, "openrouter")
        notion_key = session_manager.get_api_key(session_id, "notion")
        
        print(f"[AUTH] Status - OpenRouter key exists: {bool(openrouter_key)}")
        print(f"[AUTH] Status - Notion key exists: {bool(notion_key)}")
        
        return {
            "openrouter_configured": bool(openrouter_key),
            "notion_configured": bool(notion_key),
            "session_valid": True
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/session")
async def delete_session(session_id: str = Header(..., alias="X-Session-ID")):
    """Delete a session"""
    try:
        success = session_manager.delete_session(session_id)
        if not success:
            raise HTTPException(status_code=404, detail="Session not found")
        
        return {"message": "Session deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
