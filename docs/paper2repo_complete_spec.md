# Paper2Repo: Complete Project Specification

## Executive Summary
Paper2Repo enables ML researchers to upload a research paper (PDF + supplements) and instantly generate a runnable, provenance-linked repository with tests and verification loops. Target: <10 minutes from upload to working baseline.

## Product Vision
**"From paper to runnable repo in 10 minutes"**

Transform Maria's traditional hours-long process of deciphering methods, tracing equations, and building scaffolding into a 10-minute automated workflow with clear traceability and confidence in output quality.

## Goals & Success Metrics

### Business Goals
- >60% "simple-moderate" ML papers compile/pass smoke tests in <10 minutes
- 20-30 active deployments in top ML labs during alpha (3 months)
- <30 lines median user correction effort per repo
- >60% task completion rate with provenance-documented outputs
- Cost/run beneath fixed benchmark based on paper complexity

### User Goals
- Upload paper → get runnable, traceable repo in 10 minutes
- Click-to-see provenance linking (code ↔ paper sections)
- Error-guided regeneration for quick iteration
- Download complete repos for immediate use
- Trust results through transparent verification

### Success Metrics
- **Speed**: Median time to first runnable repo ≤ 10 minutes
- **Quality**: ≥60% auto-generated repos pass smoke tests first try
- **Trust**: Provenance clicks/session (proxy for traceability usage)
- **Efficiency**: <30 lines edited per repo median
- **Reach**: 20-30 active alpha lab deployments by Q-end

## Core User Stories

### Researcher (Maria)
*"As a grad student, I upload an arXiv PDF and, within minutes, get a runnable repo with smoke tests and clear documentation of what came from where."*

### Engineer
*"As an applied ML engineer, I spot which paper snippet caused an error in train.py, then use 'Fix with context' to resolve and quickly re-run tests."*

### Student
*"As a learner, after seeing failing tests, I receive actionable guidance with suggested fixes and one-click 'Regenerate Module' to iterate—no code expertise required."*

## Functional Requirements

### Core Pipeline (Must Have)
1. **PDF Processing**
   - arXiv/DOI ingestion
   - Extract title, abstract, methods, pseudocode, equations, figure captions
   - Generate document outline and structure

2. **Code Generation**
   - Per-module codegen (model.py, train.py, data.py)
   - Source-cited docstrings with provenance links
   - Minimal smoke test suite generation

3. **Verification & Provenance**
   - Compile and run code in sandboxed environment
   - Real-time console logs and error capture
   - Bidirectional provenance links (code ↔ paper)

4. **Debug & Iteration**
   - Error interpretation and fix suggestions
   - One-click "Regenerate Module"
   - Error trace summarization with ambiguity flagging

5. **Export**
   - Download repo as .zip with README
   - Document known gaps and assumptions
   - Export configuration files

6. **UI/UX**
   - Three-pane layout (source | actions/logs | code)
   - Responsive design for mobile/desktop
   - Real-time progress updates

## Technical Architecture

### System Components
```
PDF Upload → Parser → Planner → Generator → Verifier → Export
     ↓         ↓        ↓         ↓         ↓        ↓
  Storage   Embeddings Structure  Code    Tests   Repo
```

### Tech Stack
- **Backend**: Python FastAPI, PostgreSQL, Redis
- **Frontend**: React with WebSocket real-time updates
- **Storage**: S3-compatible object storage
- **Execution**: Docker containers for sandboxed testing
- **LLM**: OpenAI/Anthropic APIs with fallback models

### Key Services
1. **PDF Processor**: Parse and extract structured content
2. **Repo Planner**: Infer module structure and mapping
3. **Code Generator**: Generate modules with provenance tracking
4. **Verifier**: Sandboxed execution and test running
5. **Provenance Tracker**: Bidirectional code-paper linking

## Non-Goals (v1 Scope)
- No scanned PDFs/OCR support (until v1.5+)
- No multimodal diagram parsing beyond captions
- No full training runs or large-scale benchmarking
- No educational content (study guides, media, audio/video)

## Implementation Timeline

### v1 MVP: 8-12 weeks
**Core Deliverables:**
- PDF parsing with arXiv/DOI support
- Repo planning and per-module code generation
- Smoke tests and sandboxed verification
- Provenance tracking and three-pane UI
- Repo export with documentation

**Team**: 2-3 people (1 product/UX, 1-2 engineering)

### Weekly Milestones
- **Weeks 1-2**: Foundation (database, API, basic parsing)
- **Weeks 3-4**: Core pipeline (structure extraction, code generation)
- **Weeks 5-6**: Provenance system (bidirectional linking)
- **Weeks 7-8**: Verification (sandboxed testing, error handling)
- **Weeks 9-10**: Export and UI polish
- **Weeks 11-12**: Integration and launch preparation

### Future Versions
- **v1.5 (4-6 weeks)**: OCR support, diagram captions, config wizard
- **v2 (6-10 weeks)**: Advanced tests, datasets, collaborative features
- **v3 (TBD)**: Multimodal analysis, debugging agents, notebook integration

## Go-to-Market Strategy

### Private Alpha
- **Target**: 20-30 ML labs and graduate students
- **Duration**: 3 months
- **Focus**: Monitor compile/test/pass rates, measure time and edit effort
- **Feedback**: Gather insights on traceability and workflow effectiveness

### Pricing Strategy
- **Alpha**: Free usage to gather data and feedback
- **Post-alpha**: Usage-metered (runs/month) with student/free tier
- **Monetization**: Delayed until empirical learning from alpha trials

### Success Criteria for Alpha
- Achieve target success metrics (>60% compile rate, <10 min processing)
- Validate user workflows and pain points
- Establish baseline costs and pricing model
- Build pipeline for broader market expansion

## Risk Mitigation

### Technical Risks
1. **LLM Quality**: Code generation accuracy
   - *Mitigation*: Extensive prompt engineering, multiple model fallbacks
2. **PDF Parsing**: Structure variation complexity
   - *Mitigation*: Multiple parsing libraries, manual input fallbacks
3. **Sandbox Security**: Safe code execution
   - *Mitigation*: Container isolation, resource limits, network restrictions

### Product Risks
1. **User Adoption**: Complex workflow acceptance
   - *Mitigation*: Extensive user testing, simplified onboarding
2. **Performance**: 10-minute processing target
   - *Mitigation*: Parallel processing, aggressive caching, optimization

## Reference Patterns
- **NotebookLM**: Multi-panel, source-grounded UX with actionable traces
- **Paper2Code/PaperCoder**: Multi-agent repo-level codegen baselines

## Next Steps
1. **Week 1**: Set up development environment and core infrastructure
2. **User Research**: Validate assumptions with target ML labs/students
3. **Technical Proof-of-Concept**: Build minimal end-to-end demo
4. **Alpha Recruitment**: Identify and engage 20-30 target labs

---

**Ready to transform ML research reproducibility. Let's build Paper2Repo!**
