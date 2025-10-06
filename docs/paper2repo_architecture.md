# Paper2Repo System Architecture

## Overview
Paper2Repo converts ML research papers into runnable, provenance-linked repositories in <10 minutes with >60% success rate.

## System Architecture

### Core Pipeline
```
PDF Upload → Parser → Planner → Generator → Verifier → Export
     ↓         ↓        ↓         ↓         ↓        ↓
  Storage   Embeddings Structure  Code    Tests   Repo
```

### Tech Stack
- **Backend**: Python FastAPI
- **Frontend**: React with WebSocket for real-time updates
- **Database**: PostgreSQL for metadata, Redis for caching
- **Storage**: S3-compatible object storage
- **Containers**: Docker for sandboxed execution
- **LLM**: OpenAI/Anthropic APIs with fallback models

## Core Services

### 1. PDF Processing Service
```python
class PDFProcessor:
    def parse_paper(self, pdf_path: str) -> PaperStructure:
        # Extract title, abstract, methods, equations, captions
        # Generate document outline
        # Create embeddings for retrieval
        pass
    
    def extract_sections(self, content: str) -> Dict[str, str]:
        # Identify methods, pseudocode, equations
        pass
```

### 2. Planning Service
```python
class RepoPlanner:
    def generate_structure(self, paper: PaperStructure) -> RepoStructure:
        # Infer module structure (model.py, train.py, data.py)
        # Map paper sections to modules
        pass
    
    def create_module_plan(self, section: str, context: str) -> ModulePlan:
        # Per-module generation plan with provenance
        pass
```

### 3. Code Generation Service
```python
class CodeGenerator:
    def generate_module(self, plan: ModulePlan, context: str) -> GeneratedCode:
        # Generate code with source-cited docstrings
        # Track provenance links
        pass
    
    def generate_tests(self, module: GeneratedCode) -> TestSuite:
        # Create smoke tests (imports, forward passes)
        pass
```

### 4. Verification Service
```python
class CodeVerifier:
    def run_in_sandbox(self, code: str) -> ExecutionResult:
        # Execute in ephemeral container
        # Capture logs, errors, pass/fail status
        pass
    
    def analyze_errors(self, error: str, context: str) -> ErrorAnalysis:
        # Map errors to paper sections
        # Suggest fixes
        pass
```

### 5. Provenance Service
```python
class ProvenanceTracker:
    def link_code_to_source(self, code_line: int, paper_section: str):
        # Bidirectional linking
        pass
    
    def get_source_context(self, code_block: str) -> List[PaperSection]:
        # Return originating paper sections
        pass
```

## Database Schema

### Core Tables
```sql
-- Papers and processing runs
CREATE TABLE papers (
    id UUID PRIMARY KEY,
    title TEXT,
    arxiv_id TEXT,
    pdf_path TEXT,
    created_at TIMESTAMP
);

CREATE TABLE processing_runs (
    id UUID PRIMARY KEY,
    paper_id UUID REFERENCES papers(id),
    status TEXT, -- parsing, planning, generating, verifying, complete
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    success_rate FLOAT
);

-- Generated code and provenance
CREATE TABLE generated_modules (
    id UUID PRIMARY KEY,
    run_id UUID REFERENCES processing_runs(id),
    module_name TEXT,
    code TEXT,
    test_results JSONB,
    compile_success BOOLEAN
);

CREATE TABLE provenance_links (
    id UUID PRIMARY KEY,
    module_id UUID REFERENCES generated_modules(id),
    paper_section TEXT,
    code_line_start INT,
    code_line_end INT,
    confidence FLOAT
);

-- Metrics tracking
CREATE TABLE user_interactions (
    id UUID PRIMARY KEY,
    run_id UUID REFERENCES processing_runs(id),
    action TEXT, -- click_provenance, regenerate_module, fix_with_context
    timestamp TIMESTAMP,
    context JSONB
);
```

## API Design

### REST Endpoints
```python
# Upload and processing
POST /api/papers/upload
POST /api/papers/from-arxiv/{arxiv_id}
GET /api/runs/{run_id}/status
GET /api/runs/{run_id}/progress

# Code generation
POST /api/runs/{run_id}/generate
POST /api/runs/{run_id}/modules/{module_name}/regenerate
POST /api/runs/{run_id}/fix-with-context

# Verification
POST /api/runs/{run_id}/verify
GET /api/runs/{run_id}/test-results

# Export
GET /api/runs/{run_id}/download
GET /api/runs/{run_id}/readme

# Provenance
GET /api/modules/{module_id}/provenance
GET /api/provenance/code-to-source
GET /api/provenance/source-to-code
```

### WebSocket Events
```python
# Real-time updates
{
    "type": "parsing_progress",
    "progress": 45,
    "current_section": "Methods"
}

{
    "type": "module_generated",
    "module": "model.py",
    "status": "success",
    "provenance_count": 12
}

{
    "type": "test_result",
    "module": "train.py",
    "passed": false,
    "error": "Missing hyperparameter: learning_rate",
    "suggested_fix": "Add lr=0.001 to optimizer"
}
```

## Frontend Architecture

### Component Structure
```
App/
├── Layout/
│   ├── SourcePanel/          # PDF viewer with highlighting
│   ├── ActionPanel/          # Upload, logs, controls
│   └── CodePanel/            # File explorer, editor
├── Components/
│   ├── ProvenanceLink/       # Bidirectional linking
│   ├── ErrorBadge/          # Test results display
│   ├── RegenerateButton/    # One-click fixes
│   └── ProgressIndicator/   # Real-time status
└── Services/
    ├── WebSocketService/    # Real-time updates
    ├── APIService/          # REST calls
    └── ProvenanceService/   # Link management
```

## Deployment Architecture

### Container Setup
```yaml
# docker-compose.yml
services:
  api:
    build: ./backend
    environment:
      - DATABASE_URL=postgresql://...
      - REDIS_URL=redis://...
      - S3_BUCKET=paper2repo-storage
    
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    
  worker:
    build: ./backend
    command: celery worker
    
  sandbox:
    image: python:3.11-slim
    security_opt:
      - no-new-privileges:true
    read_only: true
```

### Monitoring & Metrics
```python
# Key metrics to track
METRICS = {
    "processing_time": "histogram",
    "success_rate": "gauge", 
    "provenance_clicks": "counter",
    "user_corrections": "histogram",
    "error_types": "counter",
    "cost_per_run": "histogram"
}
```

## Security Considerations

### Sandboxed Execution
- Ephemeral containers with no network access
- Resource limits (CPU, memory, time)
- Read-only filesystem except /tmp
- No persistent storage access

### Data Privacy
- User-owned outputs with clear TOS
- No PDF redistribution
- Secure storage with encryption
- Session-based access control

## Performance Optimizations

### Caching Strategy
- Paper embeddings cached for 30 days
- Generated code cached per paper version
- LLM responses cached for identical contexts

### Concurrent Processing
- Async pipeline stages
- Module generation in parallel
- Queue-based job processing

## Error Handling & Recovery

### Failure Modes
1. **PDF parsing failure** → Manual text input fallback
2. **Code generation failure** → Retry with simplified context
3. **Compilation failure** → Error analysis and fix suggestions
4. **Test failure** → Regeneration with additional context
5. **Timeout** → Partial results with clear status

### Recovery Strategies
- Automatic retries with exponential backoff
- Graceful degradation (partial success)
- Clear error messaging with suggested actions
- Manual intervention points for complex cases

This architecture supports all requirements: <10min processing, >60% success rate, provenance tracking, real-time UI, and scalable deployment for 20-30 concurrent labs.
