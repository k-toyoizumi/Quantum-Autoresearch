#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")"
SELECTION_BUILD=$(mktemp -d)
trap 'rm -rf "$SELECTION_BUILD"' EXIT
for language in en ja; do
  sh ../qmsve/compile-tex.sh "main-$language.tex" "$SELECTION_BUILD"
done
cp "$SELECTION_BUILD/main-en.pdf" Filter-selection-en.pdf
cp "$SELECTION_BUILD/main-ja.pdf" Filter-selection-ja.pdf
