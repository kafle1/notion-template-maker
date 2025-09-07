"""
Template Preview UI Component for Notion Template Maker.
Displays generated template structure and content preview.
"""

import streamlit as st
from typing import Dict, Any, Optional, List
import json
from datetime import datetime


def render_template_preview(
    template_data: Optional[Dict[str, Any]] = None,
    on_export: Optional[callable] = None,
    on_edit: Optional[callable] = None,
) -> None:
    """
    Render the template preview component.

    Args:
        template_data: Generated template data to preview
        on_export: Callback function for export action
        on_edit: Callback function for edit action
    """
    if not template_data:
        _render_empty_preview()
        return

    st.header("👀 Template Preview")

    # Template summary
    _render_template_summary(template_data)

    st.divider()

    # Preview tabs
    tab1, tab2, tab3, tab4 = st.tabs(
        ["📄 Pages", "🗂️ Databases", "📊 Structure", "🔧 Raw Data"]
    )

    with tab1:
        _render_pages_preview(template_data.get("pages", []))

    with tab2:
        _render_databases_preview(template_data.get("databases", []))

    with tab3:
        _render_structure_preview(template_data)

    with tab4:
        _render_raw_data_preview(template_data)

    # Action buttons
    _render_preview_actions(template_data, on_export, on_edit)


def _render_empty_preview():
    """Render empty preview state."""
    st.info("🎨 No template generated yet")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
        ### 📝 What you'll see here:
        - **Pages**: Individual Notion pages with content
        - **Databases**: Structured data tables
        - **Structure**: Complete template hierarchy
        - **Raw Data**: JSON export for debugging
        """
        )

    with col2:
        st.markdown(
            """
        ### 🎯 Preview Features:
        - ✅ Live content preview
        - ✅ Structure validation
        - ✅ Export options
        - ✅ Edit capabilities
        """
        )

    st.markdown("---")
    st.caption("Generate a template to see the preview in action!")


def _render_template_summary(template_data: Dict[str, Any]):
    """Render template summary metrics."""
    metadata = template_data.get("metadata", {})

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        pages_count = len(template_data.get("pages", []))
        st.metric("📄 Pages", pages_count)

    with col2:
        databases_count = len(template_data.get("databases", []))
        st.metric("🗂️ Databases", databases_count)

    with col3:
        template_type = metadata.get("template_type", "Unknown").title()
        st.metric("🎯 Type", template_type)

    with col4:
        risk_level = metadata.get("risk_level", "Unknown")
        risk_color = {"low": "🟢", "medium": "🟡", "high": "🔴"}.get(
            risk_level.lower(), "⚪"
        )
        st.metric("⚠️ Risk", f"{risk_color} {risk_level.title()}")

    # Additional info
    if metadata.get("generated_at"):
        st.caption(f"Generated: {metadata['generated_at']}")


def _render_pages_preview(pages: List[Dict[str, Any]]):
    """Render pages preview section."""
    if not pages:
        st.info("No pages in this template")
        return

    st.subheader(f"📄 Pages ({len(pages)})")

    for i, page in enumerate(pages):
        with st.expander(f"📄 {page.get('title', f'Page {i+1}')}", expanded=(i == 0)):
            _render_single_page_preview(page, i)


def _render_single_page_preview(page: Dict[str, Any], index: int):
    """Render preview for a single page."""
    col1, col2 = st.columns([1, 2])

    with col1:
        # Page metadata
        st.markdown("**Metadata:**")
        metadata_items = []

        if page.get("icon"):
            metadata_items.append(f"Icon: {page['icon']}")
        if page.get("cover"):
            metadata_items.append(f"Cover: {page['cover']}")
        if page.get("parent"):
            metadata_items.append(f"Parent: {page['parent']}")

        if metadata_items:
            for item in metadata_items:
                st.caption(item)
        else:
            st.caption("No metadata")

    with col2:
        # Content preview
        content = page.get("content", [])
        if content:
            st.markdown("**Content Preview:**")
            _render_content_blocks_preview(content[:5])  # Show first 5 blocks

            if len(content) > 5:
                st.caption(f"... and {len(content) - 5} more blocks")
        else:
            st.caption("No content blocks")

    # Full content (expandable)
    if content:
        with st.expander("📋 Full Content", expanded=False):
            _render_content_blocks_preview(content, show_all=True)


def _render_content_blocks_preview(
    blocks: List[Dict[str, Any]], show_all: bool = False
):
    """Render preview of content blocks."""
    for i, block in enumerate(blocks):
        block_type = block.get("type", "unknown")
        block_content = block.get(block_type, {})

        # Format block preview based on type
        if block_type == "paragraph":
            text = _extract_rich_text(block_content.get("rich_text", []))
            st.markdown(f"📝 {text[:100]}{'...' if len(text) > 100 else ''}")

        elif block_type == "heading_1":
            text = _extract_rich_text(block_content.get("rich_text", []))
            st.markdown(f"# {text}")

        elif block_type == "heading_2":
            text = _extract_rich_text(block_content.get("rich_text", []))
            st.markdown(f"## {text}")

        elif block_type == "heading_3":
            text = _extract_rich_text(block_content.get("rich_text", []))
            st.markdown(f"### {text}")

        elif block_type == "bulleted_list_item":
            text = _extract_rich_text(block_content.get("rich_text", []))
            st.markdown(f"• {text}")

        elif block_type == "numbered_list_item":
            text = _extract_rich_text(block_content.get("rich_text", []))
            st.markdown(f"{i+1}. {text}")

        elif block_type == "to_do":
            text = _extract_rich_text(block_content.get("rich_text", []))
            checked = block_content.get("checked", False)
            checkbox = "☑️" if checked else "☐"
            st.markdown(f"{checkbox} {text}")

        elif block_type == "code":
            language = block_content.get("language", "text")
            code_text = _extract_rich_text(block_content.get("rich_text", []))
            st.code(
                code_text[:200] + ("..." if len(code_text) > 200 else ""),
                language=language,
            )

        elif block_type == "quote":
            text = _extract_rich_text(block_content.get("rich_text", []))
            st.markdown(f"> {text}")

        elif block_type == "callout":
            icon = block_content.get("icon", {}).get("emoji", "💡")
            text = _extract_rich_text(block_content.get("rich_text", []))
            st.markdown(f"{icon} **Callout:** {text}")

        elif block_type == "divider":
            st.markdown("---")

        elif block_type == "image":
            st.markdown("🖼️ *Image block*")

        elif block_type == "video":
            st.markdown("🎥 *Video block*")

        elif block_type == "file":
            st.markdown("📎 *File block*")

        elif block_type == "embed":
            st.markdown("🔗 *Embed block*")

        elif block_type == "bookmark":
            st.markdown("🔖 *Bookmark block*")

        elif block_type == "link_preview":
            st.markdown("🌐 *Link preview block*")

        elif block_type == "table":
            st.markdown("📊 *Table block*")

        elif block_type == "column_list":
            st.markdown("📋 *Column list block*")

        else:
            st.markdown(f"📦 *{block_type.title()} block*")

        if not show_all and i >= 4:  # Limit preview items
            break


def _render_databases_preview(databases: List[Dict[str, Any]]):
    """Render databases preview section."""
    if not databases:
        st.info("No databases in this template")
        return

    st.subheader(f"🗂️ Databases ({len(databases)})")

    for i, db in enumerate(databases):
        with st.expander(f"🗂️ {db.get('title', f'Database {i+1}')}", expanded=(i == 0)):
            _render_single_database_preview(db, i)


def _render_single_database_preview(database: Dict[str, Any], index: int):
    """Render preview for a single database."""
    col1, col2 = st.columns([1, 2])

    with col1:
        # Database metadata
        st.markdown("**Properties:**")
        properties = database.get("properties", {})

        if properties:
            for prop_name, prop_config in properties.items():
                prop_type = (
                    list(prop_config.keys())[0]
                    if isinstance(prop_config, dict)
                    else "unknown"
                )
                st.caption(f"{prop_name}: {prop_type}")
        else:
            st.caption("No properties defined")

    with col2:
        # Database info
        if database.get("description"):
            st.markdown(f"**Description:** {database['description']}")

        if database.get("icon"):
            st.markdown(f"**Icon:** {database['icon']}")

        if database.get("cover"):
            st.markdown(f"**Cover:** {database['cover']}")

    # Sample entries preview
    entries = database.get("entries", [])
    if entries:
        st.markdown("**Sample Entries:**")
        preview_entries = entries[:3]  # Show first 3 entries

        for entry in preview_entries:
            entry_title = entry.get("title", "Untitled")
            st.markdown(f"• {entry_title}")

        if len(entries) > 3:
            st.caption(f"... and {len(entries) - 3} more entries")


def _render_structure_preview(template_data: Dict[str, Any]):
    """Render template structure overview."""
    st.subheader("📊 Template Structure")

    # Create a hierarchical view
    structure_data = {
        "Template": {
            "Metadata": template_data.get("metadata", {}),
            "Pages": len(template_data.get("pages", [])),
            "Databases": len(template_data.get("databases", [])),
        }
    }

    # Add pages structure
    pages = template_data.get("pages", [])
    if pages:
        structure_data["Template"]["Pages"] = {}
        for i, page in enumerate(pages):
            page_title = page.get("title", f"Page {i+1}")
            content_count = len(page.get("content", []))
            structure_data["Template"]["Pages"][page_title] = f"{content_count} blocks"

    # Add databases structure
    databases = template_data.get("databases", [])
    if databases:
        structure_data["Template"]["Databases"] = {}
        for i, db in enumerate(databases):
            db_title = db.get("title", f"Database {i+1}")
            prop_count = len(db.get("properties", {}))
            entry_count = len(db.get("entries", []))
            structure_data["Template"]["Databases"][
                db_title
            ] = f"{prop_count} properties, {entry_count} entries"

    # Display structure as JSON
    st.json(structure_data)

    # Structure statistics
    st.markdown("### 📈 Statistics")
    col1, col2, col3 = st.columns(3)

    with col1:
        total_blocks = sum(len(page.get("content", [])) for page in pages)
        st.metric("Total Blocks", total_blocks)

    with col2:
        total_properties = sum(len(db.get("properties", {})) for db in databases)
        st.metric("Total Properties", total_properties)

    with col3:
        total_entries = sum(len(db.get("entries", [])) for db in databases)
        st.metric("Total Entries", total_entries)


def _render_raw_data_preview(template_data: Dict[str, Any]):
    """Render raw template data for debugging."""
    st.subheader("🔧 Raw Template Data")

    # JSON viewer
    st.json(template_data)

    # Download button
    json_str = json.dumps(template_data, indent=2, default=str)
    st.download_button(
        label="📥 Download JSON",
        data=json_str,
        file_name=f"template_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        mime="application/json",
        use_container_width=True,
    )


def _render_preview_actions(
    template_data: Dict[str, Any],
    on_export: Optional[callable],
    on_edit: Optional[callable],
):
    """Render action buttons for the preview."""
    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("🔄 Regenerate", use_container_width=True):
            st.rerun()

    with col2:
        if st.button("✏️ Edit Template", use_container_width=True):
            if on_edit:
                on_edit(template_data)
            else:
                st.info("Edit functionality would be implemented here")

    with col3:
        if st.button("💾 Save Locally", use_container_width=True):
            st.info("Local save functionality would be implemented here")

    with col4:
        if st.button("📤 Export to Notion", use_container_width=True):
            if on_export:
                on_export(template_data)
            else:
                st.info("Notion export functionality would be implemented here")


def _extract_rich_text(rich_text_array: List[Dict[str, Any]]) -> str:
    """
    Extract plain text from Notion rich text array.

    Args:
        rich_text_array: Array of rich text objects

    Returns:
        Plain text content
    """
    if not rich_text_array:
        return ""

    text_parts = []
    for text_obj in rich_text_array:
        if isinstance(text_obj, dict) and "plain_text" in text_obj:
            text_parts.append(text_obj["plain_text"])
        elif isinstance(text_obj, str):
            text_parts.append(text_obj)

    return "".join(text_parts)


def render_template_comparison(
    original_data: Dict[str, Any], modified_data: Dict[str, Any]
):
    """
    Render comparison between original and modified templates.

    Args:
        original_data: Original template data
        modified_data: Modified template data
    """
    st.header("🔍 Template Comparison")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📄 Original")
        _render_template_summary(original_data)

    with col2:
        st.subheader("📝 Modified")
        _render_template_summary(modified_data)

    # Show differences
    st.subheader("⚡ Changes")
    _render_template_differences(original_data, modified_data)


def _render_template_differences(original: Dict[str, Any], modified: Dict[str, Any]):
    """Render differences between templates."""
    # Simple difference detection
    orig_pages = len(original.get("pages", []))
    mod_pages = len(modified.get("pages", []))
    orig_dbs = len(original.get("databases", []))
    mod_dbs = len(modified.get("databases", []))

    changes = []

    if orig_pages != mod_pages:
        changes.append(f"Pages: {orig_pages} → {mod_pages}")
    if orig_dbs != mod_dbs:
        changes.append(f"Databases: {orig_dbs} → {mod_dbs}")

    if changes:
        for change in changes:
            st.write(f"• {change}")
    else:
        st.write("• No structural changes detected")


# Export the main function
__all__ = ["render_template_preview", "render_template_comparison"]
