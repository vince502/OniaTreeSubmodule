# Upsilon OO track-correction models

The Upsilon OO analyzer does not run a neural network. Its analysis-specific
models are binned `TH3F` lookup tables used to weight tracks in the per-dimuon
second-harmonic Q vector.

## Model variants

| Variant | Used by | Correction file |
|---|---|---|
| Hijing minimum-bias | 2025 OO data config | `Eff_OO_2025_Hijing_MB_Centrality_fromHihfpf_NoPU_3D_Nominal_Official.root` |
| Pythia+Hijing QCD, pThat15 | Y(1S), Y(2S), and Y(3S) MC configs | `Eff_OO_2025_PythiaHijing_QCD_pThat15_Centrality_fromHihfpf_NoPU_3D_Nominal_Official.root` |

The three Upsilon MC samples use the same model. They differ by generated
resonance sample, not by correction architecture.

## Inputs and architecture

Both variants have the same architecture: four independent 3D histogram
lookups, with no interpolation or trainable inference layer.

| Input | Code value | Histogram axis |
|---|---|---|
| Track pseudorapidity | `track->eta()` | 14 bins over `[-3, 3]` |
| Track transverse momentum | `track->pt()` | 50 bins over `[0, 500]` GeV |
| Occupancy | `twoParticleFlowQVecOccupancy` | 10 bins over `[0, 200]` |

The current OO data and MC configs set occupancy to the fixed value `100.0`;
it is not presently read from the event.

The four lookup outputs are tracking efficiency (`hEff_3D`), fake fraction
(`hFak_3D`), secondary fraction (`hSec_3D`), and multiple-reconstruction
fraction (`hMul_3D`). Their combined per-track weight is

```text
w = (1 - fake) (1 - secondary) / [efficiency (1 + multiple)]
```

The analyzer then stores, for every reconstructed dimuon,

```text
Q2x = sum(w cos(2 phi)),  Q2y = sum(w sin(2 phi)),  sumW = sum(w)
```

Tracks entering this calculation are charged, high-purity, compatible with the
reference vertex, distinct from both dimuon daughters, and satisfy
`0.4 < pT <= 3.0 GeV` and `|eta| <= 2.4`.

## Implementation references

- Defaults: `HiAnalysis/HiOnia/python/hioniaanalyzer_cfi.py`
- Lookup and weighting: `HiAnalysis/HiOnia/plugins/HiOniaAnalyzer.cc`
- Data selection: `HiAnalysis/HiOnia/test/hioniaanalyzer_Data_MINIAOD_OO_cfg.py`
- MC selections: `HiAnalysis/HiOnia/test/hioniaanalyzer_MC_MINIAOD_OO_cfg_Y{1,2,3}S.py`

`Reco_mu_softMvaRun3Value` is only copied from the input `pat::Muon`; the
HiOnia analyzer neither defines nor evaluates that upstream CMSSW muon-ID
model.
