# ONE PATIENT Data Flow - Exact Shapes

## Patient_001: From Raw Data → Model → Prediction

---

## STEP 1: Raw Input Files

```
📁 Patient_001/
├── tcr_sequences.csv (3.2 MB)
├── hla_genotype.txt (1 KB)
└── clinical_label.txt (1 KB)
```

---

## STEP 2: Loaded into Memory (Python)

### 2.1 TCR Sequences (List of Dictionaries)

```python
tcr_data = [
    {
        'cdr3': 'CASSLAPGATNEKLFF',      # string, length 16
        'v_gene': 'TRBV19',               # string (categorical)
        'd_gene': 'TRBDX',                # string (categorical)
        'j_gene': 'TRBJ1-4',              # string (categorical)
        'frequency': 0.0125               # float
    },
    {
        'cdr3': 'CASSLGQAYEQYF',          # string, length 13
        'v_gene': 'TRBV7-9',
        'd_gene': 'TRBDX',
        'j_gene': 'TRBJ2-7',
        'frequency': 0.0086
    },
    # ... 49,998 more sequences
]

# Type: List[Dict]
# Length: 50,000 sequences
```

### 2.2 HLA Genotype (List of Strings)

```python
hla_data = [
    'HLA-A*02:01',
    'HLA-A*24:02',
    'HLA-B*07:02',
    'HLA-B*44:03',
    'HLA-C*05:01',
    'HLA-C*07:02'
]

# Type: List[str]
# Length: 6 alleles
```

### 2.3 Clinical Label (Integer)

```python
label = 1  # 1 = Responder (CRPR), 0 = Non-responder (SDPD)

# Type: int
```

---

## STEP 3: Preprocessing - Convert to Numbers

### 3.1 CDR3 Sequence → One-Hot Matrix

```python
# Example: 'CASSLAPGATNEKLFF' (16 amino acids)

# Define amino acid alphabet
AA_ALPHABET = 'ACDEFGHIKLMNPQRSTVWY'  # 20 amino acids

# Convert each position to one-hot
# Position 0: 'C' → [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
# Position 1: 'A' → [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
# Position 2: 'S' → [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0]
# ... continues for all 16 positions

cdr3_onehot = np.array([
    [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],  # C
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],  # A
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0],  # S
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0],  # S
    [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],  # L
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],  # A
    [0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],  # P
    [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],  # G
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],  # A
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],  # T
    [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0],  # N
    [0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],  # E
    [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],  # K
    [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],  # L
    [0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],  # F
    [0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],  # F
])

# Shape: (16, 20) - 16 positions, 20 possible amino acids
# Type: np.ndarray, dtype=float32
```

### 3.2 V/D/J Genes → One-Hot Vectors

```python
# V gene: 'TRBV19'
# Total V genes: 50 options
v_gene_onehot = np.array([0,0,0,...,1,...,0])  # 1 at position 19
# Shape: (50,)

# D gene: 'TRBDX'
# Total D genes: 3 options
d_gene_onehot = np.array([0,1,0])  # 1 at position for 'TRBDX'
# Shape: (3,)

# J gene: 'TRBJ1-4'
# Total J genes: 13 options
j_gene_onehot = np.array([0,0,0,1,0,...,0])  # 1 at position 4
# Shape: (13,)
```

### 3.3 HLA Alleles → Multi-Hot Vector

```python
# All possible HLA alleles in dataset: ~200 options
# Patient has 6 alleles: A*02:01, A*24:02, B*07:02, B*44:03, C*05:01, C*07:02

hla_multihot = np.array([
    0, 1, 0, 0, 1, 0, ..., 1, 0, 1, ..., 1, 0, 1, 0, 0
])
# 1s at positions: 1, 4, 56, 89, 134, 178 (example positions)

# Shape: (200,)
# Sum of vector: 6 (number of 1s = number of alleles)
```

---

## STEP 4: Neural Network Embedding

### 4.1 Embed Each Component

```python
# Input tensors
cdr3_input = torch.tensor(cdr3_onehot)      # Shape: (16, 20)
v_input = torch.tensor(v_gene_onehot)       # Shape: (50,)
d_input = torch.tensor(d_gene_onehot)       # Shape: (3,)
j_input = torch.tensor(j_gene_onehot)       # Shape: (13,)
hla_input = torch.tensor(hla_multihot)      # Shape: (200,)

# Pass through embedding layers
cdr3_embedded = embedding_layer_cdr3(cdr3_input)
# Shape: (16, 128) - each position now 128-dim vector

v_embedded = embedding_layer_v(v_input)
# Shape: (32,) - single 32-dim vector

d_embedded = embedding_layer_d(d_input)
# Shape: (16,) - single 16-dim vector

j_embedded = embedding_layer_j(j_input)
# Shape: (32,) - single 32-dim vector

hla_embedded = embedding_layer_hla(hla_input)
# Shape: (64,) - single 64-dim vector for all HLAs
```

### 4.2 Flatten and Concatenate

```python
# Flatten CDR3 embedding
cdr3_flat = cdr3_embedded.flatten()
# Shape: (2048,) - from (16, 128) → 16*128 = 2048

# Concatenate everything
sequence_representation = torch.cat([
    cdr3_flat,      # 2048 dims
    v_embedded,     # 32 dims
    d_embedded,     # 16 dims
    j_embedded,     # 32 dims
    hla_embedded    # 64 dims
], dim=0)

# Final shape: (2192,) - ONE vector representing ONE TCR sequence
```

---

## STEP 5: Entire Repertoire (All 50k Sequences)

```python
# For Patient_001, we have 50,000 sequences

# Stack all sequence representations
patient_repertoire = torch.stack([
    sequence_representation_1,   # (2192,)
    sequence_representation_2,   # (2192,)
    sequence_representation_3,   # (2192,)
    # ... 49,997 more
])

# Final input shape: (50000, 2192)
# Type: torch.Tensor, dtype=torch.float32
# Memory: ~400 MB per patient (50k * 2192 * 4 bytes)
```

---

## STEP 6: Through DeepTCR Model

### 6.1 Attention Layer

```python
# Input: (50000, 2192)

# Attention mechanism learns which sequences are important
attention_weights = attention_layer(patient_repertoire)
# Shape: (50000, 10) - 10 concepts/attention heads

# Apply attention (soft selection)
attended_sequences = patient_repertoire * attention_weights
# Shape: (50000, 2192)
```

### 6.2 Aggregation Layer

```python
# Take weighted average across all sequences
# This is where MIL happens: bag of sequences → single representation

repertoire_summary = torch.mean(attended_sequences, dim=0)
# Shape: (2192,) - single vector for entire patient

# Alternative: Use concept frequencies
concept_frequencies = torch.mean(attention_weights, dim=0)
# Shape: (10,) - proportion of each concept in repertoire
```

### 6.3 Classification Layer

```python
# Final prediction
logits = classifier_layer(repertoire_summary)
# Shape: (1,) - single number

# Apply sigmoid for probability
probability = torch.sigmoid(logits)
# Shape: (1,)
# Value: 0.87 (87% chance of response)

# Binary prediction
prediction = int(probability > 0.5)
# Value: 1 (Responder)
```

---

## COMPLETE DATA FLOW DIAGRAM

```
RAW DATA
┌─────────────────────────────────────────┐
│ TCR CSV: 50k rows × 5 columns          │
│ HLA TXT: 6 alleles                     │
│ Label: 1 integer                       │
└─────────────────────────────────────────┘
              ↓
PREPROCESSING
┌─────────────────────────────────────────┐
│ CDR3 matrices: (50k, 16, 20)           │
│ V genes: (50k, 50)                     │
│ D genes: (50k, 3)                      │
│ J genes: (50k, 13)                     │
│ HLA: (200,) - same for all seqs       │
└─────────────────────────────────────────┘
              ↓
EMBEDDING
┌─────────────────────────────────────────┐
│ CDR3: (50k, 16, 128) → (50k, 2048)    │
│ V: (50k, 32)                           │
│ D: (50k, 16)                           │
│ J: (50k, 32)                           │
│ HLA: (50k, 64) - broadcast to all     │
│                                         │
│ Concatenated: (50k, 2192)              │
└─────────────────────────────────────────┘
              ↓
ATTENTION (MIL)
┌─────────────────────────────────────────┐
│ Attention weights: (50k, 10)           │
│ Weighted sequences: (50k, 2192)        │
└─────────────────────────────────────────┘
              ↓
AGGREGATION
┌─────────────────────────────────────────┐
│ Mean pooling: (2192,)                  │
│ OR                                      │
│ Concept frequencies: (10,)             │
└─────────────────────────────────────────┘
              ↓
CLASSIFICATION
┌─────────────────────────────────────────┐
│ Logits: (1,)                           │
│ Probability: 0.87                      │
│ Prediction: 1 (Responder)              │
└─────────────────────────────────────────┘
```

---

## Memory Breakdown

For ONE patient (50k sequences):

| Component | Shape | Memory |
|-----------|-------|--------|
| Raw CDR3 one-hot | (50k, 16, 20) | 32 MB |
| V/D/J one-hot | (50k, 66) | 13 MB |
| HLA multi-hot | (200,) | <1 MB |
| **After Embedding** | | |
| Final concatenated | (50k, 2192) | 400 MB |
| Attention weights | (50k, 10) | 2 MB |
| Final repertoire vector | (2192,) | <1 KB |

**Total per patient: ~450 MB in GPU memory**

---

## Batch Processing

In practice, patients are processed in batches:

```python
# Batch of 4 patients
batch = {
    'Patient_001': (50000, 2192),
    'Patient_002': (48500, 2192),
    'Patient_003': (52000, 2192),
    'Patient_004': (49200, 2192)
}

# Challenge: Variable sequence counts!
# Solution: Pad to max length OR process separately

# If padding to 52000:
batch_tensor = torch.zeros((4, 52000, 2192))
# Shape: (batch_size, max_sequences, feature_dim)
# Memory: ~1.8 GB for 4 patients
```

---

## Key Takeaways

1. **ONE patient = ONE "bag" of ~50k sequences**
2. **Each sequence → ONE vector of 2192 dimensions**
3. **Entire patient → Stack of (50k, 2192)**
4. **Model learns which sequences matter (attention)**
5. **Final output = ONE number (probability)**

**This is Multiple Instance Learning in action!**
