# 2026-10-24_9_gapfree-minimax-envelope

更新日：2026-10-24（日本時間）  
作業モデル：Luna、medium。研究方針/仮説採否は本人認可に基づき委任。追加予算・公開なし。

## 要点

未知の基底エネルギー (E_0\in[L,U])、gapなし、初期ground overlap (p_0\ge\eta) のもとで、**同じ非適応filter weight (w(E)=|f(E)|^2\le1)** が任意の初期spectral weightsに対しfiltered-mean biasを (b) 以下にする条件を導いた。この条件下で bracket上の最小ground transmission (inf_{E_0\in[L,U]}w(E_0)) の厳密な上限と、その上限を達成する任意スカラーweightを構成した。物理herald probabilityそのものの最適化ではなく、LCU normalization、有限次数/query depth、filter実装費を一切含まない関数レベルの補題である。

この補題はFQPEのknown-target relative-rejection/minimax枠組みの直接的なrobust extensionに見える。**新規性は未確認**で、完成済み新規成果とは扱わない。固定filterの新familyも見つかっていない。次の有望候補は、厳密なスカラー最適weightをdepth-bounded polynomial/trigonometric filterで近似するときのworst-case bias / ground-transmission / depthの交換条件だが、既存FQPE minimaxに包含される可能性が高く、まだ着手/採用していない。

## モデルと必要十分条件

Hamiltonian spectrumは各許容instanceについて ([E_0,E_{max}])、真のground energyは利用可能なbracket ([L,U]) 内、gap lower boundはない。filterは真の (E_0) に依存しない固定関数で、(0\le w(E)=|f(E)|^2\le1)。(w(E_0)=0) ならそのinstanceを受理できず、uniform mean guaranteeに使えない。

入力状態 (p_0\ge\eta) に対し、filter成功後のenergy meanと (E_0) の差を考える。単一excited energy (E_0+d) に残余確率を置く二準位状態では
\[
B(E_0,d)=
\frac{(1-\eta)w(E_0+d)d}
{\eta w(E_0)+(1-\eta)w(E_0+d)}.
\]
任意分布に対するbias (\le b) の必要十分条件は、全許容 (E_0) と全 (d>b) で
\[
\frac{w(E_0+d)}{w(E_0)}
\le
\frac{A}{d-b},\qquad A:=\frac{b\eta}{1-\eta}.
\]
十分性は、bias−(b) の分子を (\sum_{j>0}p_jw(E_j)(d_j-b)) と書き、各excited termの比条件を使う。必要性はviolating energyにtail全量を置く二準位状態で達成する。(d\le b) の状態は許容誤差内なので相対抑制を要しない。これは直接の代数導出で、既存論文の定理を引用したものではない。

## 固定filter transmissionの厳密なスカラー上限

\[
\delta_0:=b+A=\frac{b}{1-\eta},\qquad
F(x):=\max\left(\{0\}\cup
\left\{n\log\frac{x/n-b}{A}:
n\in\mathbb Z_{>0},\;x/n>\delta_0\right\}\right).
\]
空集合のとき (F(x)=0)。各 (n) を固定したとき、(log(d-b)) の凹性から総幅 (x) を (n) 個に等分した刻みが、attenuation chainの積を最大化する。したがって任意の可行 (w\le1) について
\[
w(U)\le e^{-F(U-L)}.
\]
左辺はbracket上の最小ground transmission以上とは限らないので、一般には (inf_{E_0\in[L,U]}w(E_0)\le w(U)\le e^{-F(W)})（(W=U-L)）。純粋ground inputであれば、(E_0=U) におけるideal direct-filter herald確率はこの上限以下、期待試行数は (e^{F(W)}) 以上。混合入力のactual (z_f)、LCU normalization (L_1)、成功確率平均を最適化した主張ではない。

この上限はスカラー関数のクラスでは達成可能。(x\ge0) に対し
\[
w_*(L+x):=e^{-F(x)}.
\]
(F) は非減少かつsuperadditive。(d>\delta_0) なら (F(x+d)-F(x)\ge\log((d-b)/A))、一方 (b<d\le\delta_0) なら右辺は非正で非減少性だけで十分。よって (w_*) は全連続tail上の必要十分比条件を満たし、(w_*(E_0)) はbracket内で非増加、(w_*(U)=e^{-F(W)})。従って
\[
\sup_{w:\,\text{uniform mean-bias}\le b,\;0\le w\le1}
\inf_{E_0\in[L,U]} w(E_0)=e^{-F(W)}
\]
は**unconstrained scalar weight**の厳密解。証明は手導出であり、Lean/形式検証は未実施。

(w_*=1) が ([L,L+\delta_0]) にわたり一定で、その後非定数となる。有限degree polynomial/trigonometric responseの (|f|^2) は実解析的なので、このprofileを区間全体で厳密に実現できない（解析関数が開区間で定数なら恒等的に定数）。従って有限depthでの達成には近似・bias slack・success低下を避けられない。次数や追加depthの評価は今回行っていない。

## 有限区間の数値と近似誤差の小例

標準Python 3.12.14、乱数なしで、(\eta=0.1)、([L,U]=[-0.05,0.05])、(E_{max}=1) を固定した。(F(W)) の最大化は有限個の整数 (n) の比較で、attempt proxyは有理数の厳密比較から出した。

| 許容mean bias (b) | 最適chain刻み (W/n) | step ratio上限 (A/(W/n-b)) | scalar transmission上限 (e^{-F(W)}) | ideal pure-ground試行下界 (e^{F(W)}) |
|---:|---:|---:|---:|---:|
| 0.02 | 0.033333… ((n=3)) | 1/6 | 1/216 | 216 |
| 0.01 | 0.02 ((n=5)) | 1/9 | 1/59,049 | 59,049 |
| 0.005 | 0.01 ((n=10)) | 1/9 | 1/3,486,784,401 | 3,486,784,401 |

前memoの (\Delta=2b/(1-\eta)) は有効だが有限幅で最良とは限らないchain刻みであり、例えば (b=0.01) では下界14,641だった。今回 (F(W)) で全等分chain数を比較し、59,049へ強めた。これも理想スカラーtransmissionの結果だけで、algorithmic runtimeや量子回路数の報告ではない。

大幅区間では指数rateの比較用に (r=W_0(((1-\eta)/\eta)/e)) と置く。(w_{exp}(E)=\exp[-(r/b)(E-L)]) は比条件を満たし、(F(W)\le rW/b)。これは既知のimaginary-time/Gibbs型指数filterの比較基準であり、有限幅では一般に (w_*) のスカラー最適性を達成せず、LCU/CTE実装費も未評価。

active constraintの感度確認では (b=0.01,E_0=U=0.05,d=0.02) とすると厳密profileのweightはground (1/59{,}049\approx1.6935\times10^{-5})、excited (1/531{,}441\approx1.8817\times10^{-6})、比 (1/9)、mean biasちょうど (0.01)。仮にweight responseへ一様な絶対floor (10^{-6}) を加えると比は0.16067、biasは0.011824に増え、certificateを破る。これはactive constraintにslackがないことを示す簡単な感度例に過ぎず、有限degree filterの近似実験や新しい結果とは主張しない。絶対近似誤差だけではtailの相対比を守れず、将来の近似設計では非一様relative error/slackを扱う必要がある。

コードは[gapfree_minimax_bound.py](../../experiments/gapfree_minimax_bound.py)、出力は[gapfree_minimax_bound.json](../../results/gapfree_minimax_bound.json)。再現：
```sh
python experiments/gapfree_minimax_bound.py > results/gapfree_minimax_bound.json
python -m py_compile experiments/gapfree_minimax_bound.py
```
二回のscript出力は `cmp` でbyte一致。JSON内のprofile pairwise grid checkは公式性を与える証明ではなく、小数実装の整合確認のみ。連続条件の成立は上記手導出による。

## 既存法との照合と候補の棄却

| 一次資料 | 読んだ範囲・関係 | 判断 |
|---|---|---|
| Lee et al., *Filtered Quantum Phase Estimation*, [arXiv:2510.04294v2](https://arxiv.org/html/2510.04294v2) | 本文§II.1–II.4、IV.1–IV.3、補遺V.1–V.4を再確認。§IV.1 Eq.(IV.3)はknown (E_0) に対するrelative rejection ratio、IV.3/Vはsuppression-band Chebyshev/Dolph/general-basis minimax、V.4はknown shifted center (mu)。本文II.3はcoarse (E_0,E_1)+gap priors、II.4は先にQPEでcoarse estimatesを得る二段法。 | 固定filterのsuccess/relative-leakage tradeoffと一般basis minimaxは強く既出。今回のunknown-target bracket全体のfiltered-mean lossから導く exact finite-W scalar envelopeが同じ結果の単なる書き換えかは未確認。新規性未確立。 |
| Filip & Fitzpatrick, *Beyond asymptotic reasoning: the practicalities of a quantum ground state projector based on the wall-Chebyshev expansion*, [arXiv:2508.00533v3](https://arxiv.org/html/2508.00533v3) | Abstract、§I–II、III、IVの実装/成功確率、Vの数値比較。未知 (E_0) に対しoverestimate (S>E_0) を使う壁関数projectorは、delta/step filterが失敗する例でも基底成分を維持する。一方でsuccess probabilityの低下、LCU normalization、product/GQSVT選択を比較する。 | broad one-sided priorでfilterを頑健化する発想も既出。状態射影/fidelityを扱い、今回のtarget-bracket一様filtered-mean guaranteeとはlossが異なるが、強baselineとして必要。 |
| Wang et al., *Efficient ground-state energy estimation and certification on early fault-tolerant quantum computers*, [arXiv:2304.09827v2](https://arxiv.org/html/2304.09827v2) | Abstract、§1のlimited-operations cost modelとgap-free rejection-sampling certificationの説明。主GSEE estimatorはknown gap下界を使う。Gap-free testは正しい (\epsilon)-energy estimateだけを受理するが、sample complexityを持つ。 | depth-limited certification/GSEE baselineは既出。filter-mean chainはその一般lower boundではなく、direct comparisonが必要。 |
| Lin & Tong, *Heisenberg-limited ground-state energy estimation*, arXiv:2102.11340v2, §§1–5, Apps. D–E、および Ding & Lin QCELS arXiv:2211.11973v2, §§I–IV, Thm.1–3, Cor.4 | 先行一次資料レビュー[memo](2026-10-24_2_filter-literature-and-asset-review.md)と[stage2 memo](2026-10-24_5_stage2-theory-candidates.md)で読了範囲記録済み。CDFはCTE/Hadamardからのfilter-free GSEE、QCELSはFourier filteringを含む浅いenergy estimator。 | Adaptive localization+filterを主案とするだけでは二段FQPE/CDF/QCELSと重なるため棄却。 |

## 候補判断

**次段の候補（条件付き、未採用）：** scalar optimum (w_*) を有限degreeのbounded polynomial/trigonometric (w_K=|f_K|^2) に近似し、次を同時に評価する問い。
- 固定gap-free bracketと (p_0\ge\eta) のもとで、全 (E_0\in[L,U])、全excited energy、全weightにmean bias (\le b) を保証すること。
- finite time support/query degree・filter normalizationを制約し、最小度数とworst-case ground transmissionを同じprofile (w_*) に対して比較すること。
- (epsilon)-slackのないexact optimumが有限degreeで実装不能なため、relative error envelopeとdesign slackが追加次数/成功費用をどう変えるか、FQPE minimax・wall-Cheb・Gibbs filterに対して評価すること。
- **棄却条件：** weighted-envelope問題がFQPE general-basis minimaxの直接再パラメータ化に過ぎる、または同一hard-depth/CTE/LCU costで既存baselineを超える解析・数値条件が残らない。現時点でこれらは未確認なので新規性を主張しない。

**今回保留した候補：** coarse localizationの後にlocal filterを当てるだけのadaptive pipeline。FQPE §II.4、Lin–Tong CDF、QCELS、wall-Chebの粗いenergy guess更新が近い既存経路。続けるには同一hard depth capにおける新しい全工程worst-case theorem/cost crossoverが必要。

本単位では有限degree最適化、QSP/QSVT実装、強baselineとの数値比較は実施していない。物理system、hardware/backend、追加予算、外部公開の判断は必要ない。新規性と有用性は未確定。
