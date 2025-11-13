# Student Errors and Fixes Guide

## Overview
This document lists common errors students encounter when executing notebooks, along with fixes and clarifications.

---

## Critical Issues Found

### Issue 1: File Path Errors (Days 2-4)

**Error Students See:**
```
FileNotFoundError: [Errno 2] No such file or directory: '../data/...'
```

**Why It Happens:**
- Path assumes notebook is in `Day_X/` folder
- In Colab, paths are different
- Students might be in wrong directory

**Fix Needed:**
Add to Day 2, Cell 3 (file path setup):
```python
# Check if directory exists
if not data_dir.exists():
    print("⚠️ WARNING: Directory not found!")
    print("  Trying alternative paths...")
    alt_paths = [
        Path("data/DeepTCR_Cancer-master/Data/yost/data"),
        Path("../data/DeepTCR_Cancer-master/Data/yost/data"),
        Path("./data/DeepTCR_Cancer-master/Data/yost/data")
    ]
    for alt_path in alt_paths:
        if alt_path.exists():
            data_dir = alt_path
            print(f"✓ Found data at: {alt_path}")
            break
    else:
        print("✗ ERROR: Data directory not found!")
        print("  For Colab users: Upload data files first!")
```

---

### Issue 2: AttributeError from None (Days 2-7)

**Error Students See:**
```
AttributeError: 'NoneType' object has no attribute 'shape'
```

**Why It Happens:**
- TODO cells have `df = None`
- Subsequent code tries to use `df.shape` or `len(df)`
- Student hasn't completed TODO yet

**Fix Needed:**
Wrap all code that uses `df` in checks:
```python
if df is not None:
    print(f"Shape: {df.shape}")
    print(f"Rows: {len(df):,}")
else:
    print("⚠️ Complete the TODO above first!")
    print("  Uncomment: df = pd.read_csv(file_path, sep='\\t')")
```

**Affected Cells:**
- Day 2, Cell 4 (df loading)
- Day 3, Multiple cells (filtering operations)
- Day 4, Multiple cells (statistics)
- Day 5, Multiple cells (encoding)

---

### Issue 3: Column Name Errors (Days 2-3)

**Error Students See:**
```
KeyError: 'aminoAcid' or KeyError: 'frame'
```

**Why It Happens:**
- Column names might be different in actual files
- Students might use wrong column name
- File format might vary

**Fix Needed:**
Add column checking:
```python
# Check available columns
print("Available columns:")
print(df.columns.tolist())

# Find the right column (handle variations)
if 'aminoAcid' in df.columns:
    seq_col = 'aminoAcid'
elif 'amino_acid' in df.columns:
    seq_col = 'amino_acid'
else:
    print("⚠️ WARNING: Sequence column not found!")
    print("  Available columns:", df.columns.tolist()[:10])
```

---

### Issue 4: Import Errors (All Days)

**Error Students See:**
```
ModuleNotFoundError: No module named 'pandas'
```

**Why It Happens:**
- Packages not installed
- Wrong Python environment
- Colab needs restart after install

**Fix Needed:**
Add to Day 1:
```python
# Check if packages are installed
try:
    import pandas as pd
    print("✓ pandas installed")
except ImportError:
    print("✗ pandas not installed")
    print("  Run: pip install pandas")
    print("  In Colab: Restart runtime after installing!")
```

---

### Issue 5: Empty Data Errors (Days 3-4)

**Error Students See:**
```
ValueError: Cannot take mean of empty array
```

**Why It Happens:**
- Filtering removed all rows
- File is empty
- Wrong filter condition

**Fix Needed:**
Add data checks:
```python
if len(df) == 0:
    print("⚠️ WARNING: DataFrame is empty!")
    print("  Check your filter conditions")
    print("  Original file had rows, but filter removed all")
else:
    # Proceed with analysis
    print(f"✓ {len(df)} rows after filtering")
```

---

## Student Doubts and Clarifications Needed

### Doubt 1: "What if I get an error?"

**Add to each day:**
```markdown
## 🆘 What If I Get an Error?

**Don't panic!** Errors are normal when learning.

**Steps to fix:**
1. **Read the error message** - It usually tells you what's wrong
2. **Check the line number** - See which line caused the error
3. **Common fixes:**
   - File not found → Check file path
   - Module not found → Install package (`pip install package_name`)
   - AttributeError → Check if variable is None
   - KeyError → Check column name spelling
4. **Still stuck?** Check the "Common Errors" section below
```

### Doubt 2: "Do I need to complete all TODOs?"

**Add clarification:**
```markdown
**About TODOs:**
- TODOs are exercises for YOU to complete
- You can run cells with TODOs, but they won't work until you fill them in
- Each TODO has hints - read them carefully!
- If you're stuck, look at the example code above
```

### Doubt 3: "What if my output is different?"

**Add clarification:**
```markdown
**Your output might be different:**
- Different file → Different number of rows
- Different Python version → Slight differences OK
- As long as code runs without errors, you're good!
```

---

## Systematic Fixes Needed

### Priority 1: Critical (Breaks Execution)

1. **Day 2, Cell 4:** Add `if df is not None:` check
2. **Day 2, Cell 3:** Add path existence checking
3. **Day 3, All filtering cells:** Add `if df is not None:` checks
4. **Day 4, Statistics cells:** Add empty data checks

### Priority 2: Important (Causes Confusion)

5. **All Days:** Add "Common Errors" sections
6. **All Days:** Add "What If I Get an Error?" sections
7. **Days 2-4:** Add column name checking
8. **Day 1:** Add import verification with error messages

### Priority 3: Helpful (Improves Experience)

9. **All Days:** Add "Student Doubts" sections
10. **All Days:** Add "Troubleshooting" tips
11. **Days 5-7:** Add shape verification before operations
12. **Days 9-11:** Add DeepTCR-specific error handling

---

## Testing Checklist

For each day, verify:
- [ ] All code cells execute without errors (when TODOs completed)
- [ ] Error messages are helpful and guide students
- [ ] File paths work in both local and Colab environments
- [ ] None checks prevent AttributeErrors
- [ ] Empty data checks prevent ValueErrors
- [ ] Import errors provide installation instructions
- [ ] Column name errors provide helpful alternatives

---

## Next Steps

1. Fix Day 2 critical issues (file paths, None checks)
2. Fix Day 3 critical issues (filtering, None checks)
3. Fix Day 4 critical issues (statistics, empty data)
4. Add error handling to Days 5-11
5. Add "Common Errors" sections to all days
6. Test all days end-to-end as a student would
