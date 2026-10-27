# GitHub cloneと数値計算環境の構築

日付：2026-10-26（日本時間）

## 目的・取得先

本人の依頼により https://github.com/k-toyoizumi/Quantum-Autoresearch をcloneし、既存Pythonスクリプトの実行環境を構築した。研究内容の追加・変更は行っていない。

- 作業先：`/home/ktoyo/projects/Quantum-Autoresearch-github`
- ブランチ：`main`
- 取得commit：`f82a42f1eb0e58847f1a8c70203b8a96757e844c`
- 元の `/home/ktoyo/projects/Quantum-Autoresearch` は未送信2コミットとGitHub側3コミットが分岐していたため、fetchのみ行い、ファイル・ブランチを変更せず保全した。

## 環境と再構築

WSL/Linux、Python 3.12.3。プロジェクト専用 `.venv` にNumPy 2.3.5、SciPy 1.17.0を導入した。取得commitには依存定義がなかったため、既存コードのimportを確認して `requirements-numerics.txt` を追加。固定版は別の既存checkoutで動作していた版を使用した。

```sh
cd /home/ktoyo/projects/Quantum-Autoresearch-github
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-numerics.txt
source .venv/bin/activate
```

## 動作確認

- `pip check`：No broken requirements found。
- NumPy/SciPyと使用する最適化関数のimport成功。
- HiGHSの小さな線形計画：成功、最適値1を確認。
- 以下の既存スクリプトは終了コード0、全5条件がsolver status 0。新規研究や結果の厳密再現を主張するものではない。

```sh
mkdir -p work
.venv/bin/python experiments/gapfree_degree_minimax_exchange.py > work/setup-degree-minimax.json
```

出力にPython・NumPy・SciPyの版、設定、seedなし（決定的計算）が含まれる。結果は無視対象の `work/` に保存。既存の `results/` は変更していない。

## 未実施事項・次回

現checkoutの既存コードに不要な量子回路SDK、Lean、LaTeXは導入していない。次回は上記ディレクトリで仮想環境を有効化し、依頼された作業に進む。新しい研究方針はAGENTS.md末尾とPROJECT_STATE.mdを確認する。Gitへのcommit・pushは行っていない。
