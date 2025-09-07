# OpenRouter API Contract

## Overview
Contract for AI model interactions via OpenRouter API.

## Endpoint: POST /chat/completions
**Purpose**: Generate Notion template structure from user requirements

**Request**:
```json
{
  "model": "string (required) - Model identifier (e.g., 'openai/gpt-4')",
  "messages": [
    {
      "role": "system",
      "content": "You are an expert at creating Notion templates. Generate complete, functional Notion workspace structures."
    },
    {
      "role": "user",
      "content": "string (required) - User's template requirements"
    }
  ],
  "temperature": 0.7,
  "max_tokens": 4000,
  "response_format": {
    "type": "json_schema",
    "json_schema": {
      "name": "notion_template",
      "schema": {
        "type": "object",
        "properties": {
          "pages": {"type": "array"},
          "databases": {"type": "array"},
          "relations": {"type": "array"},
          "views": {"type": "array"},
          "properties": {"type": "array"},
          "content": {"type": "array"}
        },
        "required": ["pages", "databases"]
      }
    }
  }
}
```

**Response**:
```json
{
  "id": "string - Completion ID",
  "object": "chat.completion",
  "created": "integer - Unix timestamp",
  "model": "string - Model used",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "string - JSON template structure"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": "integer",
    "completion_tokens": "integer",
    "total_tokens": "integer"
  }
}
```

**Error Responses**:
- 400 Bad Request: Invalid model or parameters
- 401 Unauthorized: Invalid API key
- 429 Too Many Requests: Rate limit exceeded
- 500 Internal Server Error: Model unavailable

## Endpoint: GET /models
**Purpose**: Retrieve available models for user selection

**Request**: None (API key in header)

**Response**:
```json
{
  "object": "list",
  "data": [
    {
      "id": "string - Model identifier",
      "name": "string - Human-readable name",
      "description": "string - Model description",
      "pricing": {
        "prompt": "number - Cost per token",
        "completion": "number - Cost per token"
      },
      "context_length": "integer - Max tokens"
    }
  ]
}
```

## Authentication
- Header: `Authorization: Bearer {api_key}`
- API key provided by user, stored in session only

## Rate Limits
- 50 requests per minute
- 1000 requests per hour
- Implement exponential backoff on 429 errors

## Contract Tests
- [ ] Valid API key returns model list
- [ ] Invalid API key returns 401
- [ ] Valid template request returns JSON structure
- [ ] Rate limit exceeded returns 429
- [ ] Model unavailable returns 500
