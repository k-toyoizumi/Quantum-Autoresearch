# Project State

更新日：2026-10-24（日本時間）

## Goal
化学・物性のエネルギー推定を対象に、深さ制約下の量子スペクトルフィルタを調査する。現段階は段階1（既存法の仮定・保証・費用、過去資産の再利用条件の確認）。

## 現在地
- 重点文献・過去資産の一次資料照合を記録した：[段階1レビュー](memo/research/2026-10-24_2_filter-literature-and-asset-review.md)
- 研究計画の段階1は未完了。Booster本文の仮定・費用、FQPE robustness補遺、過去コードの実行条件が未確認。
- 数値実験、過去コードの実行、Lean検証は未実施。
- READMEと研究計画の現在地表示は整合しているため変更していない。
- 最終保存commit：`362583faaa678b4e54d1435a92321d0ce302fcb3`（レビューmemo）。

## 次回最初の一手
Booster本文とFQPE robustness補遺の未確認条件を読み、既存レビューへ差分として記録する。その後、段階1完了条件を再評価する。深さ・総queryの比較では入力oracle、精度、失敗確率、事前情報取得をそろえる。

## Source pointers
- `docs/project/research-plan.md`
- `docs/project/research-direction.md`
- `memo/research/2026-10-24_2_filter-literature-and-asset-review.md`
