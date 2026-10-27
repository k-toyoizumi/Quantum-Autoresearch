#!/usr/bin/env python3
"""Audit saved evidence, selection decisions, manuscripts and source archives.

This is an artifact consistency audit, not a replacement for mathematical proofs.
"""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile
import pymupdf

ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    budget_path = ROOT/'results/finite_budget.json'
    precision_path = ROOT/'results/finite_precision.json'
    data = json.loads(budget_path.read_text())
    precision = json.loads(precision_path.read_text())
    summary = json.loads((ROOT/'results/finite_sampling_summary.json').read_text())
    assert data['metadata']['input_sha256'] == sha(ROOT/'results/selection_ising_application.json')
    for name, digest in data['metadata']['source_sha256'].items():
        assert sha(ROOT/'experiments'/name) == digest, name
    assert precision['metadata']['input_sha256'] == sha(budget_path)
    assert precision['metadata']['source_sha256'] == sha(ROOT/'experiments/selection_finite_precision.py')
    assert len(data['cases']) == 6
    batch_count = replicates = prior_count = 0
    for case in data['cases']:
        assert len(case['curves']) == 8
        u = F(case['prior']['u'])
        for row in case['curves']:
            feasible = [F(r['conditional_mse_upper_exact']) for r in row['candidate_bounds']
                        if F(r['abstention_upper_exact']) <= F(1, 20)]
            selected = row['selection']
            assert F(selected['conditional_mse_upper_exact']) == min([u*u/4, *feasible])
            assert F(selected['abstention_upper_exact']) <= F(1, 20)
            if selected['id'] == 'prior-midpoint':
                prior_count += 1
            else:
                assert selected['attempts']*(case['parameters']['spins']+4*selected['degree']+1) <= row['budget']
                assert row['selected_audit']['ideal_conditional_mse'] <= selected['conditional_mse_upper']+1e-12
            for name in ['selected_audit', 'original_fixed_design_audit']:
                audit = row[name]
                if 'simulation' in audit:
                    batch_count += 1; replicates += audit['simulation']['replicates']
                    assert audit['simulation']['mse_agreement_standard_errors'] < 6
    assert len(precision['curves']) == 3
    for curve in precision['curves']:
        assert len(curve['rows']) == 13
        for row in curve['rows']:
            batch_count += 1; replicates += row['simulation']['replicates']
            assert row['simulation']['mse_agreement_standard_errors'] < 6
    assert batch_count == summary['sampling_settings'] == 114
    assert replicates == summary['sampling_replicates'] == 2280000
    assert prior_count == summary['prior_only_selections'] == 21
    assert len(data['support_reduction_controls']) == 100
    for control in data['support_reduction_controls']:
        assert control['support_count'] <= 3
        assert abs(control['mean_after']-control['mean_before']) < 1e-8
        assert control['success_after'] <= control['success_before']+1e-9
        assert control['conditional_mse_after'] >= control['conditional_mse_before']-1e-10
    paper = ROOT/'paper/filter-selection'
    result = {'status': 'passed', 'audit_scope': 'saved artifact and evidence consistency; not formal verification',
              'physical_cases': 6, 'budget_conditions': 48, 'sampling_batches': batch_count,
              'sampling_replicates': replicates, 'prior_only_choices': prior_count,
              'mathematics': 'complete hand proofs in bilingual manuscripts; four additional scalar Lean lemmas locally checked',
              'remote_ci': 'not run for the finite-sampling extension', 'pdfs': {}, 'archives': {}}
    for lang in ['en', 'ja']:
        path = paper/f'Filter-selection-{lang}.pdf'
        document = pymupdf.open(path)
        text = '\n'.join(p.get_text() for p in document)
        assert '??' not in text and '\ufffd' not in text
        assert '228' in text or '2,280,000' in text or '2.28' in text
        result['pdfs'][lang] = {'pages': len(document), 'sha256': sha(path)}
    for filename in ['Filter-selection-source.zip', 'Filter-selection-arxiv.zip']:
        path = paper/filename
        with ZipFile(path) as archive:
            assert archive.testzip() is None
            manifest_name = 'anc/SOURCE-MANIFEST.json' if 'arxiv' in filename else 'SOURCE-MANIFEST.json'
            manifest = json.loads(archive.read(manifest_name))
            for name, digest in manifest.items():
                assert hashlib.sha256(archive.read(name)).hexdigest() == digest
            # Verify the new mathematics is actually in the supplied article.
            assert 'finite-en.tex' in archive.namelist() and 'finite-results-en.tex' in archive.namelist()
            for tex in ['main-en.tex', 'finite-en.tex', 'finite-results-en.tex', 'verification-en.tex', 'references.tex']:
                archived = 'main.tex' if tex == 'main-en.tex' else tex
                expected = (paper/tex).read_text().replace('../../figures/', 'figures/').replace('../qmsve/fonts/', 'fonts/')
                assert archive.read(archived).decode() == expected
            for name in ['finite_sampling.py', 'selection_finite_budget.py', 'selection_finite_precision.py']:
                prefix = 'anc/' if 'arxiv' in filename else ''
                assert archive.read(prefix+'experiments/'+name) == (ROOT/'experiments'/name).read_bytes()
            if 'arxiv' in filename:
                assert 'main-ja.tex' not in archive.namelist()
                assert not any(name.startswith('anc/') and name.endswith('.tex') for name in archive.namelist())
        result['archives'][filename] = {'sha256': sha(path), 'manifest_files': len(manifest)}
    (paper/'validation-summary.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
