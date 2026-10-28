#!/usr/bin/env python3
"""Generate measured venue headers for readers and executors; stdlib only."""
import argparse
from pathlib import Path
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--task-dir", type=Path, required=True)
    parser.add_argument("--role", choices=("reader", "executor"), required=True)
    parser.add_argument("--evidence-dir", type=Path, action="append", default=[])
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        top = subprocess.run(["git", "-C", str(root), "rev-parse", "--show-toplevel"],
                             capture_output=True, text=True, check=True)
        head = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"],
                              capture_output=True, text=True, check=True)
    except (OSError, subprocess.CalledProcessError):
        print("venue-header: git measurement failed", file=sys.stderr)
        return 2
    if Path(top.stdout.strip()).resolve() != root:
        print("venue-header: root is not the repository top level", file=sys.stderr)
        return 2
    sha = head.stdout.strip()
    task = args.task_dir.resolve()
    evidence = [path.resolve() for path in args.evidence_dir]
    if args.role == "reader":
        print("Venue (supplied by the head, not measured by you):")
        print(f"- repo root: {root}")
        print(f"- HEAD: {sha}")
        print(f"- task directory: {task}")
        for path in evidence:
            print(f"- evidence directory: {path}")
        print('Echo the repo root and HEAD as the first lines of your report, marked "supplied, not measured".')
        print("Read repository files only by absolute path under the repo root, plus the directories above; search with your read/grep/find tools.")
        print("Do not run or request shell commands, counts, or test runs; mark anything that needs one UNMEASURED for the head.")
    else:
        print(f"Venue: absolute repo root {root} at HEAD {sha}; task directory {task}.")
        for path in evidence:
            print(f"- evidence directory: {path}")
        print(f"Before anything else, run `git -C {root} rev-parse --show-toplevel HEAD` and paste the output as the first lines of your report; if it differs from the venue, STOP.")
        print(f"Address every file and command by absolute path or `git -C {root}`: shell and eval-kernel cwd does not persist between calls.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
