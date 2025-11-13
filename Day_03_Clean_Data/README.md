# Day 3: Clean Data 🧹

## 🎯 Today's Goal

Remove bad data and prepare the data for analysis!

**Time:** 2-3 hours  
**Difficulty:** ⭐⭐ Easy-Medium (using pandas filtering and grouping)

---

## 📚 What You'll Learn Today

- Why we need to clean data
- How to filter out bad sequences
- How to aggregate duplicate sequences
- How to prepare data for machine learning

---

## 🤔 Questions to Think About (Before Starting)

1. **Why do we filter to productive sequences?**
   - Non-productive sequences don't work
   - They're like errors in the data
   - We only want sequences that actually function

2. **Why might sequences have invalid amino acids?**
   - Sequencing errors
   - Data quality issues
   - We only want the 20 standard amino acids

3. **Why do we aggregate sequences?**
   - Same sequence might appear multiple times
   - Different DNA sequences can encode same amino acid sequence
   - We want unique sequences with total counts

4. **What does `df.groupby().sum()` do?**
   - Groups rows with same values
   - Sums numeric columns
   - Like pivot tables in Excel!

---

## ✅ What You Need to Do

### Step 1: Filter Sequences
```bash
cd Day_03_Clean_Data
python3 filter_sequences.py
```

**What this script does:**
- Filters to productive sequences only
- Removes sequences with invalid amino acids
- Filters by sequence length
- Explains each filtering step

---

### Step 2: Aggregate Data
```bash
python3 aggregate_data.py
```

**What this script does:**
- Combines duplicate sequences
- Sums read counts for duplicates
- Creates clean, unique sequence list
- Explains grouping operations

---

## 📝 Exercises (Do These!)

### Exercise 1: Understand Filtering
```python
import pandas as pd

# Load data
file_path = "../data/DeepTCR_Cancer-master/Data/yost/data/su001_BCC_pre1_TCRB.tsv"
df = pd.read_csv(file_path, sep='\t')

# Step 1: Filter to productive
productive = df[df['sequenceStatus'] == 'In']
print(f"After productive filter: {len(productive)} sequences")

# Step 2: Filter by length (keep 10-25 amino acids)
if 'aminoAcid' in productive.columns:
    lengths = productive['aminoAcid'].str.len()
    length_filtered = productive[(lengths >= 10) & (lengths <= 25)]
    print(f"After length filter: {len(length_filtered)} sequences")
    
    # See what was removed
    removed = productive[(lengths < 10) | (lengths > 25)]
    print(f"Removed: {len(removed)} sequences")
    print(f"  Too short (<10): {(lengths < 10).sum()}")
    print(f"  Too long (>25): {(lengths > 25).sum()}")
```

**Questions:**
- Why filter by length? (Very short/long sequences are unusual)
- What percentage of sequences pass the length filter?
- Should we keep or remove unusual sequences?

---

### Exercise 2: Remove Invalid Amino Acids
```python
import pandas as pd

# Valid amino acids (20 standard ones)
valid_aa = set('ACDEFGHIKLMNPQRSTVWY')

# Load and filter
file_path = "../data/DeepTCR_Cancer-master/Data/yost/data/su001_BCC_pre1_TCRB.tsv"
df = pd.read_csv(file_path, sep='\t')
productive = df[df['sequenceStatus'] == 'In']

# Check for invalid sequences
if 'aminoAcid' in productive.columns:
    # Check each sequence
    # .apply() applies a function to each row
    # lambda x: ... is a small function
    # all(c in valid_aa for c in str(x)) checks if all characters are valid
    valid_mask = productive['aminoAcid'].apply(
        lambda x: all(c in valid_aa for c in str(x))
    )
    
    valid_sequences = productive[valid_mask]
    invalid_sequences = productive[~valid_mask]
    
    print(f"Valid sequences: {len(valid_sequences)}")
    print(f"Invalid sequences: {len(invalid_sequences)}")
    
    if len(invalid_sequences) > 0:
        print("\nExample invalid sequences:")
        print(invalid_sequences[['aminoAcid']].head())
```

**Questions:**
- What makes a sequence invalid? (Contains characters that aren't amino acids)
- How many invalid sequences are there? (Usually very few)
- Should we keep or remove them? (Remove - they're errors)

---

### Exercise 3: Aggregate Duplicates
```python
import pandas as pd

# Load and basic filter
file_path = "../data/DeepTCR_Cancer-master/Data/yost/data/su001_BCC_pre1_TCRB.tsv"
df = pd.read_csv(file_path, sep='\t')
productive = df[df['sequenceStatus'] == 'In']

# Before aggregation
print(f"Before aggregation: {len(productive)} rows")

# Aggregate by sequence, V gene, and J gene
# This combines rows with same aminoAcid, vGeneName, jGeneName
# And sums the counts
count_col = 'count (templates/reads)' if 'count (templates/reads)' in productive.columns else 'templates'

if 'aminoAcid' in productive.columns and count_col in productive.columns:
    # Group by sequence + V gene + J gene
    # Sum the counts
    df_agg = productive.groupby(['aminoAcid', 'vGeneName', 'jGeneName']).agg({
        count_col: 'sum'  # Sum the counts
    }).reset_index()
    
    print(f"After aggregation: {len(df_agg)} rows")
    print(f"Reduction: {len(productive) - len(df_agg)} duplicate rows removed")
    print(f"Percentage reduction: {(1 - len(df_agg)/len(productive))*100:.1f}%")
```

**Questions:**
- Why might the same sequence appear multiple times? (Different DNA sequences can encode same amino acid)
- What does `.groupby().agg({'column': 'sum'})` do? (Groups and sums)
- Why do we group by sequence + V gene + J gene? (All three together make it unique)

---

## 🎓 Key Concepts Explained

### What is Data Cleaning?
- **Purpose:** Remove errors and prepare data for analysis
- **Why:** Bad data = bad results
- **Steps:** Filter, validate, aggregate

### What is Filtering?
- **Purpose:** Keep only rows that meet criteria
- **Syntax:** `df[df['column'] == 'value']`
- **Think:** Like filtering in Excel

### What is Aggregation?
- **Purpose:** Combine duplicate rows
- **Syntax:** `df.groupby('columns').agg({'column': 'sum'})`
- **Think:** Like pivot tables - group and sum

### What is `.apply()`?
- **Purpose:** Apply a function to each row/column
- **Syntax:** `df['column'].apply(function)`
- **Think:** Like applying a formula to each cell

---

## ✅ Checklist: Did You Complete Everything?

- [ ] Ran `filter_sequences.py` successfully
- [ ] Ran `aggregate_data.py` successfully
- [ ] Did Exercise 1 (understood filtering)
- [ ] Did Exercise 2 (removed invalid sequences)
- [ ] Did Exercise 3 (aggregated duplicates)
- [ ] Understand why we filter data
- [ ] Understand what `.groupby()` does
- [ ] Understand what `.apply()` does

---

## 🎉 You're Done with Day 3!

**What you accomplished:**
- ✅ Filtered data to remove bad sequences
- ✅ Validated sequences (removed invalid amino acids)
- ✅ Aggregated duplicate sequences
- ✅ Created clean data ready for analysis

**Next Step:** Go to `Day_04_Understand_Data/` folder and read `README.md`

**Remember:**
- Clean data = better results
- Filtering removes bad data
- Aggregation combines duplicates
- You're using pandas operations you know!

---

## 📝 Notes Section

Write down:
- How many sequences were removed at each step
- Why each filtering step is important
- What you learned about data cleaning
- Questions you still have

---

*Great progress! Keep going! 🚀*
