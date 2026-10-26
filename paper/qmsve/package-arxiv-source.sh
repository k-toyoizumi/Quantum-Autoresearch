#!/usr/bin/env sh
set -eu
QMSVE_ROOT=$(CDPATH= cd -- "$(dirname "$0")/../.." && pwd)
QMSVE_TEMP_DIR=$(mktemp -d)
QMSVE_BUILD_DIR=$(mktemp -d)
trap 'rm -rf "$QMSVE_TEMP_DIR" "$QMSVE_BUILD_DIR"' EXIT
mkdir -p "$QMSVE_TEMP_DIR/figures" "$QMSVE_TEMP_DIR/lean" "$QMSVE_TEMP_DIR/fonts" "$QMSVE_TEMP_DIR/experiments" "$QMSVE_TEMP_DIR/results"
cp "$QMSVE_ROOT/paper/qmsve/main-en.tex" "$QMSVE_TEMP_DIR/main.tex"
cp "$QMSVE_ROOT/figures/qmsve_matrix_level.png" "$QMSVE_TEMP_DIR/figures/"
cp "$QMSVE_ROOT/experiments/qmsve_matrix_level.py" "$QMSVE_TEMP_DIR/experiments/"
cp "$QMSVE_ROOT/results/qmsve_matrix_level.json" "$QMSVE_TEMP_DIR/results/"
cp "$QMSVE_ROOT/lean/QMSVE.lean" "$QMSVE_TEMP_DIR/lean/"
cp "$QMSVE_ROOT/lean/lean-toolchain" "$QMSVE_ROOT/lean/lakefile.lean" "$QMSVE_ROOT/lean/lake-manifest.json" "$QMSVE_TEMP_DIR/lean/"
cp "$QMSVE_ROOT/lean/Audit.lean" "$QMSVE_ROOT/lean/README.md" "$QMSVE_ROOT/lean/appendix_mapping.md" "$QMSVE_ROOT/lean/verification.log.md" "$QMSVE_TEMP_DIR/lean/"
mkdir -p "$QMSVE_TEMP_DIR/lean/tools"
cp "$QMSVE_ROOT/lean/tools/procfs_exe_compat.c" "$QMSVE_TEMP_DIR/lean/tools/"
cp "$QMSVE_ROOT/paper/qmsve/fonts/DejaVuSansMono.ttf" "$QMSVE_ROOT/paper/qmsve/fonts/DejaVu-font-license.txt" "$QMSVE_TEMP_DIR/fonts/"
sed -i 's#../../figures/qmsve_matrix_level.png#figures/qmsve_matrix_level.png#g; s#../../lean/QMSVE.lean#lean/QMSVE.lean#g' "$QMSVE_TEMP_DIR/main.tex"
cat > "$QMSVE_TEMP_DIR/README.txt" <<'TXT'
English QMSVE technical-report source draft. This is not an arXiv submission.

Build the PDF from this directory with:
  xelatex -interaction=nonstopmode -halt-on-error main.tex
  xelatex -interaction=nonstopmode -halt-on-error main.tex

The Lean appendix source is lean/QMSVE.lean. Its standalone project files are in lean/.
The deterministic matrix-level experiment and saved output are in experiments/ and results/.
The manuscript does not claim circuit synthesis, end-to-end quantum advantage, or novelty.
TXT
# Compile in a fresh directory before packaging.
cp -R "$QMSVE_TEMP_DIR"/. "$QMSVE_BUILD_DIR/"
(cd "$QMSVE_BUILD_DIR" && xelatex -interaction=nonstopmode -halt-on-error main.tex >/dev/null && xelatex -interaction=nonstopmode -halt-on-error main.tex >/dev/null)
OUT="$QMSVE_ROOT/paper/qmsve/QMSVE-source.zip"
rm -f "$OUT"
(cd "$QMSVE_TEMP_DIR" && zip -qr "$OUT" .)
echo "$OUT"
