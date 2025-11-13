#!/usr/bin/env python3
"""
DeepTCR Project Setup Script
=============================

This script sets up the DeepTCR project by:
1. Checking if data is downloaded
2. Verifying data structure
3. Installing required packages
4. Testing the setup

This script complements Day_01_Setup notebook.
Run this script to get started:
    python setup_project.py

Author: Setup script for DeepTCR learning project
"""

import os
import sys
import subprocess
from pathlib import Path

# ============================================================================
# CONFIGURATION - Simple variables you can understand
# ============================================================================

# Where the data should be located (try multiple common layouts)
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent

def _find_data_root():
    """
    Try common data locations relative to both the repo root and the scripts directory.
    This supports the project shipping data inside `data/` as well as alongside the repo.
    """
    candidate_dirs = [
        REPO_ROOT / "data" / "DeepTCR_Cancer-master" / "Data",
        REPO_ROOT / "DeepTCR_Cancer-master" / "Data",
        SCRIPT_DIR / "data" / "DeepTCR_Cancer-master" / "Data",
        SCRIPT_DIR / "DeepTCR_Cancer-master" / "Data",
    ]

    for candidate in candidate_dirs:
        if candidate.exists():
            return candidate
    return candidate_dirs[0]

DATA_DIR = _find_data_root()
YOST_DATA_DIR = DATA_DIR / "yost" / "data"
RESPONSE_FILE = DATA_DIR / "yost" / "response.csv"

# Required Python packages (simple list)
REQUIRED_PACKAGES = [
    "pandas",      # For reading CSV/TSV files (like Excel but for code)
    "numpy",       # For working with arrays and numbers
    "matplotlib",  # For making plots and graphs
    "seaborn",     # For prettier plots
    "scikit-learn", # For machine learning tools
]

# Optional but recommended packages
OPTIONAL_PACKAGES = [
    "DeepTCR",     # The main DeepTCR package (takes longer to install)
]

# ============================================================================
# HELPER FUNCTIONS - Simple functions that do one thing each
# ============================================================================

def print_header(text):
    """
    Print a nice header to make output easier to read
    
    This is just formatting - makes the output look nice!
    """
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")


def check_file_exists(file_path, description):
    """
    Check if a file exists and print the result
    
    Parameters:
    -----------
    file_path : Path
        Path to the file to check
    description : str
        What this file is for (for the user to understand)
    
    Returns:
    --------
    bool : True if file exists, False otherwise
    """
    if file_path.exists():
        print(f"✓ Found: {file_path}")
        print(f"  ({description})")
        return True
    else:
        print(f"✗ Missing: {file_path}")
        print(f"  ({description})")
        return False


def check_directory_exists(dir_path, description):
    """
    Check if a directory exists and count files in it
    
    Similar to check_file_exists but for folders
    """
    if dir_path.exists() and dir_path.is_dir():
        file_count = len(list(dir_path.glob("*.tsv")))
        print(f"✓ Found directory: {dir_path}")
        print(f"  Contains {file_count} TSV files")
        print(f"  ({description})")
        return True
    else:
        print(f"✗ Missing directory: {dir_path}")
        print(f"  ({description})")
        return False


def install_package(package_name):
    """
    Install a Python package using pip
    
    This is like running: pip install package_name
    But we do it from Python code so we can check if it works
    
    Parameters:
    -----------
    package_name : str
        Name of the package to install (e.g., "pandas")
    
    Returns:
    --------
    bool : True if installation succeeded, False otherwise
    """
    print(f"\nInstalling {package_name}...")
    try:
        # Run pip install command
        # subprocess.run() lets us run terminal commands from Python
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", package_name],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(f"✓ Successfully installed {package_name}")
            return True
        else:
            print(f"✗ Failed to install {package_name}")
            print(f"  Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ Error installing {package_name}: {str(e)}")
        return False


def test_import(package_name):
    """
    Test if we can import a package (check if it's installed correctly)
    
    This is like running: python -c "import pandas"
    If it works, the package is installed correctly!
    
    Parameters:
    -----------
    package_name : str
        Name of the package to test
    
    Returns:
    --------
    bool : True if import succeeded, False otherwise
    """
    try:
        __import__(package_name)
        print(f"✓ {package_name} can be imported successfully")
        return True
    except ImportError:
        print(f"✗ {package_name} cannot be imported (not installed?)")
        return False


# ============================================================================
# MAIN SETUP FUNCTIONS - These do the actual work
# ============================================================================

def check_data_files():
    """
    Check if all required data files are present
    
    This function:
    1. Checks if the data directory exists
    2. Checks if patient data files are there
    3. Checks if response labels file exists
    
    Returns:
    --------
    bool : True if all files are present, False otherwise
    """
    print_header("STEP 1: Checking Data Files")
    
    all_good = True
    
    # Check main data directory
    if not check_directory_exists(DATA_DIR, "Main data directory"):
        all_good = False
    
    # Check Yost dataset directory (the one we'll use for learning)
    if not check_directory_exists(YOST_DATA_DIR, "Yost dataset - patient TCR files"):
        all_good = False
    else:
        # List a few example files
        example_files = list(YOST_DATA_DIR.glob("*.tsv"))[:5]
        print(f"\n  Example files found:")
        for f in example_files:
            print(f"    - {f.name}")
        if len(list(YOST_DATA_DIR.glob("*.tsv"))) > 5:
            print(f"    ... and more!")
    
    # Check response labels file
    if not check_file_exists(RESPONSE_FILE, "Patient response labels (CR/PR/SD/PD)"):
        all_good = False
    
    if all_good:
        print("\n✓ All data files are present!")
    else:
        print("\n✗ Some data files are missing!")
        print("\nTo download the data:")
        print("  1. Go to: https://zenodo.org/record/6590167")
        print("  2. Download: DeepTCR_Cancer-master.zip")
        print("  3. Extract it in this directory")
    
    return all_good


def install_packages():
    """
    Install all required Python packages
    
    This function:
    1. Tries to import each package first (maybe already installed?)
    2. If not installed, installs it using pip
    3. Tests the installation by importing again
    
    Returns:
    --------
    bool : True if all packages installed successfully, False otherwise
    """
    print_header("STEP 2: Installing Python Packages")
    
    print("First, checking which packages are already installed...\n")
    
    packages_to_install = []
    
    # Check each required package
    for package in REQUIRED_PACKAGES:
        if test_import(package):
            # Already installed, skip it
            continue
        else:
            # Need to install it
            packages_to_install.append(package)
    
    if not packages_to_install:
        print("\n✓ All required packages are already installed!")
        return True
    
    print(f"\nNeed to install {len(packages_to_install)} packages:")
    for pkg in packages_to_install:
        print(f"  - {pkg}")
    
    # Ask user if they want to install (in a real script, you might want this)
    # For now, we'll just install them
    
    print("\nInstalling packages...")
    print("(This may take a few minutes, especially for DeepTCR)\n")
    
    success_count = 0
    for package in packages_to_install:
        if install_package(package):
            success_count += 1
    
    # Invalidate import caches after installation
    # This ensures Python recognizes newly installed packages
    import importlib
    import sys
    if hasattr(importlib, 'invalidate_caches'):
        importlib.invalidate_caches()
        print("\n✓ Invalidated Python import caches (ensures new packages are recognized)")
    
    # Test all packages again
    print("\n" + "-"*70)
    print("Testing all packages...")
    print("-"*70)
    
    all_working = True
    for package in REQUIRED_PACKAGES:
        if not test_import(package):
            all_working = False
    
    if all_working:
        print("\n✓ All packages installed and working correctly!")
        return True
    else:
        print("\n✗ Some packages failed to install correctly")
        return False


def test_setup():
    """
    Test the setup by trying to load one data file
    
    This function:
    1. Tries to import pandas (we need it to read files)
    2. Tries to load one patient's TCR data file
    3. Prints some basic info about the data
    
    This proves everything is working!
    
    Returns:
    --------
    bool : True if test passed, False otherwise
    """
    print_header("STEP 3: Testing Setup")
    
    try:
        # Import pandas (we need this to read TSV files)
        import pandas as pd
        print("✓ Successfully imported pandas")
        
        # Find one example file
        example_files = list(YOST_DATA_DIR.glob("*.tsv"))
        if not example_files:
            print("✗ No data files found to test with")
            return False
        
        test_file = example_files[0]
        print(f"\nTesting with file: {test_file.name}")
        
        # Try to load the file
        # pd.read_csv() reads CSV files, but TSV files are just CSV with tabs instead of commas
        # So we use sep='\t' to tell pandas "use tabs as separators"
        df = pd.read_csv(test_file, sep='\t')
        
        print(f"✓ Successfully loaded file!")
        print(f"  - Number of rows: {len(df):,}")
        print(f"  - Number of columns: {len(df.columns)}")
        print(f"  - Columns: {', '.join(df.columns[:5])}...")
        
        # Check if it has the expected columns
        expected_cols = ['amino_acid', 'v_gene', 'j_gene', 'frame_type']
        missing_cols = [col for col in expected_cols if col not in df.columns]
        
        if missing_cols:
            print(f"\n⚠ Warning: Missing expected columns: {missing_cols}")
        else:
            print(f"\n✓ File has all expected columns!")
        
        print("\n✓ Setup test passed! Everything is working correctly.")
        return True
        
    except Exception as e:
        print(f"\n✗ Setup test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def print_next_steps():
    """
    Print instructions for what to do next
    
    This helps the user know what to do after setup is complete
    """
    print_header("SETUP COMPLETE! Next Steps")
    
    print("""
Now that everything is set up, here's what you can do:

1. EXPLORE THE DATA:
   Run the TCR explorer script to see what the data looks like:
   
   python tcr_explorer.py
   
   This will:
   - Load one patient's TCR data
   - Show you what the data looks like
   - Calculate some basic statistics
   - Create visualizations

2. FOLLOW THE DAY-BY-DAY PLAN:
   Start with Day 0 and work through Day 11:
   - Day_00_Getting_Started/ - Learn Jupyter/Colab basics
   - Day_01_Setup/ - Install packages (this script helps!)
   - Day_02_Explore_Data/ - Explore TCR data files
   - Day_03_Clean_Data/ - Clean and prepare data
   - Day_04_Understand_Data/ - Statistics and visualizations
   - Day_05_Encode_Sequences/ - Convert strings to numbers
   - Day_06_Multiple_Patients/ - Work with multiple patients
   - Day_07_Simple_ML/ - Try simple ML baselines
   - Day_08_Understand_MIL/ - Learn Multiple Instance Learning
   - Day_08.5_DeepTCR_Architecture/ - Understand DeepTCR architecture
   - Day_09_DeepTCR_Setup/ - Install DeepTCR package
   - Day_10_Run_DeepTCR/ - Train and evaluate DeepTCR
   - Day_11_Attention_Analysis/ - Analyze attention weights

3. TRY THE EXAMPLES:
   Modify tcr_explorer.py to:
   - Load different patients
   - Compare responders vs non-responders
   - Analyze pre vs post treatment

4. LEARN GRADUALLY:
   Follow the WEEK-BY-WEEK plan in LEARNING_ROADMAP.md
   Don't rush - take time to understand each concept!

For help, check the guides or modify the example scripts.
Good luck with your learning journey! 🚀
""")


# ============================================================================
# MAIN FUNCTION - This is what runs when you execute the script
# ============================================================================

def main():
    """
    Main function that runs the entire setup process
    
    This function:
    1. Checks if data files exist
    2. Installs required packages
    3. Tests the setup
    4. Prints next steps
    
    Think of it as a recipe:
    - Step 1: Check ingredients (data files)
    - Step 2: Get tools (install packages)
    - Step 3: Test everything works
    - Step 4: Tell user what to do next
    """
    print("\n" + "="*70)
    print("  DeepTCR Project Setup")
    print("="*70)
    print("\nThis script will help you set up the DeepTCR learning project.")
    print("It will check data files, install packages, and test everything.\n")
    print("Tip: If `python` is not recognised on your system, run this script with `python3`.")
    
    # Step 1: Check data files
    data_ok = check_data_files()
    
    if not data_ok:
        print("\n⚠ Please download and extract the data first!")
        print("See instructions above.")
        return False
    
    # Step 2: Install packages
    packages_ok = install_packages()
    
    if not packages_ok:
        print("\n⚠ Some packages failed to install.")
        print("You may need to install them manually:")
        print("  pip install " + " ".join(REQUIRED_PACKAGES))
        return False
    
    # Step 3: Test setup
    test_ok = test_setup()
    
    if not test_ok:
        print("\n⚠ Setup test failed. Please check the error messages above.")
        return False
    
    # Step 4: Print next steps
    print_next_steps()
    
    print("\n" + "="*70)
    print("  Setup Complete! ✓")
    print("="*70 + "\n")
    
    return True


# ============================================================================
# RUN THE SCRIPT
# ============================================================================

if __name__ == "__main__":
    """
    This special line means: "Only run main() if someone runs this script directly"
    
    If you import this file as a module, main() won't run automatically.
    This is good practice - it means the script can be used in two ways:
    1. Run directly: python setup_project.py
    2. Import as module: import setup_project (won't run main())
    """
    success = main()
    
    # Exit with appropriate code (0 = success, 1 = failure)
    # This is useful if other scripts want to check if setup succeeded
    sys.exit(0 if success else 1)
