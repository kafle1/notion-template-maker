"""
Notion Template Maker - Main Streamlit Application
A beautiful, simple app for generating customized Notion templates using AI.
"""

import streamlit as st
import json
from typing import Dict, Any, Optional
from datetime import datetime

# Import our services and models
from src.services.session_manager import SessionManager
from src.services.template_generator import TemplateGenerator
from src.services.template_validator import TemplateValidator
from src.services.notion_import_service import NotionImportService
from src.services.notion_oauth_service import NotionOAuthService
from src.services.logging_service import get_logger
from src.services.error_handler import get_error_handler, handle_errors
from src.api.notion_client import NotionClient
from src.api.openrouter_client import OpenRouterClient
from src.models.template import Template
from src.models.user import User
from src.utils.input_validator import InputValidator

# Configure page
st.set_page_config(
    page_title="Notion Template Maker",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Initialize services
@st.cache_resource
def get_services():
    """Initialize and cache service instances."""
    return {
        "session_manager": SessionManager(),
        "template_generator": TemplateGenerator(),
        "template_validator": TemplateValidator(),
        "notion_import_service": NotionImportService(),
        "notion_oauth_service": None,  # Will be initialized with OAuth credentials
        "notion_client": None,  # Will be initialized with API key
        "openrouter_client": None,  # Will be initialized with API key
    }


def initialize_clients_with_api_keys(services: Dict[str, Any]) -> Dict[str, Any]:
    """Initialize API clients with stored API keys and OAuth data."""
    if not st.session_state.session_id:
        return services

    session_manager = services["session_manager"]

    # Initialize OpenRouter client if API key is available
    openrouter_key = session_manager.get_api_key(
        st.session_state.session_id, "openrouter"
    )
    if openrouter_key and not services["openrouter_client"]:
        services["openrouter_client"] = OpenRouterClient(openrouter_key)

    # Initialize Notion client if API key is available (manual)
    notion_key = session_manager.get_api_key(st.session_state.session_id, "notion")
    if notion_key and not services["notion_client"]:
        services["notion_client"] = NotionClient(notion_key)

    # Initialize Notion client from OAuth data if available
    if not services["notion_client"]:
        oauth_data = session_manager.get_oauth_data(st.session_state.session_id)
        if oauth_data:
            try:
                services["notion_client"] = NotionClient.from_oauth_token_data(
                    oauth_data
                )
            except Exception as e:
                st.warning(f"Failed to initialize Notion client from OAuth data: {e}")

    # Connect clients to template generator
    if services["openrouter_client"] and services["notion_client"]:
        services["template_generator"].set_clients(
            services["openrouter_client"], services["notion_client"]
        )

        # Connect Notion client to import service
        services["notion_import_service"].set_client(services["notion_client"])

    return services


def main():
    """Main application entry point."""
    # Initialize logging and error handling
    logger = get_logger("notion-template-maker")
    error_handler = get_error_handler()

    logger.info("Application started")

    try:
        services = get_services()

        # Initialize session state
        if "session_id" not in st.session_state:
            st.session_state.session_id = None
        if "generated_template" not in st.session_state:
            st.session_state.generated_template = None
        if "generation_status" not in st.session_state:
            st.session_state.generation_status = None
        if "oauth_state" not in st.session_state:
            st.session_state.oauth_state = None
        if "oauth_code_verifier" not in st.session_state:
            st.session_state.oauth_code_verifier = None

        # Handle OAuth callback if present
        handle_oauth_callback(services)

        # Validate session security
        validate_session_security(services)

        # Initialize clients with API keys from session
        services = initialize_clients_with_api_keys(services)

        # Header
        st.title("📝 Notion Template Maker")
        st.markdown("*Create beautiful, customized Notion templates with AI*")

        # Sidebar - API Configuration
        render_sidebar(services)

        # Main content
        if not is_api_configured(services):
            render_welcome_screen()
            return

        # Template creation workflow
        render_main_content(services)

    except Exception as e:
        error_handler.handle_error(e, {"component": "main"})
        st.error("🚨 A critical error occurred. Please refresh the page and try again.")
        logger.critical(f"Critical error in main: {e}")

    logger.info("Application session ended")


def render_sidebar(services: Dict[str, Any]):
    """Render the sidebar with API configuration."""
    with st.sidebar:
        st.header("🔧 API Configuration")

        # OpenRouter API Key
        openrouter_key = st.text_input(
            "OpenRouter API Key",
            type="password",
            help="Get your API key from https://openrouter.ai/keys",
        )

        # Notion Integration
        st.subheader("Notion Integration")

        # OAuth configuration
        notion_client_id = st.text_input(
            "Notion OAuth Client ID",
            type="password",
            help="Get from https://developers.notion.com/",
        )

        notion_client_secret = st.text_input(
            "Notion OAuth Client Secret",
            type="password",
            help="Get from https://developers.notion.com/",
        )

        if notion_client_id and notion_client_secret:
            # Initialize OAuth service
            if not services["notion_oauth_service"]:
                services["notion_oauth_service"] = NotionOAuthService(
                    notion_client_id,
                    notion_client_secret,
                    "http://localhost:8501",  # Default redirect URI
                )

            if st.button(
                "🔗 Connect with Notion OAuth", type="primary", use_container_width=True
            ):
                initiate_notion_oauth(services)
        else:
            st.info(
                "Enter your Notion OAuth credentials above to enable OAuth integration"
            )

        # Manual API key fallback
        st.divider()
        st.markdown("**Alternative: Manual API Key**")
        notion_api_key = st.text_input(
            "Notion API Key (Manual)",
            type="password",
            help="Get from https://www.notion.so/my-integrations",
        )

        if notion_api_key:
            services["notion_client"] = NotionClient(notion_api_key)
            st.success("✅ Notion client initialized with manual API key")

        # Store manual API key if provided
        if notion_api_key and st.session_state.session_id:
            services["session_manager"].store_api_key(
                st.session_state.session_id, "notion", notion_api_key
            )

        # Session management
        st.divider()
        if st.session_state.session_id:
            st.success("✅ Session active")
            if st.button("🔄 New Session"):
                st.session_state.session_id = None
                st.session_state.generated_template = None
                st.rerun()
        else:
            if st.button("🚀 Start Session"):
                session_id = services["session_manager"].create_session("user_123")
                st.session_state.session_id = session_id
                st.rerun()

        # Store API keys if provided
        if openrouter_key and st.session_state.session_id:
            services["session_manager"].store_api_key(
                st.session_state.session_id, "openrouter", openrouter_key
            )


def is_api_configured(services: Dict[str, Any]) -> bool:
    """Check if required APIs are configured."""
    if not st.session_state.session_id:
        return False

    # Check if clients are properly initialized
    return (
        services.get("openrouter_client") is not None
        and services.get("notion_client") is not None
    )


def render_welcome_screen():
    """Render the welcome screen for new users."""
    st.info("👋 Welcome to Notion Template Maker!")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🚀 Getting Started")
        st.markdown(
            """
        1. Configure your OpenRouter API key in the sidebar
        2. Start a new session
        3. Describe your template requirements
        4. Generate and preview your template
        5. Import to Notion (coming soon)
        """
        )

    with col2:
        st.subheader("✨ Features")
        st.markdown(
            """
        - 🤖 AI-powered template generation
        - 📝 Customizable content blocks
        - 🗂️ Database creation
        - 🎨 Beautiful, modern design
        - 🔒 Secure session management
        - 📱 Mobile-friendly interface
        """
        )

    st.divider()
    st.markdown("### 📋 Example Templates")
    examples = [
        "Project Management Dashboard",
        "Personal Knowledge Base",
        "Meeting Notes Template",
        "Habit Tracker",
        "Reading List Manager",
    ]

    for example in examples:
        if st.button(f"Try: {example}", key=f"example_{example}"):
            st.session_state.template_description = (
                f"Create a {example.lower()} template"
            )
            st.rerun()


def render_main_content(services: Dict[str, Any]):
    """Render the main template creation interface."""
    st.header("🎯 Create Your Template")

    # Template input form
    with st.form("template_form"):
        col1, col2 = st.columns([2, 1])

        with col1:
            template_type = st.selectbox(
                "Template Type",
                [
                    "General",
                    "Project Management",
                    "Knowledge Base",
                    "Personal",
                    "Business",
                    "Education",
                    "Health",
                    "Finance",
                    "Marketing",
                    "Development",
                    "Design",
                    "Writing",
                    "Research",
                    "Meeting Notes",
                    "Task Management",
                    "Goal Tracking",
                    "Habit Tracking",
                    "Budget Tracking",
                ],
                help="Choose the category that best fits your template",
            )

            title = st.text_input(
                "Template Title",
                placeholder="e.g., My Project Dashboard",
                help="Give your template a descriptive name",
            )

            description = st.text_area(
                "Description",
                placeholder="Describe what this template will be used for...",
                height=100,
                help="Be specific about features, structure, and purpose",
            )

        with col2:
            st.subheader("🎨 Customization")

            include_database = st.checkbox("Include Database", value=True)
            include_pages = st.checkbox("Include Sample Pages", value=True)

            complexity = st.select_slider(
                "Complexity Level",
                options=["Simple", "Medium", "Advanced"],
                value="Medium",
            )

            features = st.multiselect(
                "Additional Features",
                [
                    "Calendar Integration",
                    "Progress Tracking",
                    "File Attachments",
                    "Tags/Categories",
                    "Priority Levels",
                    "Due Dates",
                    "Status Tracking",
                    "Custom Properties",
                ],
                help="Select any additional features you want",
            )

        # Submit button
        submitted = st.form_submit_button(
            "🚀 Generate Template", type="primary", use_container_width=True
        )

    # Template generation
    if submitted:
        if not title.strip():
            st.error("Please provide a template title")
            return

        if not description.strip():
            st.error("Please provide a template description")
            return

        generate_template(
            services,
            {
                "template_type": template_type.lower().replace(" ", "_"),
                "title": title.strip(),
                "description": description.strip(),
                "include_database": include_database,
                "include_pages": include_pages,
                "complexity": complexity.lower(),
                "features": features,
            },
        )

    # Template preview
    if st.session_state.generated_template:
        render_template_preview(services)


def generate_template(services: Dict[str, Any], user_input: Dict[str, Any]):
    """Generate a template based on user input."""
    logger = get_logger()
    error_handler = get_error_handler()

    with error_handler.error_boundary(
        "template_generation", {"user_input": user_input}
    ):
        logger.log_user_action("template_generation_started", **user_input)

        # Validate input
        validator = services["template_validator"]
        errors = validator.validate_user_input(user_input)

        if errors:
            for error in errors:
                st.error(error)
                logger.warning(f"Template validation failed: {error}")
            return

        with st.spinner("🤖 Analyzing your requirements..."):
            logger.info("Starting template analysis")

        with st.spinner("🎨 Generating your custom template..."):
            start_time = datetime.now()

            # Generate template
            generator = services["template_generator"]
            template_data = generator.generate_template(user_input)

            generation_time = (datetime.now() - start_time).total_seconds()
            logger.log_performance("template_generation", generation_time, user_input)

            # Validate generated template
            validation_errors = validator.validate_template_data(template_data)
            if validation_errors:
                st.warning("Template generated with some issues:")
                for error in validation_errors:
                    st.warning(error)
                    logger.warning(f"Template validation issue: {error}")

        # Store in session
        st.session_state.generated_template = template_data
        st.session_state.generation_status = "success"

        logger.log_user_action(
            "template_generation_completed",
            template_pages=len(template_data.get("pages", [])),
            template_databases=len(template_data.get("databases", [])),
        )

        st.success("✅ Template generated successfully!")
        st.rerun()


def validate_session_security(services: Dict[str, Any]):
    """Validate session security and handle any security issues."""
    if not st.session_state.session_id:
        return

    session_manager = services["session_manager"]

    # Check if session is still valid
    session_data = session_manager.get_session(st.session_state.session_id)
    if not session_data:
        # Session expired or invalid
        st.session_state.session_id = None
        st.session_state.generated_template = None
        st.session_state.oauth_state = None
        st.session_state.oauth_code_verifier = None
        st.warning("Your session has expired. Please start a new session.")
        st.rerun()

    # Validate encryption
    encryption_info = session_manager.get_encryption_info()
    if not encryption_info.get("key_valid", False):
        st.error("Session encryption is compromised. Please restart the application.")
        st.stop()


def initiate_notion_oauth(services: Dict[str, Any]):
    """Initiate Notion OAuth flow."""
    if not services["notion_oauth_service"]:
        st.error("OAuth service not configured")
        return

    try:
        # Generate OAuth URL
        auth_url, state, code_verifier = services[
            "notion_oauth_service"
        ].get_authorization_url()

        # Store state and code verifier in session
        st.session_state.oauth_state = state
        st.session_state.oauth_code_verifier = code_verifier

        # Redirect to Notion OAuth
        st.markdown(
            f"""
        <meta http-equiv="refresh" content="0; url={auth_url}">
        """,
            unsafe_allow_html=True,
        )

        st.info("🔄 Redirecting to Notion for authentication...")

    except Exception as e:
        st.error(f"Failed to initiate OAuth: {str(e)}")


def handle_oauth_callback(services: Dict[str, Any]):
    """Handle OAuth callback from Notion."""
    logger = get_logger()
    error_handler = get_error_handler()

    # Get URL parameters
    query_params = st.query_params

    # Check if this is an OAuth callback
    if "code" in query_params and "state" in query_params:
        with error_handler.error_boundary("oauth_callback"):
            logger.info("OAuth callback received")

            try:
                # Validate state parameter
                callback_state = query_params["state"]
                if callback_state != st.session_state.oauth_state:
                    raise ValueError("OAuth state mismatch - possible CSRF attack")

                # Get OAuth service
                if not services["notion_oauth_service"]:
                    raise ValueError("OAuth service not configured")

                # Exchange code for token
                with st.spinner("🔄 Completing OAuth authentication..."):
                    token_data = services["notion_oauth_service"].handle_oauth_callback(
                        st.get_option("server.headless")
                        or f"http://localhost:8501?{st.query_params}",
                        st.session_state.oauth_state,
                        st.session_state.oauth_code_verifier,
                    )

                    # Create Notion client from token
                    services["notion_client"] = NotionClient.from_oauth_token_data(
                        token_data
                    )

                    # Store token data in session
                    if st.session_state.session_id:
                        services["session_manager"].store_oauth_data(
                            st.session_state.session_id, token_data
                        )

                    # Clear OAuth state
                    st.session_state.oauth_state = None
                    st.session_state.oauth_code_verifier = None

                    # Clear URL parameters
                    st.query_params.clear()

                    logger.log_user_action(
                        "oauth_completed", workspace_id=token_data.get("workspace_id")
                    )
                    st.success("✅ Successfully connected to Notion!")
                    st.rerun()

            except Exception as e:
                error_handler.handle_error(e, {"operation": "oauth_callback"})
                # Clear OAuth state on error
                st.session_state.oauth_state = None
                st.session_state.oauth_code_verifier = None


def import_template_to_notion(services: Dict[str, Any]):
    """Import the generated template to Notion."""
    logger = get_logger()
    error_handler = get_error_handler()

    if not st.session_state.generated_template:
        st.error("No template to import")
        return

    with error_handler.error_boundary(
        "notion_import",
        {
            "template_type": st.session_state.generated_template.get(
                "metadata", {}
            ).get("template_type")
        },
    ):
        logger.log_user_action("notion_import_started")

        try:
            # Get the import service
            import_service = services["notion_import_service"]

            # Validate the template data
            template_data = st.session_state.generated_template
            validation_errors = import_service.validate_import_data(template_data)

            if validation_errors:
                st.error("Template validation failed:")
                for error in validation_errors:
                    st.error(f"• {error}")
                    logger.error(f"Template validation error: {error}")
                return

            with st.spinner("📤 Importing template to Notion..."):
                start_time = datetime.now()

                # Perform the import
                import_result = import_service.import_template(template_data)

                import_time = (datetime.now() - start_time).total_seconds()
                logger.log_performance("notion_import", import_time)

                # Show results
                if import_result["success"]:
                    st.success(import_service.get_import_status(import_result))

                    # Show details of what was imported
                    if import_result.get("created_pages"):
                        st.info(
                            f"📄 Created {len(import_result['created_pages'])} pages"
                        )
                        for page in import_result["created_pages"][:5]:  # Show first 5
                            st.write(f"• [{page['title']}]({page['url']})")

                    if import_result.get("created_databases"):
                        st.info(
                            f"🗂️ Created {len(import_result['created_databases'])} databases"
                        )
                        for db in import_result["created_databases"][
                            :5
                        ]:  # Show first 5
                            st.write(f"• [{db['title']}]({db['url']})")

                    logger.log_user_action(
                        "notion_import_completed",
                        pages_created=len(import_result.get("created_pages", [])),
                        databases_created=len(
                            import_result.get("created_databases", [])
                        ),
                    )

                    # Option to view in Notion
                    if st.button("🔗 Open in Notion", type="secondary"):
                        if import_result.get("created_pages"):
                            st.markdown(
                                f"[Open First Page]({import_result['created_pages'][0]['url']})"
                            )
                        elif import_result.get("created_databases"):
                            st.markdown(
                                f"[Open First Database]({import_result['created_databases'][0]['url']})"
                            )

                else:
                    st.error("Import failed:")
                    for error in import_result.get("errors", []):
                        st.error(f"• {error}")
                        logger.error(f"Notion import error: {error}")

        except Exception as e:
            error_handler.handle_error(e, {"operation": "notion_import"})
            st.error(f"❌ Import failed: {str(e)}")


def render_template_preview(services: Dict[str, Any]):
    """Render the generated template preview."""
    if not st.session_state.generated_template:
        return

    st.header("👀 Template Preview")

    template_data = st.session_state.generated_template
    metadata = template_data.get("metadata", {})

    # Template info
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Template Type", metadata.get("template_type", "Unknown").title())
    with col2:
        st.metric("Pages", len(template_data.get("pages", [])))
    with col3:
        st.metric("Databases", len(template_data.get("databases", [])))

    # Preview tabs
    tab1, tab2, tab3 = st.tabs(["📄 Pages", "🗂️ Databases", "📋 Summary"])

    with tab1:
        render_pages_preview(template_data.get("pages", []))

    with tab2:
        render_databases_preview(template_data.get("databases", []))

    with tab3:
        render_template_summary(template_data)

    # Action buttons
    st.divider()
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🔄 Regenerate", use_container_width=True):
            st.session_state.generated_template = None
            st.rerun()

    with col2:
        if st.button("💾 Save Template", use_container_width=True):
            st.info("Template saving would be implemented here")

    with col3:
        if st.button("📤 Import to Notion", use_container_width=True):
            import_template_to_notion(services)


def render_pages_preview(pages: list):
    """Render preview of generated pages."""
    if not pages:
        st.info("No pages generated")
        return

    for i, page in enumerate(pages):
        with st.expander(f"📄 {page.get('title', f'Page {i+1}')}"):
            st.write(f"**Content blocks:** {len(page.get('content', []))}")

            if page.get("icon"):
                st.write(f"**Icon:** {page['icon']}")
            if page.get("cover"):
                st.write(f"**Cover:** {page['cover']}")

            # Show first few content blocks
            content = page.get("content", [])
            if content:
                st.write("**Sample content:**")
                for j, block in enumerate(content[:3]):
                    block_type = block.get("type", "unknown")
                    st.write(f"- {block_type.title()} block")


def render_databases_preview(databases: list):
    """Render preview of generated databases."""
    if not databases:
        st.info("No databases generated")
        return

    for i, db in enumerate(databases):
        with st.expander(f"🗂️ {db.get('title', f'Database {i+1}')}"):
            st.write(f"**Properties:** {len(db.get('properties', {}))}")

            if db.get("description"):
                st.write(f"**Description:** {db['description']}")

            # Show properties
            properties = db.get("properties", {})
            if properties:
                st.write("**Database properties:**")
                for prop_name, prop_config in properties.items():
                    prop_type = (
                        list(prop_config.keys())[0] if prop_config else "unknown"
                    )
                    st.write(f"- {prop_name}: {prop_type}")


def render_template_summary(template_data: Dict[str, Any]):
    """Render a summary of the generated template."""
    metadata = template_data.get("metadata", {})

    st.subheader("📊 Template Summary")

    summary_data = {
        "Generated At": metadata.get("generated_at", "Unknown"),
        "Template Type": metadata.get("template_type", "Unknown").title(),
        "Risk Level": metadata.get("risk_level", "Unknown"),
        "Total Pages": len(template_data.get("pages", [])),
        "Total Databases": len(template_data.get("databases", [])),
    }

    for key, value in summary_data.items():
        st.write(f"**{key}:** {value}")

    # Show raw JSON for debugging
    with st.expander("🔧 Raw Template Data (Debug)"):
        st.json(template_data)


if __name__ == "__main__":
    main()

from src.ui.api_config import render_api_config
from src.ui.template_input import render_template_input
from src.ui.template_preview import render_template_preview
from src.ui.progress_indicator import render_progress
from src.ui.error_handler import handle_error
from src.services.session_manager import SessionManager

# Initialize session manager
session_manager = SessionManager()
