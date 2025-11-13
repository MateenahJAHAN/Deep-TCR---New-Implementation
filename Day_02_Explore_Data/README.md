# Day 2: Explore Data 🔍

## 🎯 Today's Goal

Look at one patient's TCR data file and understand what's in it!

**Time:** 2-3 hours  
**Difficulty:** ⭐⭐ Easy-Medium (using pandas you know)

---

## 📚 What You'll Learn Today

- How to load TSV files using pandas
- What columns exist in TCR-seq data
- What each column means
- How to explore a DataFrame (using pandas operations you know!)

---

## 🤔 Questions to Think About (Before Starting)

1. **What is a TSV file?**
   - CSV uses commas to separate values
   - TSV uses tabs to separate values
   - How do I read a TSV file in pandas? (Hint: `sep='\t'`)

2. **What is a TCR sequence?**
   - It's a string of amino acids (like "CASSLAPGATNEKLFF")
   - Each sequence is unique to one T cell
   - Think: Like a barcode for each immune cell

3. **What does "productive" mean?**
   - "In" frame = productive (the sequence works)
   - "Out" frame = non-productive (the sequence doesn't work)
   - We usually only care about productive sequences

4. **How many sequences does one patient have?**
   - Usually thousands or tens of thousands!
   - Each row = one TCR sequence
   - One patient = one DataFrame with many rows

---

## ✅ What You Need to Do

### Step 1: Load One File
```bash
# Make sure you're in Day_02_Explore_Data folder
cd Day_02_Explore_Data

# Run the script
python3 load_one_file.py
```

**What this script does:**
- Loads one patient's TCR data file
- Shows you what columns exist
- Shows you the first few rows
- Explains what each column means

---

### Step 2: Explore the DataFrame
```bash
# Run the exploration script
python3 explore_dataframe.py
```

**What this script does:**
- Uses pandas operations you know (`head()`, `info()`, `value_counts()`)
- Shows you how many sequences are productive vs non-productive
- Calculates basic statistics
- Explains each pandas operation

---

## 📝 Exercises (Do These!)

### Exercise 1: Load Different Files
```python
# Try loading different patient files
import pandas as pd
from pathlib import Path

data_dir = Path("../data/DeepTCR_Cancer-master/Data/yost/data")

# Load patient su001, pre-treatment, BCC tumor
file1 = data_dir / "su001_BCC_pre1_TCRB.tsv"
df1 = pd.read_csv(file1, sep='\t')
print(f"File 1: {len(df1)} sequences")

# Load patient su005, pre-treatment, BCC tumor
file2 = data_dir / "su005_BCC_pre_TCRB.tsv"
df2 = pd.read_csv(file2, sep='\t')
print(f"File 2: {len(df2)} sequences")

# Compare: Which patient has more sequences?
```

**Questions:**
- Why might different patients have different numbers of sequences?
- What does "BCC" mean? (Basal Cell Carcinoma - a type of skin cancer)
- What does "pre" mean? (Pre-treatment - before therapy)

---

### Exercise 2: Understand Column Names
```python
import pandas as pd

file_path = "../data/DeepTCR_Cancer-master/Data/yost/data/su001_BCC_pre1_TCRB.tsv"
df = pd.read_csv(file_path, sep='\t')

# Print all column names
print("All columns:")
for i, col in enumerate(df.columns, 1):
    print(f"{i}. {col}")

# Focus on important columns
important_cols = ['aminoAcid', 'sequenceStatus', 'vGeneName', 'jGeneName', 
                  'count (templates/reads)', 'frequencyCount (%)']

print("\nImportant columns:")
for col in important_cols:
    if col in df.columns:
        print(f"  ✓ {col}")
    else:
        print(f"  ✗ {col} (not found)")
```

**Questions:**
- What is `aminoAcid`? (The TCR sequence - the actual barcode!)
- What is `sequenceStatus`? (Tells if sequence is "In" or "Out" frame)
- What is `count (templates/reads)`? (How many times this sequence was seen)
- What is `frequencyCount (%)`? (What percentage of all sequences this is)

---

### Exercise 3: Filter to Productive Sequences
```python
import pandas as pd

file_path = "../data/DeepTCR_Cancer-master/Data/yost/data/su001_BCC_pre1_TCRB.tsv"
df = pd.read_csv(file_path, sep='\t')

# Count sequences by status
print("Sequence status counts:")
print(df['sequenceStatus'].value_counts())

# Filter to only productive (In frame) sequences
# This is like: df[df['column'] == 'value']
productive = df[df['sequenceStatus'] == 'In']

print(f"\nTotal sequences: {len(df)}")
print(f"Productive sequences: {len(productive)}")
print(f"Non-productive sequences: {len(df) - len(productive)}")
print(f"Percentage productive: {len(productive)/len(df)*100:.1f}%")
```

**Questions:**
- Why do we usually only use productive sequences?
- What percentage of sequences are productive? (Usually 60-80%)
- What happens to non-productive sequences? (We ignore them)

---

### Exercise 4: Look at Sequence Lengths
```python
import pandas as pd

file_path = "../data/DeepTCR_Cancer-master/Data/yost/data/su001_BCC_pre1_TCRB.tsv"
df = pd.read_csv(file_path, sep='\t')

# Filter to productive
productive = df[df['sequenceStatus'] == 'In']

# Calculate sequence lengths
# This is like: df['column'].str.len() - gets length of each string
lengths = productive['aminoAcid'].str.len()

print("Sequence length statistics:")
print(f"  Min length: {lengths.min()}")
print(f"  Max length: {lengths.max()}")
print(f"  Mean length: {lengths.mean():.1f}")
print(f"  Median length: {lengths.median():.1f}")

# Count sequences by length
print("\nMost common lengths:")
print(lengths.value_counts().head(10))
```

**Questions:**
- What is the typical TCR sequence length? (Usually 10-25 amino acids)
- Why are sequences different lengths? (Different T cells have different barcodes)
- Why might very short or very long sequences be unusual?

---

## 🎓 Key Concepts Explained

### What is `pd.read_csv()`?
- **Purpose:** Read a CSV or TSV file into a pandas DataFrame
- **Syntax:** `pd.read_csv(file_path, sep='\t')`
- **`sep='\t'`:** Use tabs as separator (for TSV files)
- **Think:** Like opening an Excel file, but in Python

### What is `df.head()`?
- **Purpose:** Show first 5 rows of DataFrame
- **Syntax:** `df.head()` or `df.head(10)` for 10 rows
- **Think:** Like scrolling to top of spreadsheet

### What is `df['column']`?
- **Purpose:** Get one column from DataFrame
- **Syntax:** `df['column_name']`
- **Think:** Like selecting a column in Excel

### What is `df[df['column'] == 'value']`?
- **Purpose:** Filter rows where column equals value
- **Syntax:** `df[df['column'] == 'value']`
- **Think:** Like filtering in Excel (show only rows where column = value)

### What is `.value_counts()`?
- **Purpose:** Count how many times each value appears
- **Syntax:** `df['column'].value_counts()`
- **Think:** Like making a frequency table

---

## ✅ Checklist: Did You Complete Everything?

- [ ] Ran `load_one_file.py` successfully
- [ ] Ran `explore_dataframe.py` successfully
- [ ] Did Exercise 1 (loaded different files)
- [ ] Did Exercise 2 (understood column names)
- [ ] Did Exercise 3 (filtered to productive sequences)
- [ ] Did Exercise 4 (looked at sequence lengths)
- [ ] Understand what a TSV file is
- [ ] Understand what `pd.read_csv()` does
- [ ] Understand what filtering means (`df[df['col'] == 'value']`)
- [ ] Understand what `.value_counts()` does

---

## 🎉 You're Done with Day 2!

**What you accomplished:**
- ✅ Loaded TCR data files using pandas
- ✅ Explored DataFrames using operations you know
- ✅ Understood what each column means
- ✅ Filtered data (productive vs non-productive)
- ✅ Calculated basic statistics

**Next Step:** Go to `Day_03_Clean_Data/` folder and read `README.md`

**Remember:**
- You're using pandas operations you already know!
- The data is just a DataFrame with many rows
- Each row = one TCR sequence
- One patient = one DataFrame

---

## 📝 Notes Section

Write down:
- What you learned about TCR data structure
- What each column means (in your own words)
- How many sequences one patient typically has
- Questions you still have
- Anything else!

---

## 🆘 Troubleshooting

### Problem: "FileNotFoundError"
**Solution:** 
- Check the file path is correct
- Make sure you're in the right directory
- Use `Path("../data/...")` to go up one folder

### Problem: "KeyError: 'column_name'"
**Solution:**
- Column name might be different (check with `df.columns`)
- Some files use different column names
- Use the column mapping function from Day 1

### Problem: "Memory error" when loading large file
**Solution:**
- Use `nrows=1000` to load only first 1000 rows for testing
- Example: `pd.read_csv(file, sep='\t', nrows=1000)`

---

*Great job! You're learning! 🚀*
