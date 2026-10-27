#!/usr/bin/env python3
"""Build a self-contained source archive; compile and test in empty folders."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from zipfile import ZipFile, ZIP_DEFLATED

ROOT=Path(__file__).resolve().parents[2]
PAPER=ROOT/'paper/filter-selection'
EXPERIMENTS=['filter_selection.py','selection_certificates.py','selection_qsp.py',
             'selection_matrix_audit.py','selection_figures.py','check_selection_certificates.py',
             'selection_ising_application.py','selection_ising_figures.py','finite_sampling.py',
             'check_finite_sampling.py','selection_finite_budget.py','selection_finite_precision.py',
             'finite_sampling_figures.py']


def main():
    with tempfile.TemporaryDirectory(prefix='selection-source-') as temporary:
        temp=Path(temporary);source=temp/'source';source.mkdir()
        for name in ['main-en.tex','main-ja.tex','results-en.tex','results-ja.tex',
                     'verification-en.tex','verification-ja.tex','references.tex','generated-table.tex',
                     'finite-en.tex','finite-ja.tex','finite-results-en.tex','finite-results-ja.tex']:
            text=(PAPER/name).read_text().replace('../../figures/','figures/').replace('../qmsve/fonts/','fonts/')
            (source/('main.tex' if name=='main-en.tex' else name)).write_text(text)
        for folder in ['experiments','results','figures','fonts','lean/verification']:(source/folder).mkdir(parents=True)
        for name in EXPERIMENTS:shutil.copy2(ROOT/'experiments'/name,source/'experiments'/name)
        for name in ['filter_selection.json','filter_selection_qsp.json','filter_selection_matrix.json','filter_selection_summary.json',
                     'selection_ising_application.json','selection_ising_pilot.json','selection_ising_summary.json',
                     'finite_budget.json','finite_budget_pilot.json','finite_precision.json','finite_sampling_summary.json']:
            shutil.copy2(ROOT/'results'/name,source/'results'/name)
        for name in ['selection_costs.png','selection_crossover.png','selection_prior_limit.png',
                     'selection_ising_application.png','finite_precision.png','finite_budget.png']:
            shutil.copy2(ROOT/'figures'/name,source/'figures'/name)
        for name in ['ipaexg.ttf','IPA_Font_License_Agreement_v1.0.txt','DejaVuSansMono.ttf','DejaVu-font-license.txt']:
            shutil.copy2(ROOT/'paper/qmsve/fonts'/name,source/'fonts'/name)
        for name in ['Selection.lean','SelectionAudit.lean','QMSVE.lean','FiniteSampling.lean','FiniteSamplingAudit.lean',
                     'lean-toolchain','lakefile.lean','lake-manifest.json']:
            shutil.copy2(ROOT/'lean'/name,source/'lean'/name)
        for name in ['selection-build.log','selection-axioms.log','selection-verification.md',
                     'finite-sampling-build.log','finite-sampling-axioms.log','finite-sampling-verification.md']:
            shutil.copy2(ROOT/'lean/verification'/name,source/'lean/verification'/name)
        for name in ['requirements.txt','claim-evidence.md','novelty-review.md','finite-novelty-review.md','ising-application.md']:
            (source/name).write_text((PAPER/name).read_text().replace('../../figures/','figures/'))
        (source/'README.txt').write_text('''Prior-Robust QSVT Filter Selection: Gap-Free Bias and Finite-Budget Risk

English entry point: main.tex. Japanese companion: main-ja.tex.
Author information is intentionally omitted in this review copy.
No upload/submission has been performed.

Compile (XeLaTeX with AMS/fontspec/hyperref/geometry packages):
  xelatex -interaction=nonstopmode -halt-on-error main.tex
  xelatex -interaction=nonstopmode -halt-on-error main.tex
  xelatex -interaction=nonstopmode -halt-on-error main-ja.tex
  xelatex -interaction=nonstopmode -halt-on-error main-ja.tex
Tectonic can also compile both entry points; some static builds require
the matching ICU data for Japanese line breaking.

From this directory, install requirements.txt in an isolated Python environment.
Full numerical reproduction:
  python experiments/filter_selection.py
  python experiments/selection_qsp.py
  python experiments/selection_matrix_audit.py
  python experiments/selection_figures.py
  python experiments/check_selection_certificates.py
Application and finite-sampling extension (ideal circuits):
  python experiments/selection_ising_application.py
  python experiments/selection_ising_figures.py
  python experiments/check_finite_sampling.py
  python experiments/selection_finite_budget.py
  python experiments/selection_finite_precision.py
  python experiments/finite_sampling_figures.py
The full design run is finite (10 cases), usually a few minutes.
The pilot flag runs two nontrivial cases; use a separate output file:
  python experiments/filter_selection.py --pilot --output work/pilot.json
Regeneration overwrites the corresponding results and figures.
Exact certificate decisions use rational/integer arithmetic. LP and phase
solver candidates use floating point and may vary across platforms.
No Git repository is needed. SOURCE-MANIFEST.json identifies the supplied files.

Lean reproduction from lean/ with the pinned Lean toolchain:
  lake build Selection
  lake env lean SelectionAudit.lean
  lake build FiniteSampling
  lake env lean FiniteSamplingAudit.lean
Five selection and four finite-sampling scalar lemmas were checked locally.
The statistical/support-reduction theorem is a hand proof, not fully formalized.
No successful remote CI run is claimed. Read claim-evidence.md and novelty-review.md.

The query guarantees are for the specified real endpoint-nulling polynomial,
restart, ideal signal, and finite bias-allocation model; not a general
quantum advantage or hardware resource estimate.
''')
        manifest={str(p.relative_to(source)):hashlib.sha256(p.read_bytes()).hexdigest()
                  for p in sorted(source.rglob('*')) if p.is_file()}
        (source/'SOURCE-MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
        build=temp/'build';shutil.copytree(source,build)
        log=ROOT/'work/selection-source-validation.log'
        with log.open('w') as output:
            for target in ['main.tex','main-ja.tex']:
                subprocess.run(['sh',str(ROOT/'paper/qmsve/compile-tex.sh'),target],cwd=build,stdout=output,stderr=subprocess.STDOUT,check=True)
            env=os.environ.copy();env['MPLCONFIGDIR']='/tmp/qmsve-mpl'
            subprocess.run([str(ROOT/'.venv/bin/python'),'experiments/check_selection_certificates.py'],cwd=build,env=env,stdout=output,stderr=subprocess.STDOUT,check=True)
            subprocess.run([str(ROOT/'.venv/bin/python'),'experiments/check_finite_sampling.py'],cwd=build,env=env,stdout=output,stderr=subprocess.STDOUT,check=True)
            subprocess.run([str(ROOT/'.venv/bin/python'),'experiments/filter_selection.py','--pilot','--output','work/pilot.json'],cwd=build,env=env,stdout=output,stderr=subprocess.STDOUT,check=True)
            subprocess.run([str(ROOT/'.venv/bin/python'),'experiments/selection_finite_budget.py','--pilot','--repeats','1000'],cwd=build,env=env,stdout=output,stderr=subprocess.STDOUT,check=True)
        output=PAPER/'Filter-selection-source.zip'
        staged=temp/'source.zip'
        with ZipFile(staged,'w',ZIP_DEFLATED) as archive:
            for p in sorted(source.rglob('*')):
                if p.is_file():archive.write(p,p.relative_to(source))
        staged_copy=output.with_suffix('.zip.new');shutil.copy2(staged,staged_copy);os.replace(staged_copy,output)
        print(output)
        print('Both PDFs compiled; exact arithmetic controls and no-Git pilot passed in an empty directory.')


if __name__=='__main__':main()
