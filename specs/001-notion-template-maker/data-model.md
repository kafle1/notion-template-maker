# Data Model: Notion Template Maker

## Overview
The application manages template generation and Notion integration with the following core entities.

## Entity: User
**Purpose**: Represents the application user and their session state

**Fields**:
- `openrouter_api_key`: str (required) - User's OpenRouter API key
- `notion_token`: str (optional) - OAuth access token for Notion
- `selected_model`: str (required) - Chosen AI model (e.g., "gpt-4", "claude-3")
- `session_id`: str (auto-generated) - Unique session identifier

**Validation Rules**:
- API key must be non-empty and valid format
- Model must be one of supported OpenRouter models
- Token must be valid OAuth token when present

**Relationships**:
- 1:1 with Template (user generates templates)

## Entity: Template
**Purpose**: Represents a generated Notion template structure

**Fields**:
- `id`: str (auto-generated) - Unique template identifier
- `name`: str (required) - Template name from user requirements
- `description`: str (optional) - Template description
- `structure`: dict (required) - Complete Notion JSON structure
- `created_at`: datetime (auto-generated) - Creation timestamp
- `complexity_level`: str (auto-generated) - AI-determined complexity (simple/medium/complex)
- `size_bytes`: int (auto-generated) - JSON size in bytes

**Validation Rules**:
- Structure must be valid Notion API JSON
- Size must be < 5MB
- Name must be non-empty

**Relationships**:
- Belongs to User
- Contains multiple Databases and Pages

## Entity: NotionWorkspace
**Purpose**: Represents user's Notion workspace for import operations

**Fields**:
- `id`: str (required) - Notion workspace ID
- `name`: str (required) - Workspace name
- `access_token`: str (required) - OAuth access token
- `permissions`: list (auto-generated) - Granted permissions

**Validation Rules**:
- ID must be valid Notion workspace ID
- Token must be valid and not expired
- Permissions must include page creation rights

**Relationships**:
- Referenced by Template during import

## Entity: Database
**Purpose**: Represents Notion databases within templates

**Fields**:
- `id`: str (auto-generated) - Unique database identifier
- `name`: str (required) - Database name
- `properties`: dict (required) - Database property definitions
- `views`: list (optional) - Database view configurations

**Validation Rules**:
- Properties must include at least one property
- Name must be non-empty

**Relationships**:
- Belongs to Template
- Can have Relations to other Databases

## Entity: Page
**Purpose**: Represents Notion pages within templates

**Fields**:
- `id`: str (auto-generated) - Unique page identifier
- `title`: str (required) - Page title
- `content`: list (optional) - Page content blocks
- `parent_id`: str (optional) - Parent page/database ID

**Validation Rules**:
- Title must be non-empty
- Content must be valid Notion block format

**Relationships**:
- Belongs to Template
- Can be child of Database or other Page

## Entity Relationships Diagram
```
User
├── Templates (1:N)
    ├── Databases (1:N)
    │   ├── Properties (1:N)
    │   └── Views (1:N)
    └── Pages (1:N)
        ├── Content Blocks (1:N)
        └── Child Pages (1:N)

NotionWorkspace
└── Imported Templates (1:N)
```

## State Transitions
**Template Generation States**:
1. `draft` → User provides requirements
2. `generating` → AI processing requirements
3. `ready` → Template structure complete
4. `previewed` → User has reviewed template
5. `importing` → Template being imported to Notion
6. `imported` → Successfully imported
7. `failed` → Import or generation failed

**User Session States**:
1. `unauthenticated` → No API keys provided
2. `api_ready` → OpenRouter key provided
3. `notion_ready` → Notion OAuth completed
4. `ready` → Both APIs configured

## Data Flow
1. User inputs requirements → Template entity created
2. AI generates structure → Template updated with JSON
3. User reviews → Template marked as previewed
4. User imports → NotionWorkspace used for API calls
5. Success/failure → Template state updated
