# Project State

更新日：2026-10-24（日本時間）

## Goal
化学・物性のエネルギー推定を対象に、深さ制約下の量子スペクトルフィルタを調査する。

## 現在地
- 段階1（文献・過去資産の静的レビュー）完了。詳細：[文献・過去資産レビュー](memo/research/2026-10-24_2_filter-literature-and-asset-review.md)、[QSVT toolchain比較](memo/research/2026-10-24_3_qsvt-toolchain-review.md)、[残件・段階2引継ぎ](memo/research/2026-10-24_4_stage1-remainder-review.md)
- 重点文献の仮定・費用と未確認条件、旧QCGコードのimportと現行Qiskit API差分を記録。
- 旧依存version pinsが見つからず、旧環境の再現とコード実行は未確認。これは段階3で再現/移植を分けて検証する。
- PennyLane QSVT high-level APIは角度合成と既定encodingを組み立て、low-level APIはcustom block encoding/projector phasesからQSVT回路を生成することを確認。移行採用は未決。
- 実験・環境構築・Lean検証は未実施。研究仮説とフィルタ選択は未決定。

## 次回最初の一手
本人と段階2の判断を詰める：①初期対象と入力oracle ②成功確率/深さ/最終エネルギー精度を含む主評価指標 ③比較baseline・filter仮説と棄却条件。合意後に段階3の最小検証仕様を確定する。

## Source pointers
- `docs/project/research-plan.md`
- `docs/project/research-direction.md`
- `memo/research/2026-10-24_2_filter-literature-and-asset-review.md`
- `memo/research/2026-10-24_3_qsvt-toolchain-review.md`
- `memo/research/2026-10-24_4_stage1-remainder-review.md`
