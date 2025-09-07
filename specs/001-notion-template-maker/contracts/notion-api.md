# Notion API Contract

## Overview
Contract for Notion workspace integration and template import.

## Authentication: OAuth 2.0
**Purpose**: Obtain access token for user's Notion workspace

**Flow**:
1. Redirect user to Notion OAuth URL
2. User grants permissions
3. Receive authorization code
4. Exchange code for access token

**Permissions Required**:
- `pages:read`
- `pages:write`
- `databases:read`
- `databases:write`
- `users:read` (for workspace info)

## Endpoint: GET /v1/oauth/authorize
**Purpose**: Initiate OAuth flow

**Parameters**:
- `client_id`: Application client ID
- `redirect_uri`: Callback URL
- `response_type`: "code"
- `owner`: "user"
- `scope`: Space-separated permissions

**Response**: Redirect to Notion authorization page

## Endpoint: POST /v1/oauth/token
**Purpose**: Exchange authorization code for access token

**Request**:
```json
{
  "grant_type": "authorization_code",
  "code": "string - Authorization code from callback",
  "redirect_uri": "string - Must match initial redirect_uri"
}
```

**Response**:
```json
{
  "access_token": "string - Bearer token for API calls",
  "token_type": "Bearer",
  "workspace_id": "string - User's workspace ID",
  "workspace_name": "string - Workspace name",
  "owner": {
    "type": "user",
    "user": {
      "id": "string",
      "name": "string"
    }
  }
}
```

## Endpoint: POST /v1/pages
**Purpose**: Create a new page in Notion workspace

**Request Headers**:
- `Authorization: Bearer {access_token}`
- `Content-Type: application/json`
- `Notion-Version: 2022-06-28`

**Request Body**:
```json
{
  "parent": {
    "type": "workspace",
    "workspace": true
  },
  "properties": {
    "title": {
      "title": [
        {
          "text": {
            "content": "Template Name"
          }
        }
      ]
    }
  },
  "children": [
    // Page content blocks
  ]
}
```

**Response**:
```json
{
  "object": "page",
  "id": "string - New page ID",
  "created_time": "string",
  "last_edited_time": "string",
  "properties": { ... },
  "url": "string - Notion page URL"
}
```

## Endpoint: POST /v1/databases
**Purpose**: Create a new database in Notion workspace

**Request Body**:
```json
{
  "parent": {
    "type": "page_id",
    "page_id": "string - Parent page ID"
  },
  "title": [
    {
      "type": "text",
      "text": {
        "content": "Database Name"
      }
    }
  ],
  "properties": {
    "Name": {
      "title": {}
    },
    "Status": {
      "select": {
        "options": [
          {"name": "To Do", "color": "red"},
          {"name": "In Progress", "color": "yellow"},
          {"name": "Done", "color": "green"}
        ]
      }
    }
  }
}
```

**Response**:
```json
{
  "object": "database",
  "id": "string - New database ID",
  "created_time": "string",
  "last_edited_time": "string",
  "title": [ ... ],
  "properties": { ... },
  "url": "string - Database URL"
}
```

## Error Responses
- 400 Bad Request: Invalid request format
- 401 Unauthorized: Invalid or expired token
- 403 Forbidden: Insufficient permissions
- 404 Not Found: Resource doesn't exist
- 429 Too Many Requests: Rate limit exceeded

## Rate Limits
- 3 requests per second
- Implement retry with exponential backoff

## Contract Tests
- [ ] Valid OAuth flow returns access token
- [ ] Invalid token returns 401
- [ ] Create page with valid data returns page object
- [ ] Create database with properties returns database object
- [ ] Rate limit exceeded returns 429
- [ ] Insufficient permissions returns 403
