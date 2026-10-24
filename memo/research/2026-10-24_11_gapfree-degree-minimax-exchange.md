# 2026-10-24_11_gapfree-degree-minimax-exchange

更新日：2026-10-24（日本時間）  
作業モデル：Luna、medium。研究方向・比較条件・仮説採否は本人認可に基づき委任。追加予算・外部公開なし。

## 要点

memo10の次数2以下不可能ゲートと次数58 shifted-power十分構成の間を、次数制約付きminimax LP exchangeでscreenした。固定条件は \(\eta=0.1\)、ground bracket \([L,U]=[-.05,.05]\)（幅 \(W=.1\)）、全support \([E_0,E_{max}=1]\)、gap unknown、受理後filtered-mean bias目標 \(b=.01\)。前memoの制約なしscalar最適伝送は \(1/59049=1.6935\times10^{-5}\)。

- arbitrary weight polynomial relaxationとnonnegative amplitude polynomialのfinite-grid LPを分けた。LP solverの最適値だけを厳密上界・下界として扱わず、係数実現性、grid制約、validation残差を併記した。
- design slack \(b_{design}=.0095\)、evaluation target \(.01\)、support grid floor \(p\ge10^{-5}\) とした次数20の実振幅多項式候補は、独立validation grid上で最大bias \(.00950000000008\)、bracketの最小weight \(8.9177\times10^{-6}\) を得た。Chebyshev係数L1は \(0.9999999999999999\) で、正規化domain上の \(|p|\le1\) は係数三角不等式で満たす。しかし連続bias/positivity certificateは得ていないため、**grid-validated candidate**に留める。次数20での改善は未確認。
- no-slack次数20のdense biasは \(.01001068\) でわずかに不合格。weight relaxationは次数30でgrid objective \(1.8544\times10^{-5}\) がscalar上限を超え、dense biasも \(.0109626\)。これはgrid/relaxationの楽観性を示す数値反例で、真の連続最適値ではない。
- 既存のgeneral-basis minimaxと深さ/重なりtradeoffが強く既出。LP exchange自体は既存最適化技法で、新アルゴリズムとは主張しない。robust unknown-bracket mean-bias lossの最小次数/実質GSEE価値は未解決である。

## 定式化

二準位必要十分bias条件（前memo9–10）は全 \(x=E_0-L\in[0,W]\)、全 \(d>b\) で
\[
 \frac{w(L+x+d)}{w(L+x)}\le\frac{A}{d-b},
 \qquad A=\frac{b\eta}{1-\eta}.
\]
線形weight-residualは \((d-b)w(L+x+d)-Aw(L+x)\le0\)。二つのLPを区別した。

1. **weight relaxation**：Chebyshev基底の \(w\) をdegree \(2n\) の多項式変数とし、sampled supportで \(0\le w\le1\)、ground gridで \(w\ge t\)、grid pairで上の線形条件を課し \(t\) を最大化する。これは \(w=|p|^2\) 実現条件を外した上、連続条件をgridに限定した二重緩和である。数学的grid LP optimumは真のcontinuous amplitude optimum以上になり得るが、HiGHSが返すprimal feasible objectiveはgrid LP optimum以下であり、それ自体は厳密upper boundではない。
2. **amplitude LP**：grid上でreal \(p\ge0\) と \(p\le1\) を課す。非負性のもとでweight ratioは \(p(y)\le\sqrt{A/(d-b)}p(x)\) と同値になり、これも線形制約となる。評価側ではsquare-weight biasと \(|p(y)|/|p(x)|\) を検査する。有限gridで正でも連続区間正値とは限らず、QSVT parity/phase synthesis・circuit costも含まない。

各solveはChebyshev変数 \(z=2(E-L)/(E_{max}-L)-1\)。初期gridはground 21点、excitation 101点、support 201点。5回まで各roundのworst dense-pair違反を最大4本cutとして加え、独立validationにground 101、excitation 501、support 501点を用いた。SciPy HiGHS feasibility tolerancesは \(10^{-9}\)。最大化されたgrid objectiveだけでなく、primal residual、dual gap、dense bias、support extremaをJSONに出力する。solver residual/gapは浮動小数診断で厳密証明ではない。

## Screen結果

| LP family / amplitude degree | design bias | LP grid min-ground weight | dense max bias at target .01 | dense min support response | dense pair violation | dense target pass |
|---|---:|---:|---:|---:|---:|---|
| weight relaxation, n=16 (weight degree 32) | .01 | \(1.2492\times10^{-5}\) | .0101002 | \(-2.53\times10^{-9}\) | .01031 | no |
| weight relaxation, n=30 (weight degree 60) | .01 | \(1.8544\times10^{-5}\) | .0109626 | \(-6.61\times10^{-9}\) | .09998 | no |
| nonnegative amplitude LP, n=16 | .01 | 0 (trivial LP solution) | 0 (no accepted state) | 0 | undefined | not evidence of impossibility |
| nonnegative amplitude LP, n=20 | .01 | \(1.6451\times10^{-5}\) | .0100107 | \(-8.52\times10^{-7}\) | .001134 | no |
| nonnegative amplitude LP, n=20, slack/floor | .0095 | \(8.9177\times10^{-6}\) | .00950000000008 | \(9.9994\times10^{-6}\) | \(4.2\times10^{-12}\) | yes, dense grid only |

For the last row the dense bracket min weight after global coefficient-L1 scaling is also \(8.9177\times10^{-6}\); the L1 coefficient sum is 0.9999999999999999. The scalar optimum is \(1.6935\times10^{-5}\), so this grid-screen candidate is 0.5267 of that ideal scalar transmission and 0.9824 of the degree-58 shifted-power raw transmission \(9.0778\times10^{-6}\). These ratios are candidate screening figures only; no continuous guarantee or degree improvement is established.

A small Bernstein interval-certificate attempt for the slack candidate (one full rectangle and 2-by-4 subdivision of the ground/support rectangle) retained positive Bernstein coefficients for the pair residual, so it did not certify the continuous condition. Higher refinement was not run. The dense-grid minimum amplitude is positive, but that alone is not an interval proof.

## 既存法との照合・新規性

- Lee et al., *Filtered Quantum Phase Estimation*, [arXiv:2510.04294v2](https://arxiv.org/html/2510.04294v2)：本文§IV.1–IV.3、補遺§V.1–V.4、§VI、§VIIIを確認。known-center rejection ratio、Gaussian/low-pass/band-pass、polynomial/trigonometric general-basis minimax、coarse prior後の二段設計とcost-overlapを扱う。現在のlossは「未知ground bracketの全targetに対するgap-free conditional-mean bias」で論文の個別定式化とは一致しないように見えるが、既存minimaxの制約変換/一様化に包含されるかは未解決。今回の数値LPはその一般minimaxを上回らない。
- Filip & Fitzpatrick, *Beyond asymptotic reasoning: the practicalities of a quantum ground state projector based on the wall-Chebyshev expansion*, [arXiv:2508.00533v3](https://arxiv.org/html/2508.00533v3)：§II、IV–Vを確認。粗い上側エネルギーpriorへの頑健性、projector fidelity、serial oracleと成功確率を比較する。目的損失はfiltered meanと異なるが実装baselineとして必要。
- Lin & Tong, *Optimal polynomial based quantum eigenstate filtering with application to solving quantum linear systems*, [arXiv:1910.14596v4](https://arxiv.org/abs/1910.14596v4)：Abstractと本文既読範囲（既存レビュー参照）。QSP/minimax polynomial filteringは既出で、nontrivial target overlapとreasonable gap lower boundを仮定する。
- Dong, Lin & Tong, *Ground state preparation and energy estimation on early fault-tolerant quantum computers via quantum eigenvalue transformation of unitary matrices*, [arXiv:2204.05955v2](https://arxiv.org/abs/2204.05955v2)：Abstractを確認。controlled-time-evolution oracleを使うQET-Uで、浅いcircuit GSEEとfilteringを扱う。CTE baselineとの比較上、単なる関数族screenより強い。
- Wang et al., *State Preparation Boosters for Early Fault-Tolerant Quantum Computation*, [arXiv:2202.06978v3](https://arxiv.org/abs/2202.06978v3)：Abstractを確認。limited-depth Gaussian boosterがN₂を含むground-overlap増幅を示す。フィルタ深さとoverlap tradeoffは既出で、化学動機とも近い。
- McArdle et al., *Variational ansatz-based quantum simulation of imaginary time evolution*, [arXiv:1804.03023v4](https://arxiv.org/abs/1804.03023)：Abstractを確認。molecular H₂/LiHでimaginary-time ground-state preparationを実演。指数的tilting/energy cooling自体を新規動機とはしない。

Focused novelty auditでも、broad depth-aware filter designは既出、unknown-bracket uniform filtered-mean lossと最小ground transmissionの完全同型資料は確認できていない一方、目的関数の違いだけでは研究価値にならず、same error/success/depthでfilter-free CTE/Hadamard、FQPE、QET-Uと比較する必要があると判断された。探索は網羅的でない。Powers–Reznick (2000, DOI [10.1090/S0002-9947-00-02595-2](https://doi.org/10.1090/S0002-9947-00-02595-2))のinterval-positive polynomial SOS結果は今後の連続正値制約の関連手法候補だが、今回のfiltered-mean目的を扱った証拠ではない。

**仮説位置付け：** degree-constrained robust filter designの数値minimaxを新methodとして提案しない。現時点での具体的成果は、次数58の解析十分構成に近いtransmissionを示す次数20のgrid candidateと、連続証明・oracle/implementation costが残る明確な再現仕様である。n=20 improvement、algorithm novelty、energy-estimation advantage、量子優位性はいずれも未確認。

## 再現・残件

[script](../../experiments/gapfree_degree_minimax_exchange.py) / [full JSON](../../results/gapfree_degree_minimax_exchange.json)。NumPy 2.3.5、SciPy 1.17.0、Python 3.12.14、乱数なし。5 exchange rounds、solver tolerances/grid sizes/coefficients/LP primal-dual diagnosticsをJSONに保存。スクリプトから結果JSONを二度再生成しbyte一致、`py_compile`成功。

```sh
python experiments/gapfree_degree_minimax_exchange.py > results/gapfree_degree_minimax_exchange.json
python -m py_compile experiments/gapfree_degree_minimax_exchange.py
```

次の判定に必要なのはslack candidateのfull-precision Chebyshev係数による連続 \(p(E)>0\) とpair residual \((d-b)p(E)^2-Ap(E_0)^2\le0\) の区間検証、および既存FQPE/QET-U/CTE estimatorと同じ全工程depth・success・errorでの比較である。標準QSVT parity/phase列、compiled depth、LCU cost、circuit実行、Lean検証は未実施。
