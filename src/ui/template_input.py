"""
Template Input UI Component for Notion Template Maker.
Handles user input for template requirements and customization.
"""

import streamlit as st
from typing import Dict, Any, Optional, List
from datetime import datetime


def render_template_input(
    default_values: Optional[Dict[str, Any]] = None,
    on_input_change: Optional[callable] = None,
) -> Optional[Dict[str, Any]]:
    """
    Render the template input form component.

    Args:
        default_values: Default values for form fields
        on_input_change: Callback function when input changes

    Returns:
        Dictionary with user input or None if not submitted
    """
    st.header("📝 Template Requirements")

    # Initialize default values
    defaults = default_values or {}

    user_input = {}

    # Template type selection
    template_type = _render_template_type_selector(defaults.get("template_type"))
    user_input["template_type"] = template_type

    st.divider()

    # Basic information
    basic_info = _render_basic_info(defaults)
    user_input.update(basic_info)

    st.divider()

    # Template customization
    customization = _render_customization_options(defaults)
    user_input.update(customization)

    st.divider()

    # Advanced options
    advanced = _render_advanced_options(defaults)
    user_input.update(advanced)

    # Validation
    validation_result = _validate_user_input(user_input)

    # Submit section
    return _render_submit_section(user_input, validation_result, on_input_change)


def _render_template_type_selector(default_type: Optional[str] = None) -> str:
    """
    Render template type selection component.

    Args:
        default_type: Default selected template type

    Returns:
        Selected template type
    """
    st.subheader("🎯 Template Category")

    template_categories = {
        "General": ["General", "Personal", "Business"],
        "Productivity": [
            "Project Management",
            "Task Management",
            "Meeting Notes",
            "Goal Tracking",
            "Habit Tracking",
        ],
        "Knowledge": ["Knowledge Base", "Research", "Writing", "Education"],
        "Creative": ["Design", "Development", "Marketing", "Writing"],
        "Finance": ["Budget Tracking", "Finance", "Business"],
        "Health": ["Health", "Habit Tracking", "Personal"],
    }

    # Create tabs for categories
    tabs = st.tabs(list(template_categories.keys()))

    selected_type = default_type or "General"

    for i, (category, types) in enumerate(template_categories.items()):
        with tabs[i]:
            col1, col2 = st.columns([1, 2])

            with col1:
                st.markdown(f"**{category}**")
                for template_type in types:
                    if st.button(
                        template_type,
                        key=f"template_type_{template_type}",
                        use_container_width=True,
                        type="secondary"
                        if selected_type != template_type
                        else "primary",
                    ):
                        selected_type = template_type
                        st.rerun()

            with col2:
                # Show description for each type
                descriptions = _get_template_descriptions()
                for template_type in types:
                    with st.expander(f"📋 {template_type}", expanded=False):
                        st.write(
                            descriptions.get(
                                template_type, "Custom template for various purposes"
                            )
                        )

    return selected_type


def _render_basic_info(defaults: Dict[str, Any]) -> Dict[str, Any]:
    """
    Render basic template information inputs.

    Args:
        defaults: Default values

    Returns:
        Dictionary with basic information
    """
    st.subheader("📋 Basic Information")

    col1, col2 = st.columns(2)

    with col1:
        title = st.text_input(
            "Template Title *",
            value=defaults.get("title", ""),
            placeholder="e.g., My Project Dashboard",
            help="Give your template a descriptive name",
            key="template_title",
        )

    with col2:
        icon = st.text_input(
            "Icon (optional)",
            value=defaults.get("icon", ""),
            placeholder="e.g., 📊, 🚀, 📝",
            help="Choose an emoji icon for your template",
            key="template_icon",
        )

    # Description
    description = st.text_area(
        "Description *",
        value=defaults.get("description", ""),
        placeholder="Describe what this template will be used for. Be specific about features, structure, and purpose...",
        height=100,
        help="Detailed description helps generate better templates",
        key="template_description",
    )

    return {"title": title, "icon": icon, "description": description}


def _render_customization_options(defaults: Dict[str, Any]) -> Dict[str, Any]:
    """
    Render template customization options.

    Args:
        defaults: Default values

    Returns:
        Dictionary with customization options
    """
    st.subheader("🎨 Customization")

    col1, col2 = st.columns(2)

    with col1:
        # Complexity level
        complexity = st.select_slider(
            "Complexity Level",
            options=["Simple", "Medium", "Advanced"],
            value=defaults.get("complexity", "Medium"),
            help="Simple: Basic structure, Medium: Balanced features, Advanced: Full-featured",
            key="complexity_level",
        )

        # Include sample data
        include_samples = st.checkbox(
            "Include Sample Data",
            value=defaults.get("include_samples", True),
            help="Add example content to demonstrate the template",
            key="include_samples",
        )

    with col2:
        # Template style
        style = st.selectbox(
            "Visual Style",
            ["Modern", "Minimal", "Colorful", "Professional", "Creative"],
            index=["Modern", "Minimal", "Colorful", "Professional", "Creative"].index(
                defaults.get("style", "Modern")
            ),
            help="Choose the visual theme for your template",
            key="template_style",
        )

        # Color scheme
        color_scheme = st.selectbox(
            "Color Scheme",
            ["Default", "Blue", "Green", "Purple", "Orange", "Gray"],
            index=["Default", "Blue", "Green", "Purple", "Orange", "Gray"].index(
                defaults.get("color_scheme", "Default")
            ),
            help="Choose a color theme",
            key="color_scheme",
        )

    # Additional features
    st.subheader("⚡ Additional Features")
    features = _render_feature_selector(defaults.get("features", []))

    return {
        "complexity": complexity,
        "include_samples": include_samples,
        "style": style,
        "color_scheme": color_scheme,
        "features": features,
    }


def _render_feature_selector(selected_features: List[str]) -> List[str]:
    """
    Render feature selection checkboxes.

    Args:
        selected_features: List of pre-selected features

    Returns:
        List of selected features
    """
    available_features = [
        "📅 Calendar Integration",
        "📊 Progress Tracking",
        "📎 File Attachments",
        "🏷️ Tags/Categories",
        "⭐ Priority Levels",
        "📅 Due Dates",
        "📈 Status Tracking",
        "🔧 Custom Properties",
        "👥 Team Collaboration",
        "📱 Mobile Optimized",
        "🔍 Search & Filter",
        "📊 Charts & Analytics",
        "🔗 External Integrations",
        "📧 Email Notifications",
        "💾 Data Export",
        "🔄 Automation Rules",
    ]

    # Create a grid layout
    cols = st.columns(2)
    selected = []

    for i, feature in enumerate(available_features):
        col_idx = i % 2
        with cols[col_idx]:
            is_selected = feature in selected_features
            if st.checkbox(
                feature,
                value=is_selected,
                key=f"feature_{i}",
                help=f"Include {feature.lower()} functionality",
            ):
                selected.append(feature)

    return selected


def _render_advanced_options(defaults: Dict[str, Any]) -> Dict[str, Any]:
    """
    Render advanced template options.

    Args:
        defaults: Default values

    Returns:
        Dictionary with advanced options
    """
    with st.expander("⚙️ Advanced Options", expanded=False):
        col1, col2 = st.columns(2)

        with col1:
            # Database options
            include_database = st.checkbox(
                "Include Database",
                value=defaults.get("include_database", True),
                help="Create a Notion database for structured data",
                key="include_database",
            )

            max_pages = st.number_input(
                "Maximum Pages",
                min_value=1,
                max_value=50,
                value=defaults.get("max_pages", 10),
                help="Maximum number of pages to generate",
                key="max_pages",
            )

        with col2:
            # Content options
            include_cover = st.checkbox(
                "Include Cover Images",
                value=defaults.get("include_cover", True),
                help="Add cover images to pages",
                key="include_cover",
            )

            language = st.selectbox(
                "Content Language",
                ["English", "Spanish", "French", "German", "Chinese", "Japanese"],
                index=0,
                help="Language for generated content",
                key="content_language",
            )

        # Custom properties
        st.subheader("🔧 Custom Properties")
        custom_properties = _render_custom_properties_editor(
            defaults.get("custom_properties", {})
        )

        return {
            "include_database": include_database,
            "max_pages": max_pages,
            "include_cover": include_cover,
            "language": language,
            "custom_properties": custom_properties,
        }

    # Return defaults if expander is collapsed
    return {
        "include_database": defaults.get("include_database", True),
        "max_pages": defaults.get("max_pages", 10),
        "include_cover": defaults.get("include_cover", True),
        "language": defaults.get("language", "English"),
        "custom_properties": defaults.get("custom_properties", {}),
    }


def _render_custom_properties_editor(
    existing_properties: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Render custom properties editor.

    Args:
        existing_properties: Existing custom properties

    Returns:
        Dictionary with custom properties
    """
    st.write("Add custom database properties:")

    # Display existing properties
    properties = dict(existing_properties)

    # Add new property form
    with st.form("add_property_form"):
        col1, col2, col3 = st.columns([2, 2, 1])

        with col1:
            prop_name = st.text_input("Property Name", key="new_prop_name")

        with col2:
            prop_type = st.selectbox(
                "Type",
                ["text", "number", "select", "checkbox", "date", "person"],
                key="new_prop_type",
            )

        with col3:
            add_property = st.form_submit_button("Add", use_container_width=True)

        if add_property and prop_name.strip():
            properties[prop_name.strip()] = prop_type
            st.rerun()

    # Display current properties
    if properties:
        st.write("**Current Properties:**")
        for prop_name, prop_type in list(properties.items()):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"{prop_name} ({prop_type})")
            with col2:
                if st.button("❌", key=f"remove_{prop_name}"):
                    del properties[prop_name]
                    st.rerun()

    return properties


def _validate_user_input(user_input: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate user input.

    Args:
        user_input: User input dictionary

    Returns:
        Validation result dictionary
    """
    errors = []
    warnings = []

    # Required fields
    if not user_input.get("title", "").strip():
        errors.append("Template title is required")

    if not user_input.get("description", "").strip():
        errors.append("Template description is required")

    # Title length
    if len(user_input.get("title", "")) > 100:
        errors.append("Title must be 100 characters or less")

    # Description length
    if len(user_input.get("description", "")) > 1000:
        warnings.append("Description is quite long, consider making it more concise")

    # Custom properties validation
    custom_props = user_input.get("custom_properties", {})
    if len(custom_props) > 20:
        warnings.append("Many custom properties may make the template complex")

    return {"valid": len(errors) == 0, "errors": errors, "warnings": warnings}


def _render_submit_section(
    user_input: Dict[str, Any],
    validation: Dict[str, Any],
    on_input_change: Optional[callable],
) -> Optional[Dict[str, Any]]:
    """
    Render the submit section with validation feedback.

    Args:
        user_input: User input dictionary
        validation: Validation result
        on_input_change: Callback function

    Returns:
        User input if submitted, None otherwise
    """
    # Show validation messages
    if validation["errors"]:
        for error in validation["errors"]:
            st.error(f"❌ {error}")

    if validation["warnings"]:
        for warning in validation["warnings"]:
            st.warning(f"⚠️ {warning}")

    # Submit button
    col1, col2 = st.columns([1, 1])

    with col1:
        submitted = st.button(
            "🚀 Generate Template",
            type="primary",
            use_container_width=True,
            disabled=not validation["valid"],
            key="generate_template_btn",
        )

    with col2:
        preview = st.button(
            "👀 Preview",
            use_container_width=True,
            disabled=not validation["valid"],
            key="preview_template_btn",
        )

    if submitted and validation["valid"]:
        # Call callback if provided
        if on_input_change:
            on_input_change(user_input)

        return user_input

    if preview and validation["valid"]:
        st.info("Preview functionality would be implemented here")
        return None

    return None


def _get_template_descriptions() -> Dict[str, Any]:
    """
    Get template type descriptions.

    Returns:
        Dictionary mapping template types to descriptions
    """
    return {
        "General": "Versatile template for various purposes and use cases",
        "Personal": "Templates for personal organization and productivity",
        "Business": "Professional templates for business and work management",
        "Project Management": "Comprehensive project planning and tracking",
        "Task Management": "Simple and effective task organization",
        "Meeting Notes": "Structured note-taking for meetings and discussions",
        "Goal Tracking": "Monitor progress towards personal and professional goals",
        "Habit Tracking": "Build and maintain positive habits and routines",
        "Knowledge Base": "Organize and manage information and documentation",
        "Research": "Academic and professional research organization",
        "Writing": "Content creation and writing project management",
        "Education": "Learning materials and educational content",
        "Design": "Creative project management and design workflows",
        "Development": "Software development and coding project templates",
        "Marketing": "Marketing campaign planning and content creation",
        "Budget Tracking": "Financial planning and expense management",
        "Health": "Health and wellness tracking and management",
        "Finance": "Financial planning, budgeting, and investment tracking",
    }


# Export the main function
__all__ = ["render_template_input"]
