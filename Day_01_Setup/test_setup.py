#!/usr/bin/env python3
"""
Day 1: Test Setup Script
=========================

This script tests that everything is set up correctly.

WHAT THIS SCRIPT DOES:
1. Tests if all packages can be imported
2. Tests if data files can be loaded
3. Shows you what the data looks like

HOW TO USE:
1. After running setup_project.py
2. Run: python3 test_setup.py
3. If you see "✓ All tests passed!", you're ready!

AUTHOR: Beginner-friendly test script
"""

from pathlib import Path
import sys

# ============================================================================
# TEST FUNCTIONS - Each tests one thing
# ============================================================================

def test_imports():
    """
    Test if all required packages can be imported
    
    WHAT THIS DOES:
    - Tries to import each package
    - If all work, returns True
    - If any fail, returns False
    
    THINK OF IT LIKE:
    - Checking if all your tools are in your toolbox
    """
    print("="*70)
    print("TEST 1: Checking if packages can be imported")
    print("="*70)
    
    packages = {
        "pandas": "pd",
        "numpy": "np",
        "matplotlib.pyplot": "plt",
        "seaborn": "sns",
        "sklearn": None
    }
    
    all_passed = True
    
    for package, alias in packages.items():
        try:
            if alias:
                # Import with alias (like: import pandas as pd)
                exec(f"import {package} as {alias}")
            else:
                # Import without alias
                exec(f"import {package}")
            print(f"✓ {package} imported successfully")
        except ImportError as e:
            print(f"✗ {package} failed to import: {e}")
            all_passed = False
    
    return all_passed


def test_load_data():
    """
    Test if we can load a data file
    
    WHAT THIS DOES:
    - Tries to load one patient's TCR data file
    - Shows you what it looks like
    - Verifies the file format is correct
    
    THINK OF IT LIKE:
    - Opening a book to see if you can read it
    """
    print("\n" + "="*70)
    print("TEST 2: Testing if data files can be loaded")
    print("="*70)
    
    try:
        import pandas as pd
        
        # Find data directory
        data_dir = Path("../data/DeepTCR_Cancer-master/Data/yost/data")
        
        if not data_dir.exists():
            print(f"✗ Data directory not found: {data_dir}")
            return False
        
        # Find one file
        files = list(data_dir.glob("*.tsv"))
        if not files:
            print(f"✗ No TSV files found in {data_dir}")
            return False
        
        test_file = files[0]
        print(f"\nTesting with file: {test_file.name}")
        
        # Try to load it
        # sep='\t' means "use tabs as separator" (TSV format)
        # nrows=10 means "only read first 10 rows" (faster for testing)
        df = pd.read_csv(test_file, sep='\t', nrows=10)
        
        print(f"✓ Successfully loaded file!")
        print(f"  - Rows loaded: {len(df)}")
        print(f"  - Columns: {len(df.columns)}")
        print(f"  - File size: {test_file.stat().st_size / 1024:.1f} KB")
        
        # Show column names
        print(f"\n  Column names (first 10):")
        for i, col in enumerate(df.columns[:10], 1):
            print(f"    {i}. {col}")
        if len(df.columns) > 10:
            print(f"    ... and {len(df.columns) - 10} more columns")
        
        # Show first row (as example)
        print(f"\n  First row example:")
        if 'aminoAcid' in df.columns:
            print(f"    Sequence: {df.iloc[0]['aminoAcid']}")
        if 'sequenceStatus' in df.columns:
            print(f"    Status: {df.iloc[0]['sequenceStatus']}")
        
        return True
        
    except Exception as e:
        print(f"✗ Failed to load data: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_basic_operations():
    """
    Test basic pandas/numpy operations
    
    WHAT THIS DOES:
    - Tests that you can do basic operations
    - Like filtering, grouping, etc.
    - Verifies packages work correctly
    
    THINK OF IT LIKE:
    - Testing that your tools actually work, not just exist
    """
    print("\n" + "="*70)
    print("TEST 3: Testing basic operations")
    print("="*70)
    
    try:
        import pandas as pd
        import numpy as np
        
        # Create a simple test DataFrame
        # This is like creating a small example to test with
        test_data = {
            'name': ['Alice', 'Bob', 'Charlie'],
            'age': [25, 30, 35],
            'score': [85, 90, 95]
        }
        df = pd.DataFrame(test_data)
        
        print("✓ Created test DataFrame")
        print(f"  Shape: {df.shape}")
        
        # Test filtering (like df[df['age'] > 28])
        filtered = df[df['age'] > 28]
        print(f"✓ Filtering works: {len(filtered)} rows where age > 28")
        
        # Test grouping (like df.groupby('name').mean())
        grouped = df.groupby('name')['score'].mean()
        print(f"✓ Grouping works: {len(grouped)} groups")
        
        # Test numpy operations
        arr = np.array([1, 2, 3, 4, 5])
        print(f"✓ NumPy works: mean = {arr.mean()}")
        
        return True
        
    except Exception as e:
        print(f"✗ Basic operations failed: {e}")
        return False


# ============================================================================
# MAIN FUNCTION
# ============================================================================

def main():
    """
    Run all tests and report results
    """
    print("\n" + "="*70)
    print("  DeepTCR Learning Project - Setup Test")
    print("="*70)
    print("\nThis script will test that everything is set up correctly.\n")
    
    results = []
    
    # Run all tests
    results.append(("Package imports", test_imports()))
    results.append(("Data loading", test_load_data()))
    results.append(("Basic operations", test_basic_operations()))
    
    # Summary
    print("\n" + "="*70)
    print("  TEST SUMMARY")
    print("="*70)
    
    all_passed = True
    for test_name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{test_name}: {status}")
        if not passed:
            all_passed = False
    
    print("\n" + "="*70)
    if all_passed:
        print("  ✓ ALL TESTS PASSED! You're ready to continue!")
        print("="*70)
        print("\nNext step: Go to Day_02_Explore_Data folder")
        print("Read the README.md there to start exploring the data!")
        return True
    else:
        print("  ✗ SOME TESTS FAILED")
        print("="*70)
        print("\nPlease fix the errors above before continuing.")
        print("Check the error messages for clues on what's wrong.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
