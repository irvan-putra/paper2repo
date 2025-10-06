# Paper2Repo Architecture

## Overview

Paper2Repo converts ML research papers into runnable, provenance-linked repositories using a modular pipeline approach.

## System Components

### Core Pipeline
```
PDF Upload → Parser → Planner → Generator → Verifier → Export
     ↓         ↓        ↓         ↓         ↓        ↓
  Storage   Analysis  Structure  Code    Tests   Repo
```

### 1. PDF Parser
- Extracts text from research papers
- Identifies sections (abstract, methods, equations)
- Handles arXiv and DOI formats
- Fallback for manual text input

### 2. Paper Analyzer
- Uses AI (AWS Bedrock/heuristics) to understand content
- Extracts key information:
  - Paper title and abstract
  - Main methodology
  - Architecture details
  - Implementation hints

### 3. Repository Planner
- Proposes Python module structure
- Maps paper sections to code files
- Suggests dependencies and frameworks
- Creates implementation roadmap

### 4. Code Generator
- Generates runnable Python code
- Creates proper class/function structure
- Adds docstrings with paper references
- Implements error handling and type hints

### 5. Test Generator
- Creates comprehensive test suites
- Smoke tests for basic functionality
- Input/output validation
- Edge case handling

### 6. Verifier (Future)
- Sandboxed code execution
- Compilation and import checks
- Test execution and validation
- Error analysis and suggestions

## AI Integration

### Current: Heuristic Analysis
- Pattern matching for method detection
- Keyword-based architecture identification
- Template-based code generation
- Fast and reliable for demo purposes

### Future: AWS Bedrock
- Claude 3 Sonnet for code generation
- Claude 3 Haiku for parsing/planning
- Advanced context understanding
- Higher accuracy and quality

## Data Flow

1. **Input**: PDF file upload
2. **Extraction**: Text and structure parsing
3. **Analysis**: AI-powered content understanding
4. **Planning**: Repository structure design
5. **Generation**: Code and test creation
6. **Output**: Complete runnable repository

## Quality Metrics

- **Speed**: <10 minutes end-to-end
- **Success Rate**: >60% compile/test pass
- **User Effort**: <30 lines of corrections
- **Provenance**: Clear code-to-paper linking

## Scalability

- Modular design for easy extension
- Caching for repeated operations
- Async processing for multiple papers
- Cloud-native deployment ready
