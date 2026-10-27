#!/usr/bin/env python3
"""Prepare one English TeX entry point and ancillary reproducibility files."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / 'paper/filter-selection'


def main():
    with tempfile.TemporaryDirectory(prefix='selection-arxiv-') as temporary:
        source = Path(temporary) / 'source'
        source.mkdir()
        article = {'main.tex', 'results-en.tex', 'verification-en.tex',
                   'references.tex', 'generated-table.tex'}
        with ZipFile(PAPER / 'Filter-selection-source.zip') as archive:
            for name in archive.namelist():
                if name in article or name.startswith('figures/') or name in {
                    'fonts/DejaVuSansMono.ttf', 'fonts/DejaVu-font-license.txt'
                }:
                    destination = source / name
                elif name.startswith(('experiments/', 'results/', 'lean/')) or name in {
                    'requirements.txt', 'claim-evidence.md', 'novelty-review.md'
                }:
                    destination = source / 'anc' / name
                else:
                    continue
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(archive.read(name))
        shutil.copytree(source / 'figures', source / 'anc/figures')
        (source / 'anc/README.txt').write_text('''Reproducibility files for Prior-Robust QSVT Filter Selection.
Author metadata is intentionally omitted from this review copy.
No submission has been performed.

From this ancillary directory, install requirements.txt in an isolated Python
environment and run:
  python experiments/check_selection_certificates.py
  python experiments/filter_selection.py
  python experiments/selection_qsp.py
  python experiments/selection_matrix_audit.py
  python experiments/selection_figures.py
The scripts use the data paths relative to this directory. No Git checkout
is needed. Regeneration overwrites corresponding data and figures.
For a short design run:
  python experiments/filter_selection.py --pilot --output work/pilot.json
The plot script writes its generated TeX table under paper/filter-selection/;
copy that table to the article source if regenerating the manuscript.
From lean/, use the pinned toolchain:
  lake build Selection
  lake env lean SelectionAudit.lean
Only the five documented scalar lemmas were checked in Lean.
Read claim-evidence.md and novelty-review.md for the restricted claim scope.
''')
        manifest = {str(p.relative_to(source)): hashlib.sha256(p.read_bytes()).hexdigest()
                    for p in sorted(source.rglob('*')) if p.is_file()}
        (source / 'anc/SOURCE-MANIFEST.json').write_text(json.dumps(manifest, indent=2) + '\n')
        build = Path(temporary) / 'validation'
        shutil.copytree(source, build)
        with (ROOT / 'work/selection-arxiv-validation.log').open('w') as log:
            subprocess.run(['sh', str(ROOT / 'paper/qmsve/compile-tex.sh'), 'main.tex'],
                           cwd=build, stdout=log, stderr=subprocess.STDOUT, check=True)
            env = os.environ.copy()
            env['MPLCONFIGDIR'] = '/tmp/qmsve-mpl'
            for arguments in [
                ['experiments/check_selection_certificates.py'],
                ['experiments/filter_selection.py', '--pilot', '--output', 'work/pilot.json']
            ]:
                subprocess.run([str(ROOT / '.venv/bin/python'), *arguments], cwd=build / 'anc',
                               env=env, stdout=log, stderr=subprocess.STDOUT, check=True)
        staged = PAPER / 'Filter-selection-arxiv.zip.new'
        with ZipFile(staged, 'w', ZIP_DEFLATED) as archive:
            for p in sorted(source.rglob('*')):
                if p.is_file():
                    archive.write(p, p.relative_to(source))
        staged.replace(PAPER / 'Filter-selection-arxiv.zip')
        print('English source compiled; ancillary exact checks and no-Git pilot passed.')


if __name__ == '__main__':
    main()
