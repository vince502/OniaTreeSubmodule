# Detail Track Counting Feature

## Overview
A new feature has been added to `HiOniaAnalyzer` to count tracks in specific |eta| and pT regions at the event level.

## Configuration Parameters

### New Parameters in `hioniaanalyzer_cfi.py`:

```python
useDetailEventInfo = cms.bool(False)  # Enable detailed track counting
ptTrkDetail = cms.vdouble(0.5, 1.0, 2.0)  # pT thresholds in GeV
absEtaTrkDetail = cms.vdouble(1.0, 2.0, 2.4)  # |eta| upper limits
```

## Output Branches

When `useDetailEventInfo = True`, the analyzer creates branches for each combination of eta and pt cuts:

```
Ntrack_abseta<X>_pt<Y>
```

Where:
- `X` corresponds to values in `absEtaTrkDetail`
- `Y` corresponds to values in `ptTrkDetail`

### Example:
With default settings:
- `ptTrkDetail = cms.vdouble(0.5, 1.0, 2.0)`
- `absEtaTrkDetail = cms.vdouble(1.0, 2.0, 2.4)`

The following branches will be created:
```
Ntrack_abseta1p0_pt0p5  # Tracks with |eta| < 1.0 and pt >= 0.5 GeV
Ntrack_abseta1p0_pt1p0  # Tracks with |eta| < 1.0 and pt >= 1.0 GeV
Ntrack_abseta1p0_pt2p0  # Tracks with |eta| < 1.0 and pt >= 2.0 GeV
Ntrack_abseta2p0_pt0p5  # Tracks with |eta| < 2.0 and pt >= 0.5 GeV
Ntrack_abseta2p0_pt1p0  # Tracks with |eta| < 2.0 and pt >= 1.0 GeV
Ntrack_abseta2p0_pt2p0  # Tracks with |eta| < 2.0 and pt >= 2.0 GeV
Ntrack_abseta2p4_pt0p5  # Tracks with |eta| < 2.4 and pt >= 0.5 GeV
Ntrack_abseta2p4_pt1p0  # Tracks with |eta| < 2.4 and pt >= 1.0 GeV
Ntrack_abseta2p4_pt2p0  # Tracks with |eta| < 2.4 and pt >= 2.0 GeV
```

## Track Selection Criteria

All counted tracks must satisfy:
1. **High purity** quality flag
2. **|dz/σ_dz| < 3.0** (track-vertex compatibility in z)
3. **|dxy/σ_dxy| < 3.0** (track-vertex compatibility in transverse plane)
4. **|eta| < specified limit** from `absEtaTrkDetail`
5. **pT > specified threshold** from `ptTrkDetail`

## Usage Example

```python
process.hionia.useDetailEventInfo = cms.bool(True)
process.hionia.useGeTracks = cms.untracked.bool(True)  # Automatically forced when useDetailEventInfo=True
process.hionia.ptTrkDetail = cms.vdouble(0.5, 1.0, 1.5, 2.0, 3.0)
process.hionia.absEtaTrkDetail = cms.vdouble(0.5, 1.0, 1.5, 2.0, 2.4)
```

## Important Notes

1. **Automatically enables `useGeTracks = True`**: Enabling `useDetailEventInfo` forces reading `srcTracks`
2. **Event-level information**: These are global event multiplicities, not associated with specific dimuons
3. **Inclusive counting**: A track passing |eta| < 2.4 and pt > 0.5 will be counted in ALL applicable bins
4. **Branch naming**: Decimal points in values are replaced with 'p' (e.g., 1.5 → 1p5)

## Performance Considerations

- The number of branches created = (# of eta bins) × (# of pt bins)
- More bins = more branches but finer granularity
- Default 3×3 = 9 branches is reasonable for most analyses

## Modified Files

1. `HiAnalysis/HiOnia/interface/HiOniaAnalyzer.h`
2. `HiAnalysis/HiOnia/plugins/HiOniaAnalyzer.cc`
3. `HiAnalysis/HiOnia/python/hioniaanalyzer_cfi.py`
