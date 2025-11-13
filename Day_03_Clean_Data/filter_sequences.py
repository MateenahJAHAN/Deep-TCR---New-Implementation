#!/usr/bin/env python3
"""
Day 3: Filter Sequences Script
================================

This script shows you how to filter and clean TCR data.

WHAT THIS SCRIPT DOES:
1. Filters to productive sequences only
2. Removes sequences with invalid amino acids
3. Filters by sequence length
4. Explains each filtering step

HOW TO USE:
1. Make sure you're in Day_03_Clean_Data folder
2. Run: python3 filter_sequences.py
3. Read the comments to understand each step!

AUTHOR: Beginner-friendly data cleaning script
"""

import pandas as pd
from pathlib import Path

# ============================================================================
# STEP 1: Load Data
# ============================================================================

print("="*70)
print("STEP 1: Loading Data")
print("="*70)

data_dir = Path("../data/DeepTCR_Cancer-master/Data/yost/data")
file_path = data_dir / "su001_BCC_pre1_TCRB.tsv"

print(f"Loading: {file_path.name}")
df = pd.read_csv(file_path, sep='\t')

print(f"✓ Loaded {len(df):,} sequences")
print(f"  Starting point: {len(df):,} rows")

# ============================================================================
# STEP 2: Filter to Productive Sequences
# ============================================================================

print("\n" + "="*70)
print("STEP 2: Filter to Productive Sequences Only")
print("="*70)

print("\nWhat are productive sequences?")
print("  - 'In' frame = productive (sequence works correctly)")
print("  - 'Out' frame = non-productive (sequence doesn't work)")
print("  - We only want sequences that actually function!")

if 'sequenceStatus' in df.columns:
    # Count before filtering
    print("\nBefore filtering:")
    status_counts = df['sequenceStatus'].value_counts()
    print(status_counts)
    
    # Filter to only 'In' frame sequences
    # This is like: df[df['sequenceStatus'] == 'In']
    # It means: "give me all rows where sequenceStatus equals 'In'"
    df_filtered = df[df['sequenceStatus'] == 'In'].copy()
    
    print(f"\nAfter filtering (only 'In' frame):")
    print(f"  Remaining: {len(df_filtered):,} sequences")
    print(f"  Removed: {len(df) - len(df_filtered):,} sequences")
    print(f"  Percentage kept: {len(df_filtered)/len(df)*100:.1f}%")
    
    print("\nWhy filter to productive?")
    print("  - Non-productive sequences are errors or don't function")
    print("  - They would confuse our analysis")
    print("  - We only care about sequences that actually work")
else:
    print("⚠ 'sequenceStatus' column not found - skipping this step")
    df_filtered = df.copy()

# ============================================================================
# STEP 3: Remove Sequences with Invalid Amino Acids
# ============================================================================

print("\n" + "="*70)
print("STEP 3: Remove Invalid Amino Acids")
print("="*70)

print("\nWhat are valid amino acids?")
print("  - There are 20 standard amino acids")
print("  - Letters: A, C, D, E, F, G, H, I, K, L, M, N, P, Q, R, S, T, V, W, Y")
print("  - Any other characters are invalid (errors)")

# Define valid amino acids
valid_aa = set('ACDEFGHIKLMNPQRSTVWY')
print(f"\nValid amino acids: {len(valid_aa)}")
print(f"  {''.join(sorted(valid_aa))}")

if 'aminoAcid' in df_filtered.columns:
    print(f"\nBefore filtering:")
    print(f"  Sequences: {len(df_filtered):,}")
    
    # Check each sequence
    # .apply() applies a function to each row
    # lambda x: ... creates a small function
    # all(c in valid_aa for c in str(x)) checks if all characters are valid
    print("\nChecking each sequence...")
    print("  Using: df['column'].apply(lambda x: all(c in valid_aa for c in str(x)))")
    print("  This checks: 'are all characters in this sequence valid amino acids?'")
    
    valid_mask = df_filtered['aminoAcid'].apply(
        lambda x: all(c in valid_aa for c in str(x))
    )
    
    # Filter to only valid sequences
    df_valid = df_filtered[valid_mask].copy()
    df_invalid = df_filtered[~valid_mask]
    
    print(f"\nAfter filtering:")
    print(f"  Valid sequences: {len(df_valid):,}")
    print(f"  Invalid sequences removed: {len(df_invalid):,}")
    
    if len(df_invalid) > 0:
        print(f"\nExample invalid sequences (showing why they're invalid):")
        for idx, row in df_invalid.head(5).iterrows():
            seq = row['aminoAcid']
            invalid_chars = [c for c in seq if c not in valid_aa]
            print(f"  '{seq}' - invalid characters: {invalid_chars}")
    
    print("\nWhy remove invalid sequences?")
    print("  - They're sequencing errors or data quality issues")
    print("  - They would cause problems in later analysis")
    print("  - We only want clean, valid sequences")
else:
    print("⚠ 'aminoAcid' column not found - skipping this step")
    df_valid = df_filtered.copy()

# ============================================================================
# STEP 4: Filter by Sequence Length
# ============================================================================

print("\n" + "="*70)
print("STEP 4: Filter by Sequence Length")
print("="*70)

print("\nWhat is a typical TCR sequence length?")
print("  - Usually 10-25 amino acids")
print("  - Very short (<10) or very long (>25) sequences are unusual")
print("  - They might be errors or rare cases")

if 'aminoAcid' in df_valid.columns:
    # Calculate lengths
    lengths = df_valid['aminoAcid'].str.len()
    
    print(f"\nBefore filtering:")
    print(f"  Sequences: {len(df_valid):,}")
    print(f"  Min length: {lengths.min()}")
    print(f"  Max length: {lengths.max()}")
    print(f"  Mean length: {lengths.mean():.1f}")
    
    # Filter to typical lengths (10-25)
    # This is like: df[(condition1) & (condition2)]
    # It means: "keep rows where length >= 10 AND length <= 25"
    length_mask = (lengths >= 10) & (lengths <= 25)
    df_length_filtered = df_valid[length_mask].copy()
    df_too_short = df_valid[lengths < 10]
    df_too_long = df_valid[lengths > 25]
    
    print(f"\nAfter filtering (length 10-25):")
    print(f"  Kept: {len(df_length_filtered):,} sequences")
    print(f"  Removed (too short <10): {len(df_too_short):,}")
    print(f"  Removed (too long >25): {len(df_too_long):,}")
    print(f"  Percentage kept: {len(df_length_filtered)/len(df_valid)*100:.1f}%")
    
    if len(df_too_short) > 0:
        print(f"\nExample too-short sequences:")
        for idx, row in df_too_short.head(3).iterrows():
            seq = row['aminoAcid']
            print(f"  Length {len(seq)}: '{seq}'")
    
    if len(df_too_long) > 0:
        print(f"\nExample too-long sequences:")
        for idx, row in df_too_long.head(3).iterrows():
            seq = row['aminoAcid']
            print(f"  Length {len(seq)}: '{seq[:30]}...' (showing first 30 chars)")
    
    print("\nWhy filter by length?")
    print("  - Very short/long sequences are unusual")
    print("  - They might be errors or rare edge cases")
    print("  - For consistency, we keep typical lengths")
else:
    print("⚠ 'aminoAcid' column not found - skipping this step")
    df_length_filtered = df_valid.copy()

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "="*70)
print("FILTERING SUMMARY")
print("="*70)

print(f"""
Starting point:     {len(df):,} sequences

After filtering:
  1. Productive only:    {len(df_filtered):,} sequences
  2. Valid amino acids:  {len(df_valid):,} sequences  
  3. Typical length:     {len(df_length_filtered):,} sequences

Total removed:      {len(df) - len(df_length_filtered):,} sequences
Percentage kept:    {len(df_length_filtered)/len(df)*100:.1f}%

What you learned:
1. Filtering: df[df['column'] == 'value']
2. Multiple conditions: df[(cond1) & (cond2)]
3. String operations: df['column'].str.len()
4. Apply function: df['column'].apply(function)

Next step: Aggregate duplicate sequences!
""")

print("="*70)
print("Day 3 - Step 1 Complete! ✓")
print("="*70)
