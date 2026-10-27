#!/usr/bin/env python3
"""Full block-matrix QSP/LCU audit with the fixed input |0>.

The synthetic oracle is constructed classically; no hardware gate compilation.
The selector receives only (a,u,E,N,c), never the actual test eigenvalues.
"""
import hashlib
import json
import math
from fractions import Fraction as F
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
SEED=20261028


def main():
    design=json.loads((ROOT/'results/filter_selection.json').read_text())
    phases=json.loads((ROOT/'results/filter_selection_qsp.json').read_text())
    rng=np.random.default_rng(SEED);rows=[]
    for index,case in enumerate(design['cases']):
        prior=case['prior'];a=float(F(prior['a']));u=float(F(prior['u']));E=float(F(prior['mean_error']))
        selected=case['selected'];realization=phases['cases'][index]['phase_realization']
        angles=np.array([float(F(v)) for v in realization['phases_exact_decimal_radians']])
        n=8;target=u*.73;mass=a+(1-a)*.21
        lam=np.r_[target,target+(1-target)*np.sort(rng.uniform(.00001,1,n-1))]
        # Include a nearly degenerate excitation in one test of each pair.
        if index%2==0:lam[1]=target+1e-7
        probabilities=np.r_[mass,(1-mass)*rng.dirichlet(np.ones(n-1))]
        x=np.sqrt(probabilities);v=np.eye(n)[0]-x
        Q=np.eye(n)-2*np.outer(v,v)/(v@v)
        B=(Q*np.sqrt(lam))@Q.T;G=B.T@B
        complement=(Q*np.sqrt(1-lam))@Q.T
        W=np.block([[B,1j*complement],[1j*complement,B]])
        def rotation(phi):return np.diag(np.r_[np.full(n,np.exp(1j*phi)),np.full(n,np.exp(-1j*phi))])
        U=rotation(angles[0])
        for angle in angles[1:]:U=U@W@rotation(angle)
        H=np.kron(np.array([[1,1],[1,-1]])/math.sqrt(2),np.eye(2*n))
        select=np.zeros((4*n,4*n),complex);select[:2*n,:2*n]=-1j*U;select[2*n:,2*n:]=1j*U.conj().T
        full=H@select@H
        input_state=np.eye(n)[0];accepted=full[:n,:n]@input_state
        success=float(np.vdot(accepted,accepted).real)
        state=accepted/math.sqrt(success);mean=float(np.vdot(state,G@state).real)
        c=np.array([float(F(v)) for v in selected['chebyshev_coefficients']])
        response=float(F(prior['kappa']))*np.polynomial.chebyshev.chebval(2*lam-1,c)/selected['certificate']['global_normalization']
        reference=float(probabilities@response**2)
        expected=(Q*response)@Q.T
        response_error=float(np.max(np.abs(full[:n,:n]-expected)))
        unitary_error=float(np.max(np.abs(full.conj().T@full-np.eye(4*n))))
        assert response_error<1e-10 and unitary_error<1e-10
        assert mean-target<=float(F(selected['bias']))
        assert success>=realization['implemented_success_lower']-1e-12
        M=selected['samples'];repetitions=200
        readouts=rng.binomial(M,mean,size=repetitions)/M
        attempts=M+rng.negative_binomial(M,success,size=repetitions)
        failure_count=int(np.sum(np.abs(readouts-target)>E))
        rows.append({'design_index':index,'prior':prior,'matrix_dimension':n,
                     'initial_state':'computational |0>; no target-eigenvector preparation',
                     'B_matrix':B.tolist(),'gram_eigenvalues':lam.tolist(),
                     'initial_spectral_weights':probabilities.tolist(),
                     'QSP_signal_queries':len(angles)-1,'LCU_serial_signal_queries':2*(len(angles)-1),
                     'unitarity_error':unitary_error,'matrix_response_error':response_error,
                     'success':success,'spectral_success_reference':reference,
                     'filtered_mean':mean,'true_minimum':target,'mean_bias':mean-target,
                     'replicates':repetitions,'confidence_failures':failure_count,
                     'mean_attempts_simulated':float(np.mean(attempts)),
                     'mean_attempts_theory':M/success,
                     'max_observed_estimation_error':float(np.max(np.abs(readouts-target)))})
    out={'metadata':{'seed':SEED,'numpy':np.__version__,
                     'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                     'design_sha256':hashlib.sha256((ROOT/'results/filter_selection.json').read_bytes()).hexdigest(),
                     'phase_sha256':hashlib.sha256((ROOT/'results/filter_selection_qsp.json').read_bytes()).hexdigest(),
                     'scope':'32x32 block-unitary matrix simulation; synthetic oracle, no physical-gate synthesis'},
         'cases':rows}
    (ROOT/'results/filter_selection_matrix.json').write_text(json.dumps(out,indent=2)+'\n')
    print('PASS',len(rows),'full block-matrix cases,',sum(r['replicates'] for r in rows),'sampling replicates')


if __name__=='__main__':main()
