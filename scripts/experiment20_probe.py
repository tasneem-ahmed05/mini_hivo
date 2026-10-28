"""Same-fixture baseline/treatment scope comparison; no model or browser."""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import types
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
BASELINE = "d15b6068f78dd5b9e46daacd81f5543af5c2cf89"
CASES = [
    "foundation_controller_does_not_require_later_movement_collection",
    "foundation_worker_tool_uses_same_scope",
    "movement_child_requires_movement_not_product_name_collection",
    "mechanics_child_requires_collection_and_collision",
    "flow_child_keeps_restart_and_persistence",
    "missing_or_unknown_assignment_does_not_opt_out",
    "single_full_task_keeps_legacy_game_requirements",
    "complete_parent_profile_accepts_all_checks",
    "parent_cannot_forget_unassigned_touch_or_win",
    "explicit_bridge_assignment_is_not_removed",
    "approved_execution_contract_does_not_get_narrowed",
    "plain_profile_api_retains_existing_behavior",
]


def arm(label):
    sys.path.insert(0, str(ROOT))
    sys.path.insert(0, str(ROOT / "tests"))
    if label == "baseline":
        source = subprocess.check_output(["git", "show", BASELINE + ":mini.py"], cwd=ROOT)
        mini = types.ModuleType("mini")
        mini.__file__ = str(ROOT / "mini.py")
        sys.modules["mini"] = mini
        exec(compile(source, mini.__file__, "exec"), mini.__dict__)
    else:
        import mini
    from test_experiment20_child_scope import Experiment20ScopeTests
    suite = unittest.TestSuite(Experiment20ScopeTests("test_" + name) for name in CASES)
    stream = io.StringIO()
    with patch.object(mini, "ask_ollama", side_effect=AssertionError("Live model forbidden")), \
            patch.object(mini, "structured_model_call", side_effect=AssertionError("Live provider forbidden")):
        result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    failed = {t.id().split(".")[-1] for t, _ in result.failures + result.errors}
    print(json.dumps({"label": label, "methods": result.testsRun,
                      "failures": len(result.failures), "errors": len(result.errors),
                      "cases": [{"case_id": name, "passed": "test_" + name not in failed} for name in CASES],
                      "log": stream.getvalue()}))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--arm", choices=["baseline", "treatment"])
    args = parser.parse_args()
    if args.arm:
        arm(args.arm)
        return 0
    if args.output_dir is None:
        parser.error("--output-dir is required")
    args.output_dir.mkdir(parents=True, exist_ok=False)
    temporary = args.output_dir.resolve() / "tmp"
    temporary.mkdir()
    env = dict(os.environ, TEMP=str(temporary), TMP=str(temporary), PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8")
    comparison = {"experiment": 20, "baseline": BASELINE,
                  "boundary": "controlled fixtures, production routes/gates, scripted verifier observations",
                  "model_calls": 0, "browser_calls": 0, "live_e2e": False,
                  "fixture_sha256": hashlib.sha256((ROOT / "tests/fixtures/experiment20_scope.json").read_bytes()).hexdigest(),
                  "arms": {}}
    for label in ("baseline", "treatment"):
        process = subprocess.run([sys.executable, "-B", str(Path(__file__).resolve()), "--arm", label],
                                 cwd=ROOT, env=env, encoding="utf-8", errors="replace",
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120)
        if process.returncode:
            raise RuntimeError(process.stderr)
        record = json.loads(process.stdout.splitlines()[-1])
        (args.output_dir / (label + ".log")).write_text(record.pop("log"), encoding="utf-8")
        comparison["arms"][label] = record
    (args.output_dir / "comparison.json").write_text(json.dumps(comparison, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({label: {k: v for k, v in row.items() if k != "cases"} for label, row in comparison["arms"].items()}))
    return int(comparison["arms"]["treatment"]["failures"] != 0 or comparison["arms"]["treatment"]["errors"] != 0)


if __name__ == "__main__":
    raise SystemExit(main())
