#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")"
for target in main-en.tex main-ja.tex; do
  xelatex -interaction=nonstopmode -halt-on-error "$target"
  xelatex -interaction=nonstopmode -halt-on-error "$target"
done
