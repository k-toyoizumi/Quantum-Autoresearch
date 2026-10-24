# Project State

更新日：2026-10-24（日本時間）

## Goal
化学・物性のエネルギー推定を対象に、深さ制約下の量子スペクトルフィルタを調査する。

## 現在地
- 段階1（文献・過去資産の静的レビュー）完了。詳細：[文献・過去資産レビュー](memo/research/2026-10-24_2_filter-literature-and-asset-review.md)、[QSVT toolchain比較](memo/research/2026-10-24_3_qsvt-toolchain-review.md)、[残件・段階2引継ぎ](memo/research/2026-10-24_4_stage1-remainder-review.md)
- 研究者が段階2の中心を候補Bに確定：下流も浅い推定器に固定し、フィルタ形・強さと下流推定を全工程depth cap内で共同設計する。候補A（操作可能な事前情報下での優位/棄却条件）は補助評価とする。詳細：[研究方向](docs/project/research-direction.md)、[理論候補と費用モデル](memo/research/2026-10-24_5_stage2-theory-candidates.md)
- FQPE v2が一般filter、有限窓band-pass、minimax/Chebyshev、積分漏れ最小化、粗い見積り・two-stage等を含むため、単純な近縮退窓filterの新規性は弱い。候補の差分・新規性・優位性は未確認。
- 次に比較条件を具体化する：入力oracle、下流浅深度推定器、state preparation費、失敗再試行、事前情報と取得費、目標精度・信頼度、全工程最大深さ。これらの値・方式はまだ未選択。
- 固定予算式は独立試行・費用モデルに限定したmemo内の導出で、未知の目標イベントが識別できない場合は停止可能な期待費用として扱わない。
- 旧依存version pinsが見つからず、旧環境の再現とコード実行は未確認。これは段階3で再現/移植を分けて検証する。
- PennyLane QSVT high-level APIは角度合成と既定encodingを組み立て、low-level APIはcustom block encoding/projector phasesからQSVT回路を生成することを確認。移行採用は未決。
- 実験・環境構築・Lean検証は未実施。

## 次回最初の一手
比較の土台を合意可能な形に具体化する：①入力oracleと同等性 ②下流浅深度推定器 ③状態準備・失敗再試行・事前情報の取得費 ④最終精度・信頼度 ⑤状態準備から読み出しまでの最大深さの定義。物理系や特定アルゴリズムの選定はこの比較条件を確認してから行う。

## Source pointers
- `docs/project/research-plan.md`
- `docs/project/research-direction.md`
- `memo/research/2026-10-24_2_filter-literature-and-asset-review.md`
- `memo/research/2026-10-24_3_qsvt-toolchain-review.md`
- `memo/research/2026-10-24_4_stage1-remainder-review.md`
- `memo/research/2026-10-24_5_stage2-theory-candidates.md`
