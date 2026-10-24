# 深さ制約下の物理フィルタ・信号フィルタ比較

更新日：2026-10-24（日本時間）
状態：段階2の具体化と最小scalar check。研究仮説・物理系・入力oracle・実装方式は未確定。
作業モデル：Luna、medium。批判的レビューの会計上の指摘を反映。
作業範囲：一次資料レビューとPython標準ライブラリの小さな複素数計算。回路実行・環境導入・有料計算なし。

## 要約と方針上の位置付け

本人が確定したB（下流も浅い推定器に固定し、全工程のhard depth cap内でフィルタ形・強さと推定器を共同設計）を保つ。その比較土台として、同じ filtered spectral signal を (i) 量子状態フィルタ後にHadamard/Fourier推定する方法、(ii) フィルタなしHadamard time-seriesを古典的に重み付けする方法で実現できることを明示する。後者は古典的な信号再構成であり、物理状態の準備ではない。両者を同じoracle、精度、信頼度、最大coherent depth、総shot/query数で比べる問いは具体的である。

現時点でこの比較を研究の主題へ格上げする根拠はない。FQPE、QETU、Lin–TongのFourier filtering、QCELSのFourier-filtered版、低深度Gaussian-derivative GSEE、およびQPE based filteringの先行範囲は広く、近いアイデアは既に含まれる可能性が高い。したがって推奨は、研究の中心をユーザー確定のB（深さ上限内でのfilter/downstream共同設計）に維持し、physical-vs-virtual signal filterを同等性・費用の必須比較軸として使うこと。物理postselectionが同じdepth capで有利になる明確な領域が示せるかは、第一の理論検証問いとして残す。新規性・優位性は未確認で、主題を変更してはいない。

## 暫定比較モデル

### 入力oracle

理論的な初期モデルとしてHamiltonian-evolution (HE) accessを置く。状態準備ユニタリで `|psi>` を準備し、controlled evolution `U(t)=exp(-i (H-E_ref)t)` と必要な逆時間を使う。この選択は暫定分析モデルであり、本人のoracle選定ではない。QETU、QPE/Fourier filtering、QCELS、Lin–Tongのsingle-ancilla CDF法は、論文上このHamiltonian evolution modelを用いるため、同じquery familyで比較をそろえやすい。最大回路深さは、単にquery回数でなく、各controlled evolutionの実装深さ・時間、state preparation、filter、readoutを加えた最大coherent pathで定義する。

Block encoding + QSVTも候補となるが、HE oracleとraw query数を直接比較できない。block-encoding正規化（例えばLCU係数絶対値和）・ancilla・制御・構築費を別に評価し、必要ならqubitization walkによる同oracle downstream estimatorを用意してから比較する。現段階ではBE路を排除せず、総cost換算もしていない。

`E_ref`、時間刻み、既知energy bracketは位相aliasingを避けて固有値を特定するための入力情報となる。scalar shiftはcontrolled unitaryで相対位相として実装する。bracket/gapが必要なfilterやQCELS変種では、その取得費 `C_prior` と誤差をcostへ含める。未知の `E_0` やgapをfilter設計で無料の情報として使わない。HE queryの物理costは `C_sim(H,t,epsilon_sim)` とし、product-formula誤差や `||H|| |t|` 依存を別記する。状態準備費・深さ `C_psi,D_psi)、フィルタcost/depth、readout、ancilla、postselection、再試行、全shotsを含める。

### 対象信号・フィルタ

初期状態 `rho` のHadamard-test complex signalを
`g(t)=Tr[rho exp(-i(H-E_ref)t)]`
とする。初期ground-state squared overlapを `eta_0=Tr[rho P_0]` と記す。目標energy窓の総重みとは区別し、既知の下界・窓重み・相対重みは同じ量にまとめない。

有限時間supportをもつ関数
`f(H-E_ref)=sum_j c_j exp(-i tau_j (H-E_ref))`
を考える。filter normを
`z_f=Tr[rho f^dagger f]`
とし、物理的にpostselectした状態は `rho_f=f rho f^dagger/z_f` である。実際のherald確率は回路のnormalizationに依存する。例えば`f/L`をtop blockに実装するLCUなら `p_herald=z_f/L^2`、`L=sum_j |c_j|`。QETU等で`f`自体をtop blockに実装できればscaleは1となる。一般に `z_f`（正規化後の信号mass）と `p_herald`（実装した回路が成功する確率）を混同しない。success amplificationなどを使うときも深さとcostを再計算する。

批判レビューで確認した信号同値性は次のとおり。記号
`a_omega = sum_{(j,k): tau_k-tau_j=omega} c_j^* c_k`
で重複する時間差をmergeすると、
`N_f(t)=sum_omega a_omega g(t+omega)`,
`z_f=N_f(0)`、
`g_f(t)=Tr[rho f^dagger exp(-i(H-E_ref)t)f]/z_f=N_f(t)/z_f`。
これは `[f(H),H]=0` と固有値分解からの直接導出で、物理的にpostselectした `rho_f` 上の同じHadamard信号と、filterなしraw signalの古典的線形結合が、期待値レベルで一致することを示す。理想信号の一致はshot-noise付き推定器、シミュレーション誤差、同一depth内のコスト優位を意味しない。

`B_f=sum_omega |a_omega|` とおけば三角不等式から `B_f <= (sum_j |c_j|)^2=L^2`。各raw Hadamard outcomeが有界で、重要度samplingを使う単一の `N_f(t)` 推定では `MSE(Nhat_f) <= C B_f^2/N` の形の上界を置ける（`C` は実部/虚部や測定設定の定数）。既知 `z_f` なら `MSE(g_hat_f) <= C B_f^2/(N z_f^2)`。これは合成signalの標準統計上界であり、ground energy全体のサンプル複雑度ではない。未知 `z_f` の比推定 `Nhat_f/zhat_f` は一般にunbiasedではない。例えば同時信頼事象 `|Nhat-N|<=e_N`、`|zhat-z|<=e_z<z` と `|N|<=z` から、
`|Nhat/zhat-N/z| <= (e_N+e_z)/(z-e_z)`
を得る。実験では分母推定誤差・failure probability・shotsを明示する。

## 同一depth・total-cost比較の会計

各 downstream estimatorの時刻セットを `T_read`、`T_readmax=max_t |t|` とする。filter time setのdiameterを `span(tau)=max_j tau_j-min_j tau_j` とすれば古典的信号合成に必要なraw signalのsupportは `T_read + {tau_k-tau_j}`、最大時間の上界は `T_readmax+span(tau)`。係数cancellationがあれば実際のsupportは短くなりうる。対称support `tau_j in [-T_f,T_f]` なら `span(tau)=2T_f` なので `T_readmax+2T_f` 以下となる。この式はsample time supportであり、LCU/SELECT/QETU回路のphysical depthが単純に `max |tau_j|` と等しいとは仮定しない。

| 方法 | 最大coherent depth（記号） | 総query/shotの会計 |
| --- | --- | --- |
| フィルタなし estimator | `D_psi + max_t D_read(t) <= D` | estimatorが必要とするshotsを `eta_0` 等の正確な仮定で決め、各shotのstate prepと `C_sim(H,t,epsilon_sim)` を加える |
| physical filter + estimator | 成功データ経路で `D_psi + D_filter + max_t D_read(t) <= D` | `M_t` はpostfiltered signal上で必要なsuccess shots。各tでfiltered stateを測定ごとに再準備するため、費用は `sum_t M_t[(C_psi+C_filter)/p_herald + C_read(t)]`。初期overlap依存を既に含む `M_t` にさらに旧QPE型のoverlap逆数を重ねない |
| virtual `|f|^2` signal + estimator | `D_psi + max_{t,omega} D_read(t+omega) <= D`。対称filter supportでは `D_psi+T_readmax+2T_f` がtime-query上界 | 必要なraw `g(t+omega)` Hadamard shots、係数norm/importance-sampling、分母 `z_f` 推定、状態準備、classical postprocessingをすべて数える。物理filterのpostselection成功率は払わない |
| 強い既存法 | 方法ごとに論文定義の最大evolution timeを同じ (D) に換算 | FQPE、QETU、Fourier-filtered QCELS、Lin–Tong CDF、Gaussian-derivative GSEEを比較候補にする。oracle/normalization/overlap/gap仮定を合わせる |

`M_t` の条件は、filtered stateのground overlap、`z_f`、estimatorの所要confidenceを含む estimator-specific なsample requirementである。postselection factorを別に二重計上しないよう、`M_t` は「受理されたfiltered-state測定shot数」と定義した。state preparationとfilterを各accepted shotに対して実行し、平均 `1/p_herald` 回のtrialを要する。downstream measurementの時間evolutionはsuccessful prepared state上で行う。成功枝を特定できないeventに応じて任意停止できると仮定せず、固定budgetなら成功確率を直接比較する。

## 最小scalar check（実行済み）

目的は期待信号恒等式、normalization/ratio error、accepted-sampleに対するretry計数のsanity checkだけである。`E_0` とgapを既知としてfilterを作るoracle-assisted toyであり、未知ground energyの推定性能を示す実験ではない。

設定：`H-E_ref=diag(0,1)`、初期重み `(eta_0,1-eta_0)=(0.15,0.85)`、`f(E)=cos(pi E/2)=0.5 exp(+i pi E/2)+0.5 exp(-i pi E/2)`。ここで既知のgap `Delta=1` を使っている。よってtarget振幅は1、excited振幅は数値的に `6.1e-17`、`z_f=0.15`。時間差係数は `a_0=0.5`、`a_{+pi}=a_{-pi}=0.25`、`B_f=1`、filter-support spanは `pi` となる。物理とvirtualの `g_f(t)` は `t=0,0.17,0.61,2` で絶対差 `2.2e-16)–`5.3e-16`（浮動小数点誤差）だった。したがってこの有限スペクトル例では期待信号のidentityと重複周波数の係数集約が数値的に一致した。普遍定理や費用優位を主張しない。

正規化誤差の算術例は `z_f=0.15`、`e_N=0.003`、`e_z=0.006` と置いた。ratioの誤差上界は `(e_N+e_z)/(z_f-e_z)=0.0625`、`N=z_f)、`Nhat=z_f+e_N)、`zhat=z_f+e_z` の選択例の実誤差は `0.01923`。この一例は一般ratio boundの証明ではない。さらに各時刻あたり100受理shotを3時刻から得る仮想会計では、`p_herald=z_f=0.15` のときphysical filter試行の期待値は `300/0.15=2000`。これもactual estimatorやvirtual costとの性能比較ではなく、再試行係数の確認である。virtualの信号shot、分母推定、読出し時刻の伸長を入れて初めて比較になる。

再現用Python（標準ライブラリのみ、回路/追加依存なし）：

```python
import cmath, math

energies = (0.0, 1.0)
weights = (0.15, 0.85)
tau = math.pi
coeffs = (0.5, 0.5)
times = (-tau / 2, tau / 2)

def raw_signal(t):
    return sum(w * cmath.exp(-1j * e * t)
               for e, w in zip(energies, weights))

def filter_value(e):
    return sum(c * cmath.exp(-1j * t * e)
               for c, t in zip(coeffs, times))

z = sum(w * abs(filter_value(e))**2
        for e, w in zip(energies, weights))

merged = {}
for cj, tj in zip(coeffs, times):
    for ck, tk in zip(coeffs, times):
        omega = tk - tj
        merged[omega] = merged.get(omega, 0j) + cj.conjugate() * ck

def virtual_signal(t):
    numerator = sum(a * raw_signal(t + omega)
                    for omega, a in merged.items())
    return numerator / z

def physical_signal(t):
    numerator = sum(w * abs(filter_value(e))**2
                    * cmath.exp(-1j * e * t)
                    for e, w in zip(energies, weights))
    return numerator / z

for t in (0.0, 0.17, 0.61, 2.0):
    print(t, abs(virtual_signal(t) - physical_signal(t)))

e_N, e_z = 0.003, 0.006
print("ratio bound =", (e_N + e_z) / (z - e_z))
print("accepted filter attempts =", 3 * 100 / z)
```

## 既存手法との境界・新規性リスク

| 資料・読んだ範囲 | 入力モデル/条件 | 本候補への既存の包含と残る差分候補 |
| --- | --- | --- |
| Lee et al., [Filtered Quantum Phase Estimation, arXiv:2510.04294v2](https://arxiv.org/abs/2510.04294v2) — main §II.1–II.4、Suppl. IV.2–IV.3 | polynomial/block-encodingとtrigonometric/Hamiltonian-evolution filter、初期overlap、filter success・depth・coarse E0/E1。§II.4は粗いpriorを得る費用も入れた2-stage Gaussian FQPE | physical filterでoverlapを上げてdownstream QPEを実行し、successとcostを既に扱う。virtual `|f|^2` signalの係数norm/ratio confidence、または同一 hard cap下のvirtual-versus-physical comparisonが本文で同条件評価済みかは未確認。有限窓filter形状自体は新規性になりにくい |
| Dong, Lin & Tong, [QET-U, arXiv:2204.05955v2](https://arxiv.org/abs/2204.05955v2) — §I–III.1、Theorem 1, 4, 5 | controlled Hamiltonian evolution input、real/even-polynomial transformation、1 ancilla。ground energy estimatesは既知input assumptionsの下でquery/depth tradeoffを与える | CTEでのphysical polynomial filteringとenergy estimationが既存。特定の新規filterを立てる際のstrong baseline |
| Lin & Tong, [Heisenberg-limited ground-state energy estimation, arXiv:2102.11340v2](https://arxiv.org/abs/2102.11340v2) — §§1–5、Appendix D–E | fixed `e^{-i tau H}` HE input、準備状態のground overlap下界、single-ancilla Hadamard testとspectral CDF postprocessing。Appendix Eでcontrol-free条件も扱う | フィルタなしのsame-oracle CDF estimator baseline。線形precision/query tradeoffと信頼度、simulation costの同条件化が必要 |
| Ding & Lin, [Even Shorter Quantum Circuit for Phase Estimation, arXiv:2211.11973v2](https://arxiv.org/abs/2211.11973v2) — §§I–IV、Theorems 1–3, Corollary 4 | HE oracle、ground overlap/relative-overlapと既知interval/prior assumptions。QCELSはtime-series least-squares、初期overlapが小さい場合Fourier filteringを明示的に併用 | `filter + shallow estimator` は既存強baselineに含まれる。Corollary 4では粗いprior費・filter深さ・QCELS深さを同じ最大time/total-time式へ含む。よって単なる物理filterとQCELSの直列化は新規とは言いにくい |
| Wang et al., [Low-depth GSEE, arXiv:2209.06811v3](https://arxiv.org/abs/2209.06811v3) — §§1–2、Theorem 1.1、Corollary 1.2 | controlled `exp(iHt)`、known gap lower bound `Delta` と initial ground-overlap lower bound `eta`。Gaussian-derivative convolutionを古典後処理する | 物理状態を直接変換しない短深度 signal-processing baseline。深さと総時間を既にtradeoffするため、virtual filterやFQPEのみとの比較では足りない |
| Sakuma et al., [QPE-based filtering, arXiv:2507.01361v3](https://arxiv.org/abs/2507.01361v3) — §§II.1–II.5、III.1、Appendix A–B | time-evolution QPE、rectangular/sine/Kaiser window、古典postselection/coherent versionとQETU query比較 | Kaiser filterとQETUの必要evolution queriesを比較し、粗いgrid filterからfine high-resolution spectrumを得るtwo-step法を含む。filter窓や単純coarse-to-fine自体は既出 |
| Lin & Tong上記資料とQCELS v2 | HE/Hadamard time samples。Fourier filterには既知のrough energy intervalやrelative overlap条件が必要 | 固定時間supportとrelative overlap条件が、unknown `E0` の無料利用を防ぐための最低限の入力契約になる |

上表の「未確認」は文献に存在しないと断定するものではない。特にFQPE/QCELSにvirtual filteringとratio-estimation統計が含まれるかは、今回は該当箇所を見た範囲で未確認。既存式の再組み合わせにすぎない場合、研究価値は弱い。

## 次に行う最小理論・数値確認仕様

環境導入なしで、scalar spectrumから以下を同じ表に出せる。先に実行した小例は、ここでいう第1項のidentity/sanity checkだけであり、未知target推定・finite-shot性能探索はまだ行っていない。

1. **synthetic families:** 2–8準位の固有値列と初期確率を明示。gap既知/未解像、exact `E0` bracketと誤差のあるbracket、相対overlapの高低を別の軸とする。target `E0` とgapを使って作ったfilterはoracle-assisted diagnosticとし、unknown-target performanceの結果と呼ばない。
2. **同一filter:** 係数 `c_j)、time support、`z_f`、`p_herald`、正規化scaleを固定。正規化 `z_f` が既知/推定の場合を分け、物理的postselectionとvirtual signal synthesisが理想期待値で一致することを全時刻で確認する。誤差予算はfilter approximation、Hamiltonian simulation、shot noise、ratio estimateを分ける。
3. **公平baseline:** (a) filterなし同一downstream estimator、(b) 既存Fourier-filtered QCELS、(c) FQPE/QETU、(d) Lin–Tong CDFまたはWang Gaussian-derivative GSEE、(e) virtual `|f|^2` signal。主比較でfilter familyを追加提案する前に、既存filterを使って比較のshape/scale感度を確認する。
4. **同じcap / accuracy / confidence:** 全successful data pathのcoherent depthに `D_psi+D_filter+D_read`、virtualは `D_psi+max|t+omega|`、no-filterは `D_psi+D_read` を適用。全法で同じfinal energy error `epsilon)、failure probability `delta)、total evolution costとshotsを比べる。成功試行数、失敗postselection、state preparation、`C_prior`、query-dependent simulation errorを含める。query countとcompiled physical depthは別列のまま保つ。
5. **virtual variance / normalization:** frequency differencesをmergeし `B_f=sum|a_omega|` を算出、importance allocationでraw Hadamard shotsとtime costを見積もる。unknown `z_f` のnumerator/denominator confidenceを別に確保し、ratio biasを式で制御する。actual statistical experimentに進む場合は疑似乱数seedとshot allocationを記録する。

このチェックは通常のPython標準ライブラリだけで再現でき、まだ量子回路・Simulator・backendは不要。actual circuit-depth比較へ進む前にはHamiltonian simulation方式、backend/gates/compilerを決める必要がある。現時点で追加予算や環境構築のため本人判断は必要ない。理論上はcontrolled-time-evolutionを暫定モデルとして、候補・baseline・式の絞り込みを続けられる。応用物理系、実装oracle、simulator資源を固定する段階では本人の重要判断を改めて問う。

## 次に残す重要な研究判断

次の段階で本人の入力が価値を持つのは、以下のどちらをBの中心的な見せ方にするかである（現時点ではどちらも確定しない）。

| 選択肢 | 内容 | 推奨と理由 | 主なリスク |
| --- | --- | --- | --- |
| B1: filter/downstream共同設計を中心にし、physical-vs-virtualを評価基準とする | 同じdepth capでfilter形・強さとshallow estimatorを共同最適化し、no-filter・既存filtered estimators・virtual signalを含む総費用で比較 | **推奨。** すでに合意済みBに直結し、物理filterが古典信号処理に対して何を増やすかを評価土台で切り分けられる | 公平な同条件比較でも既存FQPE/QCELS/Gaussian derivativeを越える差が見つからない可能性がある |
| B2: physical-vs-virtual filterの有利境界を主定理の中心にする | `p_herald`、`B_f`、`z_f`、filter/readout support、state-preparation costから、同一capの物理postselectionが勝つ/負ける領域を示す | 成功率と信号推定分散の境界を明確にできれば数学的に焦点が狭い | 研究課題が実装戦略比較へ偏り、広い関数設計Bからずれる。既存のFQPE・QCELS費用解析や単なるimportance-sampling計算の再整理に終わる恐れ |

推奨B1はB2を評価の一部として含めるが、主題変更は行わない。B2の境界が一般的で非自明と判明した場合だけ、後で重点を移す判断材料にする。

## 作業終了条件に関する運用

AGENTSとagent-policyに、チャット依頼起点とモデル承認制は維持したまま「commitは保存点であって会話停止点ではない。依頼範囲内の成果・レビュー材料・必要判断まで自律継続する」と記録した。重要な研究方向、追加予算、外部公開は本人判断に戻す。このturnで環境追加、回路実装、テーマ変更、費用発生はしていない。
