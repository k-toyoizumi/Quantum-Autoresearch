# 段階1残件レビューと段階2への引継ぎ

更新日：2026-10-24（日本時間）
状態：文献・過去資産の静的レビューを完了。旧実行環境の再現・移植は段階3に引き継ぐ。
作業モデル：Luna、medium。サブエージェント不使用。

## サマリー

PennyLaneはQSVT回路を生成する。高水準の `qml.qsvt` は多項式角度合成と対応する標準block encodingをつなぐ。低水準の `qml.QSVT` はcustom block-encoding Operatorとprojector-controlled phase-shift Operator列（PCPhase等）を交互回路へ展開する。旧QCG oracleを維持して比較する場合は低水準APIが適するが、oracle生成・費用・成功率を自動で決めるものではない。

State Preparation BoostersとFQPE robustness補遺を本文まで確認し、旧コードの依存とQiskit APIを静的に確認した。Stage 1の「既存法の仮定・費用・過去資産の再利用候補/条件」の比較資料は揃った。実行確認は段階3で行い、現時点で大規模な環境構築には進まない。

## 過去手法を段階2へ持ち込むときの要点

| 観点 | Booster / FQPEから得た要点 | 深さ制約フィルタへの含意 |
| --- | --- | --- |
| 入力モデル | Booster数値例はcontrolled time evolutionをLCU実装。QET-Uもtime-evolution input。FQPEはpolynomial block encodingまたはtrigonometric implementationを分けて論じる | 同一の深さ表へ並べる前に、available oracle・controlled access・近似精度をそろえる |
| 成功確率 | 非ユニタリfilterの状態準備はprobabilisticであり、Booster/FQPEともpostselection overheadを総費用に含める | overlap増加率だけで有利と判定しない |
| 誤差 | FQPE Note IXではfilterのLipschitz感度、gap依存のeigenspace stability、Krylov Gram matrixのconditioningを別々に扱う | polynomial approximation error以外にHamiltonian/oracle、basis、sampling誤差とgap条件を切り分ける |
| 深さ | Boosterの `T` は最大evolution time proxy、controlled-evolution depthを `D` とすると本文換算は `2TD`。LCU ancilla/成功率も別に必要 | 多項式次数、query-depth、物理回路depth、再試行込み総costを別指標にする |
| 研究仮説 | いずれの資料も今回の特定対象・深さ上限での優位性は示さない | filter族・coarse estimate・基準法・棄却条件は未決のまま段階2で合意する |

## 段階1の完了判定

文献・過去資産を理論検討に渡す段階1の記録は完了としてよい。重点論文の仮定、query/depth/成功確率の比較、過去コードのpath/commit/import、API互換の問題、未確認事項を記録した。特にState Preparation Boostersの正確な実機深さ・成功率やQCGコードの現行実行は未検証だが、これらは次の試行錯誤を明示して段階3へ移す。旧コードの依存version pinsが見つからないため、当時環境を厳密に復元できるかは未確認であり「再現不能」とは断定しない。

## 段階2で合意が必要な判断

1. **入力モデルと対象**：最初に扱う小分子/スピン模型と、利用可能と仮定するoracle（block encoding、controlled time evolution、state preparation）を選ぶ。
2. **評価目標**：最大回路深さ制約、許容成功確率・失敗確率、最終エネルギー精度、およびstate preparationを含む総費用のどれを主指標にするか決める。
3. **検証する仮説**：どのfilter族が、何の条件で、baselineをどの量だけ改善すると予想するかと、仮説を棄却する結果を定める。

これらは未決定であり、本メモでは選択していない。

## 段階3へ引き継ぐ受入条件

PennyLaneと旧環境/移植版の照合では、同じ対象多項式・係数basis・正規化係数・入力oracle・信号/位相規約を使う。応答（encoded blockまたは固有値上の (p(x))）、postselection成功率、出力状態（global phaseを除いて比較）を照合し、必要ならfull unitaryの差もglobal phaseを除いて測る。depth比較時はbackend、basis gate、connectivity、compiler/transpiler/decomposition/optimization条件を固定して記録する。旧版環境再現と現行Qiskitへの移植は別成果として扱う。

現行Qiskitへの静的移行候補は `qiskit.Aer`→`qiskit_aer`、`qiskit.execute`→`transpile`とbackend.run()等。ただし旧依存を復元・実行する前に、存在する依存履歴を確認し、pinがなければ採用した仮想環境とバージョンを明示する。今段階では依存導入や大量実装はしていない。

## 出典と読んだ範囲

- [State Preparation Boosters, arXiv:2202.06978v3](https://arxiv.org/pdf/2202.06978v3) — §§2.1–2.4、3、Appendix D。f(H)の単調性と重み変化、Fourier近似/LCU、postselection、T depth proxy、N₂例と著者が挙げるnoise/cost-benefit未解決事項。
- [Filtered Quantum Phase Estimation, arXiv:2510.04294v2](https://arxiv.org/html/2510.04294v2) — main §II.2とSupplementary Note IX.1–IX.3。expected cost theorem、Lipschitz摂動、Davis–Kahan型projector摂動、Krylov H/S摂動とconditioning。
- [PennyLane qsvt](https://docs.pennylane.ai/en/stable/code/api/pennylane.qsvt.html), [PennyLane QSVT](https://docs.pennylane.ai/en/stable/code/api/pennylane.QSVT.html) — 0.45.1 APIの高/低水準の引数、block encoding選択肢、projector-phase listおよび回路decomposition。
- [IBM Qiskit v1.0 migration guide](https://quantum.cloud.ibm.com/docs/en/guides/qiskit-1.0-features) — Aer/executeの削除と代替案。
- 過去資産は [QSVT-based_QCG commit 04e8c2a](https://github.com/k-toyoizumi/QSVT-based_QCG/tree/04e8c2aec8e3c5c4a06c6d8a92d3b515cea47555) の `qCG.py`, `utils.py`, `coefs.py`, `phases.py`, `qsvt.py`, `gates.py` を静的確認。treeにrequirements/lockfileなし。commit/blobはtoolchain memoに記載。
