# 2026-10-24_7_filter-design-screen

更新日：2026-10-24

## 要約

prior-onlyの粗い数値screenを標準Pythonで実行した。固定した比較条件では、有限差分filtered-mean proxyに対してno-filterは許容biasを満たさず、12候補中の最小query-cost候補は (f(x)=\cos^6(\pi x/2)) だった。これは探索対象に入れた既知のbinomial cosine-power基準そのものであり、新候補の改善は見つかっていない。QCELS等の強い下流推定器との比較も未実装なので、フィルタの優位性を結論しない。

## 固定したscreen

- エネルギー中心 (E_c=0)、基底エネルギーbracket (E_0\in[-0.05,0.05])、励起gap下界 \(\Delta=0.50\)、基底初期重み下界 \(\eta=0.10\)、上端 (E_{max}=1)、\(\tau=\pi\)。
- 目標 \(\epsilon=0.30,\delta=0.05\)。全工程の深さ上限 \(D=20\) はideal controlled-evolution-time proxyであり、compiled gate depthではない。状態準備費用 (S=1) も任意の共通time-equivalent proxy。
- 係数候補は非負対称Fourier係数、\(c_{-k}=c_k\)、\(c_0+2\sum_{k>0}c_k=1\)、係数刻み0.25、\(K\le2\) の有限グリッドに、binomial \(\cos^{2m}(\tau x/2)\), (m=0,1,2,3) を加えて重複除去した12候補。\(h\in\{0.1,0.3,0.5,0.8,1.0\}\)。係数選択に真の (E_0) やsynthetic validation spectrumは使わない。
- design proxyは \(E_0\) の5点、各点で励起エネルギーの51点。固定された二点分布のworst-case filtered-mean bias
  \[
  b_f(E_0,E)=\frac{(1-\eta)w(E)(E-E_0)}
  {\eta w(E_0)+(1-\eta)w(E)},\qquad w(E)=|f(E-E_c)|^2
  \]
  を走査する。この式は既知の \(p_0\ge\eta\) と許容supportの下で、励起tailを単一エネルギーに置く二準位分布について得られる解析的な式だが、今回の連続区間全体の最大値はグリッド近似である。したがってcertified interval boundとは呼ばない。
- 下流proxyはfiltered meanの一象限Hadamard有限差分 \(E_c-\mathrm{Im}\,g_f(h)/h\)。これはground energy estimator単独ではない。切断誤差上界は \(h^2R^3/6\)（このsupportでは (R=1)）。残差 \(\epsilon_{stat}=\epsilon-b_{proxy}-h^2R^3/6\) に対してHoeffding標本数を置く。
- physical列はLCU係数norm (L_1=1)、\(p_{herald}\ge z_{lower}/L_1^2\)、失敗後に毎回状態・filterを作り直す期待回数で費用化。virtual列は \(|f|^2\) のautocorrelationをmergeし、その係数norm (B\) と既知priorの (z_{lower}\) を用いた比推定誤差配分を費用化した。未知normalizerのratio estimatorがunbiasedとは仮定しない。双方に同じ (S) を課す。
- synthetic validationは設計後の評価だけ：bracket左/右スペクトル、二準位extremizer、さらにgap仮定を破る対称配置counterexample。seedなし・決定的。

## 結果

| ケース | 係数 (c_0,c_1,c_2,c_3) | (h) | gridded bias proxy | (z_{lower}) | physical費用proxy | 最大depth proxy |
|---|---:|---:|---:|---:|---:|---:|
| no-filter | (1) | 0.5 | 0.945 | 0.100 | infeasible (\(\epsilon_{stat}\le0\)) | — |
| screen最小physical費用 | (0.3125, 0.234375, 0.09375, 0.015625) | 0.5 | 0.129367 | 0.096363 | 192,911 | 9.925 / 20 |

最小候補は \(\cos^6(\pi x/2)\) のFourier係数である。LCU (L_1=1)、merged virtual係数norm (B=1)。finite-difference bias boundは0.041667、統計誤差に残る許容量は0.128966、physical accepted-shot proxyは1,775、期待attempt proxyは18,420。これらの大きな標本費用は保守的Hoeffding式とこのtoyのproxy条件による。compiled circuitのゲート費用を表さない。

選んだ関数のpost-hoc filtered-mean biasはvalidation左bracket 0.06384、右bracket 0.01052、gap下界を満たす二準位extremizer 0.129367。\((-0.05,0.05)\) の対称counterexampleでは0.09だが、これは \(\Delta=0.50\) を破るout-of-claim test。no-filter meanの対応biasは左0.623、右0.672、二準位0.45。この不利はこのmean proxyだけの結果で、QCELS/QPE/CDF等no-filter ground-energy estimator自体の失敗を意味しない。

選ばれた同一係数をvirtual列で費用評価した値は約10,271,275で、当screenの同一期待信号・保守的shot modelではphysical経路より大きい。ただし今回の関数設計主題に対する評価土台の一結果に限る。virtualとの方式優劣、新規なfilterの性能改善、化学・物性系への適用、物理回路の深さ/コストは主張しない。既知Gaussian-derivative、QCELS、QETU/FQPEなどの強いbaseline実装・同条件比較は残る。

## 解析上の読み方と限界

- この探索では既知cosine-power族に戻り、追加候補の優位はなかった。結果は「新規性なし」のscreening evidenceとして扱う。
- no-filterが失格したのは、filtered meanを下流推定量にした固定条件のためである。no-filterの強い推定器を比較していないため、フィルタを使うべきという結論にしてはいけない。
- (D=20) は時間queryのproxy。(K\tau+h) 等は理想化した経路モデルであり、QETU等の合成後depthを保証しない。SELECT/LCUの回路や具体的なHamiltonian simulation、(C_{prior})、bracket/gap/overlapを得る費用は数えていない。
- gridは区間全体を証明しない。必要なら次段でLipschitz/解析的上界を証明する。設計用priorだけで選び、既知toyの真値は係数決定に漏らしていない。
- 量子回路実行、PennyLane/旧実装の照合、実データ実験は未実施。

## 再現

標準Python 3.12.14、外部依存なし、乱数なし。

```sh
python experiments/stage2_filter_screen.py > results/stage2_filter_screen.json
```

2回の実行出力は `cmp` でbyte一致を確認した。実装：[stage2_filter_screen.py](../../experiments/stage2_filter_screen.py)、機械可読出力：[stage2_filter_screen.json](../../results/stage2_filter_screen.json)。

## 既存研究との関係・資料範囲

今回のscreenは既存法の包含/差分を証明しない。filter関数の新規性は未確認。強いbaselineと仮定の照合は以下の既存一次資料レビューを参照し、各資料の読んだ節・定理・URLをそこに記録した。

- [段階2の理論候補・費用モデル](2026-10-24_5_stage2-theory-candidates.md)：FQPE v2 (arXiv:2510.04294, §§II.1–II.4, Suppl. IV.2–IV.3)、QETU (arXiv:2204.05955, §§I–III.1, Thm. 1, 4, 5)、Lin–Tong CDF (arXiv:2102.11340, §§1–5, Apps. D–E)、QCELS (arXiv:2211.11973, §§I–IV, Thm. 1–3, Cor. 4)、Wang et al. (arXiv:2209.06811, §§1–2, Thm. 1.1, Cor. 1.2)、Kaiser/QETU比較 (arXiv:2507.01361, §§II.1–II.5, III.1, Apps. A–B)。
- [物理・virtual評価式とsanity check](2026-10-24_6_physical-virtual-filter-depth.md)：(z_f=\mathrm{Tr}(\rho f^\dagger f))、physical herald (z_f/L_1^2)、virtual numerator/denominatorの誤差・費用の区別。

Commit/pathはGitHub main上の同名memoと成果物を参照。
