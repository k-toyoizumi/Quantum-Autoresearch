# 投稿用ファイル

- 英語本文：`Filter-selection-en.pdf`。日本語の確認用：`Filter-selection-ja.pdf`。
- arXiv用：`Filter-selection-arxiv.zip`。英語の入口は `main.tex` 一つ。数値実験・データ・Lean資料は `anc/` に同梱。
- 日英両方を編集・再現する場合：`Filter-selection-source.zip`。
- 分類候補：quant-ph。表題は **Prior-Robust QSVT Filter Selection: Gap-Free Bias and Finite-Budget Risk**。
- 著者・所属・連絡先は本人の希望により空欄。投稿時に本人が確定する。投稿・外部公開は実施していない。

コンパイラは **XeLaTeX** を選択する。公式案内では2025年11月からXeLaTeXに対応しており、現行TeX Live案内にも記載されている。フォントは同梱ファイルを直接参照する構成。ローカルではTectonicで展開後の原稿をコンパイルし、再現コードも実行した。arXiv側でのコンパイル成功・受理を確認したものではない。[TeX Live公式案内](https://info.arxiv.org/help/faq/texlive.html)、[TeX投稿案内](https://info.arxiv.org/help/submit_tex.html)

付随資料は公式の `anc/` 配置に従い、その中にTeX原稿は入れていない。[付随資料の公式案内](https://info.arxiv.org/help/ancillary_files.html)

主張は固定フィルタ・平均推定・再試行方式に限定する。大幅な量子高速化や一般的な最適性を投稿メタデータで付加しない。新規性の位置づけは `novelty-review.md`、根拠の対応は `claim-evidence.md` に記載。

有限予算・理想回路の統計評価と物理応用を本文へ統合済み。有限ショット自体を新規性とはせず、支持縮約と指定推定器の保証に限定して記載する。
