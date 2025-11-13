# From Pandas to DeepTCR: A Practical Guide
## For People Who Know: pandas, numpy, Python, basic ML

---

## Part 1: What You Already Know (Your Foundation)

### Things You're Familiar With:

```python
import pandas as pd
import numpy as np

# 1. Reading CSV files
df = pd.read_csv('data.csv')

# 2. DataFrames with rows and columns
# Each row = one sample
# Each column = one feature

# 3. Arrays and matrices
X = np.array([[1, 2, 3], [4, 5, 6]])  # Shape: (2, 3)

# 4. Basic ML: Features → Model → Prediction
# sklearn: X (features), y (labels)
```

**Key concept you know:** One row = one sample with a label

---

## Part 2: The TCR-seq Data Challenge (What's Different)

### Traditional ML (what you know):

```python
# Traditional dataset
df = pd.DataFrame({
    'feature_1': [1.2, 3.4, 5.6],
    'feature_2': [2.1, 4.3, 6.5],
    'label': [0, 1, 0]
})
# Shape: (3, 3) - 3 samples, 2 features + 1 label
# One row = one sample = one label ✓
```

### TCR-seq Data (what's new):

```python
# Patient's TCR repertoire
df = pd.DataFrame({
    'cdr3_amino_acid': ['CASSLAPGATNEKLFF', 'CASSLGQAYEQYF', ...],  # 50,000 rows
    'v_gene': ['TRBV19', 'TRBV7-9', ...],
    'j_gene': ['TRBJ1-4', 'TRBJ2-7', ...],
    'frequency': [0.0125, 0.0086, ...]
})
# Shape: (50000, 4) - 50,000 sequences, 4 features

# But: ONE patient = ONE label (not 50,000 labels!)
patient_label = 1  # Single label for entire DataFrame

# This is Multiple Instance Learning (MIL)
# 50,000 rows → 1 label
```

**The challenge:** How do you train ML when one DataFrame = one label?

---

## Part 3: Hands-On - Exploring REAL Data

### Step 1: Looking at the Yost Dataset Files

From the structure you shared:
```
Data/yost/data/su001_BCC_pre1_TCRB.tsv  (1.9 MB)
```

This is an Adaptive Biotechnologies TCR-seq file (TSV format).

### Opening the File (Pure Pandas):

```python
import pandas as pd

# Load one patient's TCR sequences
file_path = 'Data/yost/data/su001_BCC_pre1_TCRB.tsv'
tcr_df = pd.read_csv(file_path, sep='\t')  # Tab-separated

# Let's explore
print(tcr_df.shape)  # Example output: (45000, 15) - 45k sequences
print(tcr_df.columns)
```

### What the columns look like (Adaptive format):

```python
# Typical columns in Adaptive TCR-seq files:
columns = [
    'nucleotide',              # DNA sequence
    'amino_acid',              # Amino acid CDR3 sequence ← KEY!
    'v_family', 'v_gene',      # V gene info
    'd_family', 'd_gene',      # D gene info  
    'j_family', 'j_gene',      # J gene info ← KEY!
    'templates',               # Read count ← KEY!
    'frame_type',              # In-frame or out-of-frame
    'productive_frequency',    # Frequency ← KEY!
    # ... more columns
]

# The KEY columns for DeepTCR:
key_cols = ['amino_acid', 'v_gene', 'j_gene', 'templates', 'productive_frequency']
```

### Exploring the Data (Pandas operations you know):

```python
# Load and preview
tcr_df = pd.read_csv(file_path, sep='\t')
print(tcr_df.head())
print(tcr_df.info())

# Filter to productive sequences only (standard practice)
productive = tcr_df[tcr_df['frame_type'] == 'In']
print(f"Productive sequences: {len(productive)}")

# Look at top clones (most frequent)
top_clones = productive.nlargest(10, 'productive_frequency')
print(top_clones[['amino_acid', 'v_gene', 'j_gene', 'productive_frequency']])

# Basic stats (pandas aggregations you know)
print(f"Total unique sequences: {productive['amino_acid'].nunique()}")
print(f"Most common V gene: {productive['v_gene'].mode()[0]}")
print(f"Mean frequency: {productive['productive_frequency'].mean()}")
```

**Output example:**
```
amino_acid             v_gene    j_gene     productive_frequency
CASSLAPGATNEKLFF       TRBV19    TRBJ1-4    0.0125
CASSLGQAYEQYF          TRBV7-9   TRBJ2-7    0.0086
CASRPGLAGGRPEQYF       TRBV4-1   TRBJ2-7    0.0043
```

---

## Part 4: Preprocessing for DeepTCR

### Step 1: Clean and Filter (Pandas operations)

```python
# Standard preprocessing steps

# 1. Keep only productive (in-frame) sequences
df_clean = tcr_df[tcr_df['frame_type'] == 'In'].copy()

# 2. Remove sequences with invalid amino acids
valid_aa = set('ACDEFGHIKLMNPQRSTVWY')
df_clean = df_clean[
    df_clean['amino_acid'].apply(lambda x: all(c in valid_aa for c in x))
]

# 3. Remove very long sequences (>40 amino acids)
df_clean = df_clean[df_clean['amino_acid'].str.len() <= 40]

# 4. Aggregate by amino acid sequence
# (multiple DNA sequences can encode same protein)
df_agg = df_clean.groupby(['amino_acid', 'v_gene', 'j_gene']).agg({
    'templates': 'sum',  # Sum read counts
    'productive_frequency': 'sum'  # Sum frequencies
}).reset_index()

print(f"Before aggregation: {len(df_clean)}")
print(f"After aggregation: {len(df_agg)}")
```

### Step 2: Convert to DeepTCR Format

```python
# DeepTCR expects specific column names
deeptcr_df = df_agg.rename(columns={
    'amino_acid': 'beta',  # CDR3-beta amino acid sequence
    'templates': 'count'
})

# Select required columns
deeptcr_df = deeptcr_df[['beta', 'v_gene', 'j_gene', 'count']]

# Save for DeepTCR
deeptcr_df.to_csv('patient_001_deeptcr_format.csv', index=False)
```

**What you've done (in pandas terms):**
- Filtered rows (like `df[df['col'] > threshold]`)
- Aggregated data (like `groupby().sum()`)
- Renamed columns (like `df.rename()`)
- Selected columns (like `df[['col1', 'col2']]`)

---

## Part 5: Loading Patient Label

The response.csv file:
```
Data/yost/response.csv
```

### What it looks like:

```csv
patient_id,response
su001,CR
su002,PR
su003,SD
su005,PD
```

### Loading labels (pure pandas):

```python
# Load response data
response_df = pd.read_csv('Data/yost/response.csv')
print(response_df)

# Convert to binary labels (like you would in sklearn)
response_df['binary_label'] = response_df['response'].map({
    'CR': 1,   # Complete Response
    'PR': 1,   # Partial Response
    'SD': 0,   # Stable Disease
    'PD': 0    # Progressive Disease
})

# Now you have:
# patient_id → label mapping
# Just like a typical classification problem!
```

---

## Part 6: From Pandas DataFrame → NumPy Array

### Converting Sequences to Numbers (What DeepTCR does internally)

```python
import numpy as np

# 1. Define amino acid alphabet
AA_ALPHABET = 'ACDEFGHIKLMNPQRSTVWY'  # 20 amino acids
aa_to_idx = {aa: idx for idx, aa in enumerate(AA_ALPHABET)}

# 2. One-hot encode a sequence (like sklearn's OneHotEncoder)
def encode_sequence(seq, max_len=40):
    """
    Convert 'CASSLAPG' → numpy array
    Like: pd.get_dummies() but for sequences
    """
    # Initialize matrix
    encoded = np.zeros((max_len, 20))  # (positions, amino_acids)
    
    # Fill in the sequence
    for i, aa in enumerate(seq[:max_len]):
        if aa in aa_to_idx:
            encoded[i, aa_to_idx[aa]] = 1
    
    return encoded  # Shape: (40, 20)

# Example
seq = 'CASSLAPGATNEKLFF'
encoded_seq = encode_sequence(seq)
print(f"Sequence: {seq}")
print(f"Encoded shape: {encoded_seq.shape}")  # (40, 20)
print(f"First position (C): {encoded_seq[0]}")  # [0,1,0,0,...]
```

**This is like:**
```python
# Similar to pandas get_dummies
df = pd.DataFrame({'color': ['red', 'blue', 'red']})
pd.get_dummies(df['color'])
#    blue  red
# 0     0    1
# 1     1    0
# 2     0    1
```

### Encoding V/D/J Genes (Categorical → Numbers)

```python
# Like sklearn's LabelEncoder or pd.get_dummies

# Get unique V genes
unique_v_genes = df_agg['v_gene'].unique()
v_gene_to_idx = {gene: idx for idx, gene in enumerate(unique_v_genes)}

# Encode one V gene
def encode_v_gene(v_gene, gene_dict, num_genes):
    """One-hot encode V gene"""
    encoded = np.zeros(num_genes)
    if v_gene in gene_dict:
        encoded[gene_dict[v_gene]] = 1
    return encoded

# Example
v_encoded = encode_v_gene('TRBV19', v_gene_to_idx, len(unique_v_genes))
print(f"V gene encoded shape: {v_encoded.shape}")  # (50,) for 50 V genes
```

**This is exactly like sklearn:**
```python
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
le.fit(['TRBV19', 'TRBV7-9', 'TRBV4-1'])
le.transform(['TRBV19'])  # [0]
```

---

## Part 7: Complete Data Pipeline (Putting It Together)

### The Full Pipeline (Pandas → NumPy → Model-Ready)

```python
import pandas as pd
import numpy as np

# STEP 1: Load raw data (pandas)
tcr_df = pd.read_csv('su001_BCC_pre1_TCRB.tsv', sep='\t')
response_df = pd.read_csv('response.csv')

# STEP 2: Clean data (pandas)
tcr_clean = (tcr_df
    .query("frame_type == 'In'")  # Productive only
    .query("amino_acid.str.len() <= 40")  # Length filter
    .groupby(['amino_acid', 'v_gene', 'j_gene'])
    .agg({'templates': 'sum'})
    .reset_index()
)

# STEP 3: Get patient label (pandas)
patient_id = 'su001'
label = response_df.query(f"patient_id == '{patient_id}'")['binary_label'].values[0]
print(f"Patient {patient_id} label: {label}")  # 1 or 0

# STEP 4: Convert to arrays (numpy)
sequences = tcr_clean['amino_acid'].values  # Array of strings
v_genes = tcr_clean['v_gene'].values
j_genes = tcr_clean['j_gene'].values

print(f"Total sequences: {len(sequences)}")
print(f"Label: {label}")

# STEP 5: Encode (numpy arrays)
encoded_sequences = np.array([encode_sequence(seq) for seq in sequences])
# Shape: (num_sequences, 40, 20)

print(f"Encoded data shape: {encoded_sequences.shape}")
# Example output: (45000, 40, 20) - 45k sequences, 40 positions, 20 amino acids

# STEP 6: This is your ML input!
X = encoded_sequences  # Features (bag of sequences)
y = label              # Label (single value)
```

**Compare to typical sklearn:**
```python
# Traditional ML (what you know)
X = df[['feature1', 'feature2']].values  # (n_samples, n_features)
y = df['label'].values                   # (n_samples,)
model.fit(X, y)

# TCR-seq ML (what's new)
X = encoded_sequences  # (n_sequences, 40, 20) - ONE patient
y = label              # (1,) - ONE label
model.fit(X, y)  # MIL model handles the bag
```

---

## Part 8: Multiple Patients (Creating a Dataset)

### Looping Over All Patients (Pandas + File I/O)

```python
import os
import glob

# Get all patient files
patient_files = glob.glob('Data/yost/data/su*_BCC_pre1_TCRB.tsv')
response_df = pd.read_csv('Data/yost/response.csv')

# Process each patient
patients_data = []

for file_path in patient_files:
    # Extract patient ID from filename
    # 'su001_BCC_pre1_TCRB.tsv' → 'su001'
    filename = os.path.basename(file_path)
    patient_id = filename.split('_')[0]
    
    # Load TCR data
    tcr_df = pd.read_csv(file_path, sep='\t')
    
    # Clean and process (same as before)
    tcr_clean = preprocess_tcr_data(tcr_df)  # Your function
    
    # Get label
    label = get_patient_label(patient_id, response_df)  # Your function
    
    # Store
    patients_data.append({
        'patient_id': patient_id,
        'tcr_sequences': tcr_clean,  # DataFrame
        'label': label  # 0 or 1
    })

print(f"Loaded {len(patients_data)} patients")

# Now you have a list of dictionaries (like sklearn's datasets)
# Each element = one patient = one "sample" with many sequences
```

**This is like:**
```python
# Loading multiple CSV files (what you know)
all_data = []
for file in files:
    df = pd.read_csv(file)
    all_data.append(df)

# Combining them
combined_df = pd.concat(all_data)
```

---

## Part 9: The MIL Trick (Understanding the Model)

### What DeepTCR Does Differently

```python
# Traditional ML (sklearn)
from sklearn.ensemble import RandomForestClassifier

X = np.array([[1, 2], [3, 4], [5, 6]])  # 3 samples, 2 features
y = np.array([0, 1, 0])                  # 3 labels

model = RandomForestClassifier()
model.fit(X, y)  # Each row gets a label

# Prediction
pred = model.predict([[7, 8]])  # Predict ONE sample
```

```python
# DeepTCR (MIL approach)
# Conceptually similar to:

def predict_patient(sequences, model):
    """
    sequences: (50000, 2192) - many sequences
    Returns: single prediction for patient
    """
    # 1. Get prediction for each sequence
    seq_predictions = model.predict_sequences(sequences)  # (50000,)
    
    # 2. Aggregate (attention mechanism does this smartly)
    # Simple version: weighted average
    weights = compute_attention(sequences)  # (50000,) - importance
    patient_pred = np.average(seq_predictions, weights=weights)
    
    # 3. Return single prediction
    return patient_pred  # Single number

# Key: Multiple sequences → ONE prediction
```

**Think of it like:**
```python
# Pandas groupby + aggregation (concept you know!)
df.groupby('patient_id').agg({
    'sequence_prediction': 'mean'  # Average all sequences
})

# But DeepTCR learns the "groupby" logic!
# It figures out which sequences to pay attention to
```

---

## Part 10: Relating to Your ML Knowledge

### Concepts You Already Know → How They Apply Here

| Your Knowledge | TCR-seq Application |
|----------------|---------------------|
| **Loading CSV** (`pd.read_csv`) | Loading TCR TSV files |
| **Filtering rows** (`df[df['col'] > x]`) | Removing non-productive sequences |
| **One-hot encoding** (`pd.get_dummies`) | Encoding amino acids |
| **Aggregation** (`groupby().sum()`) | Combining duplicate sequences |
| **Train/test split** | Cross-validation on patients |
| **Feature matrix X** | Encoded sequences (40 × 20) |
| **Label vector y** | Patient response (0/1) |
| **Neural network input** | Batch of sequences |
| **Prediction** | Probability of response |

### The NEW Concepts:

1. **Multiple Instance Learning (MIL)**
   - You know: 1 row = 1 label
   - New: 50k rows = 1 label (bag of sequences)

2. **Attention Mechanism**
   - You know: Feature importance (like RandomForest)
   - New: Learned weights on which sequences matter

3. **Repertoire-Level Prediction**
   - You know: Predict per sample
   - New: Predict per patient (aggregating sequences)

---

## Part 11: Quick Start Code (Run This!)

### Complete Working Example

```python
import pandas as pd
import numpy as np

# 1. Load one patient
patient_file = 'Data/yost/data/su001_BCC_pre1_TCRB.tsv'
tcr_df = pd.read_csv(patient_file, sep='\t')

# 2. Quick exploration (pandas operations you know)
print("=" * 50)
print("EXPLORING TCR-SEQ DATA")
print("=" * 50)
print(f"\nTotal rows: {len(tcr_df):,}")
print(f"Columns: {list(tcr_df.columns)}")
print(f"\nFirst 3 sequences:")
print(tcr_df[['amino_acid', 'v_gene', 'j_gene', 'templates']].head(3))

# 3. Basic statistics
productive = tcr_df[tcr_df['frame_type'] == 'In']
print(f"\nProductive sequences: {len(productive):,}")
print(f"Unique sequences: {productive['amino_acid'].nunique():,}")
print(f"Most common V gene: {productive['v_gene'].value_counts().head(1)}")

# 4. Sequence length distribution
seq_lengths = productive['amino_acid'].str.len()
print(f"\nSequence length stats:")
print(f"  Min: {seq_lengths.min()}")
print(f"  Max: {seq_lengths.max()}")
print(f"  Mean: {seq_lengths.mean():.1f}")
print(f"  Median: {seq_lengths.median():.1f}")

# 5. Top 5 most frequent sequences
print("\nTop 5 clones:")
top5 = productive.nlargest(5, 'productive_frequency')
for idx, row in top5.iterrows():
    print(f"  {row['amino_acid']:20s} | {row['productive_frequency']:.4f}")

print("\n" + "=" * 50)
print("This is what ONE patient's data looks like!")
print("=" * 50)
```

**Run this and you'll see:**
- Familiar pandas operations
- Real TCR-seq data structure
- How many sequences per patient
- What the sequences look like

---

## Part 12: Next Steps (Learning Path)

### Week 1: Get comfortable with data
```python
# Goals:
# 1. Load and explore 5 patient files
# 2. Calculate diversity metrics (pandas)
# 3. Visualize sequence lengths (matplotlib)
# 4. Compare pre vs post treatment (merge dataframes)
```

### Week 2: Preprocessing
```python
# Goals:
# 1. Write cleaning pipeline (pandas)
# 2. Encode amino acids (numpy)
# 3. Handle variable-length sequences (padding)
# 4. Batch multiple patients
```

### Week 3: Understanding MIL
```python
# Goals:
# 1. Implement simple bag aggregation
# 2. Try different pooling: mean, max, attention
# 3. Compare to traditional ML baseline
```

### Week 4: DeepTCR
```python
# Goals:
# 1. Install DeepTCR package
# 2. Run example code from paper
# 3. Train on Yost dataset
# 4. Interpret results
```

---

## Summary: Key Takeaways

### What's Familiar:
✅ Loading data (`pd.read_csv`)
✅ Cleaning data (filtering, aggregation)
✅ Encoding features (one-hot, label encoding)
✅ Train/test split
✅ Making predictions

### What's New:
🆕 Multiple Instance Learning (bag of sequences → 1 label)
🆕 Attention mechanism (learning which sequences matter)
🆕 Variable-length sequences (padding/truncation)
🆕 Repertoire-level features (not sequence-level)

### The Bridge:
Think of it like this:
- **Pandas DataFrame** = Patient's TCR repertoire
- **Each row** = One TCR sequence
- **Entire DataFrame** = Gets ONE label
- **Your job** = Build a model that learns which rows matter

**You're NOT predicting per row.**
**You're predicting per DataFrame!**

That's the key insight of Multiple Instance Learning.

---

Want me to create a Jupyter notebook with runnable code next?
