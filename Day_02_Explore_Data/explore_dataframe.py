#!/usr/bin/env python3
"""
Day 2: Explore DataFrame Script
=================================

This script shows you how to explore a DataFrame using pandas operations you know.

WHAT THIS SCRIPT DOES:
1. Uses pandas operations you're familiar with
2. Filters data (productive vs non-productive)
3. Calculates basic statistics
4. Shows you sequence length distributions

HOW TO USE:
1. Make sure you're in Day_02_Explore_Data folder
2. Run: python3 explore_dataframe.py
3. Read the comments to understand each operation!

AUTHOR: Beginner-friendly DataFrame exploration script
"""

import pandas as pd
import numpy as np
from pathlib import Path

# ============================================================================
# STEP 1: Load the Data
# ============================================================================

print("="*70)
print("Loading Data")
print("="*70)

data_dir = Path("../data/DeepTCR_Cancer-master/Data/yost/data")
file_path = data_dir / "su001_BCC_pre1_TCRB.tsv"

print(f"Loading: {file_path.name}")

df = pd.read_csv(file_path, sep='\t')

print(f"✓ Loaded {len(df):,} rows, {len(df.columns)} columns")

# ============================================================================
# STEP 2: Filter to Productive Sequences
# ============================================================================

print("\n" + "="*70)
print("STEP 2: Filtering to Productive Sequences")
print("="*70)

print("\nWhat is filtering?")
print("  - Like filtering in Excel: show only rows that meet a condition")
print("  - Syntax: df[df['column'] == 'value']")
print("  - This creates a new DataFrame with only matching rows")

if 'sequenceStatus' in df.columns:
    # Count sequences by status
    print("\nBefore filtering:")
    print(df['sequenceStatus'].value_counts())
    
    # Filter to only productive sequences
    # This is like: df[df['sequenceStatus'] == 'In']
    # It means: "give me all rows where sequenceStatus equals 'In'"
    productive = df[df['sequenceStatus'] == 'In'].copy()
    
    print(f"\nAfter filtering (only 'In' frame sequences):")
    print(f"  Total sequences: {len(df):,}")
    print(f"  Productive sequences: {len(productive):,}")
    print(f"  Percentage: {len(productive)/len(df)*100:.1f}%")
    
    print("\nWhy filter to productive?")
    print("  - Productive sequences are the ones that actually work")
    print("  - Non-productive sequences are errors or don't function")
    print("  - For analysis, we usually only care about productive sequences")
else:
    print("⚠ 'sequenceStatus' column not found")
    productive = df.copy()  # Use all data if column doesn't exist

# ============================================================================
# STEP 3: Look at Sequence Lengths
# ============================================================================

print("\n" + "="*70)
print("STEP 3: Sequence Length Analysis")
print("="*70)

if 'aminoAcid' in productive.columns:
    print("\nCalculating sequence lengths:")
    print("  Using: df['column'].str.len()")
    print("  This gets the length of each string in the column")
    
    # Calculate length of each sequence
    # .str.len() applies len() to each string in the column
    lengths = productive['aminoAcid'].str.len()
    
    print("\nLength statistics:")
    print(f"  Minimum length: {lengths.min()} amino acids")
    print(f"  Maximum length: {lengths.max()} amino acids")
    print(f"  Mean length: {lengths.mean():.1f} amino acids")
    print(f"  Median length: {lengths.median():.1f} amino acids")
    
    print("\nMost common lengths:")
    # .value_counts() counts how many times each length appears
    # .head(10) shows top 10
    length_counts = lengths.value_counts().head(10)
    for length, count in length_counts.items():
        pct = (count / len(productive)) * 100
        print(f"  Length {length:2d}: {count:6,} sequences ({pct:5.2f}%)")
    
    print("\nWhat does this tell us?")
    print("  - TCR sequences are usually 10-25 amino acids long")
    print("  - Very short or very long sequences might be unusual")
    print("  - Most sequences cluster around a typical length")
else:
    print("⚠ 'aminoAcid' column not found")

# ============================================================================
# STEP 4: Look at V Gene Usage
# ============================================================================

print("\n" + "="*70)
print("STEP 4: V Gene Usage Analysis")
print("="*70)

print("\nWhat is a V gene?")
print("  - V = Variable gene segment")
print("  - Part of the TCR that varies between different T cells")
print("  - Different V genes = different T cell types")

if 'vGeneName' in productive.columns:
    print("\nCounting V gene usage:")
    print("  Using: df.groupby('column')['column'].sum()")
    print("  This groups by V gene and sums the counts")
    
    # Count how many sequences use each V gene
    # First, let's just count sequences
    v_gene_counts = productive['vGeneName'].value_counts()
    
    print(f"\nTop 10 most common V genes:")
    print("-"*70)
    for i, (gene, count) in enumerate(v_gene_counts.head(10).items(), 1):
        pct = (count / len(productive)) * 100
        print(f"  {i:2d}. {gene:20s}: {count:6,} sequences ({pct:5.2f}%)")
    
    print("\nWhat does this tell us?")
    print("  - Some V genes are used more often than others")
    print("  - This is normal - some V genes are more common")
    print("  - Different patients might have different V gene patterns")
else:
    print("⚠ 'vGeneName' column not found")

# ============================================================================
# STEP 5: Look at Read Counts
# ============================================================================

print("\n" + "="*70)
print("STEP 5: Read Count Analysis")
print("="*70)

print("\nWhat is a read count?")
print("  - How many times this sequence was seen in the sequencing")
print("  - Higher count = sequence is more common")
print("  - Lower count = sequence is rare")

count_col = None
for col in ['count (templates/reads)', 'templates', 'count']:
    if col in productive.columns:
        count_col = col
        break

if count_col:
    print(f"\nUsing column: {count_col}")
    
    # Calculate statistics on read counts
    counts = productive[count_col]
    
    print("\nRead count statistics:")
    print(f"  Minimum: {counts.min():,}")
    print(f"  Maximum: {counts.max():,}")
    print(f"  Mean: {counts.mean():.1f}")
    print(f"  Median: {counts.median():.1f}")
    print(f"  Total reads: {counts.sum():,}")
    
    # Find most common sequences
    print("\nTop 5 most common sequences:")
    print("  (Using df.nlargest(5, 'column') - like sorting and taking top 5)")
    top5 = productive.nlargest(5, count_col)
    
    print("-"*70)
    for i, (idx, row) in enumerate(top5.iterrows(), 1):
        seq = row.get('aminoAcid', 'N/A')[:20]  # Show first 20 chars
        count = row[count_col]
        pct = (count / counts.sum()) * 100
        print(f"  {i}. {seq:20s}... : {count:6,} reads ({pct:.3f}%)")
    
    print("\nWhat does this tell us?")
    print("  - A few sequences dominate (high clonality)")
    print("  - Most sequences are rare (low frequency)")
    print("  - This is typical for immune repertoires")
else:
    print("⚠ Read count column not found")

# ============================================================================
# STEP 6: Basic DataFrame Operations Summary
# ============================================================================

print("\n" + "="*70)
print("SUMMARY: Pandas Operations You Used Today")
print("="*70)

print("""
Operations you learned/used:

1. df[df['column'] == 'value']
   - Filter rows where column equals value
   - Like filtering in Excel

2. df['column'].value_counts()
   - Count how many times each value appears
   - Like making a frequency table

3. df['column'].str.len()
   - Get length of each string in column
   - Applies len() to each value

4. df['column'].mean(), .median(), .min(), .max()
   - Calculate statistics on numeric columns
   - Like Excel's AVERAGE(), MEDIAN(), etc.

5. df.nlargest(n, 'column')
   - Get top N rows by column value
   - Like sorting and taking top N

6. df.groupby('column')
   - Group rows by column value
   - Like pivot tables in Excel

All of these are pandas operations you might already know!
The data is just a DataFrame - use what you know!
""")

print("="*70)
print("Day 2 - Step 2 Complete! ✓")
print("="*70)
