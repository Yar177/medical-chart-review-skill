#!/usr/bin/env bash
# Cut a tagged release of the monorepo.
#
# Usage:
#   scripts/release.sh <version> "<short message>"
#
# Example:
#   scripts/release.sh 0.3.0 "add fhir-resources skill"
#
# Flow:
#   1. Validate args + clean working tree
#   2. Run skill validator (abort on failure)
#   3. Promote CHANGELOG [Unreleased] -> [X.Y.Z] - <today>
#   4. Bump CITATION.cff version + date-released
#   5. Show diff, prompt y/N
#   6. On confirm: commit, tag, push branch + tag
#   7. Print follow-up reminder (GitHub Release + Zenodo DOI patch)

set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "usage: $0 <version> \"<short message>\"" >&2
  echo "  version: 0.3.0 or v0.3.0" >&2
  echo "  message: short summary (e.g. 'add fhir-resources skill')" >&2
  exit 2
fi

VERSION="${1#v}"
MESSAGE="$2"

if ! [[ "$VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  echo "error: version must be X.Y.Z, got $VERSION" >&2
  exit 2
fi

TAG="v$VERSION"
TODAY="$(date +%Y-%m-%d)"
REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "$REPO_ROOT"

if [[ -n "$(git status --porcelain)" ]]; then
  echo "error: working tree not clean. Commit or stash first." >&2
  exit 1
fi

if git rev-parse "$TAG" >/dev/null 2>&1; then
  echo "error: tag $TAG already exists." >&2
  exit 1
fi

echo ">> running validator..."
python3 scripts/validate-skills.py

if ! grep -q '^## \[Unreleased\]' CHANGELOG.md; then
  echo "error: CHANGELOG.md has no [Unreleased] section to promote" >&2
  exit 1
fi

# Promote [Unreleased] -> [X.Y.Z] - <today>. BSD/GNU sed compatible.
sed -i.bak "s/^## \[Unreleased\]$/## [$VERSION] - $TODAY/" CHANGELOG.md
rm -f CHANGELOG.md.bak

# Bump CITATION.cff version + date-released.
VERSION="$VERSION" TODAY="$TODAY" python3 - <<'PY'
import os, re
p = "CITATION.cff"
v = os.environ["VERSION"]
d = os.environ["TODAY"]
t = open(p).read()
if not re.search(r'^version:\s*', t, re.M):
    raise SystemExit("CITATION.cff has no 'version:' field to bump")
t = re.sub(r'^version:\s*.*$', f'version: "{v}"', t, count=1, flags=re.M)
if re.search(r'^date-released:\s*', t, re.M):
    t = re.sub(r'^date-released:\s*.*$', f'date-released: {d}', t, count=1, flags=re.M)
else:
    # insert date-released right after version
    t = re.sub(r'^(version:\s*.*)$', r'\1' + f'\ndate-released: {d}', t, count=1, flags=re.M)
open(p, 'w').write(t)
PY

echo ""
echo ">> diff:"
git --no-pager diff CHANGELOG.md CITATION.cff
echo ""

read -rp "Proceed with commit, tag $TAG, and push? [y/N] " ans
if [[ "$ans" != "y" && "$ans" != "Y" ]]; then
  echo "aborted. reverting working-tree changes."
  git checkout -- CHANGELOG.md CITATION.cff
  exit 1
fi

git add CHANGELOG.md CITATION.cff
git commit -m "release $TAG: $MESSAGE"
git tag -a "$TAG" -m "$TAG"
git push origin HEAD
git push origin "$TAG"

REMOTE_URL="$(git remote get-url origin)"
REPO_PATH="$(echo "$REMOTE_URL" | sed -E 's#(git@github.com:|https://github.com/)##; s#\.git$##')"

echo ""
echo ">> released $TAG"
echo ">> NEXT: publish GitHub Release from the tag at:"
echo "   https://github.com/$REPO_PATH/releases/new?tag=$TAG"
echo ">> After Zenodo mints the DOI, add it to CITATION.cff identifiers and push a follow-up commit."
