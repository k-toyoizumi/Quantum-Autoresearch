# 有限サンプリング更新：完了監査

2026-10-27 JST。目的は理想回路・有限測定の精度を理論/数値で検討し、新規性を評価した上で論文を更新すること。既存成果へ目的を縮小せず、次を現物で確認した。

| 要件 | 現在の証拠 | 判定 |
|---|---|---|
| 回路は理想的、サンプリングは有限 | 実験metadataはexact target polynomial/no gate noise。`finite_sampling.py` は有限BinomialのMとKを生成。`finite_precision.json` の試行数は全て有限。 | 完了 |
| 精度の理論 | 日英 `finite-*.tex` に条件付きMSE、無出力、正確な精度違反の混合式、固定締切の信頼度系と証明。hの単調性、3固有値縮約、保証上界も全て証明。 | 完了、手証明の範囲を明記 |
| 数値実験 | `finite_budget.json` 6模型48予算、`finite_precision.json` 39条件。計114独立samplingバッチ、228万回。 | 完了 |
| 理論と実験の照合 | 183厳密有理和/演算control、100支持縮約control、MSE数値予測とMC最大差3.31標準誤差。 | 完了 |
| 新規性の批判的検討 | 追加5一次文献と近接量子推定文献を比較。`finite-novelty-review.md` に既知統計/モーメント法と特定タスクの追加主張を区別。3点必要性は未証明として主張せず、実RMSEが悪化する選択も残した。 | 評価完了、網羅的優先性は保証しない |
| 物理応用との接続 | `finite-results-{en,ja}.tex` に解析的prior、Hからの写像、偶奇QSPの1/2損失、Hadamard readout、理想oracle費用の限界を明記。 | 完了 |
| 日英論文化 | 最終英語19頁、日本語16頁。新しい締切系が両PDFにあることを抽出確認し、全頁を描画確認。欠字・未定義参照・overfullなし。 | 完了 |
| 再現可能なソース | 両ZIPを新規フォルダで展開コンパイル。328従来チェックと183追加チェック、Gitなし従来pilotを両ZIPで成功。日英ZIPでは追加有限予算pilotも成功。 | 完了 |
| 配布物と実際のソース一致 | `audit_finite_update.py` が入力/コードhash、候補上界の最小化、条件数、MC照合、support、PDF、ZIP CRC/manifest、ZIPの現行本文と主要コードの一致を確認。`validation-summary.json` はpassed。 | 完了 |
| 形式検証の正確な表示 | 追加4スカラー補題のlocal build/audit成功、実ログとsourcehash。全統計理論/支持定理の形式化・remote CI成功とはしない。 | 完了、限定範囲 |
| 著者・投稿 | 著者空欄を保全。arXiv投稿・今回更新のpushなし。 | 本人の指定と依頼範囲どおり |

投稿用ZIPは英語入口main.texのみで、コード/データはanc、anc内にTeX原稿なし。日英ZIPは両言語を含む。ハッシュと頁数の正本は `paper/filter-selection/validation-summary.json`。検証ログは `work/finite-sampling/`、`work/selection-source-validation.log`、`work/selection-arxiv-validation.log`。

この監査は論文の重要性やarXiv受理を保証するものではない。今回依頼の理論検討・数値実験・新規性評価・論文化・ローカル再現確認には未完の必須作業を残していない。非可積分模型、実ゲート費用、別推定器との優位比較、外部投稿は新たな範囲であり、今回の完了条件と混同しない。
