#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")"
QMSVE_BUILD=$(mktemp -d)
trap 'rm -rf "$QMSVE_BUILD"' EXIT
for target in main-en.tex main-ja.tex; do
  sh ./compile-tex.sh "$target" "$QMSVE_BUILD"
done
# Replace the published local artifacts only after both languages succeed.
cp "$QMSVE_BUILD/main-en.pdf" QMSVE-en.pdf
cp "$QMSVE_BUILD/main-ja.pdf" QMSVE-ja.pdf
