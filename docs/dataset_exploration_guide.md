# Exploring the DeepTCR_Cancer Dataset
## Practical Guide to the GitHub Repository Structure

Based on the file structure you shared from the Zenodo repository.

---

## Repository Structure Overview

```
DeepTCR_Cancer-master/
├── Data/                       ← ALL THE DATA HERE
│   ├── yost/                   ← Validation cohort 1 (11 patients)
│   ├── sade-feldman/           ← Validation cohort 2 (19 patients)  
│   └── other/                  ← Reference data (McPAS database)
├── scripts/                    ← Python code to reproduce paper
│   ├── models/                 ← Training scripts
│   ├── antigen/                ← Analysis scripts
│   ├── dynamics/               ← Temporal analysis
│   └── valid_cohorts/          ← Validation scripts
├── requirements.txt            ← Dependencies
└── README.md                   ← Instructions
```

---

## Part 1: Understanding the Data Files

### 1.1 Yost Dataset (Best for learning!)

**Location:** `Data/yost/data/`

**What it contains:**
- 11 patients with skin cancer (BCC = basal cell carcinoma, SCC = squamous cell carcinoma)
- Pre-treatment and post-treatment samples
- Both tumor (BCC/SCC) and blood (PBMC) samples

**File naming convention:**
```
su001_BCC_pre1_TCRB.tsv
│    │   │    │   └─ TCRB = Beta chain
│    │   │    └───── pre1 = Pre-treatment, replicate 1
│    │   └────────── BCC = Basal Cell Carcinoma (tumor type)
│    └────────────── su001 = Patient ID (subject 001)

su001_PBMC_post_TCRB.tsv
      │    │    └─ TCRB = Beta chain
      │    └────── post = Post-treatment
      └─────────── PBMC = Peripheral Blood (blood sample)
```

**Files available:**

| Patient ID | Tumor Samples | Blood Samples | Total Files |
|-----------|---------------|---------------|-------------|
| su001 | BCC pre1, pre2, post1, post2 | PBMC pre, post | 6 files |
| su002 | - | PBMC post | 1 file |
| su003 | - | PBMC pre, post | 2 files |
| su005 | BCC pre, post | PBMC pre, post | 4 files |
| su006 | BCC pre, post | PBMC pre, post | 4 files |
| su007 | BCC pre, post | PBMC pre, post | 4 files |
| su008 | BCC pre, post | PBMC pre, post | 4 files |
| su009 | BCC pre, post | - | 2 files |
| su010 | BCC pre, post + SCC pre, post | - | 4 files |
| su012 | BCC pre, post | - | 2 files |
| su013 | SCC pre, post | - | 2 files |
| su014 | SCC pre, post | - | 2 files |

**File sizes tell a story:**
- Tumor samples: 91 KB - 6.6 MB (fewer sequences)
- Blood samples: 2.6 MB - 28.6 MB (way more sequences!)
- Why? Blood has more diverse T cells

---

### 1.2 Response Labels

**Location:** `Data/yost/response.csv`

**What it looks like:**
```python
import pandas as pd

response = pd.read_csv('Data/yost/response.csv')
print(response)
```

**Expected output:**
```
   patient_id response
0        su001       CR    # Complete Response (good!)
1        su002       PR    # Partial Response (good!)
2        su003       SD    # Stable Disease (not responding)
3        su005       PD    # Progressive Disease (bad)
...
```

**Converting to binary labels:**
```python
response['binary'] = response['response'].map({
    'CR': 1,  # Responder
    'PR': 1,  # Responder
    'SD': 0,  # Non-responder
    'PD': 0   # Non-responder
})
```

---

### 1.3 Sade-Feldman Dataset

**Location:** `Data/sade-feldman/`

**Files:**
- `sade-feldman_tcrs.csv` (1.2 MB) - All TCR sequences
- `response.csv` (784 bytes) - Patient labels

**Format:** Already aggregated by patient

```python
import pandas as pd

# Load TCR data
tcrs = pd.read_csv('Data/sade-feldman/sade-feldman_tcrs.csv')
print(tcrs.columns)

# Expected columns:
# ['patient_id', 'amino_acid', 'v_gene', 'j_gene', 'count', ...]

# Load responses
response = pd.read_csv('Data/sade-feldman/response.csv')
```

**This dataset is simpler:**
- Already cleaned and formatted
- All patients in one file
- Good for quick testing

---

### 1.4 McPAS-TCR Database

**Location:** `Data/other/McPAS-TCR.csv` (7.2 MB)

**What it is:**
- Curated database of TCR sequences with known antigen specificities
- Used to interpret what antigens the model is seeing
- Contains ~50,000 TCR-antigen pairs

```python
import pandas as pd

mcpas = pd.read_csv('Data/other/McPAS-TCR.csv')
print(mcpas.columns)

# Expected columns:
# ['CDR3.beta.aa', 'Epitope', 'Antigen.protein', 'HLA', ...]

# Examples
print(mcpas[['CDR3.beta.aa', 'Epitope', 'Antigen.protein']].head())
```

**Example entries:**
```
CDR3.beta.aa        Epitope      Antigen.protein
CASSLAPGATNEKLFF    GLCTLVAML    MART-1 (melanoma)
CASSLGQAYEQYF       GILGFVFTL    Flu M1
```

---

## Part 2: Hands-On Exploration

### 2.1 Load and Explore One Patient File

```python
import pandas as pd
import matplotlib.pyplot as plt

# Load one patient's tumor sample (smallest file for testing)
file = 'Data/yost/data/su010_BCC_pre_TCRB.tsv'
df = pd.read_csv(file, sep='\t')

print("="*60)
print("PATIENT FILE EXPLORATION")
print("="*60)
print(f"\nFile: {file}")
print(f"File size: {len(df):,} rows")
print(f"\nColumns ({len(df.columns)} total):")
for col in df.columns:
    print(f"  - {col}")

print("\n" + "="*60)
print("FIRST 3 SEQUENCES")
print("="*60)
print(df[['amino_acid', 'v_gene', 'j_gene', 'templates', 'productive_frequency']].head(3))

print("\n" + "="*60)
print("DATA SUMMARY")
print("="*60)
print(f"Frame types: {df['frame_type'].value_counts().to_dict()}")
print(f"Productive sequences: {(df['frame_type'] == 'In').sum():,}")
print(f"Non-productive: {(df['frame_type'] == 'Out').sum():,}")

# Focus on productive
productive = df[df['frame_type'] == 'In']
print(f"\nUnique productive sequences: {productive['amino_acid'].nunique():,}")
print(f"Total reads (templates): {productive['templates'].sum():,}")

# Sequence length distribution
seq_lengths = productive['amino_acid'].str.len()
print(f"\nSequence lengths:")
print(f"  Min: {seq_lengths.min()}")
print(f"  Max: {seq_lengths.max()}")
print(f"  Mean: {seq_lengths.mean():.1f}")
print(f"  Median: {seq_lengths.median()}")

# Top 5 clones
print("\n" + "="*60)
print("TOP 5 MOST FREQUENT CLONES")
print("="*60)
top5 = productive.nlargest(5, 'productive_frequency')
for i, (_, row) in enumerate(top5.iterrows(), 1):
    print(f"{i}. {row['amino_acid']:25s} ({row['productive_frequency']*100:.2f}%)")
```

### 2.2 Compare Pre vs Post Treatment

```python
import pandas as pd
import numpy as np

# Load pre and post treatment samples
pre_df = pd.read_csv('Data/yost/data/su001_BCC_pre1_TCRB.tsv', sep='\t')
post_df = pd.read_csv('Data/yost/data/su001_BCC_post1_TCRB.tsv', sep='\t')

# Filter to productive
pre = pre_df[pre_df['frame_type'] == 'In']
post = post_df[post_df['frame_type'] == 'In']

print("="*60)
print("PRE vs POST TREATMENT COMPARISON")
print("="*60)
print(f"\nPatient: su001 (BCC tumor)")
print(f"\nPre-treatment:")
print(f"  Total sequences: {len(pre):,}")
print(f"  Unique sequences: {pre['amino_acid'].nunique():,}")
print(f"  Total reads: {pre['templates'].sum():,}")

print(f"\nPost-treatment:")
print(f"  Total sequences: {len(post):,}")
print(f"  Unique sequences: {post['amino_acid'].nunique():,}")
print(f"  Total reads: {post['templates'].sum():,}")

# Overlap analysis
pre_sequences = set(pre['amino_acid'])
post_sequences = set(post['amino_acid'])

shared = pre_sequences & post_sequences
pre_only = pre_sequences - post_sequences
post_only = post_sequences - pre_sequences

print(f"\nOverlap:")
print(f"  Shared sequences: {len(shared):,} ({len(shared)/len(pre_sequences)*100:.1f}% of pre)")
print(f"  Pre-only: {len(pre_only):,}")
print(f"  Post-only: {len(post_only):,}")
print(f"  Turnover rate: {(len(pre_only) + len(post_only)) / (len(pre_sequences) + len(post_sequences)) * 100:.1f}%")
```

### 2.3 Explore All Patients

```python
import pandas as pd
import glob
import os

# Get all files
files = glob.glob('Data/yost/data/*.tsv')
response_df = pd.read_csv('Data/yost/response.csv')

# Summary statistics
summary = []

for file in files:
    # Parse filename
    filename = os.path.basename(file)
    parts = filename.replace('.tsv', '').split('_')
    patient_id = parts[0]
    sample_type = parts[1]  # BCC, SCC, or PBMC
    timepoint = parts[2] if len(parts) > 3 else parts[2]  # pre, post, pre1, etc.
    
    # Load and count
    df = pd.read_csv(file, sep='\t')
    productive = df[df['frame_type'] == 'In']
    
    # Get response if available
    response = response_df[response_df['patient_id'] == patient_id]['response'].values
    response = response[0] if len(response) > 0 else 'Unknown'
    
    summary.append({
        'patient_id': patient_id,
        'sample_type': sample_type,
        'timepoint': timepoint,
        'total_sequences': len(productive),
        'unique_sequences': productive['amino_acid'].nunique(),
        'total_reads': productive['templates'].sum(),
        'response': response,
        'file_size_mb': os.path.getsize(file) / 1024 / 1024
    })

# Create summary DataFrame
summary_df = pd.DataFrame(summary)

print("="*80)
print("COMPLETE DATASET SUMMARY")
print("="*80)
print(f"\nTotal files: {len(summary_df)}")
print(f"Unique patients: {summary_df['patient_id'].nunique()}")
print(f"\nSample types:")
print(summary_df['sample_type'].value_counts())
print(f"\nTimepoints:")
print(summary_df['timepoint'].value_counts())

# Show per-patient summary
print("\n" + "="*80)
print("PER-PATIENT STATISTICS")
print("="*80)
patient_summary = summary_df.groupby('patient_id').agg({
    'unique_sequences': 'sum',
    'total_reads': 'sum',
    'response': 'first'
}).reset_index()

print(patient_summary.to_string(index=False))

# Responders vs Non-responders
print("\n" + "="*80)
print("RESPONDERS vs NON-RESPONDERS")
print("="*80)
responders = summary_df[summary_df['response'].isin(['CR', 'PR'])]
non_responders = summary_df[summary_df['response'].isin(['SD', 'PD'])]

print(f"\nResponders (CR/PR):")
print(f"  Patients: {responders['patient_id'].nunique()}")
print(f"  Mean unique sequences: {responders['unique_sequences'].mean():.0f}")

print(f"\nNon-responders (SD/PD):")
print(f"  Patients: {non_responders['patient_id'].nunique()}")
print(f"  Mean unique sequences: {non_responders['unique_sequences'].mean():.0f}")
```

---

## Part 3: Data Format Deep Dive

### 3.1 Adaptive Biotechnologies TSV Format

**Standard columns in the TSV files:**

```python
# Read first file to see all columns
df = pd.read_csv('Data/yost/data/su001_BCC_pre1_TCRB.tsv', sep='\t')
print(df.dtypes)
```

**Column descriptions:**

| Column Name | Type | Description | Importance |
|-------------|------|-------------|------------|
| `nucleotide` | str | DNA sequence | Low (not used) |
| `amino_acid` | str | CDR3-β amino acid sequence | **CRITICAL** ⭐ |
| `v_family` | str | V gene family | Medium |
| `v_gene` | str | V gene segment | **CRITICAL** ⭐ |
| `d_family` | str | D gene family | Low |
| `d_gene` | str | D gene segment | Medium |
| `j_family` | str | J gene family | Low |
| `j_gene` | str | J gene segment | **CRITICAL** ⭐ |
| `templates` | int | Number of times sequenced | **CRITICAL** ⭐ |
| `frame_type` | str | In/Out of frame | **CRITICAL** ⭐ |
| `productive_frequency` | float | Frequency (0-1) | **CRITICAL** ⭐ |
| `v_deletions` | int | V gene deletions | Low |
| `d_5_deletions` | int | D gene 5' deletions | Low |
| `d_3_deletions` | int | D gene 3' deletions | Low |
| `j_deletions` | int | J gene deletions | Low |
| `v_index` | int | V gene start position | Low |
| `j_index` | int | J gene end position | Low |

**Critical columns for DeepTCR:**
1. `amino_acid` - The actual TCR sequence
2. `v_gene` - V gene usage
3. `j_gene` - J gene usage  
4. `templates` - Read count (abundance)
5. `frame_type` - Filter to 'In' only
6. `productive_frequency` - Relative abundance

---

### 3.2 Preprocessing Script

```python
import pandas as pd

def preprocess_adaptive_tsv(file_path):
    """
    Clean Adaptive TCR-seq file for DeepTCR input
    
    Returns:
    --------
    DataFrame with columns: ['beta', 'v_gene', 'j_gene', 'count']
    """
    # Load
    df = pd.read_csv(file_path, sep='\t')
    
    # Filter to productive (in-frame) sequences
    df = df[df['frame_type'] == 'In'].copy()
    
    # Remove invalid amino acids
    valid_aa = set('ACDEFGHIKLMNPQRSTVWY')
    df = df[df['amino_acid'].apply(lambda x: all(c in valid_aa for c in x))]
    
    # Length filter (keep 10-25 amino acids, typical range)
    df = df[(df['amino_acid'].str.len() >= 10) & 
            (df['amino_acid'].str.len() <= 25)]
    
    # Aggregate by amino acid sequence
    # (Different nucleotides can encode same amino acid)
    df_agg = df.groupby(['amino_acid', 'v_gene', 'j_gene']).agg({
        'templates': 'sum'
    }).reset_index()
    
    # Rename for DeepTCR compatibility
    df_clean = df_agg.rename(columns={
        'amino_acid': 'beta',
        'templates': 'count'
    })
    
    # Sort by frequency
    df_clean = df_clean.sort_values('count', ascending=False)
    
    return df_clean[['beta', 'v_gene', 'j_gene', 'count']]

# Example usage
cleaned = preprocess_adaptive_tsv('Data/yost/data/su001_BCC_pre1_TCRB.tsv')
print(f"Original → Cleaned: {cleaned.shape}")
print("\nCleaned data preview:")
print(cleaned.head())

# Save for later use
cleaned.to_csv('su001_BCC_pre_cleaned.csv', index=False)
```

---

## Part 4: Quick Start Checklist

### Getting Started Steps:

1. **Extract the zip file**
```bash
unzip DeepTCR_Cancer-master.zip
cd DeepTCR_Cancer-master
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
# or
pip install pandas numpy matplotlib seaborn scikit-learn
```

3. **Start with smallest file**
```python
# su010_BCC_pre_TCRB.tsv is only 91 KB - great for testing!
import pandas as pd
df = pd.read_csv('Data/yost/data/su010_BCC_pre_TCRB.tsv', sep='\t')
print(df.head())
```

4. **Explore the data** (use code from Part 2)

5. **Try preprocessing** (use function from Part 3.2)

6. **Load multiple patients** (use code from Part 2.3)

---

## Part 5: Common Pandas Operations on TCR Data

```python
import pandas as pd

# Load data
df = pd.read_csv('Data/yost/data/su001_BCC_pre1_TCRB.tsv', sep='\t')
productive = df[df['frame_type'] == 'In']

# 1. Top N clones
top10 = productive.nlargest(10, 'productive_frequency')

# 2. Filter by V gene
trbv19 = productive[productive['v_gene'] == 'TRBV19']

# 3. Sequence length distribution
productive['seq_length'] = productive['amino_acid'].str.len()
length_counts = productive['seq_length'].value_counts().sort_index()

# 4. V gene usage frequency
v_usage = productive.groupby('v_gene')['templates'].sum().sort_values(ascending=False)

# 5. J gene usage frequency
j_usage = productive.groupby('j_gene')['templates'].sum().sort_values(ascending=False)

# 6. Diversity metrics
total_sequences = len(productive)
unique_sequences = productive['amino_acid'].nunique()
diversity = unique_sequences / total_sequences  # Simple diversity

# 7. Clonality (concentration)
freq_sorted = productive.sort_values('productive_frequency', ascending=False)
top10_freq = freq_sorted.head(10)['productive_frequency'].sum()
print(f"Top 10 clones represent: {top10_freq*100:.1f}% of repertoire")

# 8. Find motifs (sequences containing pattern)
cassf_motif = productive[productive['amino_acid'].str.contains('CASSF')]
print(f"Sequences with CASSF motif: {len(cassf_motif)}")

# 9. Merge with response labels
response = pd.read_csv('Data/yost/response.csv')
# patient_id from filename
patient_id = 'su001'
patient_response = response[response['patient_id'] == patient_id]['response'].values[0]
print(f"Patient {patient_id} response: {patient_response}")
```

---

## Summary: Your Roadmap

### Phase 1: Exploration (1-2 days)
- [ ] Extract and explore file structure
- [ ] Load one TSV file
- [ ] Understand column meanings
- [ ] Calculate basic statistics

### Phase 2: Data Wrangling (2-3 days)
- [ ] Clean and filter data
- [ ] Aggregate sequences
- [ ] Load multiple patients
- [ ] Merge with response labels

### Phase 3: Analysis (3-5 days)
- [ ] Compare responders vs non-responders
- [ ] Analyze pre vs post treatment
- [ ] Calculate diversity metrics
- [ ] Visualize distributions

### Phase 4: Encoding (5-7 days)
- [ ] One-hot encode sequences
- [ ] Encode V/D/J genes
- [ ] Create patient-level features
- [ ] Prepare for modeling

### Phase 5: Modeling (7-14 days)
- [ ] Understand MIL concept
- [ ] Try simple baselines
- [ ] Install DeepTCR
- [ ] Run paper's code

**You've got this! Start with Phase 1 and take it step by step.**
