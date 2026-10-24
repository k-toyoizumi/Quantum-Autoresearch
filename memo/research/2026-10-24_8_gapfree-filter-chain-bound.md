# 2026-10-24_8_gapfree-filter-chain-bound

更新日：2026-10-24（日本時間）  
作業モデル：Luna、medium。研究方向の選択・仮説の採否は本人認可に基づき委任。追加予算・外部公開なし。

## 要約

基底状態overlapの下界 \(\eta\) と、真の \(E_0\) を含む幅 \(W=U-L\) のcoarse bracketだけが分かるgap-free設定を考えた。filtered spectral meanのbiasをすべての許容 \(E_0\)・二準位敵対入力について \(b\) 以下に抑える一つの固定filterは、bracket内のあるpure-ground入力で小さいherald確率を避けられない。\(\eta=0.1, W=0.1, b=0.01\) では理想的な正規化済みfilterでも期待herald試行数が少なくとも14,641となる。

これは単一の固定filterをfiltered-mean proxyで使う場合の手証明であり、一般のground-energy estimationのno-go、depth query下界、新規性、または量子優位性ではない。固定filterファミリーの積極的な新規案は得られていない。FQPEのfilter minimaxとcost-overlap framework、FQPE二段法、Lin–Tong CDF、QCELS Fourier filteringとの重複が強いため、関数族の探索は一旦保留する。

## モデルと手導出

Hamiltonianの基底エネルギー \(E_0\) は未知で、\([L,U]\) 内にある。各許容インスタンスの初期状態の基底重みは \(p_0\ge\eta>0\)。excited energyは \([E_0,E_{max}]\) 内でgapは仮定しない。固定されたfilter \(f\) はbracket内の真の \(E_0\) を設計入力にせず、\(w(E)=|f(E)|^2\le1\) とする。全bracket上で \(w(E_0)>0\) を要する。零点があれば対応するtargetを受理できず、uniform bias guarantee自体が成立しない。

特定の許容 \(E_0\) について、二準位入力 \(p_0=\eta\)、残余重み \(1-\eta\) を一つの励起値 \(E=E_0+d\) に置く。physical filter受理後の平均エネルギーのbiasは
\[
B(E_0,d)=
\frac{(1-\eta)w(E_0+d)d}
{\eta w(E_0)+(1-\eta)w(E_0+d)}.
\]
より一般の励起分布のbiasはこの二点式のsupremum以下であり、二点分布が許されるため、任意の励起分布に対してbias \(\le b\) を保証する条件は、各固定 \(E_0\) で
\[
\frac{w(E_0+d)}{w(E_0)}
\le
\frac{b\eta}{(1-\eta)(d-b)}
\quad\text{for every } d>b
\]
である。これは今回のモデル内での代数的必要十分条件。距離 \(d\le b\) の重みは目標許容誤差内なので抑制条件を要しない。区間全体の連続保証には、上式を連続support上で示す必要があり、単なるgrid確認では代替できない。

この条件から、任意の \(\Delta>b\) に対して
\[
\frac{w(E_0+\Delta)}{w(E_0)}
\le\rho(\Delta)
:=
\frac{b\eta}{(1-\eta)(\Delta-b)}
\]
を得る。 \(U+\Delta\le E_{max}\) とし、\(m=\lfloor W/\Delta\rfloor\)。各 \(j=0,\ldots,m-1\) について真のground energyが \(E_j=L+j\Delta\) である別々の許容Hamiltonian/inputを考え、excited weightを \(E_j+\Delta\) に置く。全ての \(E_j\) はbracket内なので、固定filterの一様bias条件が必要である。連鎖して
\[
w(L+m\Delta)\le\rho(\Delta)^m w(L)\le\rho(\Delta)^m
\]
となる。従って、このbracket内のあるpure-ground inputでは、ideal normalized block-encoding filterのherald probabilityは最大でも \(\rho^m\)、期待attempt数は少なくとも \(\rho^{-m}\)。LCU実装で係数norm \(L_1>1\) により受理確率が \(w/L_1^2\) になる場合、試行下界はさらに \(L_1^2\) 倍となる。ここで異なる \(E_j\) は別々のworst-case instanceである。固定のfilterがそれら全てに対して同じbias保証をする、というquantifierがこの下界の要点。

分かりやすい一つの選択は \(\Delta=2b/(1-\eta)\)。この場合 \(\rho=\eta/(1+\eta)\)、\(m=\lfloor W(1-\eta)/(2b)\rfloor\)。これは簡単な明示下界を得る選択であり、全パラメータで最適な \(\Delta\) と証明したわけではない。

## 再現可能な数値例

設定は \(\eta=0.1\)、bracket \([-0.05,0.05]\)（幅 \(W=0.1\)）、spectral support上端 \(E_{max}=1\)、gap unknown。\(\Delta=2b/(1-\eta)\) を使った正確な有理数計算を標準Pythonで実行した。

| Bias上限 \(b\) | \(\Delta\) | \(\rho\) | 鎖の長さ \(m\) | あるpure-ground入力の期待herald試行数下界 |
|---:|---:|---:|---:|---:|
| 0.02 | 0.044444… | 1/11 | 2 | 121 |
| 0.01 | 0.022222… | 1/11 | 4 | 14,641 |
| 0.005 | 0.011111… | 1/11 | 9 | 2,357,947,691 |

この数は他のfilter query、状態準備、制御、深さ、測定費を含まない楽観的なherald attempt下界である。実行可能性の判定や実際のfilter深さを意味しない。

補助確認として固定 \(f_m(E)=\cos^{2m}(\pi E/2)\)（Fourier degree \(m\)）を \(m=0,\ldots,12\) でgrid走査した。bracket 201点と各targetに対するexcited interval 1001点での最大mean-bias proxyは、\(m=0:0.945\)、\(m=3:0.24516\)、\(m=6:0.18710\)、\(m=12:0.14624\)。これらはgridded proxyで、連続保証ではない。さらにこのeven filterでは \(E_0=-0.05,E_1=0.05\) の二準位配置で \(w(E_0)=w(E_1)\) となり、biasは厳密に \((1-\eta)W=0.09\)。したがってこの対称cosine-power族は \(b=0.01\) に届かない。この反例は族固有であり、全てのasymmetric filterについての下界は上のchain argumentが担う。

コードは乱数なし、Python 3.12.14、標準ライブラリのみ。実行手順：

```sh
python experiments/gapfree_filter_bound.py > results/gapfree_filter_bound.json
python -m py_compile experiments/gapfree_filter_bound.py
```

JSONを二度生成して `cmp` でbyte一致を確認した。コードは[gapfree_filter_bound.py](../../experiments/gapfree_filter_bound.py)、出力は[gapfree_filter_bound.json](../../results/gapfree_filter_bound.json)。

## 既存法との差と仮説位置付け

| 既存法・一次資料 | 確認した仮定/内容 | 今回との関係 |
|---|---|---|
| Lee et al., *Filtered Quantum Phase Estimation*, arXiv:2510.04294v2, [本文](https://arxiv.org/html/2510.04294v2) §§II.3–II.4、IV.1–IV.3、Supplementary V.1–V.4 | §IV.1 Eq.(IV.3) は既知target \(E_0\) に対する相対filter ratioでrejection leakageを抑える。§IV.2–IV.3はlow-/band-pass、Chebyshev/Dolph minimax、spectral concentrationを接続。Supp. Vは一般basis・polynomial・trigonometric minimaxを扱い、V.4はshift \(\mu\) を置いたfilterを定式化する。本文§II.3はcoarse \(E_0,E_1\) とgap、§II.4は先にQPEでcoarse spectral estimatesを得る二段法。 | relative suppression・filter success/cost tradeoffは強く既出。既知center/gapまたは二段のrough localizationがある場合は強く包含。bracket全体でtargetが不明なgap-free mean-bias lossと、そこからのworst-case herald chainが明示された同一結果かは確認できていない。 |
| Lin & Tong, *Heisenberg-limited ground-state energy estimation*, arXiv:2102.11340v2, [一次資料](https://arxiv.org/abs/2102.11340v2) §§1–5, Apps. D–E（先行レビュー読了範囲） | controlled/uncontrolled \(e^{-i\tau H}\)、single-ancilla Hadamard dataとspectral CDF postprocessingを用いるsame-oracle energy estimator。initial ground-overlap lower boundを使う。 | filterなしでもenergy CDFから未知ground energyを直接推定する比較対象がある。gapfree filter meanのNo-goは一般GSEE lower boundではなく、CDFとの公平比較が必須。 |
| Ding & Lin, *Even Shorter Quantum Circuit for Phase Estimation*, arXiv:2211.11973v2, [一次資料](https://arxiv.org/abs/2211.11973v2) §§I–IV, Thm.1–3, Cor.4（先行レビュー読了範囲） | HE oracleによるQCELS energy estimator。小overlap時にFourier filteringを併用し、既知interval/relative-overlap等の条件下でfilter深さとestimator costを接続。 | 「粗いlocalization後にfilter＋shallow estimator」は構成として既出。独自差分には同一hard depth cap下でCDF/QCELS/FQPE strong baselinesを超える定理・数値が必要。 |
| 本作業のchain bound | gap-free、全bracket-targetに対するfixed nonadaptive \(|f|\le1\)、overlap floor \(\eta\)、filtered-mean bias \(\le b\)。 | 既存のpoint-target minimax条件をunknown-target uncertainty classへ適用した簡潔な手導出。文献の該当定理を否定するものではなく、新規性は未確認。 |

**仮説判断：** 「新しい低次数filter族」や「adaptive localization後にfilterを掛ける」だけでは研究新規性が弱いので、いったん棄却/保留する。chain boundはsingle fixed filterのrobust bias/herald tradeoffを見積もる評価補題として保存する。独立した研究貢献として追う価値があるかは未確定。adaptive coarse localization + filter co-designはFQPE二段GaussianとLin–Tong CDF/QCELSに大きく包含されるため、同条件のhard-depth theoremまたは実質的なcost crossoverを示せない限り、新規方向として進めない。化学・物性の具体的なoracle costを決めるための追加予算・環境選択は今回不要。

今回のno-goを一般GSEE impossibilityと呼ばず、下流mean estimatorもground-energy guaranteeと同一視しない。研究の中心方針（関数設計と浅い下流推定器の共同設計）は変更しない。今後もし継続する場合の必要条件は、既知eta/bracketの取得費を含め、同一controlled-time-evolution input、同一全工程hard depth cap、同一error/confidenceで、filter-free Lin–Tong CDFとfilter-using QCELS/FQPEを比較することである。今回その比較とcontinuous interval proofは未実施。

## 変更・検証状況

- AGENTS.md / docs/workflow/agent-policy.md / PROJECT_STATE.mdに、本人認可による研究方向・比較条件・仮説採否の委任範囲を記録。追加予算・公開・Astra/Sol high以上の規制は維持。
- 分析は手導出と標準Pythonのsmall screen。量子回路、QSVT、Lean証明、実系実験は未実施。
- commit/pathはGitHub main上の本memo、script、JSONを参照。
