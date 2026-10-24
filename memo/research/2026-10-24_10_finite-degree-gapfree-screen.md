# 2026-10-24_10_finite-degree-gapfree-screen

更新日：2026-10-24（日本時間）  
作業モデル：Luna、medium。研究方針・仮説採否は本人認可に基づき委任。追加予算・外部公開なし。

## 結果

memo9の任意スカラーweight optimumを、次数制約付き候補へ接続する小screenを行った。固定条件は gap-free、真の \(E_0\in[L,U]=[-.05,.05]\)、support \([E_0,E_{max}=1]\)、初期ground weight \(p_0\ge\eta=.1\)、同じprior-only filterで全instanceの受理後filtered-mean biasを \(b=.01\) 以下にすること。二準位入力から必要十分条件は全 \(E_0\in[L,U]\)、\(d>b\) に対して
\[
  w(E_0+d)/w(E_0)\le A/(d-b),\quad w=|p|^2,\quad A=b\eta/(1-\eta).
\]
memo9の制約なしscalar上限は \(e^{-F(W)}=1/59049\simeq1.6935\cdot10^{-5}\)、ただし次数・LCU norm・回路費は含まない。

得られた境界は、(a)代数多項式振幅はこの例で次数2以下が厳密に不可能、(b)shifted-power多項式の次数58は連続bias条件の十分条件を満たす、である。次数3〜57の実行可能性は未解決。screenした次数2/4/6のCTE候補は全てgrid上でbias目標を外した。新しいフィルタ族、優位性、新規性は確認していない。

## 有限差分の必要次数gate（手証明）

次数 \(n\) の代数多項式 \(p\) に対し \(w=|p|^2\) は実エネルギー上の実多項式、次数高々 \(2n\)。\(N=2n+1\)、\(\Delta=W/N\)、\(\rho=A/(\Delta-b)\) とし \(\Delta>b\) とする。各 \(k=0,\ldots,N-1\) で別々の許容instanceのgroundを \(E_k=L+k\Delta\) と置けば、bias条件から \(w(E_{k+1})\le\rho w(E_k)\)、ゆえに \(w(E_k)\le \rho^k w(E_0)\)。次数 \(2n<N\) の \(w\) のN階有限差分はゼロなので、奇数kの二項和と偶数kの二項和は等しい。偶数側は \(w(E_0)>0\) 以上、奇数側は \(w(E_0)O_N(\rho)\) 以下。ただし
\[
 O_N(\rho)=\sum_{k\text{ odd}}\binom Nk\rho^k=
 ((1+\rho)^N-(1-\rho)^N)/2.
\]
よって \(O_N(\rho)<1\) は矛盾。この証明は有限点だけを使うため連続条件に適用するが、gridの実行可能探索とは異なる。Lean未検証。trigonometric polynomialには適用しない。

| amplitude degree上限 n | N | \(\Delta\) | \(\rho\) | exact \(O_N\) | 判定 |
|---:|---:|---:|---:|---:|---|
| 1 | 3 | 1/30 | 1/21 | 0.142965… | 次数1以下を排除 |
| 2 | 5 | 1/50 | 1/9 | 0.569290… | 次数2以下を排除 |
| 3 | 7 | 1/70 | 7/30 | 2.449408… | このgateでは判定不能 |

次数0も同じ論法で排除される。これは代数多項式全体に対する必要条件であり、次数3以上が可能だという意味ではない。導出はcriticとレビュー済み。

## 有限次数候補screenと上界

CTE cosine候補は \(x=(E-L)/(E_{max}-L)\in[0,1]\)、\(p(x)=a_0+\sum_{k=1}^K a_k\cos(k\pi x)\)。各cos modeを\(\pm k\pi/(E_{max}-L)\) time-evolution pairとして扱い、係数 \(L_1=|a_0|+\sum|a_k|\) で除したので全域 \(|p|\le1\)、成功weightは正規化後の \(|p|^2\)。max Fourier timeは \(K\pi/(E_{max}-L)\)。出力のbiasはE0 bracket 101点、各targetのexcitation 501点でのgridded proxy。連続bias証明なし。

| CTE候補（振幅次数K） | 正規化後 bracket transmission proxy（K=2/4/6） | 最大bias proxy（K=2/4/6） |
|---|---|---|
| cosine-power \(\cos^{2K}(\pi x/2)\) | .9141 / .8355 / .7637 | .26493 / .19024 / .15614 |
| prior-only Gaussian amplitudeのFourier truncation | .8340 / .5362 / .2516 | .27993 / .14879 / .13662 |
| ideal \(e^{-F(x)/2}\) amplitudeのFourier truncation | .8336 / .5332 / .2433 | .28242 / .15494 / .15240 |

Gaussian幅は端点振幅が \(e^{-F(W)/2}\) となるprior-only選択。級数係数はsupport上の6000区間台形積分。係数L1正規化により \(|p|\le1\) は保証するが、truncationは次数別minimaxではなくscreen用projection。候補すべて目標 .01 をgrid上で超過した。 grid値は連続最大値ではない。

解析的多項式baselineは
\[
p_n(E)=\left(1-\frac{E-L}{S}\right)^n,\qquad S=E_{max}-L=1.05.
\]
全supportで \(0\le p_n\le1\)。\(r e^r=(1-\eta)/(e\eta)\) の正根 \(r\approx1.101003<1.102\) に対し、\(n\ge\lceil Sr/(2b)\rceil=58\) は比条件の連続十分条件。n=58 raw bracket-end transmissionは \((1-W/S)^{116}=9.0778\cdot10^{-6}\)、scalar上限の約0.536倍。LCU normalization・実回路成功費は含めない。n=57は十分条件未達に過ぎず、不可能ではない。grid最大biasはn=57で.0100471、n=58で.0098759。57のgrid超過はその候補上の数値screenで、次数57全体の不可能性証明ではない。

shifted-powerは既知のpower/imaginary-time型基準で、新方式としない。degreeは応答次数である。Fourier時間queryとblock-encoding/QSVT polynomial queryを物理回路深さへ同一視していない。混合parityのphase列合成、even/odd分解、ancilla・branching・compiled depth、追加LCU費用は未評価。QSVT circuitを実装したとは言わない。

## 既存法との差と新規性リスク

- Lee et al., *Filtered Quantum Phase Estimation*, [arXiv:2510.04294v2](https://arxiv.org/html/2510.04294v2)：本文§IV.1–IV.3（filter rejection ratio、low/bandpass、minimax/spectral concentration）、補遺§V.1–V.4（一般basis、polynomial/trigonometric minimaxとshifted center）、§VI（Gaussian finite Fourier expansion）、§VIII（粗い事前推定後の二段法）を確認。有限次数filter designとsuccess/cost tradeoffは強く既出。今回のunknown-target bracket全体に対するgap-free mean-bias lossと有限差分次数gateが既存minimaxの単なる再定式化を越えるかは未確認。強いgeneral-basis minimaxは未実装。
- Filip & Fitzpatrick, *Beyond asymptotic reasoning: the practicalities of a quantum ground state projector based on the wall-Chebyshev expansion*, [arXiv:2508.00533v3](https://arxiv.org/html/2508.00533v3)：Abstract、§§I–II, IV–Vを確認。粗い上側energy boundに頑健な多項式projector、success probability、serial oracle、LCU/QSVT実装を比較する。目的はprojector/fidelityであり、今回のfiltered mean lossと数値を同一視しない。
- Lin & Tong, *Heisenberg-limited ground-state energy estimation for early fault-tolerant quantum computers*, [arXiv:2102.11340v2](https://arxiv.org/abs/2102.11340v2)：§§1–5, Apps. D–Eはmemo2の一次資料読了範囲。CTE/Hadamard dataからのCDF系GSEEがfilter-free shallow baseline。今回screenは下流energy estimateを評価せず、一般GSEE優位を示さない。

これは少数資料を使った新規性screenで、網羅的surveyでも新規性確認でもない。degree-constrained robust weighted minimax自体がFQPEに含まれる可能性があり、新規成果として主張しない。

## 再現性・次の確認

[script](../../experiments/finite_degree_gapfree_filters.py)・[JSON](../../results/finite_degree_gapfree_filters.json)。Python標準ライブラリのみ、乱数なし。固定パラメータ、grid点、次数、6000分割積分をコードに記録。再実行出力は保存JSONとbyte一致、`py_compile`成功。実行：

```sh
python experiments/finite_degree_gapfree_filters.py > results/finite_degree_gapfree_filters.json
python -m py_compile experiments/finite_degree_gapfree_filters.py
```

結論は必要次数下界2と十分上界58の隙間、低次数screen不成立までで、最小次数を解いていない。次はFQPE general-basis minimaxがunknown-bracketのmean-bias lossに包含されるか、wall-Chebの粗い上界priorと何が違うかを限定的に確認する。その差が残らなければ本問いは棄却する。量子回路、phase synthesis、Lean、化学系、物理depth比較はいずれも未実施。
