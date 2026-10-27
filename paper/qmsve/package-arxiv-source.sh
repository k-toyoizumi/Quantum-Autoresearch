#!/usr/bin/env sh
set -eu
QMSVE_ROOT=$(CDPATH= cd -- "$(dirname "$0")/../.." && pwd)
QMSVE_TEMP_DIR=$(mktemp -d)
QMSVE_BUILD_DIR=$(mktemp -d)
trap 'rm -rf "$QMSVE_TEMP_DIR" "$QMSVE_BUILD_DIR"' EXIT
mkdir -p "$QMSVE_TEMP_DIR/figures" "$QMSVE_TEMP_DIR/lean" "$QMSVE_TEMP_DIR/fonts" "$QMSVE_TEMP_DIR/experiments" "$QMSVE_TEMP_DIR/results"
cp "$QMSVE_ROOT/paper/qmsve/main-en.tex" "$QMSVE_TEMP_DIR/main.tex"
cp "$QMSVE_ROOT/paper/qmsve/gapfree-en.tex" "$QMSVE_TEMP_DIR/"
cp "$QMSVE_ROOT/paper/qmsve/claim-evidence.md" "$QMSVE_ROOT/paper/qmsve/literature-comparison.md" "$QMSVE_TEMP_DIR/"
cp "$QMSVE_ROOT/requirements-numerics.txt" "$QMSVE_TEMP_DIR/"
cp "$QMSVE_ROOT/figures/qmsve_matrix_level.png" "$QMSVE_TEMP_DIR/figures/"
cp "$QMSVE_ROOT/figures/qmsve_gapfree_envelope.png" "$QMSVE_TEMP_DIR/figures/"
cp "$QMSVE_ROOT/experiments/qmsve_matrix_level.py" "$QMSVE_TEMP_DIR/experiments/"
cp "$QMSVE_ROOT/experiments/qmsve_gapfree_envelope.py" "$QMSVE_TEMP_DIR/experiments/"
cp "$QMSVE_ROOT/results/qmsve_matrix_level.json" "$QMSVE_TEMP_DIR/results/"
cp "$QMSVE_ROOT/results/qmsve_gapfree_envelope.json" "$QMSVE_TEMP_DIR/results/"
cp "$QMSVE_ROOT/lean/QMSVE.lean" "$QMSVE_TEMP_DIR/lean/"
cp "$QMSVE_ROOT/lean/lean-toolchain" "$QMSVE_ROOT/lean/lakefile.lean" "$QMSVE_ROOT/lean/lake-manifest.json" "$QMSVE_TEMP_DIR/lean/"
cp "$QMSVE_ROOT/lean/Audit.lean" "$QMSVE_ROOT/lean/README.md" "$QMSVE_ROOT/lean/appendix_mapping.md" "$QMSVE_ROOT/lean/verification.log.md" "$QMSVE_TEMP_DIR/lean/"
mkdir -p "$QMSVE_TEMP_DIR/lean/tools"
cp "$QMSVE_ROOT/lean/tools/procfs_exe_compat.c" "$QMSVE_TEMP_DIR/lean/tools/"
cp "$QMSVE_ROOT/paper/qmsve/fonts/DejaVuSansMono.ttf" "$QMSVE_ROOT/paper/qmsve/fonts/DejaVu-font-license.txt" "$QMSVE_TEMP_DIR/fonts/"
sed -i 's#../../figures/qmsve_matrix_level.png#figures/qmsve_matrix_level.png#g; s#../../lean/QMSVE.lean#lean/QMSVE.lean#g' "$QMSVE_TEMP_DIR/main.tex"
sed -i 's#../../figures/qmsve_gapfree_envelope.png#figures/qmsve_gapfree_envelope.png#g' "$QMSVE_TEMP_DIR/gapfree-en.tex"
cat > "$QMSVE_TEMP_DIR/README.txt" <<'TXT'
English QMSVE technical-report source draft. This is not an arXiv submission.

Build the PDF from this directory with:
  xelatex -interaction=nonstopmode -halt-on-error main.tex
  xelatex -interaction=nonstopmode -halt-on-error main.tex

The Lean appendix source is lean/QMSVE.lean. Its standalone project files are in lean/.
The deterministic matrix-level and gap-free envelope experiments are in experiments/ and results/.
Create figures/ if absent before running the scripts, and install requirements-numerics.txt.
The combined sharp analysis is a modest contribution candidate with unresolved priority.
New sharp-envelope/rate/perturbation proofs are hand-derived, not Lean-verified.
The manuscript does not claim circuit synthesis or end-to-end quantum advantage.
TXT
# Compile in a fresh directory before packaging.
cp -R "$QMSVE_TEMP_DIR"/. "$QMSVE_BUILD_DIR/"
(cd "$QMSVE_BUILD_DIR" && sh "$QMSVE_ROOT/paper/qmsve/compile-tex.sh" main.tex >/dev/null)
OUT="$QMSVE_ROOT/paper/qmsve/QMSVE-source.zip"
QMSVE_ARCHIVE="$QMSVE_BUILD_DIR/QMSVE-source.zip"
python3 - "$QMSVE_TEMP_DIR" "$QMSVE_ARCHIVE" <<'PY'
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import sys
root = Path(sys.argv[1])
with ZipFile(sys.argv[2], "w", ZIP_DEFLATED) as archive:
    for path in sorted(root.rglob("*")):
        if path.is_file():
            archive.write(path, path.relative_to(root))
PY
cp "$QMSVE_ARCHIVE" "$OUT"
echo "$OUT"
