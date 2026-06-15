# Master Orchestrator v2.0 — Universal + Codyte-Aware

**Location:** `~/.claude/skills/codyte-spawn-optimized-agents`

## Overview

**Universal Master Orchestrator** for goal-driven agent swarms with mandatory cost optimization.
Works for **any project**, but auto-detects **Codyte context** (c:\Server_Dev) and activates **mandatory**
multi-tenant enforcement: tenant isolation, multi-unit entitlement, Memory V3, n8n integration, audit trails.

You become the architect; sub-agents execute feature implementation with cost optimization + context reuse.

- **Version:** 2.0.0-unified
- **Role:** Universal orchestrator (generic projects + Codyte-specialized mode)
- **Compatibility:** Claude Code, Codex, Gemini, Claude API
- **Project Detection:** Automatic (detects c:\Server_Dev for Codyte mode)

## Quick Start

### Generic Project Usage

```powershell
/goal "Refactor auth module with security hardening + perf optimization"

→ Skill activation (generic mode)
→ Goal decomposition via /goal-plan
→ 5-10 agents spawned (planner, security, coder, reviewer, monitor)
→ Context reuse from v3-memory
→ Real-time cost tracking via cost-optimize

Results:
✅ 60-80% token savings
✅ 2.5-4x wall-clock speedup
✅ Full cost transparency
✅ Quality gates before completion
```

### Codyte Project Usage (Auto-Detected)

```powershell
/goal "Add semantic search to conversation detail endpoint (tenant-aware)"

→ Skill activation (Codyte mode auto-detected in c:\Server_Dev)
→ Goal decomposition via /goal-plan + tenant isolation checkpoint
→ 5-10 agents spawned (planner, security, coder, reviewer, monitor)
→ Context reuse from v3-memory (per-tenant HNSW indexing)
→ Real-time cost tracking via cost-optimize
→ Mandatory security review (/security-review skill for public routes)
→ CLAUDE.md compliance verification

Results:
✅ 60-80% token savings
✅ 2.5-4x wall-clock speedup
✅ 100% tenant isolation enforcement
✅ Full audit trail (metadata_json)
✅ Zero secrets leaked
✅ CLAUDE.md compliance verified
✅ All smoke scripts passing
```

## Mode Detection: Universal + Codyte-Specialized

This skill is **unified** — handles both generic projects AND Codyte with automatic mode switching.

| Feature | Generic Mode | Codyte Mode (Auto-Detected) |
|---------|----------|--------------------------|
| **Cost Optimization** | MANDATORY (all projects) | MANDATORY (all projects) |
| **Goal Decomposition** | MANDATORY (all projects) | MANDATORY (all projects) |
| **Tenant Isolation** | Optional | **MANDATORY** (every query, every layer) |
| **Multi-Unit Entitlement** | N/A | **MANDATORY** (automation_enabled + billing_status) |
| **n8n Integration** | Optional | **MANDATORY** (Decision + Commitment contracts) |
| **Audit Trail** | Optional | **MANDATORY** (metadata_json full population) |
| **Security Review** | Optional | **MANDATORY** (for public routes) |
| **Database Context** | Generic | Codyte-specific (tenants, tenant_units, conversations) |
| **Memory V3 Factory** | Supported | Per-tenant factory **enforced** |
| **CLAUDE.md Compliance** | N/A | **MANDATORY** (architecture tenets) |

**How It Works:**
- Working in `c:\Server_Dev`? → Codyte mode activated automatically
- Working elsewhere? → Generic mode (all core features, no Codyte constraints)
- Can override: explicitly set `--mode generic` or `--mode codyte` if needed

## Mandatory Practices (Codyte Tenets)

1. **Tenant Isolation** — `WHERE tenant_id = ?` in all queries; Memory V3 factory enforcement; cross-tenant tests
2. **Multi-Unit Entitlement** — Check `automation_enabled + billing_status` before Decision/Commitment
3. **n8n Webhook Contracts** — Decision + Commitment validation; no direct n8n calls from channels
4. **Audit Trail Completeness** — metadata_json: dispatcher_execution_id, tenant_id, route_final, commitment_status, fallback_reason
5. **Public Route Security** — `/security-review` skill required for `/site/chat`, `/chat/inbound`, `/channels/inbound`
6. **Testing** — All tests passing; cross-tenant isolation verified; contracts validated; smoke scripts green
7. **Code Quality** — No secrets in code; CLAUDE.md compliance; git status clean (no .env, no v1/, no artifacts)

## Files

- **SKILL.md** (900+ lines) — Complete Master Orchestrator specification
  - Codyte architecture context (FastAPI, PostgreSQL, n8n, Memory V3)
  - Mandatory practices enforcement
  - Goal-driven execution flow with tenant isolation checkpoint
  - Agent assignments (Planner, Security, Coder, Reviewer, Monitor)
  - Success metrics (tenant isolation, cost savings, security, compliance)

- **skill.json** — Metadata, required/optional skills, Codyte context mappings
  - Backend structure: routes, database, middleware, tests, smoke scripts
  - Integration points: Memory V3, n8n webhooks, audit trail
  - Mandatory practices checklist

- **README.md** — This file

## Sub-Agents (Codyte-Aware)

| Agent | Domain | Model | Codyte Responsibilities |
|-------|--------|-------|--------------------------|
| **Planner** | Timeline + Resource | Sonnet | Database migration order, n8n webhook sequencing, multi-unit impact |
| **Security** | Threat + Compliance | Sonnet | Input validation, tenant isolation audit, rate limiting, PCI DSS (if payments) |
| **Coder** | Implementation | Sonnet/Opus | Routes (FastAPI), schemas (Pydantic), DB CRUD, Memory V3 factory, tests |
| **Reviewer** | QA Gate | Haiku | Verify: tenant isolation (WHERE clause), no credential leaks, tests pass, CLAUDE.md compliance |
| **Monitor** | Progress + Metrics | Haiku | Test results, contract validation, smoke script status, tenant filter enforcement |

## Integration Points

### 1. Tenant Isolation (MANDATORY)
- Every database query: `WHERE tenant_id = ?`
- Memory V3: Factory pattern `get_memory_service(tenant_id)` enforced at `src/core/memory_factory.py`
- Redis keys: Include tenant_id (e.g., `f"conv:{tenant_id}:{conv_id}"`)
- Tests: Cross-tenant queries must return empty

### 2. Multi-Unit Entitlement (MANDATORY)
- Before Decision/Commitment webhooks: Check `automation_enabled` and `billing_status`
- If automation disabled → Return fallback (no n8n call)
- Audit trail: Log `fallback_reason` to `metadata_json`
- Implementation pattern: `src/middleware/billing_guard.py`

### 3. n8n Webhook Contracts (MANDATORY)
- **Decision:** Input `SiteChatRequest`, Output `{route, next_action}`
- **Commitment:** Input `{conversation_id, ...}`, Output `{commitment_status, commitment_id}`
- Validation: `src/core/orchestrator.py` webhook handlers
- Smoke tests: `./scripts/run-decision-smoke.ps1`, `./scripts/run-commitment-smoke.ps1`

### 4. Audit Trail (MANDATORY)
- `metadata_json` persists on every conversation:
  - `dispatcher_execution_id` (unique request ID)
  - `tenant_id`, `conversation_id`, `client_id`, `unit_id`
  - `channel`, `source`, `inbound_path`
  - `route_final`, `next_action_final`, `commitment_status`
  - `fallback_reason` (if automation skipped)
  - `workflow_name`, `delivery_status`

### 5. Security Review (MANDATORY for Public Routes)
- Routes: `/site/chat`, `/chat/inbound`, `/channels/inbound`
- Skill: `/security-review` validates input, XSS, CSRF, tenant isolation, rate limiting, no secrets
- Additional smoke tests: `./scripts/test-site-chat.ps1`, `./scripts/run-edge-security-smoke.ps1`

### 6. Memory V3 Integration
- Per-tenant SQLite: `agent_memory_{tenant_id}.db`
- HNSW indexing: 384-dim, M=16, ef=200
- Semantic search: 150x-12.5kx speedup
- Files: `src/agent_db_adapter.py`, `src/memory_service.py`, `src/core/memory_factory.py`

## Example Goal (Codyte)

```
/goal "Add memory search to conversation detail endpoint"

CONTEXT INJECTED:
  ├─ Project root: c:\Server_Dev
  ├─ Backend: FastAPI (app.py)
  ├─ Routes: routes/site.py, routes/channels.py
  ├─ Database: PostgreSQL (tenants, conversations, messages)
  ├─ Memory: v3-memory-unification (per-tenant HNSW)
  └─ Tests: test_security_unit.py, test_regression_full.py

OUTPUT:
  ├─ SG1: Design schema (embeddings + per-tenant isolation)
  ├─ SG2: Implement /conversations/{id}/search route (tenant filter)
  ├─ SG3: Integrate memory-search + v3-memory-unification
  ├─ SG4: Tests (unit + integration + cross-tenant isolation)
  ├─ SG5: Contract docs update
  ├─ SG6: Security audit (/security-review)
  └─ SG7: Smoke verification

TENANT ISOLATION CHECKPOINT (Before Agent Spawn):
  ✅ Goal scoped to single tenant? YES
  ✅ New route will filter by tenant_id? YES → Add WHERE tenant_id = ? to query
  ✅ Tests include cross-tenant validation? YES → Add test_cross_tenant_memory_search
  
→ All checks PASS → Agents spawned
```

## Success Metrics

✅ **Tenant Isolation** — 100% of queries filter by tenant_id; cross-tenant tests pass  
✅ **Multi-Unit Entitlement** — automation_enabled + billing_status validated before webhooks  
✅ **Cost Optimization** — 60-80% token savings via parallelization + context reuse  
✅ **Security** — /security-review passes; no XSS, CSRF, injection; no secrets leaked  
✅ **Compliance** — metadata_json fully populated; audit trail complete; CLAUDE.md rules enforced  
✅ **Quality** — All tests pass; contracts validated; smoke scripts green  
✅ **Wall-Clock** — 2.5-4x speedup vs serial execution  

## Before You Merge

```powershell
# 1. Syntax check
python -m py_compile .\backend\app.py

# 2. Rebuild
docker compose up -d --build backend

# 3. Health check
.\scripts\healthcheck.ps1

# 4. Run targeted smoke
.\scripts\test-site-chat.ps1 -TenantId test_tenant

# 5. Run security review (if added/modified public routes)
# (use /security-review skill in Claude Code)

# 6. Full regression (optional, but recommended)
.\scripts\run-local-regression.ps1 -SkipBuild -IncludeWhatsapp -IncludeMultiunit -IncludeExposure -IncludeEdgeSecurity

# 7. Check git status
git status --short
# (no .env, no v1/, no artifacts)

# 8. Review diff
git diff
```

## Anti-Patterns (What NOT to Do)

❌ **No tenant isolation check** — Every query MUST filter by tenant_id  
❌ **Hardcoded unit IDs** — Always parameterize (no `WHERE unit_id = 'unit_123'`)  
❌ **Direct n8n calls from channels** — All via backend webhooks  
❌ **Skipping multi-unit entitlement** — Always check `automation_enabled + billing_status`  
❌ **Silent fallback** — If automation skipped, log `fallback_reason` to `metadata_json`  
❌ **Public route without /security-review** — All routes in /site/chat require security audit  
❌ **Missing cross-tenant test** — Every DB change must include `test_cross_tenant_*`  
❌ **Ignoring CLAUDE.md** — Skill enforces via agent checklist; no exceptions  

## Key Files & Directories

```
backend/
  app.py                           # FastAPI entrypoint
  src/
    core/
      database.py                  # PostgreSQL schema (SCHEMA_SQL)
      orchestrator.py              # Request/response pipeline
      memory_factory.py            # Memory V3 factory (tenant-aware)
    database/                      # CRUD operations
    routes/
      site.py                      # /site/chat (canonical inbound)
      channels.py                  # /chat/inbound, /channels/inbound
      orchestrator.py              # Webhook handlers (Decision, Commitment)
    middleware/
      rbac_guard.py                # RBAC enforcement
      billing_guard.py             # Multi-unit entitlement check
      security.py                  # Security headers, input validation
    agent_db_adapter.py            # Memory V3 storage (SQLite + HNSW)
    memory_service.py              # Memory V3 interface
  test_*.py                        # 23 test suites
  requirements.txt                 # Python dependencies

scripts/
  test-site-chat.ps1               # Smoke test /site/chat
  run-decision-smoke.ps1           # Decision workflow test
  run-commitment-smoke.ps1         # Commitment workflow test
  run-edge-security-smoke.ps1      # nginx security test
  run-local-regression.ps1         # Full regression

docs/
  PLANO_MAE.md                     # Development governance
  contracts/                       # API contracts
  architecture/                    # Design docs (v3-memory-unification, etc.)
```

## Support & Questions

- **CLAUDE.md** (Codyte rules): `c:\Server_Dev\CLAUDE.md`
- **Architecture Overview**: `c:\Server_Dev\docs\architecture\`
- **API Contracts**: `c:\Server_Dev\docs\contracts\`
- **Author Email**: carloseduortizzxcv0987@gmail.com
- **Project Repo**: `C:\Server_Dev` (primary) | `C:\Server` (operational backup)

---

**Ready to architect Codyte features with tenant isolation + cost optimization. Let's go!** 🚀
