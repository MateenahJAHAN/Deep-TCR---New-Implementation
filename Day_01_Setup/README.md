# Day 1: Setup ⚙️

## 🎯 Today's Goal

Get everything installed and working so you can start learning!

**Time:** 2 hours  
**Difficulty:** ⭐ Easy (just following instructions)

---

## 📚 What You'll Learn Today

- How to check if Python packages are installed
- How to install missing packages
- How to verify everything works
- What the project structure looks like

---

## 🤔 Questions to Think About (Before Starting)

1. **What Python packages do I need?**
   - Think: What will I use to read data files? (pandas)
   - What will I use for arrays? (numpy)
   - What will I use for plots? (matplotlib)

2. **How do I check if something is installed?**
   - Hint: Try `import pandas` - if it works, it's installed!

3. **What is a TSV file?**
   - Hint: CSV uses commas, TSV uses tabs
   - Think: How do I read a TSV file in pandas?

---

## ✅ What You Need to Do

### Step 1: Check Your Python Version
```bash
python3 --version
```
**Expected:** Python 3.7 or higher

**What this does:**
- Checks if Python is installed
- Shows the version number
- We need 3.7+ because newer packages require it

**If it doesn't work:**
- Install Python from python.org
- Or use your system's package manager

---

### Step 2: Run the Setup Script
```bash
# Make sure you're in the Day_01_Setup folder
cd Day_01_Setup

# Run the setup script
python3 setup_project.py
```

**What this script does:**
1. Checks if data files exist (they should already be downloaded!)
2. Checks which Python packages are installed
3. Installs missing packages automatically
4. Tests that everything works

**What you'll see:**
- ✓ marks for things that work
- ✗ marks for things that need fixing
- Instructions on what to do next

---

### Step 3: Test Your Setup
```bash
# Run the test script
python3 test_setup.py
```

**What this does:**
- Tries to import all packages
- Tries to load one data file
- Shows you what the data looks like

**If everything works:**
- You'll see "✓ All tests passed!"
- You're ready for Day 2!

---

## 📝 Exercises (Do These!)

### Exercise 1: Check Packages Manually
```python
# Open Python and try these:
python3

# Then type:
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split

# If no errors, everything is installed!
```

**What you're doing:**
- Importing packages (like loading tools into your toolbox)
- If no error appears, the package is installed correctly

---

### Exercise 2: Explore the Data Directory
```python
# In Python:
import os
from pathlib import Path

# Find the data directory
data_dir = Path("../data/DeepTCR_Cancer-master/Data/yost/data")

# List files
files = list(data_dir.glob("*.tsv"))
print(f"Found {len(files)} patient files")

# Show first 5 files
for f in files[:5]:
    print(f.name)
```

**What you're doing:**
- Finding where the data files are
- Counting how many files exist
- Seeing what the filenames look like

**Questions to think about:**
- What do the filenames tell you? (patient ID, sample type, timepoint)
- How many patients do we have data for?

---

### Exercise 3: Read One File (Just Peek!)
```python
import pandas as pd

# Load one file (just first 5 rows to see what it looks like)
file_path = "../data/DeepTCR_Cancer-master/Data/yost/data/su001_BCC_pre1_TCRB.tsv"
df = pd.read_csv(file_path, sep='\t', nrows=5)  # nrows=5 means "only read 5 rows"

# See what it looks like
print(df.head())
print(f"\nColumns: {list(df.columns)}")
print(f"Shape: {df.shape}")
```

**What you're doing:**
- Reading a TSV file (note: `sep='\t'` means "use tabs as separator")
- Looking at the first few rows
- Seeing what columns exist

**Questions to think about:**
- What does each column mean?
- What is "aminoAcid"? (It's the TCR sequence!)
- What is "sequenceStatus"? (Tells if sequence is "In" frame or "Out")

---

## 🎓 Key Concepts Explained

### What is `pip`?
- **pip** = Python package installer
- Like an app store for Python packages
- `pip install pandas` = "install the pandas package"

### What is `import`?
- **import** = Load a package into your Python session
- Like opening a toolbox - you need to open it before using tools
- `import pandas as pd` = "load pandas and call it 'pd' for short"

### What is a TSV file?
- **TSV** = Tab-Separated Values
- Like CSV but uses tabs instead of commas
- `pd.read_csv(file, sep='\t')` = "read TSV file"

---

## ✅ Checklist: Did You Complete Everything?

- [ ] Checked Python version (3.7+)
- [ ] Ran `setup_project.py` successfully
- [ ] All packages installed (no errors)
- [ ] Ran `test_setup.py` successfully
- [ ] Did Exercise 1 (checked packages manually)
- [ ] Did Exercise 2 (explored data directory)
- [ ] Did Exercise 3 (read one file)
- [ ] Understand what TSV files are
- [ ] Understand what `import` does

---

## 🎉 You're Done with Day 1!

**What you accomplished:**
- ✅ Set up your Python environment
- ✅ Installed all required packages
- ✅ Verified everything works
- ✅ Got a first look at the data

**Next Step:** Go to `Day_02_Explore_Data/` folder and read `README.md`

**Remember:**
- If something didn't work, check the error message
- Google the error if you're stuck
- Take notes on what you learned!

---

## 📝 Notes Section

Write down:
- Any errors you encountered and how you fixed them
- What you learned about Python packages
- Questions you still have
- Anything else!

---

## 🆘 Troubleshooting

### Problem: "pip: command not found"
**Solution:** 
- Install pip: `python3 -m ensurepip --upgrade`
- Or use: `python3 -m pip install pandas`

### Problem: "Permission denied" when installing
**Solution:**
- Use: `pip install --user pandas` (installs for your user only)
- Or use virtual environment (more advanced)

### Problem: "ModuleNotFoundError"
**Solution:**
- Package isn't installed
- Run: `pip install [package_name]`
- Then try importing again

---

*Good luck! You've got this! 🚀*
