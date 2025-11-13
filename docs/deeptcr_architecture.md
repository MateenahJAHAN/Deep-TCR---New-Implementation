# DeepTCR System Architecture - High Level Overview

## The Big Picture Problem
**Goal:** Predict if a cancer patient will respond to immunotherapy BEFORE they get treated

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                          INPUT DATA                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  1. TCR Sequences (from tumor biopsy)                           │
│     - CDR3 sequences (amino acid strings, ~15-20 chars)         │
│     - V/D/J genes (categorical labels)                          │
│     - Frequencies (how common each sequence is)                 │
│     - Think: "immune cell barcodes" from the tumor              │
│                                                                   │
│  2. HLA Genotype (patient's immune "presentation system")       │
│     - 6 HLA alleles per patient (e.g., HLA-A*02:01)            │
│     - Think: "context" for interpreting TCR sequences          │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      DEEPTCR MODEL                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Architecture Type: Multiple Instance Learning (MIL)            │
│  - Input: A "bag" of TCR sequences (repertoire)                 │
│  - Not individual sequences, but COLLECTIONS                    │
│                                                                   │
│  Key Components:                                                 │
│  ┌──────────────────────────────────────────────────┐          │
│  │ 1. Featurization Layer                            │          │
│  │    - Embed TCR sequences (amino acids → vectors)  │          │
│  │    - Embed HLA (categorical → vectors)            │          │
│  │    - Concatenate TCR + HLA representations        │          │
│  └──────────────────────────────────────────────────┘          │
│                      ↓                                           │
│  ┌──────────────────────────────────────────────────┐          │
│  │ 2. Attention Mechanism                            │          │
│  │    - Learns which TCR sequences are important     │          │
│  │    - Assigns "concepts" to sequence groups        │          │
│  │    - Ignores noise/irrelevant sequences           │          │
│  └──────────────────────────────────────────────────┘          │
│                      ↓                                           │
│  ┌──────────────────────────────────────────────────┐          │
│  │ 3. Aggregation Layer                              │          │
│  │    - Pools information across all sequences       │          │
│  │    - Creates repertoire-level representation      │          │
│  └──────────────────────────────────────────────────┘          │
│                      ↓                                           │
│  ┌──────────────────────────────────────────────────┐          │
│  │ 4. Classification Layer                           │          │
│  │    - Binary output: Responder vs Non-responder    │          │
│  └──────────────────────────────────────────────────┘          │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                          OUTPUTS                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  1. Primary Prediction                                           │
│     → Probability of response (0-1 score)                       │
│     → Classification: Responder / Non-responder                 │
│                                                                   │
│  2. Interpretability Outputs                                     │
│     → Which TCR sequences are predictive?                       │
│     → What "concepts" (motifs) predict response?                │
│     → Likely antigen specificities (tumor vs viral)             │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Data Flow in Simple Terms

**Think of it like this:**

1. **Input = A bag of puzzle pieces**
   - Each TCR sequence is a puzzle piece
   - One patient has ~thousands of pieces
   - Some pieces matter, most don't

2. **Model = Smart sorter**
   - Figures out which pieces are important
   - Groups similar pieces together
   - Learns patterns that predict outcomes

3. **Output = Prediction**
   - Will this patient respond? (Yes/No + confidence)
   - Which puzzle pieces led to this prediction?

---

## Key Innovation: Multiple Instance Learning (MIL)

**Traditional ML:** One sample = one label
- Example: One image → cat or dog?

**MIL approach:** One bag of samples = one label
- Example: Bag of 1000 TCR sequences → responder or not?
- Not all sequences matter - model learns which ones do!

---

## Training Details

**Dataset:** CheckMate-038 clinical trial
- 43 patients (pre-treatment tumor biopsies)
- Treatment: Anti-PD1 or Anti-PD1 + Anti-CTLA4
- Labels: CRPR (responders) vs SDPD (non-responders)

**Performance:**
- AUC = 0.86 (TCR + HLA model)
- Better than conventional biomarkers (PD-L1, TMB)
- Validated on 2 independent cohorts

---

## Clinical Use Case

**Scenario:** Patient diagnosed with melanoma

1. Take tumor biopsy → sequence TCRs
2. Get HLA genotype → blood test  
3. Run through DeepTCR → get prediction
4. **Decision:** If predicted non-responder, consider:
   - Alternative treatments
   - Clinical trial enrollment
   - Combination therapies

---

## Biological Insight Discovered

**Key Finding:** Non-responders have:
- More tumor-specific T cells (seems good?)
- But these cells are dysfunctional/exhausted (bad!)
- Higher turnover during therapy (futile response)

**Responders have:**
- More virus-specific T cells (background immunity)
- Functional tumor-specific cells
- Stable response during therapy

This flips conventional thinking: More tumor-specific T cells ≠ better response!

---

## Why This Matters (CS Perspective)

1. **High-dimensional problem:** Thousands of sequences per patient
2. **Noise-heavy data:** Most sequences irrelevant  
3. **Weak supervision:** Only patient-level labels (not sequence-level)
4. **MIL solves this elegantly:** Learns which sequences matter automatically

This is like training a spam filter where you only know if an entire email account is spam-heavy, not which individual emails are spam!
