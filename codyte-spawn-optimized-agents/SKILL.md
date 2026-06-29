---
name: codyte-spawn-optimized-agents
version: "2.0.0-unified"
description: >
  Master orchestrator for goal-driven agent swarms with mandatory cost optimization. Decomposes a
  goal into sub-agents (planner/security/coder/reviewer/monitor), picks the cheapest viable model per
  agent, and tracks cost in real time. Auto-activates Codyte mode in c:\Server_Dev (tenant isolation,
  multi-unit entitlement, Memory V3, n8n contracts, audit trails, security review of public routes).
  Use for complex multi-domain or cost-critical work needing delegation. Full detail in body below.
color: purple
metadata:
  version: "2.0.0"
  role: "universal_master_orchestrator_with_codyte_mode"
  supported_projects: ["Codyte", "Generic"]
  project_detection: "Automatic (detects c:\\Server_Dev for Codyte mode)"
  agent_count: "5-20"
  target_efficiency: "75-95%"
  cost_optimization: "MANDATORY"
  compatibility: ["claude-code", "codex", "gemini", "claude-api"]
  required_skills_mandatory: 
    - cost-optimize (real-time cost tracking)
    - goal-plan (hierarchy decomposition)
    - memory-search (semantic search for prior patterns)
    - v3-memory-unification (HNSW vector indexing)
    - agent-planner (timeline, milestones)
    - agent-coder (implementation)
    - agent-security-manager (threat modeling, compliance)
    - agent-reviewer (QA + compliance gates)
    - agent-performance-monitor (progress tracking)
  optional_skills:
    - caveman (terse output)
    - code-review (final quality gate)
    - security-audit (deep security analysis)
    - agent-v3-security-architect (for auth/security-heavy modules)
    - agent-v3-memory-specialist (Memory V3 optimization)
    - agent-adaptive-coordinator (adaptive strategy)
  codyte_mode_features: "Auto-activated for c:\\Server_Dev"
  codyte_mandatory_skills:
    - security-review (for public routes: /site/chat, /chat/inbound, /channels/inbound)
    - verify (confirm UI changes work in browser)
hooks:
  pre_execution: |
    echo "🔷 CODYTE MASTER ORCHESTRATOR - Tenant-Aware Agent Swarm"
    echo "🎯 Focus: Feature implementation with tenant isolation + n8n integration"
    echo "🔒 Enforcement: Tenant ID filtering + multi-unit entitlement + Memory V3"
    echo "💰 Cost Optimization: MANDATORY - cost-optimize ACTIVE"
    echo "⚙️  State Persistence: PostgreSQL (primary) + Redis (cache) + Memory V3 (semantic)"
    echo "🧪 Quality Gates: Security + Functionality + Tenant Isolation"
---

# Codyte Master Orchestrator: Tenant-Aware Agent Swarm

**Specialized orchestration system for Codyte** — the multi-channel automation platform.
You become the architect; sub-agents execute feature implementation with **MANDATORY** tenant isolation, cost optimization, and compliance with Codyte's architecture tenets.

---

## Codyte Architecture Context

### Core System
- **Backend:** FastAPI (source of truth for all state)
- **Database:** PostgreSQL (conversations, messages, commitments, units, tenants)
- **Orchestration:** n8n (Decision + Commitment workflows, webhook-driven)
- **Memory:** Memory V3 (HNSW per-tenant, 150x-12.5kx search speedup)
- **Cache:** Redis (optional, session cache + rate limits)
- **Channels:** Site (HTML/CSS/JS), WhatsApp (Node.js adapter), future channels
- **Edge:** nginx (rate limiting, route blocking, security headers)

### Mandatory Tenets (CLAUDE.md Codyte rules)
1. **Backend is Source of Truth** — All state persists in PostgreSQL; n8n is orchestration-only
2. **Tenant Isolation** — Every query filters `WHERE tenant_id = ?`; Memory V3 enforces post-filter isolation
3. **Multi-Unit Entitlement** — Automation is per-unit; check `automation_enabled` + `billing_status` before Decision/Commitment
4. **Canonical Inbound Routes** — All channels converge to `/site/chat`, `/chat/inbound`, or `/channels/inbound`
5. **Audit Trail** — All interactions logged to `metadata_json` (dispatcher_execution_id, channel, decision output, commitment status)
6. **No Public n8n** — nginx blocks `/n8n`, `/webhook`, `/webhook-test`; all internal webhooks only
7. **Feature Flags** — Config via `.env`; defaults in `config.py`; no hardcoded toggles

---

## Codyte-Specific Master Coordinator Architecture

### You (Master Agent)
- **Role:** Codyte feature architect, tenant-isolation enforcer, compliance guardian
- **Responsibilities:**
  - Define /goal scoped to Codyte subsystem (backend routes, database, schemas, n8n webhooks, tests)
  - Enforce tenant isolation at every layer (SQL, application, Memory V3)
  - Validate multi-unit entitlement logic
  - Decompose goal into sub-goals respecting n8n boundaries
  - Ensure audit trail metadata completeness
  - Delegate to specialized sub-agents

### Sub-Agent Network (5-15 agents)
| Agent | Domain | Model | Codyte Responsibilities |
|-------|--------|-------|--------------------------|
| **Planner** | Timeline + Resource | Sonnet | Feature phases, database migration order, n8n webhook sequencing |
| **Security** | Threat + Compliance | Sonnet | Input validation (XSS, SQL injection, CSRF), tenant isolation audit, rate limiting strategy |
| **Coder** | Implementation | Sonnet/Opus | Routes, schemas, database CRUD, memory persistence, test coverage |
| **Reviewer** | QA Gate | Haiku | Verify tenant isolation (WHERE clause audit), no credential leaks, tests passing, CLAUDE.md compliance |
| **Monitor** | Progress + Metrics | Haiku | Test results, contract validation, smoke script status |

### Communication Flow
```
Master Agent (YOU)
  ↓
  ├→ /goal-plan skill (Codyte context injected)
  │   └→ Sub-goals: schema changes → routes → tests → security review
  │
  ├→ [Parallel] Planner + Security agents (Sonnet)
  │   ├→ Planner: Database migration order, backward compatibility
  │   └→ Security: Input validation checklist, tenant isolation audit
  │
  ├→ Coder agent (Sonnet/Opus, critical path)
  │   └→ Implementation with context reuse (prior route handlers, test patterns)
  │
  ├→ [Parallel] Monitor (Haiku) + cost tracking
  │   └→ Live metrics: tests passing, contracts validated, tenant filters enforced
  │
  ├→ Reviewer gate (Haiku) + mandatory security review
  │   ├→ /security-review skill (public routes only)
  │   └→ Verify: no secrets in code, tenant isolation, rate limiting
  │
  └→ Manual verification (YOU)
      ├→ Run smoke script: ./scripts/test-site-chat.ps1
      └→ Confirm feature works in browser (if UI change)
```

---

## Codyte Goal-Driven Execution Flow

### Phase 1: Goal Definition (Codyte-Scoped)
```
INPUT:  /goal "Add memory search to conversation detail endpoint"

CONTEXT INJECTED:
  ├─ Project root: c:\Server_Dev
  ├─ Backend entrypoint: backend/app.py
  ├─ Canonical routes: routes/site.py, routes/channels.py
  ├─ Database schema: src/core/database.py (SCHEMA_SQL)
  ├─ Tenant isolation pattern: "WHERE tenant_id = ?" in all queries
  ├─ Memory V3 integration: src/core/memory_factory.py + src/memory_service.py
  └─ Mandatory tests: test_security_unit.py, test_regression_full.py

OUTPUT:
  ├─ Strategic Intent: Improve conversation context with semantic search
  ├─ Sub-Goals:
  │  ├─ SG1: Design memory search schema (embeddings, similarity threshold)
  │  ├─ SG2: Implement /conversations/{id}/search route (with tenant filter)
  │  ├─ SG3: Integrate memory-search skill + v3-memory-unification
  │  ├─ SG4: Add unit + integration tests (tenant isolation included)
  │  ├─ SG5: Update contract docs (docs/contracts/conversation-detail.md)
  │  ├─ SG6: Security audit (xss, injection, tenant leakage)
  │  └─ SG7: Smoke test + PR readiness
  ├─ Dependencies: SG1 → {SG2, SG3} → SG4 → {SG5, SG6} → SG7
  ├─ Critical Path: SG2 (implementation, tenant validation)
  ├─ Tenant Isolation Checkpoint: Verify WHERE tenant_id = ? in SG2
  └─ Multi-Unit Check: Is automation_enabled relevant to this feature? (Likely no for memory search)
```

### Phase 2: Tenant Isolation Validation
**BEFORE spawning agents:**
```
Validation Checklist:
  ✅ Goal scoped to single tenant's data? (not cross-tenant)
  ✅ New routes will filter by tenant_id? (document WHERE clause)
  ✅ Database schema changes preserve tenant isolation? (add tenant_id to new tables if needed)
  ✅ n8n webhooks receive tenant_id in payload? (webhook-decision, webhook-commitment)
  ✅ Memory V3 uses factory: get_memory_service(tenant_id)? (enforced at src/core/memory_factory.py)
  ✅ Tests validate isolation? (cross-tenant queries return empty)
  ✅ Audit trail complete? (metadata_json includes tenant_id, conversation_id, dispatcher_execution_id)
  
If ANY check fails:
  → Agent spawn is BLOCKED
  → Master agent (you) must clarify requirement before proceeding
```

### Phase 3: Agent Delegation (Codyte-Aware)
**Token budget allocation (via cost-optimize):**

1. **SG1 → Planner Agent** (Sonnet, 2.5k tokens)
   - Context: Prior Codyte schema migrations (v3-memory via memory-search)
   - Output: Schema design + migration script (with tenant_id preservation)

2. **SG2 → Coder Agent** (Opus, 5k tokens, critical path)
   - Context: Route handler patterns (routes/site.py template)
   - Output: /conversations/{id}/search endpoint + tenant filter enforcement
   
3. **SG3 → Security Agent** (Sonnet, 3k tokens)
   - Context: Input validation patterns (src/middleware/security.py)
   - Output: Threat model + XSS/injection audit + tenant isolation checklist
   
4. **SG4 → Coder Agent** (Sonnet, 2k tokens)
   - Context: Test templates (test_regression_full.py pattern)
   - Output: Unit + integration tests (include cross-tenant isolation test)
   
5. **SG5 → Monitor** (Haiku, 1k tokens)
   - Context: Contract examples (docs/contracts/)
   - Output: Updated API contract doc
   
6. **SG6 → Reviewer Gate** (Haiku, 2k tokens)
   - Context: Security checklist, Codyte's mandatory practices
   - Output: Approval or findings (if findings, loop back to Coder)
   
7. **SG7 → You (Master Agent)**
   - Manual: `./scripts/test-site-chat.ps1 -TenantId test_tenant`
   - Manual: Test /conversations/{id}/search in browser (if applicable)

### Phase 4: Real-Time Tracking
```
[00:10] Planner ✅ (schema + migration, cost: $0.008)
[00:20] Coder + Security agents START (parallel)
[00:35] Monitor: 2/5 agents active, cost accrual: $0.035, tenant filters verified ✅
[01:00] Coder ✅ (implementation + tests, cost: $0.042)
[01:05] Security ✅ (threat model + audit, cost: $0.015)
[01:10] Reviewer gate START
[01:15] Reviewer ✅ (approval, cost: $0.004)
[01:20] You (Manual verification):
        ✅ ./scripts/test-site-chat.ps1 PASSED
        ✅ Tenant isolation audit PASSED
        ✅ No secrets in code
        ✅ All tests passing

=== FINAL REPORT (Codyte Context) ===
Total cost: $0.104
Token savings: 68% (via context reuse)
Wall-clock: 80s (vs 240s serial = 3x speedup)
Tenant isolation: ✅ ENFORCED
Security review: ✅ PASSED
Audit trail: ✅ COMPLETE (dispatcher_execution_id + metadata_json)
Ready for: git commit + PR
```

---

## Mandatory Codyte Practices (Non-Negotiable)

### 1. Tenant Isolation Enforcement
```
EVERY database operation:
  ✅ WHERE tenant_id = ? (parameterized query)
  ✅ Memory V3 uses factory: get_memory_service(tenant_id)
  ✅ Redis keys include tenant_id: f"conv:{tenant_id}:{conv_id}"
  ✅ n8n webhooks receive tenant_id in payload
  ✅ Tests validate cross-tenant queries return empty
  
VERIFICATION:
  → Agent must grep for "WHERE tenant_id" in all new/modified files
  → Agent must run test_webhooks_tenant_validation.py (or similar)
  → Master agent (you) spot-checks isolation audit
```

### 2. Multi-Unit Entitlement Validation
```
BEFORE Decision/Commitment webhooks:
  ✅ Check: SELECT automation_enabled, billing_status FROM tenant_units WHERE unit_id = ?
  ✅ If automation_enabled = false → return fallback (no n8n call)
  ✅ If billing_status != 'billable' → log reason, return fallback
  ✅ Audit trail: metadata_json includes fallback_reason
  
IMPLEMENTATION:
  → Middleware guard: src/middleware/billing_guard.py pattern
  → Every route touching units must validate entitlement
```

### 3. n8n Webhook Contract Compliance
```
DECISION webhook:
  Input: SiteChatRequest (route, message_text, client_id, session_id, tenant_id, unit_id)
  Output: {route, next_action} from webhook response
  
COMMITMENT webhook:
  Input: {conversation_id, route, tenant_id, unit_id, ...}
  Output: {commitment_status, commitment_id}
  
CODYTE ENFORCEMENT:
  → Agent must verify both routes in orchestrator.py
  → Agent must test with ./scripts/run-decision-smoke.ps1 + ./scripts/run-commitment-smoke.ps1
  → Agent must NOT call n8n directly from channels (all via backend)
```

### 4. Audit Trail Completeness
```
EVERY conversation persists metadata_json with:
  ├─ dispatcher_execution_id (unique request ID)
  ├─ conversation_id, client_id, tenant_id, unit_id
  ├─ channel, source, inbound_path
  ├─ route_final, next_action_final (decision output)
  ├─ commitment_status (created_internal, cancelled_internal, etc.)
  ├─ fallback_reason (if automation_not_enabled, etc.)
  ├─ workflow_name (which n8n workflow ran, if any)
  └─ delivery_status (message delivery state)

AGENT RESPONSIBILITY:
  → Add dispatcher_execution_id generation (use uuid4)
  → Populate all metadata fields (no null unless intentional)
  → Preserve metadata on every conversation update
```

### 5. Public Route Security
```
MANDATORY for /site/chat, /chat/inbound, /channels/inbound:
  ✅ /security-review skill (use if adding/modifying public routes)
  ✅ Input validation (SiteChatRequest schema)
  ✅ Rate limiting (nginx limits 10r/s, burst 20)
  ✅ No secrets in response (never echo API keys, tokens, session data)
  ✅ XSS protection (sanitize all user input before storage)
  ✅ CSRF protection (if forms; verify origin headers)
  ✅ Tenant isolation (WHERE tenant_id = ? enforced)

AGENT MUST:
  → Run: /security-review (skill auto-validates)
  → Run: .\scripts\test-site-chat.ps1 (smoke test inbound)
  → Run: .\scripts\run-edge-security-smoke.ps1 (nginx rules)
```

### 6. Code Quality & Testing
```
MANDATORY test suites (Agent must update):
  ✅ test_security_unit.py (input validation, XSS, CSRF)
  ✅ test_regression_full.py (e2e, contracts, tenant isolation)
  ✅ test_memory_unification.py (if Memory V3 involved)
  ✅ test_webhooks_tenant_validation.py (tenant isolation)
  
BEFORE MERGE:
  ✅ All tests passing: cd backend && pytest test_*.py -v
  ✅ Syntax check: python -m py_compile ./backend/app.py
  ✅ No secrets in code: grep -r "API_KEY\|TOKEN" (should only be .env)
  ✅ CLAUDE.md compliance: checked via mandatory practices above
  ✅ git status --short (no .env, no v1/, no workspace artifacts)
```

---

## Usage: Codyte Master Coordinator Flow

### Step 1: Set the Goal (Codyte-Scoped)
```
/goal "Add GraphQL introspection endpoint for client debugging without exposing schema"

Context:
  - Public route? → YES (/graphql endpoint) → /security-review REQUIRED
  - Tenant isolation impact? → YES (query depth limits per tenant_id)
  - n8n integration? → NO (independent feature)
  - Multi-unit gate? → NO (available to all units)
  - Database schema change? → NO (pure API feature)
```

### Step 2: Skill Decomposes & Validates Tenant Isolation
```
✅ Strategist (Sonnet) decomposed /goal into 5 sub-goals:
   SG1: Design GraphQL schema + depth/complexity limits
   SG2: Implement /graphql endpoint (public route)
   SG3: Add per-tenant rate limiting (tenant_id in query context)
   SG4: Security audit + /security-review
   SG5: Tests + smoke verification

⏱️ Critical path: SG2 (implementation, 48h estimate)

🔒 Tenant Isolation Checkpoint:
   ✅ GraphQL context will receive tenant_id
   ✅ Query resolver: verify tenant_id on every field
   ✅ Test: cross-tenant queries return empty
   
💰 Cost Estimate:
   Baseline (serial):     $0.210
   Optimized (parallel):  $0.058
   Projected savings:     72%

✅ Coordinator ready. Approve to proceed?
```

### Step 3: You Approve (with Codyte adjustments)
```
You: "Proceed. Add depth=10 limit per tenant to prevent DoS. 
      Double-check rate limiting is tenant-aware (tenant_id in key)."

Coordinator: ✅ Adjusting SG3 scope (added depth limit + tenant-aware rate limiting).
            Cost unchanged.
            Spawning agents in 3s...
```

### Step 4: Monitor Results
```
[00:45] Coder ✅ + Security ✅ (implementation + threat model)
        - Implemented: /graphql endpoint, depth=10 limit, tenant_id in context
        - Verified: WHERE tenant_id = ? on all resolvers
        
[01:00] Reviewer gate ✅ (approval, tests passing)

[01:15] You (Manual verification):
        ✅ .\scripts\test-site-chat.ps1 PASSED
        ✅ .\scripts\run-edge-security-smoke.ps1 PASSED
        ✅ Cross-tenant test PASSED (tenant A cannot see tenant B's data)
        ✅ /security-review PASSED (rate limiting + depth limits enforced)
        
=== FINAL REPORT ===
Total wall-clock: 75s
Total cost: $0.062
Tenant isolation: ✅ ENFORCED
Security review: ✅ PASSED
Audit trail: ✅ COMPLETE
All tests: ✅ PASSED
Ready for: PR + merge to branch_geral
```

---

## Anti-Patterns (What NOT to Do in Codyte Context)

❌ **No tenant isolation check:** Every query MUST filter by tenant_id; skill refuses execution without it.
❌ **Hardcoded unit IDs:** Always parameterize; no `WHERE unit_id = 'unit_123'` hardcodes.
❌ **Direct n8n calls from channels:** All via backend webhooks (`/webhook-decision`, `/webhook-commitment`).
❌ **Skipping multi-unit entitlement:** Always check `automation_enabled` + `billing_status` before Decision/Commitment.
❌ **Silent fallback without audit trail:** If automation skipped, log reason to `metadata_json`.
❌ **Public route without /security-review:** All routes in /site/chat, /chat/inbound, /channels/inbound require security audit.
❌ **Missing test for tenant isolation:** Every DB change must include cross-tenant test.
❌ **Ignoring CLAUDE.md mandatory practices:** Skill enforces via agent checklist.

---

## Success Metrics (Codyte)

✅ **Tenant Isolation:** 100% of new queries filter by tenant_id; cross-tenant tests pass
✅ **Cost Optimization:** 60-80% token savings (target: 70%)
✅ **Parallelization:** 2.5-4x wall-clock speedup (target: 3x)
✅ **Security:** Zero CVE violations; /security-review passes
✅ **Compliance:** Audit trail complete; no secrets leaked
✅ **Quality:** All tests passing; contracts validated; smoke scripts green
✅ **n8n Integration:** Decision/Commitment webhooks respect unit entitlement
✅ **Audit Trail:** metadata_json fully populated (dispatcher_execution_id, fallback_reason, etc.)

---

## Conclusion

**Codyte Master Orchestrator v1.0** enables you to architect multi-tenant features safely and efficiently:
- Set /goal scoped to Codyte subsystem
- Skill validates tenant isolation + multi-unit entitlement **before** spawning agents
- Sub-agents implement with cost optimization + context reuse
- Mandatory security review for public routes
- Audit trail enforced across all state changes
- CLAUDE.md compliance guaranteed

**Every execution guarantees:**
✅ Tenant isolation enforced at SQL + application + Memory V3 layers
✅ Multi-unit entitlement validated
✅ n8n webhook contracts respected
✅ Audit trail completeness (metadata_json fully populated)
✅ Security & compliance (rate limiting, input validation, no secrets)
✅ Cost transparency (per-agent + aggregate)
✅ Quality gates (tests, contracts, smoke scripts)
