# Paper2Repo v1 MVP Implementation Plan
**Timeline: 8-12 weeks | Team: 2-3 people (1 product/UX, 1-2 engineering)**

## v1 Core MVP Deliverables
- PDF parsing with arXiv/DOI support
- Repo structure planning
- Per-module code generation with provenance
- Smoke test generation and execution
- Three-pane UI with real-time updates
- Repo export with documentation

## Weekly Breakdown

### Week 1-2: Foundation & Setup
**Engineering Focus:**
- Project setup (repo, CI/CD, deployment)
- Database schema implementation
- Basic API structure (FastAPI)
- PDF parsing service (PyPDF2/pdfplumber)
- arXiv API integration

**Product/UX Focus:**
- UI wireframes and component design
- User flow validation
- Basic React app setup
- Design system foundations

**Deliverables:**
- Working PDF upload and basic parsing
- Database with core tables
- UI mockups and basic layout

### Week 3-4: Core Processing Pipeline
**Engineering Focus:**
- Paper structure extraction (sections, methods, equations)
- Text embedding and retrieval system
- Repo planning service (module structure inference)
- LLM integration for code generation

**Product/UX Focus:**
- Three-pane layout implementation
- Upload flow and progress indicators
- Basic provenance link UI components

**Deliverables:**
- End-to-end parsing pipeline
- Basic code generation for simple modules
- Working three-pane interface

### Week 5-6: Code Generation & Provenance
**Engineering Focus:**
- Per-module code generation with docstrings
- Provenance tracking system
- Smoke test generation
- Error handling and logging

**Product/UX Focus:**
- Interactive provenance links
- Code editor integration
- Real-time status updates (WebSocket)

**Deliverables:**
- Complete code generation pipeline
- Bidirectional provenance linking
- Generated smoke tests

### Week 7-8: Verification & Testing
**Engineering Focus:**
- Sandboxed code execution (Docker containers)
- Test runner and result capture
- Error analysis and fix suggestions
- Module regeneration system

**Product/UX Focus:**
- Test results display
- Error badges and fix suggestions
- One-click regeneration buttons

**Deliverables:**
- Working verification system
- Error-guided regeneration
- Complete test execution pipeline

### Week 9-10: Export & Polish
**Engineering Focus:**
- Repo export with README generation
- Performance optimizations
- Caching implementation
- Monitoring and metrics

**Product/UX Focus:**
- Export flow and download
- UI polish and responsive design
- Error handling and edge cases

**Deliverables:**
- Complete repo export functionality
- Polished UI with responsive design
- Performance monitoring

### Week 11-12: Integration & Launch Prep
**Engineering Focus:**
- End-to-end testing with real papers
- Security hardening
- Deployment automation
- Bug fixes and optimizations

**Product/UX Focus:**
- User testing and feedback integration
- Onboarding flow
- Documentation and help content

**Deliverables:**
- Production-ready MVP
- User onboarding system
- Launch-ready deployment

## Critical Path Dependencies

### Technical Dependencies
1. **LLM Provider Setup** (Week 1) - OpenAI/Anthropic API access
2. **Sandbox Infrastructure** (Week 7) - Docker container security
3. **Object Storage** (Week 1) - S3-compatible storage for PDFs
4. **Database Setup** (Week 1) - PostgreSQL with proper indexing

### Product Dependencies
1. **Design System** (Week 1-2) - Component library and styling
2. **User Testing** (Week 6, 10) - Validation with target users
3. **Sample Papers** (Week 3) - Test dataset for development

## Risk Mitigation

### High-Risk Items
1. **LLM Quality** - Code generation accuracy
   - *Mitigation*: Extensive prompt engineering, fallback models
2. **Parsing Complexity** - PDF structure variations
   - *Mitigation*: Multiple parsing libraries, manual fallback
3. **Sandbox Security** - Code execution safety
   - *Mitigation*: Container isolation, resource limits

### Medium-Risk Items
1. **Performance** - 10-minute target
   - *Mitigation*: Parallel processing, caching
2. **UI Complexity** - Three-pane responsive design
   - *Mitigation*: Progressive enhancement, mobile-first

## Success Criteria for v1

### Functional Requirements
- [ ] Upload PDF and generate runnable repo in <10 minutes
- [ ] >60% of simple-moderate papers compile successfully
- [ ] Bidirectional provenance linking works
- [ ] Smoke tests run in sandboxed environment
- [ ] Export complete repo with documentation

### Quality Requirements
- [ ] UI works on desktop and mobile
- [ ] Real-time updates during processing
- [ ] Clear error messages and recovery options
- [ ] Secure code execution
- [ ] Basic monitoring and logging

### User Experience Requirements
- [ ] Intuitive three-pane interface
- [ ] One-click regeneration and fixes
- [ ] Clear provenance indicators
- [ ] Responsive feedback during processing
- [ ] Downloadable repos with README

## Post-v1 Roadmap Preview

### v1.5 (4-6 weeks): Input Richness
- Scanned PDF/OCR support
- Diagram caption parsing
- Hyperparameter configuration wizard
- Enhanced error guidance

### v2 (6-10 weeks): Advanced Automation
- Richer test suites
- Basic dataset integration
- Collaborative features
- Team workspaces

### v3 (TBD): Multimodal & Power Features
- Figure/equation analysis
- Advanced debugging agents
- Notebook integrations
- Vision model integration

## Resource Allocation

### Engineering (1-2 people)
- **Backend**: 60% (API, processing pipeline, verification)
- **Frontend**: 30% (UI, real-time updates, provenance)
- **DevOps**: 10% (deployment, monitoring, security)

### Product/UX (1 person, can be part-time)
- **Design**: 40% (UI/UX, component design)
- **Product**: 30% (requirements, user testing)
- **Content**: 30% (documentation, onboarding)

This plan delivers Maria's complete 10-minute journey from PDF upload to runnable repo with all core features in 8-12 weeks.
