# 段階1メモ：QSVTツールチェーン候補の比較

更新日：2026-10-24（日本時間）

## サマリー

旧資産の角度合成は PyQSP の `Wx` 規約と偶奇係数配列を前提にし、返却位相を手作業で反射型へ変換している。現在の PyQSP 主APIは Chebyshev 基底の係数を受けるため、旧 `coefs.py` は `numpy.polynomial.Polynomial` とpower-basis Horner評価を使い、係数配列を昇次の単項式基底として扱う。同じ配列を現在のChebyshev基底APIへ渡すだけでは互換性がない。PennyLane は通常 QSVT の角度合成・規約変換・projector-phase 回路を同じAPIにまとめる有力な簡潔案だが、旧Qiskit回路や固有のブロック符号化を自動的に置き換えるものではない。

暫定案は、標準的な実数・確定パリティ多項式について PennyLane の `poly_to_angles(..., "QSVT", angle_solver="iterative")` を高次数候補として比較し、手元の既存Qiskit回路は Aer で行列・ゲート深さを確認できる比較基準として維持すること。対称QSPなら現行 PyQSP の `sym_qsp` と QSPPACK Python の Newton/direct NLFT も同じ多項式で比較候補にする。精度・速度・深さの実測はしておらず、採用は暫定である。

## 過去コードの実APIと規約

対象は `QSVT-based_QCG` commit `04e8c2aec8e3c5c4a06c6d8a92d3b515cea47555` の `phases.py`（blob `7c7eaff7f72ac95b4d5d7c52328d88c21ff4f0a4`）、`qsvt.py`（`650457a6e8fe363425b92835747a1b24f8088a52`）、`gates.py`（`5a2b2317661c20a20150de85086555ce3fb3a434`）。

- `calculate_polynomial_phases(even_coefs, odd_coefs, C_max, qsp_eps, qsp_tol, method)` は偶・奇係数を `C_max` で正規化し、それぞれ PyQSP `QuantumSignalProcessingPhases(..., signal_operator="Wx", method=method, eps=qsp_eps, suc=1-qsp_eps, tolerance=qsp_tol)` に渡す。その後、Wx位相を反射型の位相へ手動変換している。
- このAPIから係数が単項式基底かChebyshev基底かを自明には判定できない。新旧比較前に係数生成側 `coefs.py` と論文の多項式定義を照合し、必要なら power→Chebyshev 変換を明示する。
- `qsvt.py` はQiskit回路でQCG/Poisson向けの独自 `U` と `U†`、制御版、アンシラ反射、`S_2/S_3`、OAA、偶多項式ゲートを組み、cos/sin位相をCSVから読む構成である。汎用のQSVT層とは分けて扱う。
- `gates.py` はQCG/Poisson向けの可変回転・加減算・ブロック符号化・状態準備ゲートを含む。ここが再利用できるかは対象ハミルトニアンと入力oracle次第。

## 候補比較

| 機能・候補 | 規約・入力モデル | 長所 | 制約・注意 | 移行負担 | 暫定推薦 |
| --- | --- | --- | --- | --- | --- |
| 角度合成：現行 PyQSP `laurent` | 主API `QuantumSignalProcessingPhases` は昇順Chebyshev係数。QSPの信号演算子 Wx/Wzで位相列・出力振幅の約束が異なる | 旧資産と同系統で、既存呼出・係数検証を保ちやすい。標準Laurent分解を比較基準にできる | 旧版の単項式配列とは直結しない。Chebyshev変換と旧手動規約変換を検証する必要。アルゴリズム指定を既存コードと照合する | 低〜中 | 互換性基準として残す |
| 角度合成：現行 PyQSP `sym_qsp` | 対称QSPの制約付き位相列・実数多項式を対象。PyQSPは `(full_phi, reduced_phi, parity)` を返し、出力量の約束も通常QSPと異なる | 対称位相列に限定できる条件では、対称解を直接求める専用経路。現行PyQSP README/PyPIでDongらの反復法を案内 | 任意のQSVT位相列のdrop-inではない。出力成分・パリティ条件、実装の収束を同じ対象多項式で検証する | 中 | 多項式が対称QSP条件を満たす時のみ比較 |
| 角度合成：PennyLane `poly_to_angles` | `routine="QSP"/"QSVT"/"GQSP"`を選択。係数は低次から高次、QSP/QSVTは実係数かつ偶数次または奇数次。solvers: `root-finding`, `iterative`, `iterative-optax`。公式文書は iterative を次数およそ1000超のQSP/QSVTに有効、Optax版を同次数で係数を繰り返し変える用途に推奨 | 通常QSVTまで一つのAPIで完結。角度solverの規約変換API `transform_angles` と組み合わせられる。回路作成と角度計算の接続が簡潔 | bounded polynomial等の前提を満たす必要。角度計算はJIT非対応と文書記載。PennyLane係数順・角度順を旧PyQSP CSVと照合する必要 | 中〜高（Qiskit旧回路から移す場合） | 標準QSVTの最小実装候補。高次数は iterative を第一比較 |
| 角度合成：QSPPACK / Python `qsppack` | MATLAB QSPPACKは対称QSP等の位相探索を含む。Python port 0.4.0はChebyshev操作、L-BFGS/FPI/Newton/direct NLFT | Newtonやdirect NLFTなど複数手法を横比較でき、対称QSPの一次論文と実装の結び付きが明確 | Python port はPyPI 0.4.0・Alpha表記、依存が増え、旧APIと非互換。PyPIにprovenance表示を確認できず、現段階で安定性・数値優位の断定不可 | 中 | 対称QSPの追加比較候補。基準ソルバーにはしない |
| シミュレータ：Qiskit Aer | 既存Qiskit回路を実行。AerSimulatorのstatevector/density_matrix/unitary等。transpile後の回路構成・ゲート数・depthもQiskit側で確認可能 | 既存 `qsvt.py` の最小改修で、理想行列・回路深さ・各ゲート数を監査できる | unitary行列は小規模向けで、測定/リセットを含められない。物理ノイズ・方式の選択は別問題。Aerの回路depthはoracle分解とbasis gate設定に依存 | 低 | 旧コードの回路コスト・正しさ基準として継続 |
| シミュレータ：PennyLane Lightning.qubit | PennyLane QNode/deviceに載る状態ベクトル型シミュレータ | PennyLane QSVT回路と自然に接続し、CPU並列等のLightning機能を利用できる | Qiskit回路を移植/変換する負担。statevector規模はメモリが指数増加。Aerとの同一条件比較が必要 | 中〜高 | PennyLane案を採る場合の第一候補 |
| シミュレータ：Qulacs / PennyLane-Qulacs | Qulacs Python/C++回路シミュレータ。PennyLane plugin経由の選択肢もある | 既存Qiskitとは別系統の速度比較候補。CPU並列/GPU構成の選択肢 | API・ゲート対応・pluginバージョンを追加検証。今回のQSVTに特化した優位性は未確認 | 中 | 必要な規模でLightning/Aerが律速と分かった後の比較候補 |
| 回路：PennyLane `qml.QSVT` | ユーザー提供block-encoding Operator `UA` と projector-controlled phase-shift Operator列（例：`PCPhase`）を交互に展開して特異値変換を表現。PennyLane `qml.qsvt(A, poly, encoding_wires, block_encoding=...)` は角度合成も呼び出し、HamiltonianのPrepSelPrep/Qubitization、または行列のBlockEncode/FABLEを組む高水準入口 | projector-phase と位相列を短く記述でき、角度生成との接続も容易。独自block encodingを差し込む低水準層と、高水準行列入口を区別できる | `qml.qsvt` の自動block encodingがQCGのoracle/OAAと同じとは限らない。state prep・正規化・controlled query・ancillaコストを別に数える | 中〜高 | 手元oracleを保持しつつQSVT層のみ置換する比較案 |
| 回路：QETU | 既知のHamiltonian evolution (e^{-iHt}) を入力とし、固有位相に対する多項式変換を行うモデル | Hamiltonian simulation accessが自然にある場合はフィルタを直接設計しやすい | block-encoding QSVTの信号演算子・入力コストと異なる。evolution実装、時間、controlled/uncontrolled queryの費用を揃えないと比較不能 | 高（入力モデル変更時） | 研究の入力oracleがtime-evolutionなら別ベースラインとして比較 |
| 回路：GQSP | PennyLane routineは一般ユニタリ (U) の多項式変換を表す一般化モデル | 標準QSPのparity制約外を扱えるケースがある | 標準block-encoding QSVTの置換ではない。ユニタリ入力と追加の制御・正規化・位相条件が変わる | 高 | parity制約が障害と確認された場合のみ検討 |

## PennyLane回路APIの自動化範囲（2026-10-24追補）\n\nPennyLaneはQSVT回路を実際に生成する。`qml.qsvt(A, poly, encoding_wires, block_encoding=...)` は多項式から位相角を計算し、対応する既定block encodingを構築して高水準のQSVT operatorを返す。HamiltonianではPrepSelPrep/Qubitization、行列ではBlockEncode/FABLEが候補。ただし行列向けBlockEncodeは公式文書上hardware compatibleではなく、FABLEには規模・正規化条件と合成コストがあるため、この高水準APIだけで大規模回路の深さや効率は保証されない。\n\n低水準 `qml.QSVT(UA, projectors)` はユーザー提供のblock-encoding `Operator` とprojector-controlled phase-shift Operator列（例えば `PCPhase`）を受け取り、交互積を回路へ展開する。既存QCG oracleを包んで試す候補はこちら。角度列の生成は別途 `poly_to_angles` 等で行い、PCPhase/projector、角度の符号・順序、入力block encodingとの対応を検証する必要がある。従ってライブラリはQSVTの交互回路を生成するが、独自oracle設計・状態準備・正規化・成功確率・oraclesのgate-costまで自動で置き換えるわけではない。\n\n照合受入条件は、同一多項式・基底変換・正規化係数・oracle・位相順序/符号を固定して、(a) top-left encoded blockまたは固有値上のフィルタ応答、(b) 出力状態をglobal phaseを除いて比較、(c) ancilla postselection成功確率を比べる。full-unitaryも比較するときはglobal phaseを除去してから評価する。回路depth比較はbackend、basis gate、connectivity、transpile/decomposition/optimization条件を固定する。旧環境を再現する検査と現行Qiskitへ移植する検査は別に記録する。\n\n## 段階1での提案

1. 角度合成の正準入力を「正規化済みChebyshev係数、次数、偶奇、目標誤差」として明示し、旧 `coefs.py` 出力との変換を残す。通常QSVTでは PennyLane root-finding（中低次数）と iterative（次数およそ1000超）を同じ多項式で検証し、PyQSP `laurent` を互換基準として置く。
2. 対称位相列に理論上制約できるフィルタのみ PyQSP `sym_qsp` と QSPPACK Newton/direct NLFTを試す。位相列の短さ・最適性を一般QSVT全体の改善と見なさない。
3. 回路は既存Qiskit block encodingを固定し、まずAerで行列要素・シミュレーション・transpile後のdepth/ゲート数を記録する。簡潔な回路表現が必要ならPennyLane `qml.QSVT` に同じ (U) とprojectorsを渡す移植を比較し、block encoding/状態準備/反射を含む全コストを別途数える。
4. 全手法で、係数誤差・位相規約・パリティ・成功確率・oracle呼出数を分けて記録する。多項式次数を回路深さと同一視しない。QETU/GQSPは入力モデルと実現対象が違うため、単純に回路だけ差し替えない。

## 再利用候補・修正・未確認

**再利用候補**：旧 `gates.py` のブロック符号化ゲート・状態準備、`qsvt.py` のoracleとその逆回路、AerによるQiskit回路検査。対象系の入力モデルに合う範囲で再利用する。

**修正が必要**：power basisとChebyshev basisの変換を特定し、旧PyQSP Wx→reflectionの手計算変換を既知低次数例で照合する。角度CSVにbasis・parity・solver・規約・正規化係数を記録する。現行Qiskit実行APIへの更新は依存一覧とコードを突き合わせてから行う。移行の必然性は未確認。

**未確認**：各solverの実行速度・安定性・誤差、現行PyQSP/PennyLane/QSPPACK portの同一フィルタでの性能、Aer/Lightning/Qulacs間の速度、QSVT circuit depthの実分解、旧Qiskit環境の再現可否。今回、実装・依存追加・数値実験は行っていない。

## 出典と読んだ範囲

### 旧資産
- [QSVT-based_QCG/phases.py](https://github.com/k-toyoizumi/QSVT-based_QCG/blob/04e8c2aec8e3c5c4a06c6d8a92d3b515cea47555/phases.py) — 全体を確認。API引数、Wx規約変換、係数入力の流れ。
- [QSVT-based_QCG/qsvt.py](https://github.com/k-toyoizumi/QSVT-based_QCG/blob/04e8c2aec8e3c5c4a06c6d8a92d3b515cea47555/qsvt.py) — 全体を確認。Qiskit回路とQCG/OAA固有構成。
- [QSVT-based_QCG/gates.py](https://github.com/k-toyoizumi/QSVT-based_QCG/blob/04e8c2aec8e3c5c4a06c6d8a92d3b515cea47555/gates.py) — 全体を確認。ブロック符号化・状態準備・演算ゲート。

### 角度合成・回路API
- [PyQSP公式README](https://github.com/ichuang/pyqsp) と [PyPI API・使用説明](https://pypi.org/project/pyqsp/) — README、APIの係数basis、Wx/Wz規約、`laurent`/`sym_qsp`説明を確認。PyPIはChebyshev基底を主とするAPI、`sym_qsp`の返却値・意味も記載。
- [PennyLane 0.45.1 `poly_to_angles`](https://docs.pennylane.ai/en/stable/code/api/pennylane.poly_to_angles.html) — solver options、係数順序、次数目安、parity/real係数条件を確認。
- [PennyLane 0.45.1 `transform_angles`](https://docs.pennylane.ai/en/stable/code/api/pennylane.transform_angles.html) — QSP/QSVT規約の変換APIを確認。
- [PennyLane 0.45.1 `qml.QSVT`](https://docs.pennylane.ai/en/stable/code/api/pennylane.QSVT.html) と [`qml.qsvt`](https://docs.pennylane.ai/en/stable/code/api/pennylane.qsvt.html) — projector-phase回路と高水準block encoding API、JIT制約を確認。
- [PennyLane official releases](https://github.com/PennyLaneAI/pennylane/releases) — 安定版 v0.45.1 を確認。v0.46.0 Beta 1はpre-releaseのため推薦根拠にしない。
- [QSPPACK MATLAB toolbox](https://github.com/qsppack/QSPPACK) — READMEのsolver・導入説明、examples/docsの用途を確認。
- [Python `qsppack`](https://github.com/qsppack/pyqsppack) と [PyPI 0.4.0](https://pypi.org/project/qsppack/) — READMEとpyproject metadata、公開版のAlpha状態・依存・リリース情報を確認。
- Dong, Lin, Ni, Wang, [“Robust iterative method for symmetric quantum signal processing in all parameter regimes,” arXiv:2307.12468](https://arxiv.org/abs/2307.12468) — title/abstractと手法範囲を確認。PennyLane版との数値比較結果ではない。
- Dong et al., [“Efficient phase-factor evaluation in quantum signal processing,” arXiv:2002.11649](https://arxiv.org/abs/2002.11649) — abstract/公開要旨を確認。大次数・高精度数値は論文の報告であり、本調査の再現結果ではない。
- [PennyLane release notes](https://docs.pennylane.ai/en/stable/development/release_notes.html) — 0.40のpoly_to_angles/QSVT/GQSP追加、0.42の高次数iterative solver追加、0.45.1のiterative-optax説明を確認。

### シミュレータ・他の信号処理モデル
- [Qiskit AerSimulator docs](https://qiskit.github.io/qiskit-aer/stubs/qiskit_aer.AerSimulator.html) — simulator methodsと制約を確認。公式GitHub releasesではv0.17.2が最新のstableとして表示。docs v0.18.0ページは参照したがstable releaseとは扱っていない。
- [PennyLane Lightning docs](https://docs.pennylane.ai/projects/lightning/en/stable/) — lightning.qubitの役割と実行方式を確認。
- [Qulacs公式site/docs](https://docs.qulacs.org/en/latest/) と [Qulacs releases](https://github.com/qulacs/qulacs/releases) — Python/C++ simulatorの説明とv0.6.13 releaseを確認。
- Dong et al., [“Quantum eigenvalue processing,” arXiv:2204.05955](https://arxiv.org/abs/2204.05955) — abstractとalgorithm/input model説明を確認。Hamiltonian evolutionを使うQETUとして扱い、block-encoding QSVTと同一視していない。
- Motlagh & Wiebe, [“Generalized quantum signal processing,” arXiv:2308.01501](https://arxiv.org/abs/2308.01501) — abstractを確認。一般ユニタリ入力の一般化を、標準QSVTと区別する根拠として参照。
- [PennyLane GQSP API](https://docs.pennylane.ai/en/stable/code/api/pennylane.GQSP.html) — 一般ユニタリ (U) の多項式変換APIを確認。

## 再開時の次の一手

同一の低次数・高次数Chebyshevフィルタを入力し、PyQSP Laurent、PyQSP sym_qsp（適用条件を満たす場合）、PennyLane root-finding/iterativeの角度列から復元した応答を照合する。既知の少数量子ビットblock encodingをAerで測り、PennyLane QSVT circuitの行列・深さと照合する。比較条件を固定する前に対象系と入力oracleを決める。
