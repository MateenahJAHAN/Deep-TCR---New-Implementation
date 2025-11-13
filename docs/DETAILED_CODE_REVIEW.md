# Detailed Code Review - Specific Issues and Fixes
## Day-by-Day Code Analysis

---

## Day 1: Setup ⚙️

### Issue 1: Incomplete TODO in Step 2
**Location:** Step 2 - Check Which Packages Are Installed  
**Problem:**
```python
# TODO: Check numpy
# Copy the pattern above:
# try:
#     import numpy as np
#     print("✓ numpy is installed")
#     print(f"  Version: {np.__version__}")
# except ImportError:
#     print("✗ numpy is NOT installed")
# Write your code here:
```
**Issue:** Instructions are unclear - should student uncomment or write new code?  
**Fix:**
```python
# TODO: Check numpy
# Uncomment the code below and run it:
try:
    import numpy as np
    print("✓ numpy is installed")
    print(f"  Version: {np.__version__}")
except ImportError:
    print("✗ numpy is NOT installed")
```

### Issue 2: Missing Validation in Step 6
**Location:** Step 6 - Test Loading One File  
**Problem:**
```python
df = None  # Replace None with your code
# ... later code uses df without checking if it's None
```
**Issue:** If student doesn't complete TODO, later code fails  
**Fix:**
```python
# TODO: Load the file using pandas
# Hint: pd.read_csv(test_file, sep='\t', nrows=5)
df = None  # Replace None with your code

# Validation check
if df is None:
    print("⚠️ Please complete the TODO above to load the file!")
    print("   Example: df = pd.read_csv(test_file, sep='\\t', nrows=5)")
else:
    # Continue with rest of code
    print(f"✓ Successfully loaded file!")
    print(f"  Shape: {df.shape}")
```

---

## Day 2: Explore Data 🔍

### Issue 1: Duplicate Print Statements
**Location:** Step 1 - Load One File  
**Problem:** Print statements appear twice in the same cell  
**Fix:** Remove duplicate print statements

### Issue 2: Missing Error Handling
**Location:** Step 2 - Load TSV File  
**Problem:**
```python
df = None  # Replace None with your code
# ... later code assumes df is loaded
```
**Issue:** No check if df was actually loaded  
**Fix:**
```python
# TODO: Load the TSV file using pandas
df = None  # Replace None with your code

# Validation
if df is None:
    print("⚠️ Please complete the TODO above!")
    print("   Example: df = pd.read_csv(file_path, sep='\\t')")
    raise ValueError("DataFrame not loaded - please complete TODO")
```

### Issue 3: Column Name Assumptions
**Location:** Multiple steps  
**Problem:** Code assumes specific column names exist  
**Fix:**
```python
# Check if required columns exist
required_cols = ['aminoAcid', 'sequenceStatus', 'vGeneName']
missing = [col for col in required_cols if col not in df.columns]
if missing:
    print(f"⚠️ Missing columns: {missing}")
    print(f"Available columns: {list(df.columns)}")
    print("Note: Column names might differ in your data file")
```

---

## Day 3: Clean Data 🧹

### Issue 1: CRITICAL BUG - starting_count Not Defined
**Location:** Step 1 - Load Data  
**Problem:**
```python
df = None  # Replace None with your code
# ... later ...
print(f"✓ Loaded {starting_count:,} sequences")  # ERROR: starting_count not defined!
```
**Issue:** Variable used before definition  
**Fix:**
```python
# TODO: Load the file
df = pd.read_csv(file_path, sep='\t')

# Define starting_count AFTER loading
starting_count = len(df)
print(f"✓ Loaded {starting_count:,} sequences")
print(f"  This is the RAW data - includes errors and duplicates")
```

### Issue 2: Incomplete Code in Step 2
**Location:** Step 2 - Filter to Productive Sequences  
**Problem:**
```python
productive = None  # Replace None with your code
# ... later code uses productive without checking
```
**Fix:**
```python
# TODO: Filter to only 'In' frame sequences
productive = None  # Replace None with your code

# Validation
if productive is None:
    print("⚠️ Please complete the TODO above!")
    print("   Example: productive = df[df['sequenceStatus'] == 'In']")
    raise ValueError("Productive DataFrame not created")
```

### Issue 3: Complex Lambda Function
**Location:** Step 3 - Remove Invalid Amino Acids  
**Problem:**
```python
is_valid = None  # Replace None with your code
# Hint: Use .apply() with a lambda function
# The function should check: all(c in valid_aa for c in str(x))
```
**Issue:** Lambda with nested comprehension is advanced  
**Fix:** Provide helper function:
```python
def is_valid_sequence(seq):
    """Check if sequence contains only valid amino acids"""
    seq_str = str(seq)
    return all(c in valid_aa for c in seq_str)

# TODO: Check each sequence for invalid characters
is_valid = productive['aminoAcid'].apply(is_valid_sequence)
```

### Issue 4: Groupby Complexity
**Location:** Step 5 - Aggregate Duplicate Sequences  
**Problem:** Groupby with multiple columns and agg is complex  
**Fix:** Add step-by-step explanation:
```python
# Step 1: Group by sequence + V gene + J gene
# This groups rows that have the same aminoAcid, vGeneName, and jGeneName
grouped = df_clean.groupby(['aminoAcid', 'vGeneName', 'jGeneName'])

# Step 2: Sum the counts for each group
# This adds up the counts for duplicate sequences
df_aggregated = grouped.agg({'count (templates/reads)': 'sum'})

# Step 3: Reset index to make grouped columns regular columns again
df_aggregated = df_aggregated.reset_index()
```

---

## Day 4: Understand Data 📊

### Potential Issues (Need Full Review):
1. **File Loading Loop** - Need to verify loop works correctly
2. **Response CSV** - Need to ensure students know where response.csv is
3. **Statistics Calculations** - Need to verify numpy operations are correct

### Suggested Fixes:
```python
# Add helper function for loading cleaned data
def load_cleaned_patient(file_path):
    """Load and clean a patient file"""
    df = pd.read_csv(file_path, sep='\t')
    # Apply all cleaning steps from Day 3
    # ... (reuse Day 3 code)
    return df_cleaned

# Add path validation
response_file = Path("../data/DeepTCR_Cancer-master/Data/yost/response.csv")
if not response_file.exists():
    print("⚠️ response.csv not found!")
    print("   Expected location: data/DeepTCR_Cancer-master/Data/yost/response.csv")
```

---

## Day 5: Encode Sequences 🔢

### Potential Issues:
1. **Complexity** - Encoding is conceptually difficult
2. **Shape Confusion** - Students might struggle with array shapes
3. **Multiple Steps** - Many encoding steps might be overwhelming

### Suggested Improvements:
```python
# Add shape checking at each step
print(f"Before encoding: {len(sequences)} sequences")
encoded = encode_sequences(sequences)
print(f"After encoding: {encoded.shape}")
print(f"  Shape meaning: (num_sequences, max_length, num_amino_acids)")

# Add visual example
example_seq = "CASSLAPG"
example_encoded = encode_sequence(example_seq)
print(f"\nExample:")
print(f"  Sequence: {example_seq}")
print(f"  Encoded shape: {example_encoded.shape}")
print(f"  First 3 positions:")
for i in range(3):
    print(f"    Position {i}: {example_encoded[i]}")
```

---

## General Issues Across All Days

### Issue 1: Path Handling
**Problem:** Relative paths (`../data/...`) don't work if notebook is run from different directory  
**Solution:** Create helper function:
```python
def find_data_dir():
    """Find data directory, trying multiple paths"""
    from pathlib import Path
    possible_paths = [
        Path("../data/DeepTCR_Cancer-master/Data/yost/data"),
        Path("data/DeepTCR_Cancer-master/Data/yost/data"),
        Path("./data/DeepTCR_Cancer-master/Data/yost/data"),
        Path(__file__).parent.parent / "data" / "DeepTCR_Cancer-master" / "Data" / "yost" / "data",
    ]
    for path in possible_paths:
        if path.exists():
            return path
    raise FileNotFoundError(
        "Data directory not found! Tried:\n" + 
        "\n".join(f"  - {p}" for p in possible_paths)
    )
```

### Issue 2: Missing Error Handling
**Problem:** Many cells don't handle errors gracefully  
**Solution:** Add try/except blocks:
```python
try:
    df = pd.read_csv(file_path, sep='\t')
except FileNotFoundError:
    print(f"⚠️ File not found: {file_path}")
    print("   Check that the file path is correct")
    raise
except Exception as e:
    print(f"⚠️ Error loading file: {e}")
    print("   Common issues:")
    print("     - File path is incorrect")
    print("     - File is corrupted")
    print("     - Wrong separator (should be '\\t' for TSV)")
    raise
```

### Issue 3: Column Name Validation
**Problem:** Code assumes specific column names  
**Solution:** Add validation:
```python
def validate_columns(df, required_cols, file_name="DataFrame"):
    """Validate that required columns exist"""
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        print(f"⚠️ {file_name} is missing columns: {missing}")
        print(f"Available columns: {list(df.columns)}")
        print("\nPossible fixes:")
        print("  1. Check if column names are different in your data")
        print("  2. Check if you're using the correct data file")
        raise ValueError(f"Missing required columns: {missing}")
    return True
```

### Issue 4: TODO Completion Validation
**Problem:** No way to check if student completed TODOs  
**Solution:** Add validation functions:
```python
def validate_not_none(value, name, hint=None):
    """Validate that a value is not None"""
    if value is None:
        print(f"⚠️ {name} is None!")
        print("   Please complete the TODO above")
        if hint:
            print(f"   Hint: {hint}")
        raise ValueError(f"{name} not set - please complete TODO")
    return True

# Usage:
validate_not_none(df, "DataFrame", "df = pd.read_csv(file_path, sep='\\t')")
```

---

## Recommended Fixes Priority

### High Priority (Critical Bugs):
1. ✅ **Day 3:** Fix `starting_count` not defined bug
2. ✅ **Day 2:** Remove duplicate print statements
3. ✅ **All Days:** Add validation for TODO completion
4. ✅ **All Days:** Improve path handling

### Medium Priority (Improves Experience):
1. ✅ **Day 3:** Simplify lambda function with helper
2. ✅ **Day 3:** Add step-by-step groupby explanation
3. ✅ **All Days:** Add column name validation
4. ✅ **All Days:** Add error handling

### Low Priority (Nice to Have):
1. ✅ **All Days:** Add more visual examples
2. ✅ **All Days:** Add shape checking/printing
3. ✅ **All Days:** Add troubleshooting sections
4. ✅ **All Days:** Add expected output examples

---

## Testing Checklist

For each notebook, verify:
- [ ] All code cells can run without errors (if TODOs are completed)
- [ ] Error messages are helpful if TODOs are not completed
- [ ] Path handling works from different directories
- [ ] Column names are validated
- [ ] Error handling provides useful feedback
- [ ] Code works with actual data files
- [ ] Output matches expected results

---

## Summary

**Critical Bugs Found:** 1 (Day 3 starting_count)  
**Major Issues:** 5 (path handling, validation, error handling)  
**Minor Issues:** 10+ (explanations, examples, etc.)

**Overall Code Quality:** B (Good structure, but needs bug fixes and improvements)

**Recommendation:** Fix critical bugs first, then improve error handling and validation.
