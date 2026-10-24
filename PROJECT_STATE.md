# Project State

更新日：2026-10-24（日本時間）

## Goal
化学・物性のエネルギー推定を対象に、深さ制約下の量子スペクトルフィルタを調査する。

## 現在地
- 段階1（文献・過去資産の静的レビュー）完了。詳細：[文献・過去資産レビュー](memo/research/2026-10-24_2_filter-literature-and-asset-review.md)、[QSVT toolchain比較](memo/research/2026-10-24_3_qsvt-toolchain-review.md)、[残件・段階2引継ぎ](memo/research/2026-10-24_4_stage1-remainder-review.md)
- 段階2の条件付き候補A（操作可能な事前情報だけによるfilter棄却/crossover境界）と候補B（全工程hard depth cap下での浅い下流推定比較）、仮定付き費用式、signed-H反例を作業memoに記録：[理論候補](memo/research/2026-10-24_5_stage2-theory-candidates.md)
- FQPE v2が一般filter、有限窓band-pass、minimax/Chebyshev、積分漏れ最小化、粗い見積り・two-stage等を含むため、単純な近縮退窓filterの新規性は弱い。候補の差分・新規性・優位性は未確認。
- 理論memoは仮説候補であり、本人の選択・研究テーマ確定は未実施。固定予算式は独立試行・費用モデルに限定した本memoの導出で、未知の目標イベントが識別できない場合は停止可能な期待費用として扱わない。
- 旧依存version pinsが見つからず、旧環境の再現とコード実行は未確認。これは段階3で再現/移植を分けて検証する。
- PennyLane QSVT high-level APIは角度合成と既定encodingを組み立て、low-level APIはcustom block encoding/projector phasesからQSVT回路を生成することを確認。移行採用は未決。
- 実験・環境構築・Lean検証は未実施。

## 次回最初の一手
本人と段階2の判断を詰める：①初期対象と入力oracle・操作可能な事前情報 ②硬い物理深さ/query-depth/固定費用のどれを主評価にするかと最終精度・成功確率 ③候補A/Bのどちらを先に理論確認するか。合意後に段階3の最小検証仕様を確定する。

## Source pointers
- `docs/project/research-plan.md`
- `docs/project/research-direction.md`
- `memo/research/2026-10-24_2_filter-literature-and-asset-review.md`
- `memo/research/2026-10-24_3_qsvt-toolchain-review.md`
- `memo/research/2026-10-24_4_stage1-remainder-review.md`
- `memo/research/2026-10-24_5_stage2-theory-candidates.md`
