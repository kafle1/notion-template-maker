# Tasks: Notion Template Maker

**Input**: Design documents from `/specs/001-notion-template-maker/`
**Prerequisites**: plan.md (required), research.md, data-model.md, contracts/

## Execution Flow (main)
**Prerequisites**: plan.md (required), research.md, data-model.md, contracts/

## Execution Flow (main)
```
1. Load plan.md from feature directory
   → If not found: ERROR "No implementation plan found"
   → Extract: tech stack, libraries, structure
2. Load optional design documents:
   → data-model.md: Extract entities → model tasks
   → contracts/: Each file → contract test task
   → research.md: Extract decisions → setup tasks
3. Generate tasks by category:
   → Setup: project init, dependencies, linting
   → Tests: contract tests, integration tests
   → Core: models, services, CLI commands
   → Integration: DB, middleware, logging
   → Polish: unit tests, performance, docs
4. Apply task rules:
   → Different files = mark [P] for parallel
   → Same file = sequential (no [P])
   → Tests before implementation (TDD)
5. Number tasks sequentially (T001, T002...)
6. Generate dependency graph
7. Create parallel execution examples
8. Validate task completeness:
   → All contracts have tests?
   → All entities have models?
   → All endpoints implemented?
9. Return: SUCCESS (tasks ready for execution)
```

## Format: `[ID] [P?] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- Include exact file paths in descriptions

## Path Conventions
- **Web app**: `src/` at repository root with subdirectories
- Paths: `src/models/`, `src/services/`, `src/api/`, `src/ui/`, `tests/`

## Phase 3.1: Setup
- [x] T001 Create project structure per implementation plan
- [x] T002 Initialize Python project with Streamlit and dependencies
- [x] T003 [P] Configure linting and formatting tools (black, flake8)

## Phase 3.2: Tests First (TDD) ⚠️ MUST COMPLETE BEFORE 3.3
**CRITICAL: These tests MUST be written and MUST FAIL before ANY implementation**
- [x] T004 [P] Contract test OpenRouter API chat completions in tests/contract/test_openrouter_api.py
- [x] T005 [P] Contract test Notion API OAuth flow in tests/contract/test_notion_oauth.py
- [x] T006 [P] Contract test Notion API page creation in tests/contract/test_notion_pages.py
- [x] T007 [P] Contract test Notion API database creation in tests/contract/test_notion_databases.py
- [x] T008 [P] Integration test template generation flow in tests/integration/test_template_generation.py
- [x] T009 [P] Integration test Notion import flow in tests/integration/test_notion_import.py
- [x] T010 [P] Acceptance test complete user journey in tests/acceptance/test_user_journey.py

## Phase 3.3: Core Implementation (ONLY after tests are failing)
- [x] T011 [P] User model in src/models/user.py
- [x] T012 [P] Template model in src/models/template.py
- [x] T013 [P] NotionWorkspace model in src/models/notion_workspace.py
- [x] T014 [P] Database model in src/models/database.py
- [x] T015 [P] Page model in src/models/page.py
- [x] T016 [P] OpenRouter API client in src/api/openrouter_client.py
- [x] T017 [P] Notion API client in src/api/notion_client.py
- [x] T018 [P] Template generation service in src/services/template_generator.py
- [x] T019 [P] Template validation service in src/services/template_validator.py
- [x] T020 [P] Session management service in src/services/session_manager.py
- [x] T021 [P] Main Streamlit app in app.py
- [x] T022 [P] API configuration UI component in src/ui/api_config.py
- [x] T023 [P] Template input UI component in src/ui/template_input.py
- [x] T024 [P] Template preview UI component in src/ui/template_preview.py
- [x] T025 [P] Progress indicator UI component in src/ui/progress_indicator.py
- [x] T026 [P] Error handling UI component in src/ui/error_handler.py

## Phase 3.4: Integration
- [x] T027 Connect OpenRouter client to template generator
- [x] T028 Connect Notion client to import service
- [x] T029 Implement OAuth callback handling
- [x] T030 Add session state encryption
- [x] T031 Add comprehensive error handling and logging
- [x] T032 Add input validation and sanitization

## Phase 3.5: Polish
- [x] T033 [P] Unit tests for models in tests/unit/test_models.py
- [x] T034 [P] Unit tests for services in tests/unit/test_services.py
- [x] T035 [P] Unit tests for UI components in tests/unit/test_ui.py
- [x] T036 Performance optimization (<60s generation)
- [x] T037 [P] Update README.md with setup and usage
- [x] T038 [P] Create API documentation
- [x] T039 [P] Add example templates and use cases
- [x] T040 Final integration testing with quickstart scenarios
- [x] T041 Code cleanup and remove duplication
- [x] T042 Security audit and vulnerability check

## Dependencies
- Tests (T004-T010) before implementation (T011-T032)
- Models (T011-T015) before services (T016-T020)
- Services before UI components (T021-T026)
- Core implementation before integration (T027-T032)
- Everything before polish (T033-T042)

## Parallel Example
```
# Launch T004-T007 together (contract tests):
Task: "Contract test OpenRouter API chat completions in tests/contract/test_openrouter_api.py"
Task: "Contract test Notion API OAuth flow in tests/contract/test_notion_oauth.py"
Task: "Contract test Notion API page creation in tests/contract/test_notion_pages.py"
Task: "Contract test Notion API database creation in tests/contract/test_notion_databases.py"

# Launch T008-T010 together (integration tests):
Task: "Integration test template generation flow in tests/integration/test_template_generation.py"
Task: "Integration test Notion import flow in tests/integration/test_notion_import.py"
Task: "Acceptance test complete user journey in tests/acceptance/test_user_journey.py"
```

## Notes
- [P] tasks = different files, no dependencies
- Verify tests fail before implementing
- Commit after each task
- Follow TDD: Red-Green-Refactor cycle
- Ensure UI is simple, minimal, clean, modern, and beautiful
- Templates must be production-ready without modification
- Perfect customization based on user requirements

## Task Generation Rules
*Applied during main() execution*

1. **From Contracts**:
   - Each contract file → contract test task [P]
   - Each endpoint → implementation task
   
2. **From Data Model**:
   - Each entity → model creation task [P]
   - Relationships → service layer tasks
   
3. **From User Stories**:
   - Each story → integration test [P]
   - Quickstart scenarios → validation tasks

4. **Ordering**:
   - Setup → Tests → Models → Services → Endpoints → Polish
   - Dependencies block parallel execution

## Validation Checklist
*GATE: Checked by main() before returning*

- [x] All contracts have corresponding tests
- [x] All entities have model tasks
- [x] All tests come before implementation
- [x] Parallel tasks truly independent
- [x] Each task specifies exact file path
- [x] No task modifies same file as another [P] task
