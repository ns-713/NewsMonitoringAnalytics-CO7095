"""
Test Runner and Coverage Measurement Tool
CO7095 - Software Measurement and Quality Assurance (2026-2027)

Runs unittest discovery, per-member suites, symbolic/concolic harnesses,
and calculates statement coverage using pure standard library tracing or coverage.py.

Usage:
    python run_tests.py                  # Run all tests + coverage
    python run_tests.py --member ns713   # Run Nikitha Sarpur's tests
    python run_tests.py --member sd683   # Run Sashi Dommaraju's tests
    python run_tests.py --member jb1080  # Run Jyothi Bandalapati's tests
    python run_tests.py --member pj161   # Run Jalakam Prashanth's tests
    python run_tests.py --shared         # Run shared integration and system tests
"""

import sys
import os
import unittest
import time
import trace
from pathlib import Path
from datetime import datetime

# Set project root
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

REPORTS_DIR = PROJECT_ROOT / "reports"
EXECUTION_DIR = REPORTS_DIR / "execution"
COVERAGE_DIR = REPORTS_DIR / "coverage"

EXECUTION_DIR.mkdir(parents=True, exist_ok=True)
COVERAGE_DIR.mkdir(parents=True, exist_ok=True)


class CoverageTracer:
    """
    Measures executable statement coverage using Python's standard library trace module.
    Works natively in university lab environments without requiring external pip packages.
    """

    def __init__(self, target_dirs=None):
        if target_dirs is None:
            self.target_dirs = [
                PROJECT_ROOT / "models",
                PROJECT_ROOT / "services",
                PROJECT_ROOT / "storage",
                PROJECT_ROOT / "interface"
            ]
        else:
            self.target_dirs = [Path(d) for d in target_dirs]

        self.executed_lines = {}
        self.tracer = trace.Trace(
            count=1,
            trace=0,
            ignoredirs=[sys.prefix, sys.exec_prefix]
        )

    def run_with_trace(self, func, *args, **kwargs):
        """Executes a callable under code line tracing."""
        return self.tracer.runfunc(func, *args, **kwargs)

    def compute_coverage(self):
        """
        Analyzes executed lines versus all executable Python lines across target directories.
        Returns:
            dict containing overall metrics and per-file coverage statistics.
        """
        results = self.tracer.results()
        total_stmts = 0
        executed_stmts = 0
        file_stats = []

        for target_dir in self.target_dirs:
            for py_file in target_dir.glob("**/*.py"):
                if py_file.name == "__init__.py" and py_file.stat().st_size == 0:
                    continue

                abs_path = str(py_file.resolve())
                # Count executable lines in the file
                try:
                    with open(py_file, "r", encoding="utf-8") as f:
                        lines = f.readlines()
                except Exception:
                    continue

                # Identify non-blank, non-comment lines
                executable_line_nums = set()
                in_multiline_doc = False
                for idx, line in enumerate(lines, 1):
                    stripped = line.strip()
                    if not stripped:
                        continue
                    if stripped.startswith('"""') or stripped.startswith("'''"):
                        if stripped.count('"""') == 1 or stripped.count("'''") == 1:
                            in_multiline_doc = not in_multiline_doc
                        continue
                    if in_multiline_doc:
                        if '"""' in stripped or "'''" in stripped:
                            in_multiline_doc = False
                        continue
                    if stripped.startswith("#"):
                        continue
                    executable_line_nums.add(idx)

                file_total = len(executable_line_nums)
                if file_total == 0:
                    continue

                # Count how many of these lines were executed
                executed_lines_in_file = 0
                for line_num in executable_line_nums:
                    if (abs_path, line_num) in results.counts:
                        executed_lines_in_file += 1

                file_pct = round((executed_lines_in_file / file_total) * 100, 1) if file_total > 0 else 0.0
                rel_path = py_file.relative_to(PROJECT_ROOT)

                file_stats.append({
                    "file": str(rel_path).replace("\\", "/"),
                    "total": file_total,
                    "executed": executed_lines_in_file,
                    "missed": file_total - executed_lines_in_file,
                    "coverage_pct": file_pct
                })

                total_stmts += file_total
                executed_stmts += executed_lines_in_file

        overall_pct = round((executed_stmts / total_stmts) * 100, 1) if total_stmts > 0 else 0.0

        return {
            "total_statements": total_stmts,
            "executed_statements": executed_stmts,
            "missed_statements": total_stmts - executed_stmts,
            "overall_coverage_pct": overall_pct,
            "files": sorted(file_stats, key=lambda x: x["file"])
        }


def run_test_suite(test_dirs, pattern="test_*.py"):
    """Discovers and runs test suite across one or more directories."""
    loader = unittest.TestLoader()
    combined_suite = unittest.TestSuite()

    if isinstance(test_dirs, (str, Path)):
        test_dirs = [test_dirs]

    for d in test_dirs:
        d_path = Path(d)
        if d_path.exists():
            suite = loader.discover(start_dir=str(d_path), pattern=pattern, top_level_dir=str(PROJECT_ROOT))
            combined_suite.addTests(suite)

    runner = unittest.TextTestRunner(verbosity=2)
    return runner.run(combined_suite)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="CO7095 Test Runner & Coverage Tool")
    parser.add_argument("--member", choices=["ns713", "sd683", "jb1080", "pj161"], help="Run tests for specific student")
    parser.add_argument("--technique", choices=["blackbox", "whitebox", "symbolic", "concolic"], help="Filter by specific testing technique")
    parser.add_argument("--shared", action="store_true", help="Run shared integration and system tests")
    parser.add_argument("--legacy-tests", action="store_true", help="Run legacy tests/ folder")
    parser.add_argument("--no-coverage", action="store_true", help="Skip coverage analysis")
    args = parser.parse_args()

    # Determine test paths
    if args.member:
        base_dir = PROJECT_ROOT / args.member / "test"
        if args.technique:
            test_paths = [base_dir / args.technique]
            suite_name = f"Member {args.member.upper()} - {args.technique.upper()} Tests"
        else:
            test_paths = [base_dir]
            suite_name = f"Member {args.member.upper()} Complete Test Package"
    elif args.technique:
        test_paths = [PROJECT_ROOT / m / "test" / args.technique for m in ["ns713", "sd683", "jb1080", "pj161"]]
        suite_name = f"All Members - {args.technique.upper()} Test Suites"
    elif args.shared:
        test_paths = [PROJECT_ROOT / "tests" / "shared"]
        suite_name = "Shared Integration and System Test Suite"
    elif args.legacy_tests:
        test_paths = [PROJECT_ROOT / "tests"]
        suite_name = "CO7095 Legacy Test Directory Suite"
    else:
        # Default: Discover all 4 student packages + shared integration/system
        test_paths = [
            PROJECT_ROOT / "ns713" / "test",
            PROJECT_ROOT / "sd683" / "test",
            PROJECT_ROOT / "jb1080" / "test",
            PROJECT_ROOT / "pj161" / "test",
            PROJECT_ROOT / "tests" / "shared",
            PROJECT_ROOT / "research"
        ]
        suite_name = "CO7095 Master Test Suite (All Student Packages & Integration)"

    print("=" * 76)
    print(f"  {suite_name.upper()}")
    print("  Target Package Discovery:")
    for tp in test_paths:
        if tp.exists():
            print(f"   -> {tp.relative_to(PROJECT_ROOT)}")
    print("=" * 76)

    tracer = CoverageTracer()
    start_time = time.time()

    if args.no_coverage:
        result = run_test_suite(test_paths)
        cov_data = None
    else:
        print("\n[INFO] Executing test suite under statement coverage tracer...\n")
        result = tracer.run_with_trace(run_test_suite, test_paths)
        cov_data = tracer.compute_coverage()

    duration = time.time() - start_time
    total_tests = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    skipped = len(result.skipped)
    passed = total_tests - failures - errors - skipped
    pass_rate = round((passed / total_tests) * 100, 1) if total_tests > 0 else 0.0

    print("\n" + "=" * 76)
    print("  TEST EXECUTION SUMMARY")
    print("=" * 76)
    print(f"  Total Tests Executed : {total_tests}")
    print(f"  Passed               : {passed}")
    print(f"  Failed               : {failures}")
    print(f"  Errors               : {errors}")
    print(f"  Skipped              : {skipped}")
    print(f"  Test Pass Rate       : {pass_rate}%")
    print(f"  Execution Time       : {round(duration, 3)} seconds")

    # Generate Execution Report File
    timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    summary_path = EXECUTION_DIR / "test_run_summary.txt"
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(f"CO7095 Test Execution Summary Report\n")
        f.write(f"Generated: {timestamp_str}\n")
        f.write(f"Suite: {suite_name}\n")
        f.write(f"{'='*60}\n")
        f.write(f"Total Tests Executed : {total_tests}\n")
        f.write(f"Passed               : {passed}\n")
        f.write(f"Failed               : {failures}\n")
        f.write(f"Errors               : {errors}\n")
        f.write(f"Skipped              : {skipped}\n")
        f.write(f"Pass Rate            : {pass_rate}%\n")
        f.write(f"Duration             : {round(duration, 3)}s\n")
        if failures or errors:
            f.write(f"\nFailed / Error Details:\n")
            for fail in result.failures:
                f.write(f"\n[FAILURE] {fail[0]}\n{fail[1]}\n")
            for err in result.errors:
                f.write(f"\n[ERROR] {err[0]}\n{err[1]}\n")

    print(f"\n[SAVED] Execution summary saved to: {summary_path.relative_to(PROJECT_ROOT)}")

    # Print & Save Coverage Report if enabled
    if cov_data:
        print("\n" + "=" * 76)
        print("  CODE STATEMENT COVERAGE SUMMARY")
        print("=" * 76)
        print(f"  Total Measured Statements : {cov_data['total_statements']}")
        print(f"  Executed Statements       : {cov_data['executed_statements']}")
        print(f"  Missed Statements         : {cov_data['missed_statements']}")
        print(f"  Overall Statement Coverage: {cov_data['overall_coverage_pct']}%\n")

        print(f"  {'Source Module / File':<42} | {'Stmts':<6} | {'Exec':<6} | {'Cover %':<8}")
        print(f"  {'-'*42}-+-{'-'*6}-+-{'-'*6}-+-{'-'*8}")
        for item in cov_data["files"]:
            print(f"  {item['file']:<42} | {item['total']:<6} | {item['executed']:<6} | {item['coverage_pct']:<7}%")

        cov_summary_path = COVERAGE_DIR / "coverage_summary.txt"
        with open(cov_summary_path, "w", encoding="utf-8") as f:
            f.write(f"CO7095 Software Measurement - Code Coverage Report\n")
            f.write(f"Generated: {timestamp_str}\n")
            f.write(f"{'='*70}\n")
            f.write(f"Total Statements : {cov_data['total_statements']}\n")
            f.write(f"Executed         : {cov_data['executed_statements']}\n")
            f.write(f"Missed           : {cov_data['missed_statements']}\n")
            f.write(f"Coverage Score   : {cov_data['overall_coverage_pct']}%\n\n")
            f.write(f"{'File':<45} {'Stmts':<8} {'Exec':<8} {'Coverage'}\n")
            f.write(f"{'-'*70}\n")
            for item in cov_data["files"]:
                f.write(f"{item['file']:<45} {item['total']:<8} {item['executed']:<8} {item['coverage_pct']}%\n")

        print(f"\n[SAVED] Coverage report saved to: {cov_summary_path.relative_to(PROJECT_ROOT)}")

    sys.exit(0 if (failures == 0 and errors == 0) else 1)


if __name__ == "__main__":
    main()
