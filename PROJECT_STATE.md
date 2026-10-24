# Project State

更新日：2026-10-24（日本時間）

## Goal
化学・物性のエネルギー推定を対象に、深さ制約下の量子スペクトルフィルタ関数設計を調査する。

## 現在地
- 段階1（文献・過去資産の静的レビュー）完了。詳細：[文献・過去資産レビュー](memo/research/2026-10-24_2_filter-literature-and-asset-review.md)、[QSVT toolchain比較](memo/research/2026-10-24_3_qsvt-toolchain-review.md)、[残件・段階2引継ぎ](memo/research/2026-10-24_4_stage1-remainder-review.md)
- 研究者は①を確定：関数設計中心のBを維持し、physical-versus-virtual filterは公平比較の評価基盤とする。物理対virtualの方式比較を主題へ移さない。下流は浅い推定器として全工程hard depth cap内で共同設計する。[確定方向](docs/project/research-direction.md)
- 低次数prior-only scalar screenを実行し、既知 cosine-power baselineへ戻る結果（新規候補改善なし）を保存した：[screen memo](memo/research/2026-10-24_7_filter-design-screen.md)。スクリプト・JSONは `experiments/` と `results/`。標準Pythonで再実行一致確認済み。gridded proxyであり、物理ゲート深さや強baseline優位を示さない。\n- 現在は少数のパラメトリック候補を具体化。暫定HE/controlled-time-evolutionモデルの費用、downstream estimator固有のenergy biasとsignal-estimation stability、shot variance、成功確率、全深さ制約を統一し、既存filterをbaselineとして比較する。物理・信号フィルタ既存レビュー：[memo](memo/research/2026-10-24_6_physical-virtual-filter-depth.md)
- 候補例（未採用）：bracket中心だけで設定するbounded cosine-power filter、同じ有限supportで係数を下流エネルギーriskに合わせるprior-only optimizer。いずれも新規性未確認。filter中心・gap・初期重みの真値を選択入力に用いず、既知値synthetic testはoracle-assisted sanityと明記する。
- FQPE、QETU、QCELS内Fourier-filtered版、Lin–Tong CDF、Wang Gaussian-derivative GSEE、Kaiser/DPSS/Chebyshevと重なる可能性が強い。既存法を再発明しない棄却条件が必要。物理/virtual identityだけは低深さ性能差やenergy advantageを意味しない。
- 係数スケーリングに依存しないよう、`z_f=Tr[rho f†f]`、`p_herald=z_f/L²)、virtual merged-coefficient norm `B_f` を区別し、physical estimatorではnormalization後の成功sample数に初期overlap factorを二重に掛けない。virtual ratio `N/z_f` は一般にunbiasedでない。
- 今回の粗いgrid screenは `cos^6(πx/2)` が最小physical-cost候補だが、比較対象に含めた既知binomial族そのもの。no-filter filtered-mean proxyはprior bias条件で失格。新規性/優位は未確認、QCELS等強baselineとの同条件比較が残る。\n- 先行scalar sanity check（既知E0/gap、2-level）は期待信号の一致だけを検証した。今回の小探索は未知targetに使わないprior-only設計則とfinite-difference estimatorのbias/variance/depthを追加確認する。Python標準ライブラリで可能で、環境費用なし。回路・環境構築・Lean検証は未実施。
- AGENTS.mdとagent-policy.mdに、チャット依頼起点・上位モデルの承認制を維持したまま「commitは停止点ではなく、依頼内で必要判断材料まで自律継続」と記録。
- 旧依存version pinsが見つからず、旧環境の再現とコード実行は未確認。これは段階3で再現/移植を分けて検証する。
- PennyLane QSVT high-level APIは角度合成と既定encodingを組み立て、low-level APIはcustom block encoding/projector phasesからQSVT回路を生成することを確認。採用未決。

## 次の一手
prior-only design rulesで候補の少数人工スペクトル探索を行い、同じ `epsilon,delta,D) のもとに estimator-specific bias/variance, physical herald+retries, virtual `B_f/z_f` ratio-error, state-prep/HE-query costを比較する。関数係数と探索規則を分離し、設計で用いていない真値は評価時にだけ使う。強baselineに対して有望な条件が残る場合、criticレビュー後に結果をmemoへ保存する。応用系/高精度シミュレータ/実回路へ進む判断は今回の比較後に必要性を再評価する。

## Source pointers
- `docs/project/research-plan.md`
- `docs/project/research-direction.md`
- `docs/workflow/agent-policy.md`
- `memo/research/2026-10-24_2_filter-literature-and-asset-review.md`
- `memo/research/2026-10-24_3_qsvt-toolchain-review.md`
- `memo/research/2026-10-24_4_stage1-remainder-review.md`
- `memo/research/2026-10-24_5_stage2-theory-candidates.md`
- `memo/research/2026-10-24_6_physical-virtual-filter-depth.md`\n- `memo/research/2026-10-24_7_filter-design-screen.md`\n- `experiments/stage2_filter_screen.py`\n- `results/stage2_filter_screen.json`
