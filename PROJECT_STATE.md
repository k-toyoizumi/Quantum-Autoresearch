# Project State

更新日：2026-10-24（日本時間）

## Goal
化学・物性のエネルギー推定を対象に、深さ制約下の量子スペクトルフィルタを調査する。現在は段階1（既存法の仮定・保証・費用、過去資産の再利用条件の確認）。

## 現在地
- 文献・過去資産の重点照合を記録：[段階1レビュー](memo/research/2026-10-24_2_filter-literature-and-asset-review.md)
- QSVT位相合成・回路・シミュレータ候補の比較を記録：[ツールチェーン比較](memo/research/2026-10-24_3_qsvt-toolchain-review.md)
- READMEと研究計画の現在地表示は整合しているため変更していない。
- 段階1は未完了。Booster本文の仮定・費用、FQPE robustness補遺、過去コード実行条件、同一条件のsolver比較が未確認。
- 数値実験、過去コードの実行、Lean検証、環境構築は未実施。
- 今回の主な移行候補：PennyLane poly_to_angles/QSVT + Lightning.qubit。ただし旧Qiskit回路/Aerを比較基準として残し、採用前に同一oracle・同一多項式で照合する。

## 次回最初の一手
対象ハミルトニアンと入力oracleを確定する。その後、旧coefs.pyの基底を特定し、同一の正規化済みChebyshev多項式でPyQSP Laurent/sym_qspとPennyLane root-finding/iterativeを比較する。AerとPennyLane QSVTで既知小例の行列・ゲート深さ・成功確率を照合する。

## Source pointers
- `docs/project/research-plan.md`
- `docs/project/research-direction.md`
- `memo/research/2026-10-24_2_filter-literature-and-asset-review.md`
- `memo/research/2026-10-24_3_qsvt-toolchain-review.md`
