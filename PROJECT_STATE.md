# Project State

更新日：2026-10-24（日本時間）

## Goal
化学・物性のエネルギー推定を対象に、深さ制約下の量子スペクトルフィルタ関数設計を調査する。

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
固定filterの新規族・adaptive localization+filter単体は保留/棄却。有限次数LP exchangeでは、次数20 slack candidateがdense validationを通ったがcontinuous bias/positivityは未証明で、改善とは確定しない。次は係数を使ったpair residualと正値性の連続区間certificate、および既存FQPE/QET-U/CTE下流推定器との同一depth/error/success比較。LP値は有限grid/浮動小数のscreenであり、連続最適値の厳密境界や新規性を示さない。

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
- `experiments/gapfree_degree_minimax_exchange.py`
- `results/gapfree_degree_minimax_exchange.json`
