# Project State

更新日：2026-10-27（日本時間）

## Goal
本人の追加依頼：回路操作は理想的・測定は有限回として精度を理論と数値実験で調べ、新規性を批判的に検討し、研究・日英論文・再現資料を更新する。著者情報は今は不要、外部投稿は行わない。

## 原本PDFとGitHub反映（2026-10-27追加依頼）
- 本人指定のGoogle Driveから、QMSVE19頁とランチョス/共役勾配法16頁のPDF本体をダウンロードし、バイナリを編集せず保存。`references/qmsve/2023_0311_QMSVE.pdf`、`references/qcg/2023_0413_QLanzos_CG.pdf`。
- 出典、サイズ、頁数、SHA-256は `references/original-pdfs.json`。原本保存コミットは `d038c25`。
- 本人が原本を含むcommit/pushを明示依頼し、さらに「pdf本体も保存」と確認。未送信の有限サンプリング論文改訂も併せてmainへ反映する。arXivへの投稿は行わない。

## 最新Working Set：2026-10-27 有限回精度と論文化
- 原稿題名：Prior-Robust QSVT Filter Selection: Gap-Free Bias and Finite-Budget Risk。元の受理後サンプル数固定の保証と、棄却を含む総予算固定を区別。回路は理想応答とし、測定だけ有限回とする。
- 手証明：正の二項逆数モーメントによる厳密条件付きMSE、無出力、許容誤差違反の混合式、固定締切での信頼度系、最悪条件付きMSEの高々3固有値への縮約。逆モーメント・モーメントLP自体は既知として20文献に位置づけ。
- 選択：厳密有理数・180bit外向き累乗でMSE上界と無出力を認証。有限候補群の上界最小化のみ。事前中点を含め、48条件中21条件で量子計算なしを選ぶ。実入力ごとの最適性や一般量子優位ではない。
- 実験：物理模型6条件×8予算、固定応答3本×13試行数、計114独立samplingバッチ×20,000回=228万回。MSE最大差3.31 Monte Carlo標準誤差。183厳密算術/列挙controls、100支持縮約controls。入力/ソースhash保存。
- 成果物：`paper/filter-selection/finite-{en,ja}.tex`、`finite-results-{en,ja}.tex`、改訂日英PDF、`results/finite_budget.json`、`finite_precision.json`、`finite_sampling_summary.json`、`figures/finite_{precision,budget}.png`。追加査読は `finite-novelty-review.md`。
- Lean：追加4スカラー補題をローカル確認。全3固有値定理や二項確率の形式化ではない。実ログ・hashは `lean/verification/finite-sampling-verification.md`。remote CI未実行。
- 検証完了：最終英語19頁・日本語16頁を全頁描画確認。両ZIPを新規展開しコンパイル、328従来/183追加チェック、Gitなしpilot成功。日英ZIPでは有限予算pilotも成功。artifact監査passed、ハッシュ/頁数は `paper/filter-selection/validation-summary.json`。今回追加分も上記の本人push依頼の反映対象。arXiv未投稿。
- 今回の目的は完了。詳細checkpoint：`memo/research/2026-10-27_finite-sampling-paper_3.md`、全要件の監査：`memo/reviews/2026-10-27_finite-sampling-completion-audit_4.md`。新しい本人依頼まで自動継続しない。以前のWorking Setは履歴として保全する。

## 履歴：2026-10-27 具体的応用の初回試験
- 本人の追加依頼でTFIM基底エネルギー推定を実験。4/6/8スピン、2結合条件、計6条件。解析的なエネルギー・重なり事前境界だけで選択後、厳密対角化で監査。
- 全6条件で目標精度達成。Chebyshev型の保証費用は選択応答の1.001–1.173倍、指定制限最適下界に対する選択保証は1.0012–1.0989。保存位相の連続誤差上界最大2.04e-16。200回×6のsampling違反0。
- `paper/filter-selection/ising-application.md` に方法・結果・限界。`memo/experiments/2026-10-27_ising-application_2.md` に引継ぎ。追加データは `results/selection_ising*.json`、図は `figures/selection_ising_application.png`。
- エネルギーHamiltonianへの偶奇QSP写像と1/2振幅損失を明示。理想正規化信号のquery比較で、物理ゲート費用・古典優位・非可積分な応用性能は未実証。元の日英PDF/ZIPには組み込まず独立追加資料。今回追加分はローカル保存、未コミット・未push。
- この小規模実証は完了。次の依頼で本格的な非可積分模型、初期状態・費用感度、同一oracleでの既存法比較や本文への組込みを検討する。

## 履歴：2026-10-27 初回論文完成
- 成果物：`paper/filter-selection/`。英語13頁・日本語11頁、英語投稿ZIP、日英再現ZIP、README、主張対応表、先行研究比較。
- 主結果：gap-free一様平均バイアスの二点条件、上端零化の受理損失因子 `(1-u)(1-u-b)`、零化後の厳密最悪受理確率 `a*tau²`、固定推定・再試行モデルの半無限LP特徴づけ。全体は手証明、5つのスカラー補題はLean 4.35.0で実チェック成功。
- 本実験10条件すべて `u>4E`。連続実行可能性・厳密双対下界で費用比1.0372–1.2394。保存QSP位相の連続誤差最大3.63e-16。全行列32次元抽出回路の数値検証、1,000スカラー/2,000行列sampling、328算術チェック成功。
- 検証：日英全頁描画、未定義参照・欠字・overfullなし。日英ZIPは新規フォルダで両PDFとGitなしpilotを検証。英語投稿ZIPも新規展開コンパイル・算術・pilot成功。arXiv側実行/受理やremote CI成功は主張しない。
- 批判的対応：初期の自明prior例を本実験から除外、旧メモの非解析性から非達成を推論する誤りを不採用、反復正規化の不要な損失を排除。LP/交換法/関数選択を発明としない。一般量子優位なし。
- 記録：`memo/reviews/2026-10-27_filter-selection-paper-review_1.md`。作業先・baseは引き続き下記checkoutと `74273e4`。新成果は未コミット。別checkout・既存草稿は保全。追加モデル/サブエージェント/定期実行なし。
- 2026-10-27追加依頼：本人がGitHubへのpushを明示認可。完成原稿・コード・データと先行する今回のQMSVE改訂をmainへ記録・送信する。arXiv投稿は認可・実施していない。
- 今回の研究・執筆・ローカル検証は完了。次に投稿する場合の著者情報・外部公開判断は本人が行う。無人継続は設定しない。

## 履歴：2026-10-26レビュー改訂
- 作業先：`/home/ktoyo/projects/Quantum-Autoresearch-github`。`git pull --ff-only` で `74273e4` を取得し、その上で未コミットの原稿改善を実施。別checkoutのローカル未送信履歴は統合しない。
- 日英原稿を「Sharp Gap-Free Bias Bounds for Cosine and Polynomial Singular-Value Filters」へ改題。関連文献7→16件。直接重なるGe–Tura–Cirac、Lin–Tong、He–Zhang–Wang等との関係を明記。
- 主結果候補：固定応答・最小値・目標質量に対する平均バイアスの正確な二点最悪包絡、cosine-Gram / dilationの鋭いgap-free定数・率。固定次数多項式baseline、Taylor正規化の指数的受理損失、受理後摂動評価を追加。完全な手証明あり。新しい定理はLean未検証。優先性・単独論文としての重要性は未確定。
- 新実験：`experiments/qmsve_gapfree_envelope.py`、`results/qmsve_gapfree_envelope.json`、`figures/qmsve_gapfree_envelope.png`。1,000ランダム分布・密格子・漸近定数を照合し違反なし。数値確認と普遍命題の手証明を区別。
- 改訂PDF：`paper/qmsve/QMSVE-en.pdf`（12頁）、`QMSVE-ja.pdf`（10頁）。Tectonic 0.17.0で成功し全頁描画QA済み。既存Lean source/logは保全し、新規CI成功とは扱わない。未知状態準備・QSVT位相・実回路・量子優位は未検証。
- 評価・文献対応：`paper/qmsve/literature-comparison.md`、`paper/qmsve/claim-evidence.md`、`memo/reviews/2026-10-26_qmsve-critical-review_2.md`。
- 次の一手：正確な包絡・定数を古典weighted power-iterationと追加cosine文献へ独立照合。既出なら再現・整理へ格下げ。原案PDF・著者情報の確認、新定理の形式検証、必要なら同一oracle費用での比較を進める。

## 現在地
- 段階1（文献・過去資産の静的レビュー）完了。詳細：[文献・過去資産レビュー](memo/research/2026-10-24_2_filter-literature-and-asset-review.md)、[QSVT toolchain比較](memo/research/2026-10-24_3_qsvt-toolchain-review.md)、[残件・段階2引継ぎ](memo/research/2026-10-24_4_stage1-remainder-review.md)
- 研究者は①を確定：関数設計中心のBを維持し、physical-versus-virtual filterは公平比較の評価基盤とする。物理対virtualの方式比較を主題へ移さない。下流は浅い推定器として全工程hard depth cap内で共同設計する。[確定方向](docs/project/research-direction.md)
- 低次数prior-only scalar screenを実行し、既知 cosine-power baselineへ戻る結果（新規候補改善なし）を保存した：[screen memo](memo/research/2026-10-24_7_filter-design-screen.md)。スクリプト・JSONは `experiments/` と `results/`。標準Pythonで再実行一致確認済み。gridded proxyであり、物理ゲート深さや強baseline優位を示さない。
- 現在は少数のパラメトリック候補を具体化。暫定HE/controlled-time-evolutionモデルの費用、downstream estimator固有のenergy biasとsignal-estimation stability、shot variance、成功確率、全深さ制約を統一し、既存filterをbaselineとして比較する。物理・信号フィルタ既存レビュー：[memo](memo/research/2026-10-24_6_physical-virtual-filter-depth.md)
- 候補例（未採用）：bracket中心だけで設定するbounded cosine-power filter、同じ有限supportで係数を下流エネルギーriskに合わせるprior-only optimizer。いずれも新規性未確認。filter中心・gap・初期重みの真値を選択入力に用いず、既知値synthetic testはoracle-assisted sanityと明記する。
- FQPE、QETU、QCELS内Fourier-filtered版、Lin–Tong CDF、Wang Gaussian-derivative GSEE、Kaiser/DPSS/Chebyshevと重なる可能性が強い。既存法を再発明しない棄却条件が必要。物理/virtual identityだけは低深さ性能差やenergy advantageを意味しない。
- 係数スケーリングに依存しないよう、`z_f=Tr[rho f†f]`、`p_herald=z_f/L²`、virtual merged-coefficient norm `B_f` を区別し、physical estimatorではnormalization後の成功sample数に初期overlap factorを二重に掛けない。virtual ratio `N/z_f` は一般にunbiasedでない。
- gap-free fixed-filterのchain boundを再導出した：[前memo](memo/research/2026-10-24_8_gapfree-filter-chain-bound.md)。η=.1、bracket幅=.1、b=.01でΔ=2b/(1−η)を選んだときの理想pure-ground transmission下界は1/14,641。
- 続いてgap-free filtered-mean条件下の**任意スカラーweight**の有限W transmission optimum F(W)を手導出：[memo](memo/research/2026-10-24_9_gapfree-minimax-envelope.md)、[script](experiments/gapfree_minimax_bound.py)、[JSON](results/gapfree_minimax_bound.json)。同じη=.1,W=.1,b=.01で最適等分chainはn=5,Δ=.02、worst-case pure-ground transmission上限1/59,049。これはdegree/query depth/LCU normalizationを無視した関数レベルの厳密解で、物理herald costや一般GSEE no-goではない。新規性未確立。
- 有限次数への接続screenを実施：[memo](memo/research/2026-10-24_10_finite-degree-gapfree-screen.md)、[script](experiments/finite_degree_gapfree_filters.py)、[JSON](results/finite_degree_gapfree_filters.json)。η=.1,W=.1,b=.01で次数2以下の代数多項式振幅を有限差分gateで排除し、shifted-power次数58の連続bias十分条件を確認。次数3〜57は未解決。CTE cosine/Gaussian/envelope truncationのK=2/4/6 screenはgrid上すべて目標biasを超過。screenは新規性・優位性を示さず、回路とLeanは未実施。
- 次の次数制約minimax screen：[memo](memo/research/2026-10-24_11_gapfree-degree-minimax-exchange.md)、[script](experiments/gapfree_degree_minimax_exchange.py)、[JSON](results/gapfree_degree_minimax_exchange.json)。nonnegative amplitude LPでn=20、design bias .0095の候補がdense grid validationを通過したがcontinuous保証なし。LP primal/dual診断は浮動小数で、n=20改善・実装・新規性は未確認。
- AGENTS.mdとagent-policy.mdに、チャット依頼起点・上位モデルの承認制を維持したまま「commitは停止点ではなく、依頼内で必要判断材料まで自律継続」と記録。
- 旧依存version pinsが見つからず、旧環境の再現とコード実行は未確認。これは段階3で再現/移植を分けて検証する。
- PennyLane QSVT high-level APIは角度合成と既定encodingを組み立て、low-level APIはcustom block encoding/projector phasesからQSVT回路を生成することを確認。採用未決。
- 2026-10-24本人認可：現在の研究目標・既存予算内の研究方向選択、比較条件の設計、仮説の採否/棄却はAgentに委任。追加予算・外部公開・Astra/Sol high以上の事前承認制は維持。新規性は保証されない。

## 次の一手
今回の依頼は成果物作成とローカル検証まで完了。新しいチャット依頼があれば、最新Working Setと論文READMEから再開する。過去の下記Working Set・探索メモは履歴として扱い、未完タスクを自動再開しない。

## Source pointers
- `docs/project/research-plan.md`
- `docs/project/research-direction.md`
- `docs/workflow/agent-policy.md`
- `memo/research/2026-10-24_2_filter-literature-and-asset-review.md`
- `memo/research/2026-10-24_3_qsvt-toolchain-review.md`
- `memo/research/2026-10-24_4_stage1-remainder-review.md`
- `memo/research/2026-10-24_5_stage2-theory-candidates.md`
- `memo/research/2026-10-24_6_physical-virtual-filter-depth.md`
- `memo/research/2026-10-24_7_filter-design-screen.md`
- `experiments/stage2_filter_screen.py`
- `results/stage2_filter_screen.json`
- `memo/research/2026-10-24_8_gapfree-filter-chain-bound.md`
- `experiments/gapfree_filter_bound.py`
- `results/gapfree_filter_bound.json`
- `memo/research/2026-10-24_9_gapfree-minimax-envelope.md`
- `experiments/gapfree_minimax_bound.py`
- `results/gapfree_minimax_bound.json`
- `memo/research/2026-10-24_10_finite-degree-gapfree-screen.md`
- `experiments/finite_degree_gapfree_filters.py`
- `results/finite_degree_gapfree_filters.json`
- `memo/research/2026-10-24_11_gapfree-degree-minimax-exchange.md`
- `memo/research/2026-10-25_1_publication-go-no-go.md`
- `memo/research/2026-10-25_2_calibration-free-fmpe-screen.md`
- `memo/research/2026-10-25_3_qmsve-techreport-scope.md`
- `experiments/calibration_free_fmpe_toy.py`
- `results/calibration_free_fmpe_toy.json`
- `experiments/gapfree_degree_minimax_exchange.py`
- `results/gapfree_degree_minimax_exchange.json`


## 2026-10-26：QMSVE技術報告草稿と検証
今回のユーザー依頼に基づき、QMSVE原案を中心にした確認用日本語稿・英語技術報告草稿・Lean形式化・7例の行列レベル再現実験を作成した。英語稿は内部確認用の草稿で、著者・所属が未確定、未投稿・未公開であり、新規性・高速化は主張しない。主張と証拠・制限は `paper/qmsve/claim-evidence.md`、詳細は [作業memo](memo/research/2026-10-26_1_qmsve-technical-report-draft.md)。

- PDF: `paper/qmsve/QMSVE-ja.pdf`（9頁）、`paper/qmsve/QMSVE-en.pdf`（10頁）。XeLaTeX二回実行後に全ページ描画QA済み。IPAexフォントのstyle fallback警告のみ。
- 英語ソース/再現パッケージ: `paper/qmsve/QMSVE-source.zip`。別の空ディレクトリへ展開して2回コンパイル成功。実験スクリプト・JSON・図・Lean sourceと検証記録を含む。
- 実験: `experiments/qmsve_matrix_level.py` を再実行し、`results/qmsve_matrix_level.json` のJSON parse成功。既知右固有基底で指定した人工スペクトル重みの古典行列監査であり、量子回路/QSVT位相/未知状態準備を検証していない。
- Lean: `lean/QMSVE.lean` SHA-256 `bc9a5a6729b813b1695519174c0ae0f87db7ec00c2c52448b7bc4e9c7e7ada75`。Lean 4.35.0 / Mathlib v4.35.0で `lake build QMSVE`, `lake env lean Audit.lean` ともexit 0。二つの有限スカラー定理のみ形式検証。行列/SVD/QSVT/測定・Hoeffding/全費用は形式化範囲外。
- 次の確認は技術レビューと著者欄/書誌情報の確認。外部公開・投稿、回路合成、化学系での実装は未実施。
