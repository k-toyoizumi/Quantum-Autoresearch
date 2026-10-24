# 深さ制約スペクトルフィルタの文献・過去資産レビュー

日付：2026-10-24（日本時間）  
状態：段階1の比較用記録。新規性・優位性の確定ではない。  
作業モデル：Luna、medium（割当設定）。サブエージェントは使用していない。

## サマリー

重点4文献の一次資料を照合し、比較軸を「入力モデル、事前情報、フィルタ深さ、成功確率、下流推定、総費用」にそろえた。Lin–Tong、QET-U、Filtered QPEは本文の該当範囲を読んだ。State Preparation BoostersはarXiv書誌・要旨だけを確認したため、定理条件と費用は未確認である。

FQPEは、初期重なりを改善する利点だけでなく、フィルタ後選択確率・フィルタ回路・事前推定の費用を含めたQPE総深さを評価している。従って「浅いフィルタ」単体ではなく、同じ最終エネルギー精度・失敗確率を満たすフィルタなし推定を基準にする必要がある。既存QSVTコードは位相合成や回路組立ての参照候補だが、QCG専用実装で依存・正しさ・実深さは未検証であり、そのまま研究実装に流用できるとは判定しない。

## 一次資料との照合

### 比較表

| 方法 | 入力モデル | 事前情報・仮定 | フィルタ深さ | 成功確率 | 下流推定 | 総費用・注意 |
| --- | --- | --- | --- | --- | --- | --- |
| Lin–Tong minimax QSP (2020) | Hamiltonianの $(\alpha,m,0)$-block encoding と初期状態準備 oracle | 対象固有値が既知または指定され、スペクトルギャップの下界 $\Delta$ がある。初期重なり $\gamma>0$ を仮定 | minimax多項式次数／block-encoding queryは $O((\alpha/\Delta)\log(1/\epsilon))$。次数を物理回路深さと同一視しない | 出力をancilla測定で受理。QSPフィルタ単独の無条件成功確率ではなく $\gamma$ と後処理に依存。増幅なしは費用の $1/\gamma$ が $1/\gamma^2$ へ変わる | 本文では固有状態抽出をQLSPのAQC/QZE経路に接続。一般の低エネルギー推定器に自動で置き換えられる結果ではない | block encoding queryと初期状態queryを区別。amplitude amplificationを使うかでquery・ancilla費用が変化。一般の浅さ制約やT-countを直接与えない |
| State Preparation Boosters (2022) | Gaussian boosterを用いた基底状態準備、論文要旨の範囲では入力回路詳細未確認 | 低深さで初期状態の基底状態重なりを増加させる設計。厳密なギャップ・重なり条件は本文未確認 | 要旨はlimited-depth circuitと記述。次数・深さ式は未確認 | Gaussian boosterによる $N_2$ 数値例を報告。成功確率・再試行式は未確認 | 基底状態準備を直接目的とする場合と、QPEのサブルーチンを想定 | 要旨からは深さ―重なり変換の発想が既出と確認できる。定量的比較や仮定の引用には本文確認が必要 |
| QET-U (Dong–Lin–Tong, 2022) | $U=e^{-iH}$ の controlled/uncontrolled Hamiltonian evolution を黒箱として与えるモデル。block encodingを必須としない | エネルギー推定は初期状態重なり $|\langle\phi_0|\psi_0\rangle|\ge\gamma$ とスペクトル範囲 $[\eta,\pi-\eta]$。基底状態準備にはさらにギャップ下界 $\Delta$ とエネルギー分離位置 $\mu$ 等が必要 | 短query-depthエネルギー推定は $U$ のquery depth $\widetilde O(\epsilon^{-1}\log\gamma^{-1})$。振幅増幅を含むnear-optimal版は $\widetilde O(\epsilon^{-1}\gamma^{-1}\log(1/\delta))$ のquery depth | 短深さ版は成功確率 $1-\vartheta$ を達成するが総queryは $\widetilde O(\epsilon^{-1}\gamma^{-2}\log(1/\vartheta))$。near-optimal版は総queryの $\gamma^{-1}$ 依存へ改善、ただし多量子ビットToffoli/振幅増幅を要する | ground-state energy estimationを直接実施。ground-state preparationは近似射影を追加 | 深さと総queryの明示的なトレードオフ。controlled-$U$を実装する費用やTrotter近似誤差は別途必要で、主解析は $U$ を正確に実装すると仮定。T-count・wall-clockは未評価 |
| Filtered QPE (Lee et al., 2025/2026版) | rescaled $H$ のblock-encoded非ユニタリfilter $f(H)$。実装例はQSVT多項式またはHamiltonian evolutionの三角関数展開 | $|f(x)|\le1$。Gaussian二段法では低エネルギー $E_0,E_1$ の粗い推定とギャップ $\Delta E_0$ に対する精度条件を使う。別案は粗推定を手順内で取得 | Gaussian Fourier近似の項数は抑制誤差 $\epsilon_f$ と幅 $\sigma$ に対し $N=O(\sigma^{-1}\sqrt{\log\epsilon_f^{-1}})$、ギャップと同じ漏れ基準へ幅を合わせると $O(\Delta^{-1}\log\epsilon_f^{-1})$。filter costはoracle query数で数え、T-count未算定 | フィルタ後選択 $p_f=\sum_i|\gamma_i f(E_i)|^2$、正規化後target overlap $|\gamma_{f0}|^2$。利得だけでなく $p_f^{-1}$ を含む | Filtered stateの後にQPE。成功確率 $1-\delta$ での標準QPE総深さは $O(|\gamma_0|^{-2}\log(1/\delta)[D_{\phi_0}+D_{QPE}])$、FQPEは $O(|\gamma_{f0}|^{-2}\log(1/\delta)[p_f^{-1}(D_{\phi_0}+D_{sp,f})+D_{QPE}])$ | 有利条件はoverlap gainがpostselectionとfilter depth費用を上回ること。粗い事前推定を手順内で得る二段版はその費用込み。論文のQuery Costはunit-time propagatorまたはqubitization queryで、具体的block encoding・コンパイル・hardware依存のT-countは未評価 |

表の漸近式は各論文の定義・queryモデルの中の値であり、異なる論文間で単純に数値比較できる単一の物理深さではない。特に、filter polynomial degree、oracle query depth、回路全体の最大深さ、総query数は別の量として扱う。

### 読んだ範囲・書誌の確認

1. Lin & Tong, “Optimal polynomial based quantum eigenstate filtering with application to solving quantum linear systems,” arXiv:1910.14596v4, *Quantum* 4, 361 (2020).  
   URL: https://arxiv.org/html/1910.14596v4  
   読了範囲：Abstract、§1の問題設定と入力仮定、§2のQSP/block encoding、§3 minimaxフィルタ定理、§5.2の成功確率・忠実度・query complexity。対象固有値のギャップ下界、初期状態overlap、block encodingを仮定する点を確認した。有限のblock-encoding誤差、回路コンパイル、実験条件の独立再検証はしていない。

2. Wang, Sim & Johnson, “State Preparation Boosters for Early Fault-Tolerant Quantum Computation,” arXiv:2202.06978v3, *Quantum* 6, 829 (2022).  
   URL: https://arxiv.org/abs/2202.06978  
   読了範囲：arXiv metadataとAbstractのみ。限定深さcircuitで基底状態重なりを制御可能に増やすground-state boostingと、$N_2$ に対するGaussian boosterの数値例を確認した。定理・実装・費用式は未確認なので表では未確認とした。

3. Dong, Lin & Tong, “Ground state preparation and energy estimation on early fault-tolerant quantum computers via quantum eigenvalue transformation of unitary matrices,” arXiv:2204.05955v2, *PRX Quantum* 3, 040305 (2022).  
   URL: https://arxiv.org/html/2204.05955v2  
   読了範囲：Abstract、§IIのQET-Uと入力モデル、§IIIのタスク定義・Theorem 4/5の成功確率と費用、短query-depth構成の多項式次数・事前パラメータ、振幅増幅のToffoli要件、シミュレーション誤差への記述。論文自身がquery深さと総queryの差を評価し、$U$ 実装を正確とする主解析とTrotter誤差解析を分けることを確認した。全補遺の完全照合はしていない。

4. Lee et al., “Filtered Quantum Phase Estimation,” arXiv:2510.04294v2 (2026-06-30版), *Quantum Science and Technology* 11 (2026) 045053.  
   URL: https://arxiv.org/html/2510.04294v2  
   読了範囲：Abstract、§II.1の問題設定・コスト定義、§II.2–II.3のフィルタ・QPE比較定理、§IIIのフィルタ比較と数値例の本文、§VII Gaussian coarse spectral estimates、§VIII二段法のcoarse estimate内取得費用、Supplementary Note VIのGaussian Fourier近似式を確認した。論文の「robustness」は一部がHamiltonian/basisまたはKrylov行列の摂動解析であり、事前エネルギー不確かさ一般のロバスト保証と同一視しない。全補遺のIX節定理は未精査。Fermi–Hubbard数値例を対象化学・物性系全般の保証として扱わない。

## 過去資産の確認と再利用判定

指定されたtree commitを参照して本文・ソースを確認した。以下は構成確認でなく、該当ファイルの記述に基づく機能分類である。すべての実行、依存関係の再現、論文数値の再現、コード正当性の検証は未実施。

| 資産・参照commit | 確認したpathと読んだ範囲 | 判定 |
| --- | --- | --- |
| [QCG-paper](https://github.com/k-toyoizumi/QCG-paper/tree/5b04b302bc3e1d41f9ac933c837ab84f4c5b7164), `5b04b302bc3e1d41f9ac933c837ab84f4c5b7164` | `main.tex` Abstract、入力モデル・QLSA比較表、QCG反復、swap-test統計精度と総query評価。次いで1D Poisson応用のblock encoding記述。 | 解釈・費用見積りの参照に再利用可。QCGは線形方程式をCG反復で解くハイブリッド法で、スペクトル状態フィルタの実装ではない。主張する浅い最大深さの代わりに多数shotを要し、総query式は残差等の多項式最大値・swap-test精度 $\delta$ に依存するという自己記述を比較時の注意として使う。`reference.bib`は取得したが項目を照合していない。 |
| [QSVT-based_QCG](https://github.com/k-toyoizumi/QSVT-based_QCG/tree/04e8c2aec8e3c5c4a06c6d8a92d3b515cea47555), `04e8c2aec8e3c5c4a06c6d8a92d3b515cea47555` | `phases.py` のpyqsp位相合成とWx/Reflection convention変換、`coefs.py` の偶奇係数分割と最大値探索、`qsvt.py`/`gates.py` のQiskit回路関数、`qCG.py` のQCG/測定処理、`utils.py` のswap test・statevector経路。 | 部品の参照候補は位相合成、偶奇分割、回路構築。フィルタ入力多項式・目的の信号演算子・位相規約・正規化を今回の問題へ合わせて変更し、区間有界性や近似誤差を別途保証する必要がある。係数最大値計算は数値最適化に見えるため区間全体の証明に使えない。QCG反復とswap-testによる係数更新は直接再利用対象外。実行環境・バージョン固定が確認できず、コード動作・位相正しさ未確認。 |
| [master-thesis](https://github.com/k-toyoizumi/master-thesis/tree/6190fc34c4f85a5436a92f1bb242d9fa2cdda00f), `6190fc34c4f85a5436a92f1bb242d9fa2cdda00f` | `chapter1.tex` のQSVT/QSP・Hamiltonian simulation概説、`chapter2.tex` block encodingと多項式制約、`chapter3.tex` Hamiltonian simulation・OAA/FPAA、`chapter4.tex` 正側QSVTと拡張。 | 記法・過去導出の参照に利用可能。block encodingと有界多項式を要する変換の背景や、正側QSVTで置換用block encodingを仮定/構成する条件の参照にする。現在のfilterの正しさ・深さ保証へそのまま転用しない。章の説明・定理を独立検証していない。`reference.bib`は未照合。 |

**再利用候補**
- `phases.py` のQSP位相生成インターフェースとQSVTの位相規約変換（pyqsp依存を固定し、独立した既知多項式で検算する前提）。
- `qsvt.py` と `gates.py` のblock-encoding queryと位相演算を交互に積む回路構成の参考。
- `coefs.py` の係数偶奇分割など、機械的な変換処理。

**修正・検証が必要**
- フィルタ多項式の全区間有界性、パリティ、近似誤差、端点/スケーリング、位相合成成功条件を明示する。
- `coefs.py` の連続区間最大値評価は厳密証明または誤差保証付きinterval methodへ差し替える。グリッド/有界最適化の出力は探索値に留める。
- 各候補のpostselection probability、増幅の有無、state preparation、下流QPE、再試行をつないだ総費用を計上する。多項式次数だけで最大回路深さを報告しない。
- 過去QCGの係数更新・swap-test・Poisson特化block encodingは、本研究課題に必要な形へ設計し直す。依存パッケージ、実行可能なPython/Qiskit/pyqspバージョン、ライセンス、テストは未確認。

## 状態・未決事項・次の一手

この作業で新規研究方針は採用していない。既存の方向「化学・物性エネルギー推定のための深さ制約量子スペクトルフィルタ」に対し、比較基準と仮定を明確化した。数値実験・Lean検証・過去コードの実行は行っていない。

未決事項：Booster論文本文の定理・費用、FQPE Supplementary Note IXの全摂動仮定、各方式を同一Hamiltonian oracle・精度・失敗確率・深さ上限で比べる具体的条件、過去コードの依存環境と実行可能性。

次の一手：段階1の残件としてBooster本文とFQPE robustness補遺を確認し、関連するblock encoding / Hamiltonian evolutionの入力コストを揃える。そこまで終えた後、同条件比較用の最小filter/QPE会計仕様を段階2で提示する。本文検証なしに段階1完了とは扱わない。

## 根拠にしたrepo内文書

- `AGENTS.md`、`README.md`、`docs/project/research-plan.md`、`docs/project/documentation.md`、`docs/references/prior-projects.md`、`docs/workflow/agent-policy.md`
- `memo/research/2026-10-23_filter-topic-comparison_2.md`（前回比較の一次資料確認を更新）
- `memo/research/2026-10-24_asset-inventory_1.md`（前回の構成確認を本文/コード精査へ拡張）

このmemoは確定事項を追加しないため、`README.md`と`docs/project/research-plan.md`の現在地は変更しない。段階1は未完了のまま。
