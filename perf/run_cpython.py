#!/usr/bin/env python3
"""
Performance testing script for Advent of Code solutions.
Runs all .py scripts in the src folder using CPython and measures execution time.
"""

import os
import sys
import time
import io
import signal
from pathlib import Path
from collections import defaultdict

# Add src directory to path so scripts can find their input files
src_dir = Path(__file__).parent.parent
sys.path.insert(0, str(src_dir))


def format_time(seconds):
    """Format time in appropriate units (ns, µs, ms, s)."""
    if seconds < 1e-6:
        return f"{seconds * 1e9:.1f}ns"
    elif seconds < 1e-3:
        return f"{seconds * 1e6:.1f}µs"
    elif seconds < 1:
        return f"{seconds * 1e3:.1f}ms"
    else:
        return f"{seconds:.2f}s"


def run_script(script_path):
    """Run a script and measure execution time using exec() to avoid cold start overhead."""
    # Change to src directory so scripts can find their .txt files
    original_cwd = os.getcwd()
    os.chdir(src_dir)

    try:
        # Read the script file content
        with open(script_path, "r") as f:
            script_code = f.read()

        # Create a namespace for execution to avoid polluting globals
        exec_namespace = {
            "__file__": str(script_path),
            "__name__": "__main__",
        }

        # Capture stdout and stderr
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()

        # Set up timeout handler
        def timeout_handler(signum, frame):
            raise TimeoutError("Script execution exceeded 60 seconds")

        # Start timer right before execution (after file read and setup)
        start = time.perf_counter()

        try:
            # Set up signal-based timeout (Unix only)
            if hasattr(signal, "SIGALRM"):
                signal.signal(signal.SIGALRM, timeout_handler)
                signal.alarm(60)

            # Redirect stdout and stderr
            old_stdout = sys.stdout
            old_stderr = sys.stderr
            sys.stdout = stdout_capture
            sys.stderr = stderr_capture

            try:
                # Execute the script
                exec(compile(script_code, str(script_path), "exec"), exec_namespace)
            finally:
                # Restore stdout and stderr
                sys.stdout = old_stdout
                sys.stderr = old_stderr
                # Cancel alarm if it was set
                if hasattr(signal, "SIGALRM"):
                    signal.alarm(0)

            elapsed = time.perf_counter() - start

            # Check for errors in stderr
            stderr_content = stderr_capture.getvalue()
            if stderr_content:
                return None, f"Error: {stderr_content}"

            return elapsed, None

        except TimeoutError:
            elapsed = time.perf_counter() - start
            if hasattr(signal, "SIGALRM"):
                signal.alarm(0)
            return None, "Timeout (>60s)"
        except Exception as e:
            elapsed = time.perf_counter() - start
            if hasattr(signal, "SIGALRM"):
                signal.alarm(0)
            stderr_content = stderr_capture.getvalue()
            error_msg = stderr_content if stderr_content else str(e)
            return None, f"Exception: {error_msg}"

    finally:
        # Restore original working directory
        os.chdir(original_cwd)


def get_day_number(filename):
    """Extract day number from filename (e.g., '1.py' -> 1, '1.2.py' -> 1)."""
    base = filename.stem
    if "." in base:
        return int(base.split(".")[0])
    return int(base)


def is_part2(filename):
    """Check if file is part 2 (e.g., '1.2.py')."""
    return ".2" in filename.stem


def main():
    # Find all Python scripts in src directory
    scripts = sorted(
        src_dir.glob("*.py"), key=lambda p: (get_day_number(p), is_part2(p))
    )

    # Group scripts by day
    days = defaultdict(dict)
    for script in scripts:
        day = get_day_number(script)
        if is_part2(script):
            days[day]["part2"] = script
        else:
            days[day]["part1"] = script

    results = []

    print("Running benchmarks with CPython...\n")

    for day in sorted(days.keys()):
        day_results = {"day": day, "part1": None, "part2": None}

        # Run Part 1
        if "part1" in days[day]:
            script = days[day]["part1"]
            print(f"Day {day} Part 1: {script.name}...", end=" ", flush=True)
            elapsed, error = run_script(script)
            if error:
                print(f"❌ {error}")
                day_results["part1"] = error
            else:
                print(f"✓ {format_time(elapsed)}")
                day_results["part1"] = elapsed

        # Run Part 2
        if "part2" in days[day]:
            script = days[day]["part2"]
            print(f"Day {day} Part 2: {script.name}...", end=" ", flush=True)
            elapsed, error = run_script(script)
            if error:
                print(f"❌ {error}")
                day_results["part2"] = error
            else:
                print(f"✓ {format_time(elapsed)}")
                day_results["part2"] = elapsed

        results.append(day_results)

    # Generate README_CPYTHON.md
    readme_path = Path(__file__).parent.parent / "README_CPYTHON.md"

    with open(readme_path, "w") as f:
        f.write("# Advent of Code Benchmarks (CPython)\n\n")
        f.write("## Benchmarks\n\n")
        f.write("| Day | Part 1 | Part 2 |\n")
        f.write("|-----|--------|--------|\n")

        for result in results:
            day = result["day"]
            part1 = result["part1"]
            part2 = result["part2"]

            # Format Part 1
            if part1 is None:
                part1_str = "-"
            elif isinstance(part1, str):
                part1_str = part1
            else:
                part1_str = format_time(part1)

            # Format Part 2
            if part2 is None:
                part2_str = "-"
            elif isinstance(part2, str):
                part2_str = part2
            else:
                part2_str = format_time(part2)

            f.write(f"| [Day {day}](src/{day}.py) | {part1_str} | {part2_str} |\n")

    print(f"\n✓ Results written to {readme_path}")


if __name__ == "__main__":
    main()
