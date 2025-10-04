"""
Notion integration routes
Handles template import to Notion workspace
"""

from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))

from backend.services.session_manager import SessionManager
from backend.services.notion_import_service import NotionImportService
from backend.clients.notion_client import NotionClient

router = APIRouter()
session_manager = SessionManager()


def ensure_session_exists(session_id: str) -> str:
    """
    Ensure session exists, create if it doesn't.
    Returns the session ID.
    """
    # Check if session exists
    if session_id not in session_manager._sessions:
        print(f"[NOTION] Session {session_id} not found, creating new one with same ID")
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


class ImportRequest(BaseModel):
    """Request model for template import"""
    template_data: Dict[str, Any]
    workspace_id: Optional[str] = None
    parent_page_id: Optional[str] = None


@router.post("/import")
async def import_template(
    request: ImportRequest,
    session_id: str = Header(..., alias="X-Session-ID")
):
    """Import template to Notion workspace"""
    try:
        # Ensure session exists (create if backend restarted)
        ensure_session_exists(session_id)
        
        # Get Notion token from session
        notion_token = session_manager.get_api_key(session_id, "notion")
        if not notion_token:
            raise HTTPException(status_code=401, detail="Notion Integration Token not configured")
        
        # Initialize clients
        notion_client = NotionClient(notion_token)
        import_service = NotionImportService(notion_client)
        
        # Perform import
        result = import_service.import_template(
            request.template_data,
            request.workspace_id,
            request.parent_page_id
        )
        
        if not result["success"]:
            raise HTTPException(
                status_code=400,
                detail={"message": "Import failed", "errors": result["errors"]}
            )
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/workspaces")
async def list_workspaces(session_id: str = Header(..., alias="X-Session-ID")):
    """List accessible Notion workspaces"""
    try:
        # Ensure session exists (create if backend restarted)
        ensure_session_exists(session_id)
        
        notion_token = session_manager.get_api_key(session_id, "notion")
        if not notion_token:
            raise HTTPException(status_code=401, detail="Notion Integration Token not configured")
        
        notion_client = NotionClient(notion_token)
        workspaces = notion_client.search_workspace()
        
        return {"workspaces": workspaces.get("results", [])}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
