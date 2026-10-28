# Experiment 19 — Verification Outcome Integrity

**Status:** Offline-validated implementation and retrospective controlled protocol, 28 October 2026. **No full live E2E validation of the treatment.**

Owner: Tasneem's independent Mini Hivo validation/implementation workstream. The inherited system and Experiments 1–18 retain their original authorship. No other contributor's independent implementation is incorporated.

## Research question and hypothesis

Can Mini Hivo preserve verification outcomes across bounded evidence projection, structured parsing, route aggregation and chronological receipt supersession without manufacturing PASS or permanently rejecting valid fresh success?

Hypothesis: bounded valid structured summaries and conservative outcome interpretation prevent false PASS in the declared protocol, while preserving legitimate PASS and valid newer equivalent results. Unknown/unavailable evidence must not erase an outstanding FAIL. This concerns interpretation of evidence, not whether the original behavioral oracle tests every requirement.

## Original observation and confirmed cause

Coin Courier Run-010 used baseline `2a8b94590734cec3375047a18e0dc71df2476f85` with `gemma4:e4b`. Required game checks failed because `AGENT_GAME` was missing and keyboard/collection checks did not execute. The preserved native trace records:

| Native line | Observation |
|---|---|
| 120 | Child 1 required browser route FAIL |
| 121 | Aggregation `passed: true`, browser result PASS, retaining `actual_result: FAIL` |
| 122 | Separate deterministic quality gate FAIL |

SQLite tool events 9/10 contain failed game-verification payloads exceeding the 1,600-character evidence bound. `execute_agent_task` stored `str(result)[:1600]`; the clipped JSON was incomplete. `_parse_result` fell back to lexical success matching, including the field name `passed` despite a false value. Aggregation could prioritize that apparent PASS over the separate failed browser check.

The final gate still rejected this child. Incorrect intermediate aggregation is not a successful transaction and is not excused by a later rejection. Run-010 ended by supervised interruption, not normal root acceptance; the partial game is not included here.

## Baseline, treatment and intervention

| Arm | Immutable revision |
|---|---|
| Baseline | `2a8b94590734cec3375047a18e0dc71df2476f85` |
| Treatment | `f8bf65ece895f70c1b572b59df229314de09afbe` |

The baseline includes prior work reviewed separately in [team PR #7](https://github.com/kareem232003/mini_hivo/pull/7). Experiment 19 is only the delta after that revision; this does not re-evaluate its earlier fixes.

- [`hivo/evidence.py`](../../hivo/evidence.py), `project_tool_evidence_result`: bounded valid summaries retain supported outcome/target/profile/identity fields. Unrepresentable proof becomes unavailable rather than a clipped positive claim. Full original transcripts remain the diagnostic source.
- [`mini.py`](../../mini.py), `execute_agent_task`: use that projection and record producing role. Raw model-facing tool output remains unchanged.
- [`hivo/verification_routing.py`](../../hivo/verification_routing.py), `_parse_result`: malformed/incomplete structured evidence cannot acquire PASS through keyword fallback; explicit failure dominates conflicting success.
- `_evidence_matches`: match browser targets rather than just tool names.
- `_aggregate_verification_routes`: retain current browser failure, reject cached labels without proof, and allow supersession only for available valid outcomes within the same explicit role/target/profile in receipt order.
- [`tests/test_verification_outcome_integrity.py`](../../tests/test_verification_outcome_integrity.py): producer/parser/aggregation, Worker-boundary and transaction controls.

## Method and controls

This is a **retrospective** protocol, not a preregistered fresh-model study. Case expectations were made explicit in the runner before the final comparison. Cases are selected diagnostic challenges, not independent samples from deployment.

The [manifest](manifest.json) pins revisions, source hashes, fixture hash, cases and expectations. The [probe](../../scripts/experiment19_probe.py) loads the two pure routing/evidence revisions using `git show`, without checkout, model calls, browsers or application edits. Baseline uses its original 1,600-character projection; treatment uses its production projector. Both arms receive identical inputs per case.

The [curated fixture](supporting/run010-fixture.json) derives from SQLite event 10. It omits URL, screenshot and ignored favicon diagnostics; route/applicability metadata is retained because it causes the overflow. It is not a byte-identical full payload. Its original content hash is recorded. The dedicated overflow case asserts both length greater than 1,600 and invalid JSON after clipping. Other controls remain below that bound to isolate their mechanisms.

Controls cover: malformed structured input, missing proof, wrong target, cached PASS, basic-web versus required-game evidence, explicit conflicting status, unavailable superseding receipts, matching fresh success, weaker profiles, other roles and newer failure. Two cases expect PASS; fourteen expect non-PASS. Route PENDING and FAIL are distinguished in the detailed output; both prevent acceptance.

Development pilots are local-only and not pooled into the final matrix: v1's curated fixture lost overflow metadata; v2 retained overflow but also clipped intended short controls. The final protocol separates those conditions and checks the size preconditions. Production treatment code was not changed during protocol preparation.

## Actual results

### Same-input offline protocol

| Metric | Baseline | Treatment |
|---|---:|---:|
| Decisions matching declared expectations | 8/16 | 16/16 |
| False PASS among negative challenges | 7/14 | 0/14 |
| False rejection among positive challenges | 1/2 | 0/2 |
| Equal per-case input hashes across arms | Yes | Yes |
| Model calls / browser calls | 0 / 0 | 0 / 0 |

[Complete comparison](supporting/comparison.json). These finite challenge counts are not field false-acceptance rates. The same-state protocol does not rerun a Worker, issue a verified receipt or prove root completion.

The earlier preserved replay of original Run-010 routes plus tool events 1–14 and failed browser event 10 separately reported baseline aggregate/browser PASS and corrected FAIL. That existing replay is recorded in [results](experiment19-results.json); its raw inputs remain local-only. The new curated protocol is not represented as a byte-identical replay of every original input.

### Receipt-supersession review regression

An intermediate, uncommitted treatment deduplicated by role/target/profile before validating the outcome. A newer `passed: null`, NOT_RUN, PENDING or statusless receipt could displace a valid FAIL, allowing a controller PASS. This was discovered during final review, not observed in the original baseline run.

The [historical reproduction](supporting/historical-supersession-before-results.json) records 30 methods with four failing subtests. Final `f8bf65e` only allows available PASS/FAIL outcomes to replace equivalent receipts. Malformed/unavailable receipts cannot cancel the outstanding failure. A valid matching newer PASS remains supported. The final matrix and regression tests protect this behavior.

### Selected regression cohort, freshly rerun

| Suite | Methods | Result |
|---|---:|---|
| `test_verification_outcome_integrity.py` | 30 | PASS |
| `test_evidence_policy.py` | 9 | PASS |
| `test_verification_applicability.py` | 15 | PASS |
| `test_experiment11_evidence_compatibility.py` | 10 | PASS |
| `test_experiment13_monotonic.py` | 9 | PASS |
| `test_experiment18a_schema_feedback.py` | 9 | PASS |
| `test_context_sufficiency_gate.py` | 9 | PASS |
| `test_greenfield_context_progress.py` | 9 | PASS |
| `test_repair_impact_anchor.py` | 3 | PASS |

**103 selected test methods passed: 30 new and 73 existing; no failures, errors or skips in this cohort.** These are not 103 independent experimental cases, a full-suite result or a general reliability estimate. The old 103-test checkpoint is not added to the new 103. [Fresh results](supporting/selected-tests.json); [historical checkpoint](supporting/historical-supersession-after-results.json).

The original 20-method pre-implementation fixture produced failure/error records, including references to the then-missing projector; it is not 20 identical FAIL-to-PASS observations. [Sanitized historical record](supporting/historical-before-results.json).

## Safety and acceptance boundaries

The treatment source matches the pinned Git revision after normal Windows line-ending normalization. AST comparison with baseline confines changes to the new projector, Worker evidence recording and the three routing functions listed above. Existing `evidence_gate`, `_commit_verified_leaf`, `execute_leaf`, `repair_task`, authorization guards, planning and scheduling function ASTs are unchanged.

Selected tests include actual file tools and existing authorization/transaction machinery with deterministic providers: a failed quality gate does not commit, a valid fresh repair can commit in a declared artifact contract, and unmet impact targets still block commit. The independent quality/transaction controls are not replaced by a scripted root success. Explicit semantic-policy and authority/direct-oracle routes remain separate existing contracts; selected regressions do not certify all of them.

The legacy supersession rule uses chronological receipt order, exact profile and producing role/target. It does not independently bind freshness to an artifact hash or prove a repair occurred. This remains a limitation, not a stronger authority guarantee.

## Evidence provenance and reproducibility

- [RUNBOOK](RUNBOOK.md): exact offline command forms, prerequisites and fresh output locations.
- [Results](experiment19-results.json), [manifest](manifest.json), [protocol comparison](supporting/comparison.json), [selected cohort](supporting/selected-tests.json).
- [Earlier implementation checkpoint](../verification-outcome-integrity/README.md): historical detail and local-only raw-log references; its uncommitted wording describes that earlier checkpoint, not current publication status.
- LOCAL-ONLY EVIDENCE: original Run-010 `REPORT.md`, `logs/sqlite-tool-events.json`, native run `20261022T011102-92488c96.jsonl`, screenshots/database/game; original verification-integrity `evidence/*` logs; current submission `evidence/selected-v1` and `protocol-v1/v2/v3/v4` outputs. No broken GitHub links to host-specific paths are provided.

## Limitations and conclusion

The hypothesis is supported **on the declared offline matrix and selected regression cohort**. Both false-acceptance prevention and legitimate successful outcomes are covered. There is no evidence of full live E2E improvement yet.

The authority-closure suite needs ignored historical fixture `output/hivo-v25-5-stage6c-b-precommit-invariants-live-2/artifacts/stage5a_route_bindings.json`, absent in this clean worktree. Earlier baseline/treatment attempts failed setup without executing methods. It was not fabricated or counted as passing, and it was not unnecessarily rerun here. Broad recovery/full-suite certification is not claimed.

This protocol is finite and retrospective, and the fixture is a curated derivative. Oversized proof can become conservatively unavailable. Other/future evidence schemas and independent artifact freshness need further coverage. Correct evidence interpretation cannot make an incomplete behavioral oracle complete.

Remaining validation: review this patch and its base dependency; address authentic fixture coverage; extend supported receipt/freshness controls where required; then separately approve a bounded live integration run. No Coin Courier completion, productive live Repairer recovery, accepted application transaction or Run-011 result is claimed. No other experiment is introduced by this submission.
