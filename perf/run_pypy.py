#!/usr/bin/env python3
"""
Performance testing script for Advent of Code solutions.
Runs all .py scripts in the src folder using PyPy and measures execution time.
"""

import os
import sys
import time
import subprocess
import tempfile
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


def wrap_script_with_timer(script_code):
    """Wrap script code with timing that starts after file reads."""
    lines = script_code.splitlines()
    wrapped_lines = []
    timer_inserted = False
    last_file_read_idx = -1

    # Find the last file read operation (typically at the top)
    for i, line in enumerate(lines):
        # Look for file read patterns: open(...).read() or similar
        if "open(" in line and "read()" in line:
            last_file_read_idx = i

    # Insert timer after file reads
    for i, line in enumerate(lines):
        wrapped_lines.append(line)

        # Insert timer after the last file read line (or after blank line following it)
        if not timer_inserted:
            if i == last_file_read_idx:
                # Check if next line is blank
                if i + 1 < len(lines) and lines[i + 1].strip() == "":
                    # Will insert after next blank line
                    continue
                else:
                    # Insert timer right after this line
                    wrapped_lines.append("")
                    wrapped_lines.append("import time")
                    wrapped_lines.append("__benchmark_start__ = time.perf_counter()")
                    timer_inserted = True
            elif (
                last_file_read_idx >= 0
                and i == last_file_read_idx + 1
                and line.strip() == ""
            ):
                # Insert timer after blank line that follows file read
                wrapped_lines.append("import time")
                wrapped_lines.append("__benchmark_start__ = time.perf_counter()")
                timer_inserted = True

    # If no file read was found, insert timer at the beginning
    if not timer_inserted:
        # Check if time is already imported
        has_time_import = any(
            "import time" in line or "from time import" in line for line in lines
        )
        insert_pos = 1 if not has_time_import else 0
        if not has_time_import:
            wrapped_lines.insert(0, "import time")
        wrapped_lines.insert(insert_pos, "__benchmark_start__ = time.perf_counter()")

    # Add timer end and output at the very end
    wrapped_lines.append("")
    wrapped_lines.append(
        "__benchmark_elapsed__ = time.perf_counter() - __benchmark_start__"
    )
    wrapped_lines.append(
        'print(f"__BENCHMARK_TIME__:{__benchmark_elapsed__}", flush=True)'
    )

    return "\n".join(wrapped_lines)


def run_script(script_path):
    """Run a script with PyPy by wrapping it with timer and running as subprocess."""
    # Change to src directory so scripts can find their .txt files
    original_cwd = os.getcwd()
    os.chdir(src_dir)

    try:
        # Read the script file content
        with open(script_path, "r") as f:
            script_code = f.read()

        # Wrap the script with timing code
        wrapped_code = wrap_script_with_timer(script_code)

        # Create a temporary file with the wrapped code
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", delete=False
        ) as tmp_file:
            tmp_file.write(wrapped_code)
            tmp_file_path = tmp_file.name

        try:
            # Run with pypy3 subprocess
            result = subprocess.run(
                ["pypy3", tmp_file_path],
                capture_output=True,
                text=True,
                timeout=60,  # 60 second timeout
                cwd=str(src_dir),  # Run in src directory
            )

            if result.returncode != 0:
                return None, f"Error: {result.stderr}"

            # Parse the benchmark time from stdout
            stdout_lines = result.stdout.splitlines()
            elapsed = None

            for line in stdout_lines:
                if line.startswith("__BENCHMARK_TIME__:"):
                    try:
                        elapsed = float(line.split(":", 1)[1])
                        break
                    except (ValueError, IndexError):
                        pass

            if elapsed is None:
                return None, "Could not parse benchmark time from output"

            return elapsed, None

        except subprocess.TimeoutExpired:
            return None, "Timeout (>60s)"
        except Exception as e:
            return None, f"Exception: {str(e)}"
        finally:
            # Clean up temporary file
            try:
                os.unlink(tmp_file_path)
            except OSError:
                pass

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

    print("Running benchmarks with PyPy...\n")

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

    # Generate README.md
    readme_path = Path(__file__).parent.parent / "README.md"

    with open(readme_path, "w") as f:
        f.write("# Advent of Code Benchmarks (PyPy)\n\n")
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

            f.write(
                f"| [Day {day}]({day}.txt) | [{part1_str}]({day}.py) | [{part2_str}]({day}.2.py) |\n"
            )

    print(f"\n✓ Results written to {readme_path}")


if __name__ == "__main__":
    main()
