# QMSVE技術報告草稿と検証記録

更新日：2026-10-26（UTC）

## 成果物

原案 `references/qmsve/2023_0311_QMSVE.pdf` を基に、確認用日本語稿と英語技術報告草稿を作成した。英語稿はarXiv形式を意識した草稿だが、著者・所属は原案に記載がないため未確定プレースホルダーのまま。投稿・外部公開・新規性の主張は行っていない。QMSVEの最大特異値べき乗法と右Gram上の最小特異値cosine反復を区別し、QCG既発表資産は先行研究として別に扱った。

- `paper/qmsve/main-ja.tex`, `paper/qmsve/QMSVE-ja.pdf`
- `paper/qmsve/main-en.tex`, `paper/qmsve/QMSVE-en.pdf`
- 英語原稿・図・実験・Leanソースを含む自己完結source/reproducibility archive: `QMSVE-source.zip`
- 実験: `experiments/qmsve_matrix_level.py`, `results/qmsve_matrix_level.json`, `figures/qmsve_matrix_level.png`
- Lean形式化・対応表・版・検証ログ: `lean/QMSVE.lean`, `lean/appendix_mapping.md`, `lean/README.md`, `lean/verification.log.md`

## 主張と検証範囲

長方形行列では $B=A/\alpha$, $G=B^\dagger B$ とし、原案のcosine応答を $\cos(\beta G)$ として定式化した。対象空間の初期重みを $a>0$、対象応答を $q_*>0$、対象外の応答絶対値を $rq_*$ 以下（$0\le r<1$）とすると、$t$ 回後の条件付き漏れは $((1-a)/a)r^{2t}$ 以下である。事後Gramモーメントは $0\le\mu_t-\lambda_0\le(1-\lambda_0)(1-F_t)$。Bernoulli観測のHoeffding誤差から特異値誤差への換算も本文で導出した。

Lean 4.35.0 / Mathlib v4.35.0で `lake build QMSVE` と `lake env lean Audit.lean` が成功。二つの定理で表示される公理はLean標準の `propext`, `Classical.choice`, `Quot.sound` のみであり、`sorry`, `admit`, user axiomはない。検証対象は有限個のスカラー重みの二つの不等式。行列/SVD還元、cosine/QSVT実装、ブロックエンコーディング、observable同定、Hoeffding集中および全回路費用は形式化していない。

## 数値実験

固定seed 20261026で7つの小行列（分離ギャップ、近縮退、縮退、初期target overlapゼロ、wide full-row-rank、rank-deficient square、非対角tall full-column-rank）を古典的に右Gram対角化した。初期状態は計算した右固有基底で指定した人工スペクトル重みから作成するため、未知特異ベクトルのstate preparation検証ではない。量子回路、QSVT位相角、ゲートはシミュレートしていない。

図・JSONはコードから再生成され、JSON構文検証が通った。2,000 accepted Bernoulli drawsの例ではHoeffding区間が厳密平均を含んだ。cosineの有限次数Taylor応答には解析一様誤差と区間有界性を使ったが、位相合成・有限精度・コンパイル誤差は評価していない。cosine-Gramと拡張行列ベースcosine-$\sigma$の表は同じ多項式次数/オラクル費の比較ではない。全体費用優位・高速化は結論していない。

## 文献と技術上の限界

QSVT / singular-value transformation, quantum power method, inverse iteration, QSVT-improved power methodを関連研究として引用した。QMSVE原稿の確認コピーには著者・所属・掲載先がなく、「三角反復法」は仮題である。したがって著者情報を推定しない。QSVT対象多項式は有界性・偶奇性を示した候補に留まり、QSP completion、実部抽出、正規化規約、補助量子ビット・費用が未確定である。入力正規化$\alpha$、初期overlap、gap/退化、成功再試行、読み出しと深さ制約が残る。

## 再現・次回判断

`python experiments/qmsve_matrix_level.py` がJSONとPNGを再生成する。PDFは `paper/qmsve/build.sh`。英語source archiveの作成スクリプト `paper/qmsve/package-arxiv-source.sh` は別の空ディレクトリへ展開してXeLaTeXコンパイル後にZIP化する。

草稿の技術的読み合わせと著者欄の確認が残る。QSVT位相合成、実回路、より大きい化学系への拡張は本作業で行っていない。英語草稿は公開・投稿前の確認用である。
