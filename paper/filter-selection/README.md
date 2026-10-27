# Prior-Robust QSVT Filter Selection: Gap-Free Bias and Finite-Budget Risk

改訂日：2026-10-27（日本時間）。回路は理想的、測定データは有限という条件の理論・実験を本文へ統合。著者情報は本人希望により空欄。arXiv未投稿。

- [英語PDF・19頁](Filter-selection-en.pdf)、[日本語PDF・16頁](Filter-selection-ja.pdf)
- [arXiv向け英語ソースZIP](Filter-selection-arxiv.zip)、[日英再現ソースZIP](Filter-selection-source.zip)
- [有限サンプリングの新規性評価](finite-novelty-review.md)、[主張と根拠](claim-evidence.md)、[元の先行研究比較](novelty-review.md)
- [物性への応用の詳説](ising-application.md)、[有限サンプリング図](../../figures/finite_precision.png)、[有限予算選択図](../../figures/finite_budget.png)

## 今回追加した研究

成功数が集まるまで待つ方式と、棄却を含む総実行予算で止める方式を区別した。後者の成功数Mはランダムで、条件付きMSEは厳密に `(mu-e)^2+mu(1-mu)E[1/M | M>0]`、無出力は `(1-z)^T`。平均二乗精度と95%の精度保証は異なる。

最悪の条件付き有限回リスクは高々3固有値で達成されることを証明。既知の二項逆数モーメント・モーメントLPを用いた、このスペクトル推定設定への限定的な構造的追加であり、有限ショットや一般統計原理の発明ではない。有限候補群では、連続応答証明書と有理数リスク上界を用いて、無出力確率を制限しつつ関数・次数を選ぶ。少予算では量子計算なしの事前中点も選択する。

4/6/8スピンのイジング模型6条件、48予算条件、39固定フィルタ試行数条件を検証。114バッチ×20,000回、計228万回の集約サンプリングで厳密法則の数値評価と照合した。事前情報は解析的に与え、選択に真の固有値を使わない。100個の支持縮約照合、183の厳密有理和・区間チェックも成功。

**限界**：保証上界が小さい選択が各物理入力で常に実際の誤差を小さくするわけではない。理想的な正規化Hamiltonian信号の費用比較で、実ゲート費用・一般量子優位を示さない。3固有値定理全体は手証明。追加4補題だけをローカルLean確認し、remote CIは未実行。

## 論文の核

最小Gram固有値が `[0,u]` にあり、その初期質量が `a` 以上とだけ分かる問題を扱う。ギャップは仮定しない。平均バイアスの一様条件を二点の不等式で特徴づけ、応答に `1-x` を掛ける上端零化によって最悪受理確率の損失を `(1-u)(1-u-b)` で制御する。追加次数は1。この制限下で最悪受理確率が厳密に `a*tau²` となり、固定次数の選択を半無限線形計画として特徴づける。

LPやQSVT関数選択自体を発明とは主張しない。指定した実数多項式、有限誤差配分、次数上限、Hoeffding推定・完全再試行モデルについて、連続実行可能性の証明書と厳密双対下界を用いて費用を比較する。主結果10条件はすべて、事前区間の中点だけでは指定精度を達成できない `u>4E` を満たす。

## 実測した検証結果

| 項目 | 結果・範囲 |
|---|---|
| 選択費用上界 / 制限クラスの最適費用下界 | 1.0372–1.2394（10条件） |
| 保存位相の連続応答誤差上界 | 最大 `3.63e-16`、厳密有理区間演算 |
| 全行列QSP/LCU応答の数値誤差 | 最大 `5.55e-16`、10個の合成問題 |
| 全行列ユニタリ性残差 | 最大 `6.33e-15` |
| 独立スカラー / 行列サンプリング | 1,000 / 2,000例、観測した精度違反0 |
| 証明書用算術チェック | 328件成功、実行可能・不可能の対照例を含む |
| Lean | 5つのスカラー補題を実際にローカル検証。論文全体の形式化ではない |

濃度保証は証明に由来し、有限回の違反0はその証明の代用ではない。絶対費用は一部で数十億queryに及ぶ。既存Chebyshev応答が選ばれる例、準備費用によって次数が変わる例、他の候補が証明書を得られない例も報告する。一般量子アルゴリズムに対する優位性や物理ゲート費用は示していない。

## 再現

リポジトリ直下の隔離Python環境に `paper/filter-selection/requirements.txt` をインストールして実行する。

```sh
python experiments/check_selection_certificates.py
python experiments/filter_selection.py
python experiments/selection_qsp.py
python experiments/selection_matrix_audit.py
python experiments/selection_figures.py
```

主要結果は `results/filter_selection*.json`、図は `figures/selection_*.png`。コード・入力結果のSHA-256、設定、乱数seed、パッケージversionを保存している。LP候補・位相候補の生成は浮動小数演算であり、環境によって候補が変わる可能性がある。証明書の最終判断は有理数・整数演算による。

短い試行は `python experiments/filter_selection.py --pilot --output work/pilot.json`。全10条件の設計は通常数分。Leanの再現は `lean/` で `lake build Selection` と `lake env lean SelectionAudit.lean`。実行ログ・版・検証範囲は [Lean確認記録](../../lean/verification/selection-verification.md) に記載。

PDF再生成は `sh paper/filter-selection/build.sh`。XeLaTeX、または共有コンパイル補助が検出するTectonicが必要。投稿用ファイル再生成は次の順で行う。

```sh
python paper/filter-selection/package_source.py
python paper/filter-selection/package_arxiv.py
```

各ZIPは新しい一時ディレクトリで本文のコンパイル、算術チェック、Git情報のない状態でのpilot実験に成功した場合だけ更新する。日英ZIPは両言語を検証する。arXiv ZIPは英語入口を一つにし、コード・データを `anc/` に置く。ZIP内のmanifestに各同梱ファイルのSHA-256を記録する。arXiv側の実行や投稿は実施していない。

## 有限サンプリング部分の再現

以下はリポジトリ直下から。元の抽象実験は再処理せず、保存済みの応用データを使える。

```sh
OPENBLAS_NUM_THREADS=1 MPLCONFIGDIR=/tmp/qmsve-mpl .venv/bin/python experiments/check_finite_sampling.py
OPENBLAS_NUM_THREADS=1 MPLCONFIGDIR=/tmp/qmsve-mpl .venv/bin/python experiments/selection_finite_budget.py
OPENBLAS_NUM_THREADS=1 MPLCONFIGDIR=/tmp/qmsve-mpl .venv/bin/python experiments/selection_finite_precision.py
MPLCONFIGDIR=/tmp/qmsve-mpl .venv/bin/python experiments/finite_sampling_figures.py
```

応用データから作る場合は先に `selection_ising_application.py` を実行する。短い有限予算pilotは `selection_finite_budget.py --pilot --repeats 1000`。保存先は `results/finite_budget.json`、`finite_precision.json`、`finite_sampling_summary.json`。候補・境界・入力/ソースハッシュを保存し、既存ファイルを無断で混ぜない。集約二項分布を使うので、10^12ショットを一つずつ量子回路シミュレートしたという意味ではない。

追加Lean再現は `lean/` で `lake build FiniteSampling` と `lake env lean FiniteSamplingAudit.lean`。[確認記録](../../lean/verification/finite-sampling-verification.md)に実ログとハッシュ、厳密な検証範囲を記載した。

最終の[成果物整合性監査結果](validation-summary.json)はpassed。PDFと両ZIPのハッシュ、頁数、コード/データ対応を記録。リポジトリの `experiments/audit_finite_update.py` で再確認できる（PDF監査のみPyMuPDFが別途必要）。両ZIPは最新版の別フォルダ展開コンパイルと算術/Gitなしpilotを通した。
