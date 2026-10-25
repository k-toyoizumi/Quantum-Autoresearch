# 2026-10-25_1_publication-go-no-go
更新日：2026-10-25（日本時間）／Luna medium。追加予算・外部公開なし。研究方向変更は未確定。

## 結論
**論文化判断は保留、最新GSEE estimatorとの接続調査のみGO。** 次手をdegree-20候補の連続certificate・回路化から、実推定器への適合と出版可能性評価へ変更する。degree-20はmemo11のdense-grid candidateであり、連続bias/positivity、QSVT実装、compiled depth、GSEE advantageは未証明。gap-free filtered-mean biasは実推定器に現れない可能性があるが、normalized finite-time ITE expectationをGSEE proxyに使う先行法もあり、strawmanとは断定しない。

## 最新・近接一次資料
| 資料・確認範囲 | 内容と本候補への含意 |
|---|---|
| Dutkiewicz et al., *Accurate ground state energy estimation with noise and imperfect state preparation*, [arXiv:2603.21873v2](https://arxiv.org/abs/2603.21873), §IV | known target promise/gap下のmoment-projection estimatorでbias/variance/depth/noiseを評価、filter幅とdepth/noiseを共同最適化。強baseline。 |
| Zhang et al., *Quantum Imaginary-Time Evolution with Polynomial Resources in Evolution Time*, [arXiv:2507.00908v4](https://arxiv.org/html/2507.00908v4), §2.3, §3.1, Lemma 5, Alg. 1 | normalized finite-τ ⟨H⟩をGSEE proxyとし、overlap γ/lower bound Bからtime・ratio測定でenergy推定。本文の費用は準備/測定 γ⁻²τ query/copies、depth O(τ); lower-bound取得費の適応設計も扱う。mean relevanceはあるが指数tilt/normalization/costが既出。 |
| Kanasugi et al., *Enabling Chemically Accurate Quantum Phase Estimation in the Early Fault-Tolerant Regime*, [arXiv:2603.22778v2](https://arxiv.org/abs/2603.22778), §VI | early-FT chemistry QPEの資源評価。state preparation/overlap、LCU、physical cost・architectureを未解決に挙げる。 |
| Khinevich & Mizukami, *Symmetry-Adapted State Preparation for Quantum Chemistry on Fault-Tolerant Quantum Computers*, [arXiv:2601.08533v1](https://arxiv.org/abs/2601.08533), §§IV.6–IV.7,V | 化学QPE symmetry projection、例のsuccess約.46→.94、filter/LCU/GQSP/GQSVT費用を扱う強baseline。 |
| Bothe et al., [arXiv:2610.08667](https://arxiv.org/abs/2610.08667) (2026-10-06), abstractのみ | Hubbard低エネルギー抽出のLindblad transition filtering、unit-time evolutionに7.7e8 T gates。実用上の隣接例だがstate-weight/mean filterとは異なる。本文未取得。 |
| Lee et al., *Filtered Quantum Phase Estimation*, [arXiv:2510.04294v2](https://arxiv.org/html/2510.04294v2), memo11 §§IV–V; Filip & Fitzpatrick, wall-Cheb [arXiv:2508.00533v3](https://arxiv.org/abs/2508.00533), memo11 §§II,IV–V | known-center/general-basis minimaxとcoarse-prior projector success tradeoff。幅広いfilter designの新規性は危険。unknown-bracket all-target mean lossとの同一性は未確認。 |

著者の記述と含意（推論）を分けた限定screen。網羅的surveyではない。

## 維持・修正・転換
1. **維持**：実GSEE estimatorのrisk/costを改善できる時だけmean-biasを中心に残す。estimand接続と同一oracle/depth/error/confidence/success/overlap条件の費用改善が必要。
2. **修正（次の調査として推奨）**：finite-ITE/moment-projection等が置くpromiseの一つだけを緩和し、prior取得費込みでjoint filter-estimator costを比較する。一般query-optimality（[2608.24494](https://arxiv.org/abs/2608.24494), [2608.24493](https://arxiv.org/abs/2608.24493)）は主張しない。新テーマとして未確定。
3. **転換（保留）**：化学state-preparation/overlapまたはsymmetry/transition-filterのend-to-end物理費用。実用動機はあるが具体failure caseと既存法との差が不足。

条件付き貢献文案：維持「未知target bracket・gap-free下で浅いGSEEのfiltered-mean bias/成功率を制御する設計と費用境界」；修正「finite-ITE等のpromiseを一つ緩和しprior費込みjoint設計を等価depth/error/confidenceで比較」；転換「化学低エネルギー抽出でstate preparation/overlapまたはsymmetry projection込みのfilter+QPE資源を最適化」。各案で同条件改善と具体系が必要。

## Go/no-go
有限ITE/moment-projectionのestimand、promise、bias/variance、overlap・normalization・query/depth式を並べmean-biasとの対応を確認する。未知prior/overlapにはhidden tiny ground overlapを含むunconditional certificateを仮定せず、情報取得費とoracle-known baselineを明記する。gap-free envelope/代替filterがITEの同条件費用改善または非自明限界を示せなければ現題目をparkし、degree-20 proof/circuit化も再評価する。判断は「最新研究の追加調査のみGO」。関数設計中心の方針は変更せず、B等を新テーマに確定しない。連続certificate、QSVT位相合成、回路実行、Leanは未実施。
