#!/usr/bin/env python3
"""
Day 2: Load One File Script
============================

This script shows you how to load one patient's TCR data file.

WHAT THIS SCRIPT DOES:
1. Loads one TSV file using pandas
2. Shows you what columns exist
3. Shows you the first few rows
4. Explains what each column means

HOW TO USE:
1. Make sure you're in Day_02_Explore_Data folder
2. Run: python3 load_one_file.py
3. Read the output and comments!

AUTHOR: Beginner-friendly data loading script
"""

import pandas as pd
from pathlib import Path

# ============================================================================
# STEP 1: Find the Data File
# ============================================================================

print("="*70)
print("STEP 1: Finding the Data File")
print("="*70)

# Set the path to the data directory
# Path("../data/...") means "go up one folder, then into data folder"
data_dir = Path("../data/DeepTCR_Cancer-master/Data/yost/data")

# Check if directory exists
if not data_dir.exists():
    print(f"✗ Error: Data directory not found: {data_dir}")
    print("Make sure data is extracted in the correct location!")
    exit(1)

print(f"✓ Found data directory: {data_dir}")

# List some files to see what's available
files = list(data_dir.glob("*.tsv"))
print(f"✓ Found {len(files)} TSV files")

# Show first 5 files as examples
print("\nExample files:")
for i, f in enumerate(files[:5], 1):
    print(f"  {i}. {f.name}")

# Choose one file to work with
# We'll use su001_BCC_pre1_TCRB.tsv
# This means: Patient su001, BCC tumor, pre-treatment, sample 1
file_path = data_dir / "su001_BCC_pre1_TCRB.tsv"

print(f"\n✓ Selected file: {file_path.name}")
print("  Patient: su001")
print("  Tumor type: BCC (Basal Cell Carcinoma)")
print("  Timepoint: pre1 (pre-treatment, sample 1)")

# ============================================================================
# STEP 2: Load the File Using Pandas
# ============================================================================

print("\n" + "="*70)
print("STEP 2: Loading the File")
print("="*70)

print(f"\nLoading file: {file_path.name}")
print("Using: pd.read_csv(file_path, sep='\\t')")
print("\nWhy sep='\\t'?")
print("  - TSV files use TABS to separate values")
print("  - CSV files use COMMAS to separate values")
print("  - sep='\\t' tells pandas: 'use tabs, not commas!'")

try:
    # Load the file
    # This is like opening an Excel file, but in Python
    df = pd.read_csv(file_path, sep='\t')
    
    print(f"\n✓ Successfully loaded file!")
    print(f"  Total rows: {len(df):,}")
    print(f"  Total columns: {len(df.columns)}")
    
except Exception as e:
    print(f"\n✗ Error loading file: {e}")
    exit(1)

# ============================================================================
# STEP 3: See What Columns Exist
# ============================================================================

print("\n" + "="*70)
print("STEP 3: Understanding the Columns")
print("="*70)

print(f"\nThis file has {len(df.columns)} columns.")
print("\nAll column names:")
for i, col in enumerate(df.columns, 1):
    print(f"  {i:2d}. {col}")

# Explain important columns
print("\n" + "-"*70)
print("IMPORTANT COLUMNS EXPLAINED:")
print("-"*70)

important_cols = {
    'aminoAcid': 'The TCR sequence (the actual barcode - string of amino acids)',
    'sequenceStatus': 'Is sequence "In" frame (productive) or "Out" frame (non-productive)?',
    'vGeneName': 'V gene name (which V gene segment was used)',
    'jGeneName': 'J gene name (which J gene segment was used)',
    'count (templates/reads)': 'How many times this sequence was seen (read count)',
    'frequencyCount (%)': 'What percentage of all sequences this represents',
    'cdr3Length': 'Length of the CDR3 region (part of TCR sequence)',
}

for col, explanation in important_cols.items():
    if col in df.columns:
        print(f"\n✓ {col}:")
        print(f"    {explanation}")
    else:
        print(f"\n✗ {col}: Not found in this file")

# ============================================================================
# STEP 4: Look at the First Few Rows
# ============================================================================

print("\n" + "="*70)
print("STEP 4: First Few Rows (What the Data Looks Like)")
print("="*70)

print("\nUsing df.head() to see first 5 rows:")
print("(This is like scrolling to the top of an Excel spreadsheet)")

# Show first 5 rows
# df.head() shows first 5 rows by default
# You can also use df.head(10) to show 10 rows
print("\n" + "-"*70)
print("First 5 rows:")
print("-"*70)

# Show only important columns if they exist
cols_to_show = ['aminoAcid', 'sequenceStatus', 'vGeneName', 'jGeneName', 
                'count (templates/reads)', 'frequencyCount (%)']

# Filter to columns that actually exist
existing_cols = [col for col in cols_to_show if col in df.columns]

if existing_cols:
    print(df[existing_cols].head())
else:
    # If those columns don't exist, show all columns
    print(df.head())

# ============================================================================
# STEP 5: Basic Information About the Data
# ============================================================================

print("\n" + "="*70)
print("STEP 5: Basic Information")
print("="*70)

print("\nUsing df.info() to see data types and memory usage:")
print("(This tells you what type each column is: string, number, etc.)")

# df.info() shows:
# - Number of rows
# - Number of columns
# - Column names
# - Data types (object = string, int64 = integer, float64 = decimal)
# - Memory usage
print("\n" + "-"*70)
df.info()

# ============================================================================
# STEP 6: Count Sequences by Status
# ============================================================================

print("\n" + "="*70)
print("STEP 6: Productive vs Non-Productive Sequences")
print("="*70)

if 'sequenceStatus' in df.columns:
    print("\nCounting sequences by status:")
    print("(Using df['column'].value_counts() - like making a frequency table)")
    
    status_counts = df['sequenceStatus'].value_counts()
    print("\n" + "-"*70)
    print(status_counts)
    print("-"*70)
    
    # Calculate percentages
    total = len(df)
    if 'In' in status_counts:
        productive_count = status_counts['In']
        productive_pct = (productive_count / total) * 100
        print(f"\nProductive sequences (In frame):")
        print(f"  Count: {productive_count:,}")
        print(f"  Percentage: {productive_pct:.1f}%")
    
    print(f"\nTotal sequences: {total:,}")
    print("\nWhat does this mean?")
    print("  - 'In' frame = productive sequences (these work correctly)")
    print("  - 'Out' frame = non-productive sequences (these don't work)")
    print("  - We usually only use 'In' frame sequences for analysis")
else:
    print("\n⚠ 'sequenceStatus' column not found in this file")

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "="*70)
print("SUMMARY")
print("="*70)

print(f"""
✓ Successfully loaded file: {file_path.name}
✓ Total sequences: {len(df):,}
✓ Total columns: {len(df.columns)}

What you learned:
1. How to load TSV files: pd.read_csv(file, sep='\\t')
2. How to see columns: df.columns
3. How to see first rows: df.head()
4. How to get info: df.info()
5. How to count values: df['column'].value_counts()

What this data represents:
- Each row = one TCR sequence (one T cell barcode)
- One patient = one file = one DataFrame with many rows
- Usually thousands or tens of thousands of sequences per patient!

Next steps:
- Go to explore_dataframe.py to learn more pandas operations
- Try loading different patient files
- Experiment with filtering and grouping!
""")

print("="*70)
print("Day 2 - Step 1 Complete! ✓")
print("="*70)
