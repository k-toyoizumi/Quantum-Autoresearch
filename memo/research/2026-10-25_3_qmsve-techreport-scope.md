# 2026-10-25_3_qmsve-techreport-scope
更新日：2026-10-25（日本時間）。Luna medium。今回、新しい証明・数値実験・文献探索なし。

## 判断
本人の最終判断により、新規filter/GSEE案の新規性探索をNO-GOで終了。次は本人の既存原案から論文形式の内部技術報告を準備する。採択水準の新規性・外部投稿・公開を目的としない。報告本文はまだ書いていない。

## 確認した原案・既存資産
- 主原案はLibraryの2023_0311_QMSVE.pdf、19ページ。新しい同名コピーは /Quantum/ 配下、218,826 bytes、2026-10-23 11:33Z、library_file_id libfile_f07c79980f9c8191b6e14267373554a8。旧同名コピーは同サイズで11:15Zのため新しい方を選択。PDF text readは非抽出だったがローカルpdftotextで概要・方法・結論を確認した。
- 題名は「量子最大・最小特異値推定アルゴリズム」。概要/§3は量子べき乗法による最大SV、§4は逆反復法に基づく最小SV、§5はcosをQSVTで実装し最小SVをcos演算子の最大SVへ写す「三角反復法」。§5の原題に「仮」とあり、誤差/複雑度式や「条件数依存を改善する」主張は再検証前の原案として扱う。
- QCG-paper main.tex, commit 5b04b302bc3e1d41f9ac933c837ab84f4c5b7164の題名は “Quantum Conjugate Gradient Method using Quantum Singular Value Transformation”。章立てはQSVT、positive-side QSVT、QCG提案法、数値結果。QMSVEの三角反復とは別成果。
- QSVT-based_QCG commit 04e8c2aec8e3c5c4a06c6d8a92d3b515cea47555のcoefs.py/phases.py/qsvt.py/gates.py/qCG.py/utils.pyと、master-thesis commit 6190fc34c4f85a5436a92f1bb242d9fa2cdda00のchapter1-4は入口・章題を確認。修論はQSVT/Hamiltonian simulation/QCG、コードはQCG実装であり、QMSVEの実装とは確認していない。依存・実行再現は未実施。

## 一本の報告ストーリー
問題と入力モデル → QSVTによる多項式/cos変換 → 最大SVの量子べき乗法 → 逆反復との比較 → cos/QSVT三角反復による最小SV → 誤差・成功率・query/depth会計 → 限界と条件付き応用候補。
最大SVを対照として、最小SV推定を主な説明軸にする。一般行列のA†A拡張、block encoding正規化、初期重なりと第2特異値/gapが費用にどう入るかを一貫して書く。多項式次数、oracle query、総shot/再試行、物理回路depthを混同しない。化学系への応用は、Hamiltonianのshift・scale・oracle準備費を示せる場合に限る。これを新しいGSEE algorithm/優位性と呼ばない。

## 採用・除外
- 採用：QMSVE原案の量子最大/最小SV推定、量子べき乗法、cos/QSVT三角反復を中心とする内部技術報告。
- 別成果として参照：QCG論文・コード。QMSVEへの既存実装や新規寄与に流用しない。
- 本文に必須でない：最近のscalar mean-envelope、zero-DC/nuisance screen、次数20 grid candidate。必要時のみ研究経緯として別枠にし、報告の中心にしない。
- 断定しない：新しいGSEE/QSVT algorithm、無条件にcondition-number-free、QSVT実装済み、連続保証済み、quantum advantage、外部投稿可能。

## 次段の最小確認（今回は計画のみ）
1. block-encoding scale、特異値の正規化区間、cosの単調区間、A†A拡張と二乗効果を確認して対象演算子へ正しく対応づける。
2. 原案の収束式を初期overlap、第2SV/gap、cos近似誤差、読出しprecision、成功確率・再試行に照合する。condition-number claimを有効なgap/overlap/query/depth仮定に限定する。
3. 必要なら2×2または小矩形行列の正確な特異値とcos反復を通常Pythonで比較する。今回この実験は未実行。図・大規模環境構築は不要。

新規性探索は終了し、技術報告のための上記確認以外の新algorithm探索、全規模化学実験、simulator環境構築はしない。有料資源・外部公開なし。Astra/Sol high以上の事前承認制を維持する。
