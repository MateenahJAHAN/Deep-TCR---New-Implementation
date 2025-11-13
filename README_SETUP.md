# DeepTCR Project Setup Guide

## Quick Start

This guide will help you set up the DeepTCR learning project step by step.

## What You Need

- Python 3.7 or higher
- Internet connection (to download data and packages)
- About 100 MB of disk space

## Setup Steps

### Step 1: Download and Extract Data

The data has already been downloaded for you! It's in the `DeepTCR_Cancer-master` directory.

If you need to download it again:
1. Go to: https://zenodo.org/record/6590167
2. Download: `DeepTCR_Cancer-master.zip`
3. Extract it in this directory

### Step 2: Run the Setup Script

The easiest way to set everything up is to run the setup script:

```bash
python setup_project.py
```

This script will:
- ✓ Check if all data files are present
- ✓ Install required Python packages
- ✓ Test that everything works correctly
- ✓ Show you what to do next

**What the script does (explained simply):**
- It checks if the data files exist (like checking if ingredients are in your kitchen)
- It installs Python packages you need (like installing apps on your phone)
- It tests loading one data file to make sure everything works (like testing if a recipe works)

### Step 3: Verify Setup

After running the setup script, you should see:
```
✓ All data files are present!
✓ All packages installed and working correctly!
✓ Setup test passed! Everything is working correctly.
```

If you see any errors, the script will tell you what's wrong and how to fix it.

## Manual Setup (Alternative)

If you prefer to set up manually:

### 1. Install Python Packages

```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install pandas numpy matplotlib seaborn scikit-learn
```

### 2. Verify Data Files

Check that these directories exist:
- `DeepTCR_Cancer-master/Data/yost/data/` (should contain .tsv files)
- `DeepTCR_Cancer-master/Data/yost/response.csv` (patient labels)

### 3. Test Setup

Try running the explorer script:
```bash
python tcr_explorer.py
```

If it runs without errors, you're all set!

## Project Structure

```
/workspace/
├── setup_project.py          # Setup script (run this first!)
├── requirements.txt          # Python package requirements
├── tcr_explorer.py          # Example script to explore data
├── LEARNING_ROADMAP.md      # Your learning guide
├── pandas_to_deeptcr_guide.md  # Bridge pandas knowledge
├── dataset_exploration_guide.md # Data structure guide
├── deeptcr_architecture.md  # Model architecture guide
└── DeepTCR_Cancer-master/   # Data directory
    └── Data/
        └── yost/
            ├── data/        # Patient TCR files (.tsv)
            └── response.csv # Patient labels
```

## What Each File Does

### `setup_project.py`
- **What it does:** Sets up everything automatically
- **When to use:** Run this first to get started
- **How it works:** Checks files, installs packages, tests setup

### `tcr_explorer.py`
- **What it does:** Shows you how to load and explore TCR data
- **When to use:** After setup, to see what the data looks like
- **How it works:** Uses pandas to load files, calculates statistics, creates plots

### `requirements.txt`
- **What it does:** Lists all Python packages needed
- **When to use:** If you want to install packages manually
- **How it works:** pip reads this file and installs everything listed

### Learning Guides
- **LEARNING_ROADMAP.md:** Your complete learning path (start here!)
- **pandas_to_deeptcr_guide.md:** Connects pandas knowledge to DeepTCR
- **dataset_exploration_guide.md:** Explains the data structure
- **deeptcr_architecture.md:** Explains how the model works

## Common Issues

### Issue: "File not found" error
**Solution:** Make sure `DeepTCR_Cancer-master.zip` is extracted in the current directory

### Issue: "Module not found" error
**Solution:** Run `pip install -r requirements.txt` to install packages

### Issue: Setup script fails
**Solution:** Check the error message - it will tell you what's missing

## Next Steps

After setup is complete:

1. **Read the guides:** Start with `LEARNING_ROADMAP.md`
2. **Run the explorer:** Try `python tcr_explorer.py`
3. **Explore the data:** Modify the explorer script to load different patients
4. **Follow the roadmap:** Work through the week-by-week plan

## Getting Help

If you get stuck:
1. Check the error message - it usually tells you what's wrong
2. Read the relevant guide file
3. Look at the example code in `tcr_explorer.py`
4. Make sure all files are in the right place

## Summary

**To set up the project:**
```bash
python setup_project.py
```

**To explore the data:**
```bash
python tcr_explorer.py
```

**To start learning:**
Read `LEARNING_ROADMAP.md`

That's it! You're ready to start learning about DeepTCR! 🚀
