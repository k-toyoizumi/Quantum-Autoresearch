# Prior-Robust QSVT Filter Selection for Gap-Free Spectral-Mean Estimation

最終確認日：2026-10-27（日本時間）。QMSVE原案から発展させた、固定平均推定器に対する事前情報に頑健なフィルタ選択の論文。著者情報は本人の希望により空欄。未投稿・未公開。

- [英語PDF・13頁](Filter-selection-en.pdf)、[日本語PDF・11頁](Filter-selection-ja.pdf)
- [arXiv用・英語ソースZIP](Filter-selection-arxiv.zip)、[日英再現ソースZIP](Filter-selection-source.zip)
- [投稿用ファイルの説明](submission-notes.md)、[主張と根拠](claim-evidence.md)、[先行研究との重複・批判的評価](novelty-review.md)

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
