# Project State

更新日：2026-10-24（日本時間）

## Goal
化学・物性のエネルギー推定を対象に、深さ制約下の量子スペクトルフィルタを調査する。

## 現在地
- 段階1（文献・過去資産の静的レビュー）完了。詳細：[文献・過去資産レビュー](memo/research/2026-10-24_2_filter-literature-and-asset-review.md)、[QSVT toolchain比較](memo/research/2026-10-24_3_qsvt-toolchain-review.md)、[残件・段階2引継ぎ](memo/research/2026-10-24_4_stage1-remainder-review.md)
- 研究者が段階2の中心を候補Bに確定：下流も浅い推定器に固定し、フィルタ形・強さと下流推定を全工程depth cap内で共同設計する。候補A（操作可能な事前情報下での優位/棄却条件）は補助評価とする。[理論候補](memo/research/2026-10-24_5_stage2-theory-candidates.md)
- Bの具体的な暫定比較軸として、physical state filterとraw Hadamard time-series上のvirtual |f|² reweightingを同じ信号・同じhard cap内で比較するモデルを作成：[物理・信号フィルタ比較とscalar check](memo/research/2026-10-24_6_physical-virtual-filter-depth.md)
- CTE/HE（controlled time evolution）をQETU、QCELS、FQPE、低depth CDF/GSEEと共通化できるため、初期の理論分析モデルとして暫定利用する。block encodingは排除・確定せず、比較時は別の正規化/構築costモデルを要する。
- 同じ |f|² filtered signalをphysical/virtual両方で再構成する2準位sanity checkを標準Pythonのみで実施。期待信号一致は浮動小数誤差内。E0/gapを知って作ったoracle-assisted toyであり、unknown-target estimation、有限shotsの性能、優位性を実証しない。
- 強い既存baselineにはQCELS内のFourier-filtered版、FQPE、QETU、Lin–Tong CDF、Wang Gaussian-derivative GSEE、QPE/Kaiser filteringを含める必要がある。普通のfilter+shallow-estimatorの合成は既存法と重なる可能性が高く、新規性・優位性は未確認。
- virtual filterでは |f|² 係数のl1/variance、z_f の推定とratio bias、時間support伸長を計上する。physical filterは正規化後信号mass z_f と実際のherald確率 p_herald を区別し、各accepted downstream shotでstate prep/filterを再試行込みで再準備する。
- AGENTS.mdとagent-policy.mdに、チャット依頼起点・上位モデルの承認制を維持したまま「commitは停止点ではなく、依頼内で必要判断材料まで自律継続」と記録。
- 旧依存version pinsが見つからず、旧環境の再現とコード実行は未確認。これは段階3で再現/移植を分けて検証する。
- PennyLane QSVT high-level APIは角度合成と既定encodingを組み立て、low-level APIはcustom block encoding/projector phasesからQSVT回路を生成することを確認。移行採用は未決。
- 回路実行・環境構築・Lean検証は未実施。

## 次回最初の一手
Bを保ったまま、自律的にphysical-vs-virtual/no-filter/既存filter-baselineのsymbolic shot・query・depth表を詰める。本人判断の候補は、(1) filter/downstream共同設計を主題としphysical-vs-virtualを公平評価基準にするか、(2) physical-vs-virtual filterの有利境界を主定理の中心にするか。現時点の推奨は(1)で、(2)は評価の一部として検証する。研究の重心を変更する前に本人判断へ戻す。実行/回路構築に重要資源を要しない範囲では分析を続ける。

## Source pointers
- `docs/project/research-plan.md`
- `docs/project/research-direction.md`
- `docs/workflow/agent-policy.md`
- `memo/research/2026-10-24_2_filter-literature-and-asset-review.md`
- `memo/research/2026-10-24_3_qsvt-toolchain-review.md`
- `memo/research/2026-10-24_4_stage1-remainder-review.md`
- `memo/research/2026-10-24_5_stage2-theory-candidates.md`
- `memo/research/2026-10-24_6_physical-virtual-filter-depth.md`
