# Paper2Repo MVP Task Implementation Plan

## High-Level Sequence (Dependency-Optimized)

### Phase 1: Foundation (Weeks 1-2)
**Critical Path: Infrastructure + Core APIs**

#### DevOps/Infra (Priority 1)
- [ ] 5.1 Provision containerized environments (API, worker, sandbox)
- [ ] 5.2 Set up job queue (Redis/Celery)
- [ ] 5.4 Add logging/metrics infrastructure
- [ ] 5.5 Configure backups and access controls

#### Backend Skeleton (Priority 1)
- [ ] 3.1 Create upload API + object storage
- [ ] Database setup (PostgreSQL schema)
- [ ] Basic FastAPI structure with health checks
- [ ] Authentication/session management

#### Frontend Shell (Priority 2)
- [ ] 2.1 Scaffold React app + routing
- [ ] 2.1 Implement tri-pane responsive layout
- [ ] Basic component structure (empty states)

### Phase 2: Core Pipeline (Weeks 3-5)
**Critical Path: Parser → Planner → Generator**

#### AI/ML Integration (Priority 1)
- [ ] 4.1 Set model strategy (OpenAI/Anthropic setup)
- [ ] 4.2 Build retrieval system (embeddings + chunking)
- [ ] 4.3 Author core prompts (plan, codegen templates)

#### Backend Core Services (Priority 1)
- [ ] 3.2 Parser service (PDF → structured content)
- [ ] 3.3 Planner service (repo structure proposal)
- [ ] 3.4 Generator service (per-module codegen)
- [ ] 3.7 Provenance API (code ↔ paper mapping)

#### Product/UX Definition (Priority 2)
- [ ] 1.1 Define core user flow
- [ ] 1.2 Draft tri-pane layout specs
- [ ] 1.3 Specify states (empty, error, success)
- [ ] 1.5 Approve provenance interaction design

### Phase 3: Verification & UX (Weeks 6-7)
**Critical Path: Testing + User Interface**

#### Backend Verification (Priority 1)
- [ ] 5.3 Lock down sandbox security
- [ ] 3.5 Verifier service (sandboxed testing)
- [ ] 3.6 Regenerator service (error-aware fixes)

#### Frontend Integration (Priority 1)
- [ ] 2.2 PDF viewer with outline/anchors
- [ ] 2.3 Actions/Logs panel (real-time streaming)
- [ ] 2.4 Code Explorer + syntax highlighting
- [ ] 2.6 Core actions (Generate, Test, Regenerate)

#### AI/ML Refinement (Priority 2)
- [ ] 4.4 Error-aware refinement loop
- [ ] 4.5 Caching for embeddings/outputs

### Phase 4: Polish & Export (Weeks 8-9)
**Critical Path: Complete User Journey**

#### Frontend Polish (Priority 1)
- [ ] 2.5 Provenance UI (hover/click interactions)
- [ ] 2.7 Download .zip export
- [ ] 1.4 Copy for buttons/tooltips/guidance

#### Backend Export (Priority 1)
- [ ] 3.8 Export API (repo + README + provenance.json)
- [ ] Complete error handling and edge cases

#### QA Foundation (Priority 2)
- [ ] 6.1 Create sample paper test set
- [ ] 6.2 Write pipeline integration tests

### Phase 5: Testing & Launch Prep (Weeks 10-12)
**Critical Path: Quality Assurance + Go-to-Market**

#### QA/Testing (Priority 1)
- [ ] 6.3 Validate provenance accuracy
- [ ] 6.4 Track key metrics (compile rate, timing)
- [ ] 6.5 End-to-end testing and bug fixes

#### Program/Ops (Priority 1)
- [ ] 8.1 Define MVP acceptance criteria
- [ ] 8.2 Set quotas and cost guardrails
- [ ] 8.3 Incident response playbook
- [ ] 8.4 Feedback loop setup

#### Marketing/GTM (Priority 2)
- [ ] 7.1 Minimal homepage
- [ ] 7.2 Alpha signup/onboarding
- [ ] 7.3 Public sample repo + demo
- [ ] 7.4 Target lab outreach list

## Critical Dependencies

### Technical Dependencies
1. **LLM API Access** → Required for all code generation
2. **Sandbox Security** → Blocks verification testing
3. **Object Storage** → Required for PDF uploads
4. **Real-time Updates** → WebSocket for UI responsiveness

### Product Dependencies
1. **User Flow Definition** → Guides all UI development
2. **Provenance Design** → Core differentiator implementation
3. **Sample Papers** → Required for testing and validation
4. **Success Metrics** → Defines "done" criteria

## Resource Allocation by Phase

### Phase 1-2 (Weeks 1-5): 70% Backend, 30% Frontend
- Focus on core pipeline and infrastructure
- Basic UI for testing and validation

### Phase 3-4 (Weeks 6-9): 50% Backend, 50% Frontend
- Complete user experience implementation
- Polish and integration work

### Phase 5 (Weeks 10-12): 30% Backend, 40% Frontend, 30% QA/GTM
- Testing, bug fixes, and launch preparation
- Marketing materials and user onboarding

## Risk Mitigation by Phase

### Phase 1-2 Risks
- **LLM Integration Complexity** → Start with simple prompts, iterate
- **PDF Parsing Variations** → Use multiple libraries, manual fallback
- **Infrastructure Setup** → Use managed services where possible

### Phase 3-4 Risks
- **Sandbox Security** → Thorough container isolation testing
- **UI Complexity** → Progressive enhancement, mobile-first
- **Performance** → Early optimization, caching strategy

### Phase 5 Risks
- **Quality Issues** → Extensive testing with real papers
- **User Adoption** → Clear onboarding, sample demonstrations
- **Launch Readiness** → Staged rollout, monitoring

## Success Criteria by Phase

### Phase 1-2: Foundation Complete
- [ ] PDF upload and basic parsing works
- [ ] Simple code generation pipeline functional
- [ ] Basic three-pane UI operational

### Phase 3-4: Core Features Complete
- [ ] End-to-end pipeline (upload → code → test)
- [ ] Provenance linking functional
- [ ] Error handling and regeneration works

### Phase 5: Launch Ready
- [ ] >60% compile rate on test papers
- [ ] <10 minute processing time
- [ ] Complete user onboarding flow
- [ ] Alpha user recruitment ready

This plan ensures critical path optimization while maintaining quality and user experience standards.
