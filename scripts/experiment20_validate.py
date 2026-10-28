"""Run the selected Experiment 20 offline regressions, blocking live providers."""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SUITES = ["test_experiment20_child_scope.py", "test_experiment17_field_scoped_profile.py", "test_verified_child_integration.py", "test_experiment9_integration_targets.py", "test_verification_outcome_integrity.py", "test_evidence_policy.py",
          "test_verification_applicability.py", "test_experiment11_evidence_compatibility.py",
          "test_experiment13_monotonic.py", "test_experiment18a_schema_feedback.py",
          "test_context_sufficiency_gate.py", "test_greenfield_context_progress.py",
          "test_repair_impact_anchor.py"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--focused-only", action="store_true")
    parser.add_argument("--baseline-existing", action="store_true",
                        help="Run existing suites with pinned baseline mini.py loaded in memory")
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=False)
    temporary = args.output_dir.resolve() / "tmp"
    temporary.mkdir()
    env = dict(os.environ, TEMP=str(temporary), TMP=str(temporary),
               PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8")
    rows = []
    suites = (["test_experiment20_child_scope.py"] if args.focused_only
              else SUITES[1:] if args.baseline_existing else SUITES)
    for suite in suites:
        baseline = (
            "import types,subprocess,linecache;"
            "s=subprocess.check_output(['git','show','d15b6068f78dd5b9e46daacd81f5543af5c2cf89:mini.py']).decode('utf-8');"
            "m=types.ModuleType('mini');m.__file__='mini.py';sys.modules['mini']=m;"
            "linecache.cache['mini.py']=(len(s),None,s.splitlines(True),'mini.py');"
            "exec(compile(s,'mini.py','exec'),m.__dict__);"
        ) if args.baseline_existing else ""
        bootstrap = (
            "import sys,runpy;from unittest.mock import patch;" + baseline + "import mini;sys.argv="
            + repr(["unittest", "discover", "-s", "tests", "-p", suite, "-v"])
            + ";a=patch.object(mini,'ask_ollama',side_effect=AssertionError('Live model call forbidden'));"
            "b=patch.object(mini,'structured_model_call',side_effect=AssertionError('Live provider forbidden'));"
            "a.start();b.start();runpy.run_module('unittest',run_name='__main__')"
        )
        command = [sys.executable, "-B", "-c", bootstrap]
        process = subprocess.run(command, cwd=ROOT, env=env, encoding="utf-8",
                                 errors="replace", stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT, timeout=180)
        (args.output_dir / (suite + ".log")).write_text(process.stdout, encoding="utf-8")
        counts = re.findall(r"Ran (\d+) tests?", process.stdout)
        row = {"pattern": suite, "tests": int(counts[-1]) if counts else None,
               "exit_code": process.returncode,
               "summary": re.findall(r"^OK.*$|^FAILED.*$", process.stdout, re.M)}
        rows.append(row)
        print(json.dumps(row), flush=True)
    (args.output_dir / "results.json").write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")
    return int(any(r["exit_code"] != 0 for r in rows))


if __name__ == "__main__":
    raise SystemExit(main())
