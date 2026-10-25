# 2026-10-25_2_calibration-free-fmpe-screen

更新日：2026-10-25（日本時間）
作業モデル：Luna、medium。追加予算・外部公開なし。先行法包含を優先し、新規性を保証しない。

## 判定
校正free・固定depthのzero-DC ratio単独は新algorithm候補として棄却。中心対称では未知nuisanceのprofile MLEがoracle-nuisanceと漸近同効率、R20 toyでもzero-DCは目標誤差0.1 radの95% certificateを出せなかった。残すのは「未知nuisance下のfinite-confidence/depth adaptationが、同予算のprofile/plug-in/fixed robust推定に対し改善し、oracle情報有利ceilingに近づく条件・cost regretを示せるか」という未確立の調査候補のみ。新テーマに確定しない。

## 先行法の仮定・費用
- Zhang et al., Quantum Imaginary-Time Evolution with Polynomial Resources in Evolution Time, arXiv:2507.00908v4, §2.3, §3.1, Lemma 5, Alg.1/Thm.6: normalized finite-time ⟨H⟩をGSEE proxyにし、γ/lower bound Bのpromise下でunknown τ,λをratioと適応探索で選ぶ。Thm.2のITE state preparation cost (query Õ(γ⁻²τ), copies Õ(γ⁻²), depth Õ(τ)) はGSEE全体費と別。GSEE Alg.1/Thm.6はtotal query Õ(γ⁻⁴τ⁴) (B=O(γ²)), depth Õ(τ)、反復ごとのshotsはAlg.1に 8LΛ²t³B⁻²。固定bracket案はこの探索費と成功率/degreeを全体比較する必要。
- Dutkiewicz et al., Accurate ground state energy estimation with noise and imperfect state preparation, arXiv:2603.21873v2, §IV.E–F, Def.25 Eq.(58), Lemma 29, Thm.30–31: global-depolarizing/GDN型noise、isolated known gap/target promise、位相guess誤差 < gap/3。GDN theoremはa0を既知入力に置く。F=e^(−γt)、σ≈1/tを結合。shifted meanはpersistent varianceを持ちFMPEが改善すると報告、a0/F data estimationはfuture work。Eq.(58) normalized densityは個別F,a0でなくr=Fa0/(1−F)に依存し、profile likelihoodが必須baseline。

## 問い・比較基準
狭い問い候補は、known isolated promiseとcertified overlap lower boundを保ち、未知GDN nuisance F,a0下のfinite-confidence/depth adaptationがprofile likelihoodまたはplug-inの較正費込み同一budgetを改善するか。arbitrary unknown overlap無条件保証やgeneric query-optimalityは対象外。oracle nuisance既知は情報有利ceilingであり超える目標ではない。
最低baseline: oracle-α phase MLE proxy（論文FMPE実装ではない）、全データprofile MLE、25% pilot費込みplug-in MLE、zero-DC ratio。比較時はsame samples/depth/error/confidence、accepted windowならdiscard shots、overlap・normalization・pilot/calibration costを揃える。改善なし、必要shotが減らない、標準profile fitに帰着すればnew algorithm主張を棄却する。

## 手計算
reduced density p(x;φ,α)=αgσ(x−φ)+(1−α)/(2π)、gは円周上even wrapped Gaussian。φ=0では ∂φp はodd、∂αpとpはevenなので Fisher cross term Iφ,α=∫(∂φp)(∂αp)/p dx=0。正則条件下profile phase information Iφφ−Iφ,α²/Iαα=Iφφ。中心では未知αのprofile MLEと既知α oracleのphase漸近分散が一致する。さらに E[cos X]=αe^(−σ²/2)cosφ、E[sin X]=αe^(−σ²/2)sinφ よりzero-DC momentsの比はtanφ。これらの恒等式自体に新規性は主張しない。model-specific手導出でLean未検証。

## R20 classical toy
再現コード・出力：experiments/calibration_free_fmpe_toy.py、results/calibration_free_fmpe_toy.json。seed 20261025、N=2000 statistical samples/run、20 replicates/case、σ=.35、F=.3,a0=.1からα=Fa0/(Fa0+1−F)=.0410959、phase=0/.07、domain[-.8,.8]、Python3.12.14 / NumPy2.3.5 / SciPy1.17.0。reduced normalized mixture α·wrapped-normal+(1−α)·uniformから全circle samplesを保持。元GDN full spectral model/spurious phases/window rejection、quantum query/depth/circuit/physical gateは再現せず、Nはstatistical samplesでquery budgetではない。
zero-DCはh0=cos x,h1=sin x、δ=.05のHoeffding mean radius e=√(log(4/δ)/(2N))を使用。denominator CI available center 11/20、offcenter 8/20だが、median phase halfwidth 1.53/1.47 radで target .1を全20/20ケース認証できない。Profile MLE optimizer/boundary diagnosticは2/20、1/20で、model-intrinsic impossibilityではない。point MSE / failure-penalized screen risk:
|φ|method|MSE returned estimates|diagnostic/certificate failure|penalty risk|
|0|oracle-α MLE proxy|.0170|0/20|.0170|
|0|profile MLE|.1420|2/20|.3340|
|0|25% pilot plug-in|.0348|0/20|.0348|
|0|zero-DC ratio|.0733 (11 estimates)|20/20|2.56|
|.07|oracle-α MLE proxy|.0141|0/20|.0141|
|.07|profile MLE|.0493|1/20|.1394|
|.07|25% pilot plug-in|.0224|0/20|.0224|
|.07|zero-DC ratio|.1232 (8 estimates)|20/20|2.56|
zero-DC MSEはdenominator判定後に値を返せたsubsetの参考値であり性能判定に使わない。penalty riskは未認証/optimizer diagnosticをphase interval最大誤差1.6の二乗に置換し、失敗を良好標本から落とさない指標。R20は探索screenで統計的有意差の主張なし。script二回実行でJSON byte一致、py_compile成功。

## 継続条件
校正free fixed-depth ratio単独は棄却。未知nuisance under finite-confidence/depth adaptationは調査候補のみ。価値条件は同budgetでprofile/plug-in/fixed robustに対するcoverage・failure-aware total cost改善、かつoracle-information ceilingに近づく保証。次の最小調査はFMPE paperでa0,Fがtheorem assumptionかparameter selectionだけかを確定し、original GDN modelでaccepted/rejected shotsとdepthを含めた比較仕様を作ること。新規性・実用性未確立。連続certificate、QSVT位相合成、量子回路、化学Hamiltonian、Leanは未実施。
