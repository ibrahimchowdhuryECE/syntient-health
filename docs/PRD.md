# AI Medical Assistant Chatbot — Product Requirements Document (PRD)

**Version:** 1.0  
**Prepared by:** Development Team  
**Date:** December 2024  
**Status:** Draft  

---

## 1) Executive Summary

Large hospitals and multi-clinic networks face significant appointment backlogs that allow low-urgency visits to crowd out high-risk cases. This project delivers an AI-driven, human‑supervised appointment and triage system composed of three specialized models:

1. **Diagnosis Model (DM)** — performs structured clinical reasoning, returns a differential diagnosis, red‑flag status, an urgency band, a calibrated confidence score, and a rationale based on clinic-specific guidelines retrieved via RAG.
2. **Medical Assistant Model (MAM)** — conducts the patient conversation professionally, gathers required information identified by DM, confirms understanding, and communicates next steps.
3. **Clash Management Model (CMM)** — optimizes slot assignment under hospital policies, resolves scheduling conflicts, and orchestrates voluntary reschedules when triage slots are exhausted.

An Orchestrator coordinates models, EMR/scheduling integrations, audit logging, and safety gates. The system prioritizes urgent cases without "bumping" patients by default; instead it uses dedicated triage slots, voluntary moves, overflow policies, or human escalation.

**Primary outcomes:** reduced time‑to‑slot for urgent cases, lower administrative burden, higher throughput, and auditable safety.

---

## 2) Goals & Non‑Goals

### 2.1 Goals

* **Prioritize urgency:** Ensure high‑risk cases receive time‑appropriate appointments.
* **Reduce workload:** Automate repetitive intake and scheduling decisions with human oversight.
* **Continuity:** Always reference prior encounters to inform current routing and urgency.
* **Transparency & safety:** Confidence‑based flagging, red‑flag short‑circuits, and rationale logging.
* **Modularity:** Adapt to each hospital's guidelines via RAG; avoid per‑site LLM fine‑tunes.

### 2.2 Non‑Goals (v1)

* Treatment recommendations or clinical management beyond routing/booking instructions.
* Showing patients their internal risk scores/priority ranking.
* Fully automated rescheduling without consent (default is voluntary move campaigns).

---

## 3) Scope

### 3.1 In‑Scope (v1)

* Conversational intake for appointment requests (web, mobile, kiosk; voice in later phase).
* DM reasoning with sufficiency gating (no firm output until required fields present).
* RAG over clinic/hospital guidelines and pathways with versioned citations.
* Urgency bands: **U1 (Immediate/ER), U2 (24–48h), U3 (≤14d), U4 (routine/virtual)**.
* CMM scheduling against triage vs routine slot rules; voluntary reschedule campaigns; overflow escalation to staff when needed.
* EMR/EHR and scheduling integration where APIs exist; agent UI fallback where they don't.
* Audit logs, model rationales, and staff override workflow.

### 3.2 Out‑of‑Scope (v1)

* Demographic features in risk/urgency ranking (use symptoms and PMH only).
* Cross‑facility patient transfer orchestration.
* Billing/claims automation.

---

## 4) Stakeholders & Users

* **Patients:** request appointments; receive guidance for ER/urgent care when applicable.
* **Triage staff / nurses:** review flagged cases, red‑flags, and exceptions.
* **Scheduling/admin teams:** supervise CMM outputs, approve overflow and voluntary move campaigns.
* **Clinicians:** receive structured pre‑visit summaries in EMR; audit rationale when needed.
* **Hospital IT & Compliance:** manage integrations, security, PHIPA/HIPAA/GDPR compliance.

---

## 5) Assumptions & Dependencies

* Clinics/hospitals provide current triage pathways and slot policies.
* At least read/write access to EMR problem lists/encounters or a parallel data store; scheduling API or agent UI available.
* English language for v1; multilingual and voice/IVR in later phases.
* Data usage agreements in place; hospital legal approves scope (triage/booking vs medical advice).

---

## 6) High‑Level Architecture

**Orchestrator** coordinates the following components:

* **Diagnosis Model (DM):** structured clinical reasoning and urgency banding.
* **Medical Assistant Model (MAM):** patient communication and data collection.
* **Clash Management Model (CMM):** scheduling optimization and conflict resolution.
* **RAG subsystem:** vector KB of versioned guidelines/pathways; retrieval before DM inference.
* **EMR/EHR connector:** prior history retrieval, encounter/summary write‑back.
* **Scheduling connector:** real‑time availability checks and booking; agent console fallback.
* **Audit & analytics store:** decisions, rationales, metrics, and model outputs.
* **(Optional) Federated learning:** site‑local training with gradient aggregation (no PHI exfiltration).

---

## 7) Functional Requirements

### 7.1 Intake & Consent

* **FR‑1:** Present clear consent and scope (booking/triage only; no treatment advice); capture patient identity and consent.
* **FR‑2:** Collect presenting complaint via free text; classify to a symptom pathway.
* **FR‑3:** Retrieve prior encounters and relevant PMH/meds/allergies from EMR when permitted.

### 7.2 Diagnosis Model (DM)

* **FR‑4:** On each turn, DM returns: `info_sufficient` (bool), `missing_fields` (list), `red_flags` (list), `differential` (Dx + probability), `urgency_band` (U1–U4), `confidence` (0–1), and a succinct `rationale` with guideline citations.
* **FR‑5:** DM must not emit a firm urgency band or diagnosis until `info_sufficient=true` for that pathway's required fields. If any red‑flag criteria hit, DM can set U1 immediately.
* **FR‑6:** Per‑pathway required fields (examples):

  * **Chest pain:** onset, character, radiation, exertional nature, dyspnea, diaphoresis, risk factors, vitals.
  * **Headache:** onset/thunderclap, neuro deficits, fever/neck stiffness, age, pregnancy/anticoagulants, pattern change.
  * **Shortness of breath:** onset, triggers, cough/fever, chest pain, wheeze, leg swelling, PMH (asthma/COPD/CHF), recent surgery/travel.
* **FR‑7:** DM cites guideline version/section used via RAG; store citation IDs in log.

### 7.3 Medical Assistant Model (MAM)

* **FR‑8:** Ask only for items in `missing_fields`; avoid medical jargon; confirm understanding and summary before finalize.
* **FR‑9:** Communicate ER/urgent instructions verbatim from hospital policy when DM sets U1; notify staff.
* **FR‑10:** Produce a finalized structured encounter for DM re‑evaluation.

### 7.4 Clash Management Model (CMM)

* **FR‑11:** Given `{urgency_band, constraints, availability, policy}`, propose top‑K slots; respect provider specialty, location, hours, and triage vs routine quotas.
* **FR‑12:** If triage slots exhausted: (a) create **Pending‑Urgent** ticket for staff, (b) optionally trigger **voluntary reschedule campaign** to U3/U4 patients using approved templates and incentives, (c) request overflow approval from admin per policy.
* **FR‑13:** No forced bumping by default. If hospital policy allows targeted bumping, require human approval and full audit trail.

### 7.5 Orchestrator & State Machine

* **FR‑14:** Maintain per‑encounter state: `INTAKE → MISSING_INFO → SUFFICIENCY → URGENCY → SCHEDULING → CONFIRM → WRITEBACK`.
* **FR‑15:** When DM confidence < pathway threshold, auto‑flag to **Triage Review** queue with priority.
* **FR‑16:** Write appointment and triage summary back to EMR; store audit log with rationale and citations.

### 7.6 RAG Subsystem

* **FR‑17:** Ingest guidelines/pathways as versioned, chunked documents with metadata (facility, department, version, effective dates).
* **FR‑18:** Retrieve top‑N relevant chunks for the current pathway; pass to DM as context; include `guideline_id` and `section` in DM outputs.
* **FR‑19:** Support hot updates without redeploying models; enforce document validity windows.

### 7.7 Integrations

* **FR‑20:** EMR/EHR (read PMH/meds/allergies; write encounter summary and disposition).
* **FR‑21:** Scheduling API (search availability, place/modify/cancel bookings) or agent UI for manual execution when no API exists.
* **FR‑22:** Notification channels (SMS/email/IVR) for confirmations and voluntary reschedule outreach.

---

## 8) Data Contracts (Schemas)

### 8.1 MAM → DM (encounter update)

```json
{
  "patient_id": "P123",
  "presenting_complaint": "headache",
  "structured_fields": {
    "onset": "gradual",
    "duration_days": 10,
    "neuro_deficits": false,
    "fever": false,
    "age": 34,
    "pregnant": false,
    "anticoagulants": false,
    "pattern_change": true
  },
  "free_text": "Throbbing right-sided, light sensitivity."
}
```

### 8.2 DM → Orchestrator (final)

```json
{
  "info_sufficient": true,
  "red_flags": [{"name": "acute neuro deficit", "present": false}],
  "differential": [
    {"dx": "Migraine", "prob": 0.56},
    {"dx": "Tension-type headache", "prob": 0.28},
    {"dx": "Temporal arteritis", "prob": 0.06}
  ],
  "urgency_band": "U2",
  "confidence": 0.74,
  "rationale": "Progressive unilateral throbbing, photophobia, no red flags; age <50.",
  "citations": [{"guideline_id": "HOSP_X_HEADACHE_v3.2", "section": "3.1"}]
}
```

### 8.3 Orchestrator → CMM (scheduling request)

```json
{
  "patient_id": "P123",
  "urgency_band": "U2",
  "duration_window_hours": 48,
  "preferences": {"days": ["Fri"], "times": ["AM"]},
  "constraints": {"location": "Main Campus", "provider_type": "GP"},
  "policy_refs": ["TRIAGE_RULES_v1.4"]
}
```

### 8.4 CMM → Orchestrator (response)

```json
{
  "proposals": [
    {"slot_id": "A-2025-08-29-0930", "provider": "GP-12", "fit_score": 0.92}
  ],
  "reschedule_plan": {
    "candidate_ids": ["appt_7812", "appt_7890"],
    "contact_method": "sms",
    "message_template_id": "VOLUNTARY_MOVE_24H"
  },
  "fallback": "ESCALATE_TO_HUMAN_DISPATCH"
}
```

---

## 9) Non‑Functional Requirements

### 9.1 Security & Privacy

* PHIPA/HIPAA/GDPR compliant; data minimization; explicit consent flows.
* Encryption in transit (TLS 1.2+) and at rest (AES‑256+).
* RBAC with least privilege; SSO/OIDC for staff; IP allow‑listing for admin tools.
* Data locality per jurisdiction; configurable retention and purge policies.
* Full audit trail (who/what/when/why, including retrieved guideline versions).

### 9.2 Safety & Clinical Governance

* Per‑pathway confidence thresholds (e.g., chest pain 0.90, rash 0.60) with quarterly review.
* Red‑flag short‑circuit to U1 and ER instruction templates.
* Staff override at every decision point; mandatory override reason logging.
* Regular calibration checks (Brier score, ECE); temperature/Platt scaling as needed.

### 9.3 Performance & Reliability

* P95 response time ≤ 2.5s for MAM turns; ≤ 3.5s when DM + RAG active; scheduling search ≤ 2.0s.
* Concurrency: ≥ 10k active conversations; autoscaling of inference and retrieval services.
* Availability: ≥ 99.5% monthly; graceful degradation to human workflows on outage.

### 9.4 Observability & Ops

* Metrics: time‑to‑slot by urgency, flag rates, agree/disagree with clinicians, overflow frequency, reschedule acceptance.
* Tracing across orchestrator, DM/MAM/CMM, RAG, EMR, scheduling connectors.
* Alerting on spikes in U1 flags, confidence dips, or connector failures.

---

## 10) Decision Rules & Policies

* **Urgency taxonomy:** U1 (Immediate/ER), U2 (24–48h), U3 (≤14d), U4 (routine/virtual).
* **Triage slot policy encoding:** JSON rules defining quotas by department/day; effective windows; overflow approvals.
* **Reschedule campaign policy:** consented, voluntary; approved message templates; optional incentives (e.g., parking voucher, telehealth credit).
* **Demographics use:** excluded from ranking in v1.

---

## 11) Patient Experience (PX)

* Professional, empathetic tone; avoids jargon; summarizes back to patient for confirmation.
* Clear ER instructions when applicable; avoid disclosing internal priority/risk scores.
* Accessibility (WCAG 2.1 AA) for web/kiosk; voice/IVR path planned for v2.

---

## 12) Operational Workflows

* **Triage Review queue:** auto‑populated when confidence < threshold or conflicts in guideline retrieval.
* **Admin console:** view proposed slots, voluntary move candidates, overflow approvals.
* **Clinician view (EMR):** concise pre‑visit summary (presenting complaint, required info, urgency, rationale, citations).

---

## 13) KPIs & Targets

* **Clinical:** ≥ 85% agreement with clinician urgency; red‑flag miss rate ≤ 0.5% of red‑flagged cases.
* **Operational:** median time‑to‑slot for U1/U2 reduced ≥ 20% vs baseline; ≥ 30% reduction in manual intake touches; ≥ 70% clash auto‑resolution.
* **Experience:** Patient CSAT ≥ 4.5/5; average questions to sufficiency ≤ 8 for top pathways.

---

## 14) Rollout Plan

* **Phase 1 (MVP):** Top 5 pathways (chest pain, headache, shortness of breath, abdominal pain, medication refill); agent UI fallback; single‑site pilot; calibration runs.
* **Phase 2:** EMR write‑back at scale; triage/admin consoles; multilingual; voice/IVR; overflow automation.
* **Phase 3:** Federated learning; multi‑site deployment; advanced backlog analytics; predictive no‑show mitigation.

---

## 15) Test & Acceptance Criteria

* **Safety tests:** red‑flag scenarios route to U1 with ≥ 95% sensitivity; no unsafe U4 for red‑flags.
* **Calibration:** ECE ≤ 0.05 in validation; stable across top pathways.
* **RAG correctness:** ≥ 98% of decisions cite the correct versioned guideline sections.
* **Scheduling:** ≥ 99% booking API success; fallback to agent UI within 60s on connector failure.
* **UX:** Task success rate ≥ 90%; comprehension checks passed by ≥ 95% of users in testing.

---

## 16) Risks & Mitigations

* **Guideline drift/outdated docs:** enforce versioning and expiry; alerts on expiring policies.
* **Data sparsity in pilots:** bootstrap with public pathways; clinician‑authored synthetic cases for calibration.
* **Staff distrust/override fatigue:** succinct rationales; metrics on agreement; regular feedback loops.
* **Connector downtime:** cached availability, graceful degradation, and dispatch queue for agents.

---

## 17) Open Questions (to resolve before build freeze)

1. Finalize per‑pathway required fields and thresholds (initially conservative).
2. Define hospital slot policy JSON schema and governance for updates.
3. Decide incentives/constraints for voluntary reschedule campaigns.
4. Confirm EMR objects for write‑back (encounter note vs custom section).
5. Determine data retention windows and deletion SLAs per jurisdiction.

---

## 18) Appendices

### A. Example Red‑Flag Lists (abridged)

* **Chest pain:** hemodynamic instability, ongoing severe pain, dyspnea at rest, syncope, new neuro deficits.
* **Headache:** thunderclap onset, fever/neck stiffness, focal neuro signs, papilledema, pregnancy/post‑partum, age >50 with new headache.
* **SOB:** hypoxia, chest pain with risk factors, unilateral leg swelling with pleuritic pain, post‑op dyspnea.

### B. Example ER Instruction Template

> Your symptoms may indicate an urgent condition. Please proceed to the nearest Emergency Department now. We have notified the hospital triage team. Bring your medications and ID. If you have severe symptoms during transit, call emergency services.

### C. Federated Learning (optional v3)

* Site‑local fine‑tuning on de‑identified features with gradient aggregation; privacy‑preserving techniques (e.g., secure aggregation); no raw PHI leaves hospital boundary.

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | Dec 2024 | Development Team | Initial PRD draft |

---

**Document Status:** Draft  
**Next Review:** January 2025  
**Approval Required:** Product Manager, Technical Lead, Legal/Compliance
