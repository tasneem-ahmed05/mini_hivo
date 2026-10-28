# Experiment 20 — Child-Scoped Verification Obligations and Parent Completion Coverage

**Status:** Offline-validated, bounded greenfield-game implementation. **No live E2E validation or completed Coin Courier claim.** Prepared locally on 28 October 2026; not published.

Owner: Tasneem's independent Mini Hivo research/implementation workstream. Baseline retains original authorship and Experiments 1–19. No teammate's independent implementation was incorporated.

## Research question and hypothesis

Can Mini Hivo verify each sequential child against its assigned browser obligations, preserve already verified behavior, and retain the full original source requirements at root verification?

Hypothesis: a controller-owned, conservative verification projection can remove premature downstream checks from recognized child milestones, while full-source root verification and freshly rechecked committed duties prevent requirements disappearing. Unknown assignments must not silently become a weaker generic-web PASS.

The claim is about the existing configured browser-check families, not complete understanding of natural-language assignments or creation of new behavioral oracles.

## Observed Run-010 problem and evidence boundary

The original run used `2a8b945`, `current_recursive`, `field_scoped` classification and the unchanged Coin Courier task. The SQLite task ledger records these goals:

| Child | Stored responsibility |
|---|---|
| 1 | Basic HTML structure, canvas setup and initial game-state management |
| 2 | Player movement, arena boundaries and input |
| 3 | Coin collection, scoring and obstacle collision |
| 4 | Start, Game Over, Restart and High Score persistence |

Native line 25 identifies child 1; line 33 records mission dispatch with a null execution-contract ID. SQLite events 9/10 show required keyboard movement, collection and `AGENT_GAME` checks on child 1. Native lines 82/88/120 record failures. Later children were still pending when the supervised run stopped.

The complete original child `done_when` lists and compiled mission were not preserved. Therefore we establish scope-blind profile inference, not the exact ownership of every historical bridge obligation or a counterfactual successful original run.

## Confirmed causes

1. [`infer_web_profile`](../../hivo/verification.py) classifies project kind and then selects behavioral obligations from the same text. Any game gets keyboard movement and a bridge; `coin` adds collection. The child 1 goal alone exactly reproduces the recorded profile. Product identity and generic game-state wording are not sufficient evidence of local responsibility.
2. Worker `verify_web_app` and controller `optional_browser_check` both used this broad inference. Neither had a recognized milestone projection.
3. The root integration path can receive an active contract reduced to local/integration duties. Controlled fixtures demonstrate that inferring from this projection alone can omit original final obligations. Run-010 did not reach root verification; this third observation is **offline**, not a historical live false acceptance.

The verifier correctly rejected its selected missing checks. Experiment 19 corrected outcome corruption; Experiment 20 changes which obligations are selected, without changing result interpretation or final gate logic.

## Baseline, treatment and fixed conditions

- Baseline: `d15b6068f78dd5b9e46daacd81f5543af5c2cf89`, the Experiment 19 submission including treatment `f8bf65e`.
- Treatment implementation: `a91062551c9b346a35eb4abb5f18a6f64f95a72b`.
- Method: retrospective same-fixture comparison, production routes/gates, controlled verifier snapshots and scripted provider boundaries; **not a preregistered live-model trial**.
- Model/browser calls: zero. No tokens, retry budgets or authorization rules were increased.
- [Manifest](manifest.json) pins source/fixture identities. [Fixture](../../tests/fixtures/experiment20_scope.json) retains original goals and source contract. Its local acceptance conditions are expressly declared test inputs, not recovered historical assignments.

## Implementation and scope

[`hivo/verification_scope.py`](../../hivo/verification_scope.py) adds a verification-only projection:

1. Narrow only ordinary `NEW_PROJECT` game children with retained source requirements and recognized nonempty local conditions. Explicit local behavior in the goal remains required; a product name alone does not create collection duties.
2. Foundation-only narrowing uses fully recognized structural clauses, not a broad substring exception. Explicit bridge assignments and all recognized local behavior families remain checked. Unsupported/missing assignments conservatively retain full source-game verification.
3. Existing-project, approved execution-contract and timer routes do not receive this child narrowing. The original public classifier remains unchanged.
4. Root retains all original source requirements in its verification projection, even when its active contract or summary is reduced. Unassigned touch/win obligations do not disappear merely because all children are labeled complete.
5. Completed profiles are retained only after a successful quality/transaction result and fresh browser PASS. Later checks for that application must execute the union of current and previously committed duties. Prior results are **requirements to recheck**, not reusable success evidence. Registry is per run and target.

[`mini.py`](../../mini.py) supplies the controller projection at leaf dispatch and root aggregation, shares profile selection between Worker and controller, and retains profiles after the existing initial/post-repair acceptance paths. No mutation permission is derived from this projection, and no execution contract is fabricated.

## Paired offline comparison

The [probe](../../scripts/experiment20_probe.py) loads exact baseline `mini.py` in an isolated process and compares it with the pinned treatment source. Both use the same controlled fixture and twelve named assertions. In the baseline, tests deliberately use the existing unprojected contract when the new helper is absent. The conditions, browser snapshots and route inputs are unchanged across arms.

| Measure | Baseline | Treatment |
|---|---:|---:|
| Selected assertions satisfied | 4/12 | 12/12 |
| Failing test methods | 8/12 | 0/12 |
| Errors | 0 | 0 |
| Model / browser calls | 0 / 0 | 0 / 0 |

The eight reproduced mismatches include both premature child checks and incomplete root-profile selection. The four preserved baseline controls are unknown-scope rejection, explicit bridge retention, approved-contract exclusion and unchanged legacy classifier behavior. [Per-case results](supporting/comparison.json).

These twelve assertions are not twelve independent projects, a population reliability estimate or full E2E executions. The controlled snapshot acceptance is conditional on the declared assignment.

The [historical-scope artifact](supporting/historical-scope.json) independently records the original event 10 profile/hash and goal-only reproduction. Evaluating that stored snapshot under the declared foundation fixture succeeds; the unavailable original acceptance list prevents treating it as a successful historical child transaction.

## Expanded regression and integration evidence

| Suite | Baseline existing control | Treatment |
|---|---:|---:|
| `test_experiment20_child_scope.py` | 12 paired assertions above | 34 passed |
| `test_experiment17_field_scoped_profile.py` | 5 passed | 5 passed |
| `test_verified_child_integration.py` | 22 passed | 22 passed |
| `test_experiment9_integration_targets.py` | 12 passed | 12 passed |
| `test_verification_outcome_integrity.py` | 30 passed | 30 passed |
| `test_evidence_policy.py` | 9 passed | 9 passed |
| `test_verification_applicability.py` | 15 passed | 15 passed |
| `test_experiment11_evidence_compatibility.py` | 10 passed | 10 passed |
| `test_experiment13_monotonic.py` | 9 passed | 9 passed |
| `test_experiment18a_schema_feedback.py` | 9 passed | 9 passed |
| `test_context_sufficiency_gate.py` | 9 passed | 9 passed |
| `test_greenfield_context_progress.py` | 9 passed | 9 passed |
| `test_repair_impact_anchor.py` | 3 passed | 3 passed |

**176 selected treatment methods passed: 34 new and 142 existing, zero failures/errors/skips.** All 142 existing methods also pass with pinned baseline `mini.py` loaded in memory. Counts overlap the twelve-method comparison and earlier cohorts; do not add them together or claim full-suite success. [Treatment results](supporting/selected-tests.json), [baseline control](supporting/baseline-existing.json).

New controls cover Worker/controller agreement, missing/unknown/mixed scope, explicit bridge and Game Over ownership, other-domain/existing/approved exclusions, malformed scope metadata, same-target prior obligations, separate-target isolation and full root touch/win coverage. Real `evidence_gate` rejects incomplete parent snapshots and accepts a complete declared profile with matching tool evidence.

A leaf integration test traverses actual `execute_leaf`, a real read tool, verification routing, quality checks and transaction acceptance; it records the profile only afterward. Mission compilation/provider execution and browser observations are deterministic substitutes. The inert HTML fixture already exists before the transaction, so this is **not** autonomous application creation, a new authorized-mutation milestone or a real browser test.

## Review findings and safety

Development records are retained, not counted as final results:

- Expanded fixture initially expected a gate PASS without Builder tool evidence, and expected routing not to add its existing task metadata. Those test assumptions were corrected; gates were not relaxed.
- A negative control exposed invalid scope falling back to generic web for a movement goal. [Intermediate failure](supporting/fallback-review-failure.json); treatment now restores full-source obligations.
- Review exposed omission of explicit Game Over ownership. [Before-correction failure](supporting/gameover-review-failure.json); the terminal-state family now includes it.

AST comparisons leave `evidence_gate`, `_commit_verified_leaf`, Context Sufficiency/Impact guards, `execute_agent_task`, `repair_task` and scheduler logic unchanged. Original classifier, browser executor, outcome parser and aggregation source files are unchanged. Existing related negative tests pass. The controller adds verification duties/context, not write authority.

Further review found two unsafe/permissive mappings: a sentence with a recognized keyword could hide an additional unknown duty, and terminal "freeze movement and scoring" could be mistaken for collection ownership. [Pre-correction record](supporting/clause-safety-before.json). The final recognizer requires complete recognized clauses, not keyword hits within acceptance sentences. Complete-game children cannot opt into foundation-only checks. Explicit Start uses the existing movement-family lifecycle probe; it is not a newly independent Start-button oracle. The initial local implementation `a6cd0c5` is retained as an ancestor; `a910625` is the final treatment.

## Limitations and remaining work

1. The local assignment recognizer is a small closed set of English acceptance-clause forms plus conservative goal-action inclusion, with full-source fallback. Many legitimate paraphrases may still trigger an over-broad full-source check; general natural-language ownership is not solved.
2. The original full Run-010 child conditions are unavailable. This does not prove which treatment profile that exact historical mission would receive.
3. Full coverage here means retaining the source contract and requiring all **existing configured root browser families**. It does not prove exact point awards, every edge, repeated restart count, storage-denial handling, adapter parity or every detailed user criterion. Existing behavioral-oracle coverage gaps remain.
4. The committed-duty registry is per run/target; it is not persisted across process restart and is not artifact-hash freshness proof. Fresh verification remains necessary.
5. Shared-file dependencies such as Start/bridge/state availability may still require better decomposition. The fixture does not show that a live model will produce suitable milestones or productive repairs.
6. Existing fixture-dependent broad authority/recovery suites remain uncertified; no historical fixtures were invented. Selected passing suites are not a complete recovery certification.
7. No live model, browser, full E2E run, completed game or successful live root transaction is claimed. No GitHub publication or integration was performed.

## Conclusion and reproducibility

The hypothesis is supported on the declared offline cases: recognized child milestones avoid premature downstream checks, prior accepted behavior stays a fresh duty, and root cannot discard original configured game requirements. This is a reviewable local implementation with bounded claims, not demonstrated autonomous Coin Courier completion.

See [RUNBOOK](RUNBOOK.md), [results JSON](experiment20-results.json), [manifest](manifest.json), [tests](../../tests/test_experiment20_child_scope.py) and supporting files. Raw logs remain LOCAL-ONLY in the separate Experiment 20 submission evidence directory; original Run-010 logs/database/game and all older worktrees remain preserved.

Next: review the scope mapping and source-retention contract, assess actual generated assignment language, and separately authorize a bounded integration run if desired. An expensive full run was unnecessary to establish this mechanism result and was not started. Future publication must disclose dependency on the Experiment 19 branch/PR; no other experiment is introduced.
