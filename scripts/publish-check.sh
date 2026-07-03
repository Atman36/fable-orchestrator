#!/usr/bin/env sh
# Public-safety gate for this repo: tracked-file allowlist + leak scan.
# Run before every push; exits non-zero on any violation.
set -eu
cd "$(dirname "$0")/.."
fail=0
allow='^(SKILL\.md|README\.md|CHANGELOG\.md|LICENSE|\.gitignore|scripts/publish-check\.sh)$'
for f in $(git ls-files); do
  if ! printf '%s\n' "$f" | grep -Eq "$allow"; then
    echo "BLOCK: '$f' is not in the public allowlist" >&2
    fail=1
  fi
done
if git grep -nE '(/Users/[A-Za-z0-9._-]+|sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,}|gho_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY)' -- ':!scripts/publish-check.sh' >&2; then
  echo "BLOCK: private path or secret-like pattern in tracked files" >&2
  fail=1
fi
if [ "$fail" -eq 0 ]; then
  echo "publish-check: OK"
fi
exit "$fail"
