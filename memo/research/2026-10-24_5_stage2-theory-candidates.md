# 段階2 理論候補の批判的整理

更新日：2026-10-24（日本時間）
状態：仮説候補の比較。本人の選択・研究テーマ確定・実験・回路実行は未実施。
作業モデル：Luna、medium。批判レビュー反映済み。

## 要約

「近縮退に強い符号付き有限窓フィルタ」そのものは新規候補として弱い。FQPE v2は一般の有界複素関数を扱い、補遺でlow-pass/finite-window band-pass、minimax/Chebyshev、積分漏れ最小化（Slepian/DPSS系）を含む。gapfree性や固定次数だけも差分にならない。残る問いは、(A) 実際に利用可能な事前情報だけでフィルタが不利となる領域を証明できるか、または (B) 全工程に硬い深さ上限を課し、下流推定器も浅くしたときにフィルタが成立する領域を示せるか、である。どちらも既存FQPEの式の再整理に留まれば研究価値は弱く、新規性・優位性は未確認。

## 固定する比較モデルと記号

比較の基準モデル案は、エルミート (H) の block encoding oracle (U) と (U^dagger)、初期状態準備 (|\psi\rangle=\sum_j \gamma_j|E_j\rangle) の費用 (s)、初期の事前情報取得費用 (C_{prior}) を明示するものとする。エネルギー座標は (x_j=(E_j-E_{ref})/\alpha)、(\alpha\geq\|H-E_{ref}I\|) とする。(E_{ref}) とスペクトル包含区間、(\alpha) の根拠・取得費を記録する。Pauli-LCUなら係数絶対値和などblock-encoding正規化の費用も数える。多項式次数 (d) はquery数の指標であり、物理回路深さとは同一視しない。oracle生成、制御化、逆演算、測定、失敗時再試行、状態準備、最終推定を全費用に含める。別oracle（controlled time evolution等）を用いる比較は別モデルとして切り分ける。

窓 (W) は解析上の目標エネルギー集合とし、初期窓重み (q_0=\sum_{E_j\in W}p_j)、(p_j=|\gamma_j|^2) と置く。フィルタのスペクトル応答 (f_j=f(x_j))、(|f_j|\leq1) に対し、
\[
p_f=\sum_j p_j|f_j|^2,\qquad q=\sum_{E_j\in W}p_j|f_j|^2.
\]
これらはスペクトル分解とpostselection成功状態の規格化からの直接導出である。フィルタ後の推定器が目標サンプルを受理する条件付き確率を (r) とする。

### 仮定付きの費用計算（本メモの導出）

各試行で初期状態準備 (s) とフィルタ深さ/費用 (d) を払い、postselection成功枝だけに下流推定器費用 (c) を払う単純な独立再試行モデルでは、1試行費は (s+d+p_fc)、目標窓かつ推定成功の確率は (qr)。外部閾値などで目標イベントを識別でき、無期限に再試行してよい場合のlatent期待費用は ((s+d+p_fc)/(qr))。フィルタなしは ((s+c)/(q_0r))。(r>0) を共通とすればフィルタ側が有利となる必要十分条件は
\[
q(s+c)>q_0(s+d+p_fc),
\]
すなわち (c(q-p_fq_0)>q_0d+s(q_0-q)) である。この代数は本モデル内の導出であって、先行論文の定理ではない。イベントが (E_0) 未知などで識別できなければ、これを停止アルゴリズムまたは実用期待費用と呼ばない。固定予算 (B) なら、(N_F=\lfloor B/(s+d+p_fc)\rfloor)、(N_0=\lfloor B/(s+c)\rfloor) 回として成功率をそれぞれ (1-(1-qr)^{N_F})、(1-(1-q_0r)^{N_0}) で比較する（各試行独立、費用一定の仮定）。

(|f_j|\leq1) から (q\leq q_0)。フィルタ後も失敗枝を含む全試行に下流推定器を実行するなら、1試行費は (s+d+c) となるため、同じ (r) で (q\leq q_0) の本モデルではフィルタは成功率/費用を改善しない。postselectionを活用しても、フィルタの成功確率 (p_f) や状態準備費を無視した「重み増加」だけの比較は不十分である。硬い最大深さ (D) ではaccepted branchの深さは状態準備・filter・下流推定の直列和となる。したがって下流回路 (c) はfilterを挿入した分だけ縮む可能性があり、同じ (D) の下で、filterなしQPEだけでなく最良の浅い非QPE推定器とも比較する。query-depth制約とcompiled physical-depth制約は分ける。

## 候補A（主候補・条件付き）

**問い：** 操作可能な事前情報だけから、postselected filterが不利となる非自明なworst-case境界（または必要十分なcrossover条件）を導出できるか。得られた境界で、対象の情報領域におけるfilter採用を事前に棄却または限定できるか。

**入力・数式：** 上記block encoding、(|\psi\rangle)、状態準備費 (s)、全工程深さ上限 (D) を固定する。アルゴリズムが実際に取得する情報 (I)（厳密なenergy bracket、(alpha)、重なり下界、bracket取得費 (C_{prior}) など）を列挙し、未知の (E_0)、固有値配置、重み分布を (I) と整合する敵対的集合に置く。比較対象は既知の有限窓band-pass/minimax系と、同一oracle・同一成功基準のfilterなし推定器。目標は (I) のみで評価できる上界/下界または反例証明であり、未知の基底エネルギーや事後的に都合のよい (q,q_0,p_f) を入力に使わない。

**動機と既存法への包含可能性：** FQPE v2 §II.1–II.3はbounded complex filterとfilter有無の費用比較を既に扱い、§II.4–II.5は粗いスペクトル見積りと2段階Gaussian/Krylovも扱う。Supplementary IV.2–IV.3は有限窓band-passおよびminimax/Chebyshev・integrated leakageを含む。よって上の式を一般化・再導出するだけなら差分ではない。価値がある条件は、未知 (E_0) を漏らさず利用可能情報だけで使えるcertificate、または既存定理にない必要十分な棄却領域が得られる場合に限る。最小確認では敵対的な二準位/少数準位スペクトルと同じ (I) を持つ分布対を作り、どちらか一方に最適な単一filterが存在しない反例を探す。ここで一般的境界の存在自体がまだ確立していない。

**成立・反証条件：** 有限の実用的情報 (I) だけから計算可能で、未知の重み分布と基底エネルギーに対しても正しい境界を証明でき、既存FQPE theorem/crossoverの代数的言い換えでないことが必要。整合する分布対でfilter優位・劣位が逆転して境界が有用に識別できない、あるいは既存のFQPE解析で全内容が得られるなら候補を棄却する。

**費用：** 事前情報を得る (C_{prior})、正規化されたblock encodingの構築/利用、状態準備 (s)、filter query/depth (d)、postselection (p_f)、深さ上限で縮む下流推定 (c(D-d))、失敗確率、エネルギーシフト/正規化の費用を計上する。最小数値確認では実回路ではなく、対角行列と確率分布上の成功率・固定予算費用の総当たりで十分。現段階では未実施。

## 候補B（対抗案）

**問い：** filterと下流推定器の全直列回路にhard cap (D) を課したとき、フィルタ付きの浅い下流推定器（短時間QPE等）が、同じ深さ上限で最良のfilterなし浅い推定器を上回る、証明可能な成立領域はあるか。

**定式化：** 候補Aと同じ (U,U^\dagger)、状態準備、正規化、(I)、出力成功基準を固定する。filter後の下流推定器は (c\leq D-D_\psi-d)（(D_\psi) はstate preparationの回路深さ。コンパイル条件を含めて測る）を満たす必要がある。固定総予算 (B) 内で指定誤差 (epsilon) 以下となる確率を評価し、filterなしQPEと、同じoracleで構成できる最良の短深度推定器（既知の候補を比較対象として明記）に対して比較する。filterが成功した枝のみ下流推定を実行し、枝ごとの深さと成功確率を別々に計上する。

**既存法に含まれる可能性・成立条件：** FQPEの通常のquery/cost crossoverは候補となるが、物理的最大深さの下で短い下流推定器への置換と、filterなし浅深度推定器との公平な最適比較まで含むとは本文確認だけでは断定できない。ここが残る差分候補。ただし別推定器を許すことで単に問題を広げないよう、oracle・出力誤差・成功条件を固定する。浅い推定器の比較下界まで得られない場合は優位主張を限定または撤回する。

**成立・反証条件：** 深さ (D) に対する明示的な区間で、全費用/固定予算成功率を含む厳密な改善証明が得られれば継続候補。filterが下流精度・反復数を悪化させて差が消える場合、または既存short-depth推定法が同条件で支配する場合は棄却する。最小数値確認は小さい対角スペクトルで深さをquery-countとしてモデル化し、FQPE Gaussian/band-pass、filterなし推定器、短深度baselineを同じ測定成功目標で比較すること。回路実行ではない。

## 重要な符号付き (H) の注意

標準QSVTのsingular-value transformは、任意の符号付きHermitian固有値filter (p(H)) と自動的に同じものではない。Gilyen et al. のTheorem 17とCorollary 18はQSVT変換と実多項式のparity/有界性条件を示す。一方、これを「QSVTは符号を失う」と表現するのは誤りで、適切なeven/odd成分の組合せ、シフト、または一般化変換の選択が必要となり得る。その代価を正規化・oracle・深さ込みで評価する。

反例：(H=\mathrm{diag}(-a,+a))、初期状態を両固有状態の等重み重ね合わせとする。単一の definite-parity 実多項式 (p) は (p(-x)=\pm p(x)) なので (|p(-a)|^2=|p(a)|^2)。よってpostselectionで基底側と励起側の比率は変わらず、フィルタ利得はない。これはQSVT一般が符号を扱えないという主張ではなく、単一parity応答の制約を示す。(E_{ref}) のシフトやeven/odd合成で回避する場合は、シフト取得情報、追加次数/位相/制御、正規化増分、全深さを計上する。

## 最小の今後の確認と保留事項

段階3以降で、まず同一block encoding・正規化・状態準備・係数/位相規約の人工対角小例を使い、postselection応答・成功率・状態（global phaseを除く）を比較する。その後に限り、固定深さ・固定総費用の数値境界を探索する。今回、回路実行、環境構築、Lean証明は実施していない。

段階2で次に選ぶ判断は次の三つである。

1. 入力oracleをblock encodingに固定し、対象となるエネルギー包含情報と取得費をどう置くか。
2. 主評価を硬い物理深さ (D)、query-depth、または固定総費用 (B) のどれに置くか。成功確率と最終エネルギー誤差も指定する。
3. 候補A（情報制約付き棄却境界）と候補B（全工程hard cap下の浅い推定器比較）のどちらを先に理論確認するか。

## 出典と確認範囲

- Lee et al., [Filtered Quantum Phase Estimation, arXiv:2510.04294v2](https://arxiv.org/html/2510.04294v2) — main §II.1–II.5（generic bounded complex filter、filter cost/crossover、coarse estimate、two-stage Gaussian、modified Krylov）、Supplementary IV.2–IV.3（lowpass/finite-window bandpass、minimax/Chebyshev/integrated leakage）。理論上の既存包含範囲を確認。候補A/Bの物理深さ条件への完全適用までは未確認。
- Lin & Tong, [Optimal polynomial based quantum eigenstate filtering with application to solving quantum linear systems, arXiv:1910.14596v4](https://arxiv.org/html/1910.14596v4) — gap依存minimax polynomial filteringの設定と適用範囲を確認。既知gap・block encoding等の条件付きベースラインとして扱う。
- Gilyen et al., [Quantum singular value transformation and beyond, arXiv:1806.01838](https://arxiv.org/pdf/1806.01838) — §3のQSVT定式化、Theorem 17、Corollary 18（変換とparity/有界性条件）。本メモの二準位例は同定理の主張ではなく、定義からの直接帰結。
- PennyLane [qml.qsvt](https://docs.pennylane.ai/en/stable/code/api/pennylane.qsvt.html) と [qml.QSVT](https://docs.pennylane.ai/en/stable/code/api/pennylane.QSVT.html) — 前段レビュー済みAPI。high-level自動生成とcustom block encodingのlow-level生成の境界を参照。研究上の費用保証を与えるものとは扱わない。

## 記録上の区別

候補A/B、固定予算式、signed-H例はいずれも段階2の作業仮説または本メモ内の導出であり、確定した研究方向ではない。文献が既に含む内容と差分不明を明示し、新規性・優位性は保留する。予備実験結果は存在しない。
