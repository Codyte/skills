# Codyte profile

Auto-load this profile when the project root is `c:\Server_Dev`. It overlays the universal
lifecycle in [../SKILL.md](../SKILL.md) with Codyte's non-negotiable rules. These become
**mandatory Phase-4 review gates** and must be reflected in each agent's `plan.md` when relevant.

Source of truth for these rules: `c:\Server_Dev\CLAUDE.md`.

---

## Architecture context (inject into agent plans)

- **Backend:** FastAPI (`backend/app.py`) — source of truth for all state.
- **Database:** PostgreSQL — conversations, messages, commitments, tenants, tenant_units.
- **Orchestration:** n8n — Decision + Commitment webhooks only (never the source of truth).
- **Memory V3:** per-tenant HNSW via factory `get_memory_service(tenant_id)` (`MEMORY_V3_ENABLED`,
  **on in prod**). Embeddings via **OpenAI** `text-embedding-3-small` truncated to 384d
  (`EMBEDDING_PROVIDER=openai`, `EMBEDDING_DIMENSIONS=384`); recall drops hits below
  `MEMORY_V3_SCORE_FLOOR` (0.35). Embeddings use `OPENAI_API_KEY` **regardless of `AI_OPENAI_ENABLED`**
  (that flag is chat-only; chat is Gemini). No random-vector fallback — embedding failure re-raises.
- **AI chat:** provider chain (`AI_PROVIDER`/`AI_PROVIDER_CHAIN`), Gemini first (`gemini-2.5-flash`,
  not flash-lite) → OpenAI fallback. Customer-chat model is per-plan; owner assistant fixed.
- **RBAC:** tenant roles `viewer<agent<admin<owner` (rank-based) + platform roles
  `platform_admin/master/ops`. `admin@codyte.com` is the single **master** (only account with
  Plans×Features). `users_role_check` must list all 7 roles; the owner-backfill must never demote
  platform staff (see anti-patterns).
- **Cache:** Redis (optional). **Edge:** nginx (rate limiting, route blocking, security headers).
- **Channels:** Site (HTML/CSS/JS), WhatsApp (Node adapter) — all converge to backend inbound routes.

## Mandatory tenets

1. **Backend is source of truth** — all state in PostgreSQL; n8n orchestrates only.
2. **Tenant isolation** — every query filters `WHERE tenant_id = ?`; Memory V3 post-filters by tenant.
3. **Multi-unit entitlement** — check `automation_enabled` + `billing_status` before Decision/Commitment.
4. **Canonical inbound routes** — `/site/chat`, `/chat/inbound`, `/channels/inbound` only.
5. **Audit trail** — every interaction logged to `metadata_json`.
6. **No public n8n** — nginx blocks `/n8n`, `/webhook`, `/webhook-test`.
7. **Feature flags via `.env`** — defaults in `config.py`; no hardcoded toggles.
8. **RBAC integrity** — never narrow `users_role_check` to drop platform roles; never demote
   `master`/`platform_admin`/`ops` in any backfill. Auth/role changes are a *Forbidden autonomous
   action* (propose + `/security-review`).
9. **Schema fixes via idempotent `ALTER` in `lifespan.py`** — the DB has constraints from the
   Alembic baseline that are NOT in `schema.sql`; fix them there, idempotently (precedent:
   `users_role_check`, owner role).

---

## Planning overlay (Phase 1)

Before partitioning, answer per goal and record in `master-plan.md`:
- Public route touched? (`/site/chat`, `/chat/inbound`, `/channels/inbound`) → security review is mandatory.
- Tenant isolation impact? → which queries gain `WHERE tenant_id = ?`.
- n8n integration? → which webhook contracts (Decision / Commitment) are involved.
- Multi-unit gate relevant? → `automation_enabled` + `billing_status` checks.
- Schema change? → preserve `tenant_id` in any new table; add a cross-tenant test.

Each affected agent's `plan.md` must spell out the specific isolation / audit / contract obligations
for the files in its scope.

---

## Mandatory review gates (Phase 4)

The goal is NOT complete until all that apply pass:

1. **Tenant isolation** — every new/modified query filters by `tenant_id`; Memory V3 uses the
   factory; Redis keys include `tenant_id`; cross-tenant queries return empty.
   - **Memory V3 (if touched):** provider stays `openai`@384d consistent with the existing index
     (changing provider/dim invalidates `agent_memory_*.db` — different vector space); `OPENAI_API_KEY`
     is valid (a 401 silently no-ops recall); no random-vector fallback reintroduced.
   - **RBAC (if auth/roles touched):** `users_role_check` still lists all 7 roles; no backfill
     demotes platform staff; `admin@codyte.com` is still `master`. Confirm in DB after any boot.
2. **Multi-unit entitlement** — Decision/Commitment paths check `automation_enabled` +
   `billing_status`; skipped automation logs `fallback_reason`.
3. **n8n contracts** — Decision (`SiteChatRequest` → `{route, next_action}`) and Commitment
   (`{conversation_id, …}` → `{commitment_status, commitment_id}`) verified in `orchestrator.py`;
   no direct n8n calls from channels.
4. **Audit trail** — `metadata_json` populated: `dispatcher_execution_id`, `tenant_id`,
   `conversation_id`, `unit_id`, `channel`, `inbound_path`, `route_final`, `commitment_status`,
   `fallback_reason`, `workflow_name`, `delivery_status`; preserved on updates.
5. **Public route security** — run `/security-review`; input validation (SiteChatRequest), rate
   limiting, XSS/CSRF, no secrets echoed.
6. **Tests** — relevant suites pass:
   - `test_security_unit.py`, `test_regression_full.py`
   - `test_memory_unification.py` (if Memory V3 involved)
   - `test_webhooks_tenant_validation.py` (tenant isolation)
   - smokes: `.\scripts\test-site-chat.ps1`, `.\scripts\run-edge-security-smoke.ps1`,
     `.\scripts\run-decision-smoke.ps1`, `.\scripts\run-commitment-smoke.ps1`
7. **Hygiene** — `python -m py_compile .\backend\app.py`; no secrets in code;
   `git status --short` clean (no `.env`, no `v1/`, no `.swarm/`, no test-output artifacts).

---

## Codyte anti-patterns

- ❌ Query without `WHERE tenant_id = ?`.
- ❌ Hardcoded unit IDs.
- ❌ Direct n8n calls from channels.
- ❌ Skipping multi-unit entitlement.
- ❌ Silent fallback without `fallback_reason` in `metadata_json`.
- ❌ Public route changed without `/security-review`.
- ❌ DB change without a cross-tenant test.
- ❌ `docker compose restart` after editing `.env` — restart keeps the OLD env; the container only
  picks up new values via `up -d --force-recreate`. (Verify with `docker exec <c> sh -c 'echo $VAR'`.)
- ❌ Narrowing `users_role_check` or demoting platform staff in a backfill (locked out the master account).
- ❌ Reintroducing a random-vector embedding fallback (permanently poisons the HNSW index).
- ❌ Running `docker compose` from `c:\Server_Dev` (uses dev `.env`, recreates the wrong
  postgres/redis, takes prod down). Dev = project `server_dev`:8001; prod = `server`:8000.
- ❌ Deploying or deleting autonomously — see *Forbidden autonomous actions* in SKILL.md.

---

## Warm start (Phase 1 + every worker)

Codyte concretizes the universal warm-start rule (SKILL.md, Phase 2). Before any wide search, read:
1. `C:\Users\Carlos_Ortiz\.claude\projects\c--Server-Dev\memory\MEMORY.md` — durable non-obvious facts
   (deploy rules, role model, V3 embeddings, restart≠recreate, Gemini model, etc.);
2. the `__navi__.md` of each folder in scope (backend/src, dashboard/src, docs, scripts, …);
3. `docs/pendencias-<latest>.md` (currently `pendencias-2026-06-10.md`).
Then DON'T re-explore what those establish. `CLAUDE.md` is the source of truth for all rules.

## Timeline logging

After the goal closes, append an entry to `c:\Server_Dev\docs\worklogs\agent-timeline.md`
(objective, work done, files touched, validation, status, next step) per CLAUDE.md.
**Rotation:** that file grows unbounded (already >1400 lines). If it exceeds ~1500 lines, the
orchestrator proposes (in `review.md`) splitting the older half into
`docs/worklogs/agent-timeline-<period>.md` — a *proposal*, not an autonomous move (it's under `docs/`,
and archiving is a human-reviewed cleanup, per the docs-triage pattern).
