#!/usr/bin/env sh
# Run from the directory containing the TeX entry point.
set -eu
QMSVE_REPO=$(CDPATH= cd -- "$(dirname "$0")/../.." && pwd)
QMSVE_INPUT=${1:?TeX entry point required}
QMSVE_OUTPUT=${2:-.}
mkdir -p "$QMSVE_OUTPUT"
if command -v xelatex >/dev/null 2>&1; then
  xelatex -interaction=nonstopmode -halt-on-error -output-directory="$QMSVE_OUTPUT" "$QMSVE_INPUT"
  xelatex -interaction=nonstopmode -halt-on-error -output-directory="$QMSVE_OUTPUT" "$QMSVE_INPUT"
else
  if command -v tectonic >/dev/null 2>&1; then
    QMSVE_TECTONIC=$(command -v tectonic)
  elif [ -x "$QMSVE_REPO/work/tools/tectonic" ]; then
    QMSVE_TECTONIC="$QMSVE_REPO/work/tools/tectonic"
  else
    echo 'Install XeLaTeX or Tectonic to compile this manuscript.' >&2
    exit 1
  fi
  if [ -f "$QMSVE_REPO/work/tools/icu71/icudt71l.dat" ]; then
    ICU_DATA="$QMSVE_REPO/work/tools/icu71/"
    export ICU_DATA
  fi
  XDG_CACHE_HOME=${XDG_CACHE_HOME:-"$QMSVE_REPO/work/cache"}
  export XDG_CACHE_HOME
  "$QMSVE_TECTONIC" --keep-logs --outdir "$QMSVE_OUTPUT" "$QMSVE_INPUT"
fi
