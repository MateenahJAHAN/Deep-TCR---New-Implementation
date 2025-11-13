"""
TCR-seq Data Explorer
=====================
A beginner-friendly script to explore TCR sequencing data

This script demonstrates:
1. Loading TCR-seq files (what you know: pd.read_csv)
2. Data cleaning (what you know: filtering, groupby)
3. Basic statistics (what you know: pandas aggregations)
4. Sequence encoding (new: converting strings to numbers)

Author: Learning Guide for DeepTCR Paper
Run this after extracting DeepTCR_Cancer-master.zip
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# ============================================================================
# PART 1: LOAD ONE PATIENT (PANDAS BASICS)
# ============================================================================

def load_tcr_file(file_path):
    """
    Load a TCR-seq TSV file
    
    This is just like: pd.read_csv('file.csv')
    But with sep='\t' because it's tab-separated
    
    Parameters:
    -----------
    file_path : str
        Path to .tsv file
    
    Returns:
    --------
    DataFrame with TCR sequences
    """
    print(f"\n{'='*70}")
    print(f"LOADING: {Path(file_path).name}")
    print('='*70)
    
    # Read TSV (like CSV but tab-separated)
    df = pd.read_csv(file_path, sep='\t')
    
    print(f"✓ Loaded {len(df):,} rows")
    print(f"✓ Columns: {len(df.columns)}")
    
    return df


def explore_data(df):
    """
    Explore TCR-seq data using familiar pandas operations
    
    This uses operations you know:
    - df.head() - preview data
    - df.info() - data types
    - df['col'].value_counts() - count values
    - df.describe() - statistics
    """
    print("\n--- Data Preview ---")
    print(df.head(3))
    
    print("\n--- Column Info ---")
    print(df.info())
    
    # Frame type: In = productive, Out = non-productive
    print("\n--- Frame Types ---")
    print(df['frame_type'].value_counts())
    
    # Focus on productive sequences (standard practice)
    productive = df[df['frame_type'] == 'In']
    print(f"\n✓ Productive sequences: {len(productive):,} ({len(productive)/len(df)*100:.1f}%)")
    
    return productive


# ============================================================================
# PART 2: DATA CLEANING (PANDAS FILTERING & GROUPBY)
# ============================================================================

def clean_tcr_data(df):
    """
    Clean TCR data using pandas operations you know
    
    Operations used:
    - Filtering: df[df['col'] == value]
    - String operations: df['col'].str.len()
    - Apply: df['col'].apply(lambda x: ...)
    - Groupby: df.groupby().agg()
    """
    print(f"\n{'='*70}")
    print("DATA CLEANING PIPELINE")
    print('='*70)
    
    print(f"Starting with: {len(df):,} sequences")
    
    # Step 1: Keep only productive (in-frame) sequences
    df = df[df['frame_type'] == 'In'].copy()
    print(f"After keeping productive: {len(df):,} sequences")
    
    # Step 2: Remove sequences with invalid amino acids
    # Valid amino acids: A,C,D,E,F,G,H,I,K,L,M,N,P,Q,R,S,T,V,W,Y (20 total)
    valid_aa = set('ACDEFGHIKLMNPQRSTVWY')
    df = df[df['amino_acid'].apply(lambda x: all(c in valid_aa for c in str(x)))]
    print(f"After removing invalid AA: {len(df):,} sequences")
    
    # Step 3: Length filter (keep typical lengths 10-25)
    lengths = df['amino_acid'].str.len()
    df = df[(lengths >= 10) & (lengths <= 25)]
    print(f"After length filter: {len(df):,} sequences")
    
    # Step 4: Aggregate by sequence (sum counts for identical amino acid sequences)
    # This is like: df.groupby('key').sum()
    print("\n--- Aggregating by sequence ---")
    before_agg = len(df)
    
    df_agg = df.groupby(['amino_acid', 'v_gene', 'j_gene']).agg({
        'templates': 'sum'  # Sum read counts
    }).reset_index()
    
    print(f"Before aggregation: {before_agg:,}")
    print(f"After aggregation: {len(df_agg):,}")
    print(f"Reduction: {(1 - len(df_agg)/before_agg)*100:.1f}%")
    
    return df_agg


def calculate_statistics(df):
    """
    Calculate repertoire statistics using pandas
    
    Operations you know:
    - .sum() - add up values
    - .mean() - average
    - .nunique() - count unique values
    - .value_counts() - frequency table
    """
    print(f"\n{'='*70}")
    print("REPERTOIRE STATISTICS")
    print('='*70)
    
    # Basic counts
    total_sequences = len(df)
    total_reads = df['templates'].sum()
    
    print(f"\nBasic Stats:")
    print(f"  Unique sequences: {total_sequences:,}")
    print(f"  Total reads: {total_reads:,}")
    print(f"  Mean reads per sequence: {total_reads/total_sequences:.1f}")
    
    # Sequence lengths
    lengths = df['amino_acid'].str.len()
    print(f"\nSequence Lengths:")
    print(f"  Min: {lengths.min()}")
    print(f"  Max: {lengths.max()}")
    print(f"  Mean: {lengths.mean():.1f}")
    print(f"  Median: {lengths.median()}")
    
    # V gene usage (like value_counts())
    print(f"\nTop 5 V Genes:")
    v_usage = df.groupby('v_gene')['templates'].sum().sort_values(ascending=False)
    for gene, count in v_usage.head(5).items():
        pct = count / total_reads * 100
        print(f"  {gene:15s}: {count:8,} reads ({pct:5.2f}%)")
    
    # Top clones (like nlargest())
    print(f"\nTop 5 Clones:")
    df_sorted = df.sort_values('templates', ascending=False)
    for i, (_, row) in enumerate(df_sorted.head(5).iterrows(), 1):
        pct = row['templates'] / total_reads * 100
        print(f"  {i}. {row['amino_acid']:20s} | {row['templates']:6,} reads ({pct:.2f}%)")
    
    # Diversity metric (simple version)
    # More unique sequences = more diverse
    diversity = total_sequences / total_reads
    print(f"\nDiversity Score: {diversity:.6f}")
    print(f"  (Higher = more diverse repertoire)")
    
    # Clonality (opposite of diversity)
    # Top 10 clones' share of total
    top10_reads = df_sorted.head(10)['templates'].sum()
    clonality = top10_reads / total_reads
    print(f"\nClonality (Top 10):")
    print(f"  Top 10 clones: {top10_reads:,} reads ({clonality*100:.1f}%)")
    print(f"  (Higher = more clonal/less diverse)")


# ============================================================================
# PART 3: SEQUENCE ENCODING (NEW CONCEPT)
# ============================================================================

def encode_amino_acid_sequence(sequence, max_length=40):
    """
    Convert amino acid sequence to numerical matrix
    
    This is like pd.get_dummies() but for sequences
    
    Input:  'CASSLAPG' (string)
    Output: (40, 20) numpy array (matrix)
    
    Each position → one-hot vector of length 20 (one for each amino acid)
    
    Parameters:
    -----------
    sequence : str
        Amino acid sequence (e.g., 'CASSLAPG')
    max_length : int
        Max sequence length (pad/truncate to this)
    
    Returns:
    --------
    np.array of shape (max_length, 20)
    """
    # Define amino acid alphabet (20 amino acids)
    AA_ALPHABET = 'ACDEFGHIKLMNPQRSTVWY'
    aa_to_index = {aa: i for i, aa in enumerate(AA_ALPHABET)}
    
    # Initialize zero matrix
    # Like: np.zeros((40, 20))
    encoded = np.zeros((max_length, 20))
    
    # Fill in the sequence (one-hot encoding)
    for position, amino_acid in enumerate(sequence[:max_length]):
        if amino_acid in aa_to_index:
            aa_index = aa_to_index[amino_acid]
            encoded[position, aa_index] = 1  # Set to 1 (one-hot)
    
    return encoded


def encode_v_gene(v_gene, v_gene_list):
    """
    Convert V gene to one-hot vector
    
    This is exactly like sklearn's LabelEncoder
    
    Input:  'TRBV19' (string)
    Output: [0,0,0,...,1,...,0] (vector of 0s with one 1)
    """
    # Create mapping
    v_to_index = {gene: i for i, gene in enumerate(v_gene_list)}
    
    # Initialize zero vector
    encoded = np.zeros(len(v_gene_list))
    
    # Set the correct position to 1
    if v_gene in v_to_index:
        encoded[v_to_index[v_gene]] = 1
    
    return encoded


def demonstrate_encoding(df):
    """
    Show how encoding works with examples
    """
    print(f"\n{'='*70}")
    print("SEQUENCE ENCODING DEMONSTRATION")
    print('='*70)
    
    # Take first sequence as example
    example_seq = df.iloc[0]['amino_acid']
    example_v = df.iloc[0]['v_gene']
    
    print(f"\nOriginal sequence: {example_seq}")
    print(f"Length: {len(example_seq)} amino acids")
    
    # Encode CDR3 sequence
    encoded_seq = encode_amino_acid_sequence(example_seq)
    print(f"\nEncoded sequence shape: {encoded_seq.shape}")
    print(f"  - {encoded_seq.shape[0]} positions (padded/truncated to 40)")
    print(f"  - {encoded_seq.shape[1]} possible amino acids (20 total)")
    
    # Show first position encoding
    print(f"\nFirst amino acid: '{example_seq[0]}'")
    print(f"Encoded as: {encoded_seq[0]}")
    print(f"  (One 1, rest 0s - this is 'one-hot encoding')")
    
    # Encode V gene
    all_v_genes = df['v_gene'].unique().tolist()
    encoded_v = encode_v_gene(example_v, all_v_genes)
    print(f"\nV gene: {example_v}")
    print(f"Encoded shape: {encoded_v.shape}")
    print(f"  (One-hot vector of length {len(all_v_genes)})")
    
    # Show what this means for ML
    print(f"\n{'='*70}")
    print("WHAT THIS MEANS FOR MACHINE LEARNING")
    print('='*70)
    print(f"\nFor ONE TCR sequence, we have:")
    print(f"  - CDR3 encoded: {encoded_seq.shape} = {encoded_seq.size} numbers")
    print(f"  - V gene encoded: {encoded_v.shape} = {encoded_v.size} numbers")
    print(f"  - J gene encoded: (similar to V gene)")
    print(f"\nFor ONE patient with {len(df):,} sequences:")
    print(f"  - Shape: ({len(df):,}, ~2000)")
    print(f"  - This is like a DataFrame with {len(df):,} rows and 2000 columns")
    print(f"  - But entire DataFrame gets ONE label (responder/non-responder)")


# ============================================================================
# PART 4: VISUALIZATION (MATPLOTLIB)
# ============================================================================

def visualize_repertoire(df, patient_id='su001'):
    """
    Create visualizations using matplotlib (what you might know)
    """
    print(f"\n{'='*70}")
    print("CREATING VISUALIZATIONS")
    print('='*70)
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle(f'TCR Repertoire Analysis - Patient {patient_id}', fontsize=16)
    
    # 1. Sequence length distribution
    ax = axes[0, 0]
    lengths = df['amino_acid'].str.len()
    ax.hist(lengths, bins=20, edgecolor='black')
    ax.set_xlabel('Sequence Length (amino acids)')
    ax.set_ylabel('Count')
    ax.set_title('Sequence Length Distribution')
    ax.axvline(lengths.mean(), color='red', linestyle='--', label=f'Mean: {lengths.mean():.1f}')
    ax.legend()
    
    # 2. Top 10 clones
    ax = axes[0, 1]
    top10 = df.nlargest(10, 'templates')
    sequences = [seq[:10] + '...' for seq in top10['amino_acid']]  # Truncate for display
    ax.barh(range(10), top10['templates'])
    ax.set_yticks(range(10))
    ax.set_yticklabels(sequences)
    ax.set_xlabel('Read Count')
    ax.set_title('Top 10 Most Frequent Clones')
    ax.invert_yaxis()
    
    # 3. V gene usage
    ax = axes[1, 0]
    v_usage = df.groupby('v_gene')['templates'].sum().nlargest(10)
    ax.barh(range(len(v_usage)), v_usage.values)
    ax.set_yticks(range(len(v_usage)))
    ax.set_yticklabels(v_usage.index)
    ax.set_xlabel('Total Reads')
    ax.set_title('Top 10 V Gene Usage')
    ax.invert_yaxis()
    
    # 4. Frequency distribution (log scale)
    ax = axes[1, 1]
    frequencies = df['templates'] / df['templates'].sum()
    ax.hist(np.log10(frequencies), bins=30, edgecolor='black')
    ax.set_xlabel('Log10(Frequency)')
    ax.set_ylabel('Count')
    ax.set_title('Clone Frequency Distribution')
    
    plt.tight_layout()
    plt.savefig('tcr_repertoire_analysis.png', dpi=150, bbox_inches='tight')
    print("\n✓ Saved: tcr_repertoire_analysis.png")
    
    return fig


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """
    Main function to run the analysis
    """
    print("\n" + "="*70)
    print(" TCR-SEQ DATA ANALYSIS TUTORIAL")
    print("="*70)
    print("\nThis script will:")
    print("  1. Load TCR sequencing data")
    print("  2. Clean and preprocess")
    print("  3. Calculate statistics")
    print("  4. Demonstrate encoding")
    print("  5. Create visualizations")
    print("\nUsing pandas, numpy, and matplotlib - tools you already know!")
    
    # File path (modify this to your data location)
    file_path = 'Data/yost/data/su001_BCC_pre1_TCRB.tsv'
    
    try:
        # Step 1: Load data
        df = load_tcr_file(file_path)
        
        # Step 2: Explore
        productive = explore_data(df)
        
        # Step 3: Clean
        df_clean = clean_tcr_data(productive)
        
        # Step 4: Statistics
        calculate_statistics(df_clean)
        
        # Step 5: Demonstrate encoding
        demonstrate_encoding(df_clean)
        
        # Step 6: Visualize
        fig = visualize_repertoire(df_clean)
        
        # Summary
        print(f"\n{'='*70}")
        print("SUMMARY")
        print('='*70)
        print(f"\n✓ Successfully analyzed patient data")
        print(f"✓ Total unique sequences: {len(df_clean):,}")
        print(f"✓ Total reads: {df_clean['templates'].sum():,}")
        print(f"\nNext steps:")
        print("  1. Try this script on other patient files")
        print("  2. Compare responders vs non-responders")
        print("  3. Analyze pre vs post treatment")
        print("  4. Explore the encoding in more detail")
        print("\n✓ Script completed successfully!")
        
    except FileNotFoundError:
        print(f"\n❌ Error: Could not find file: {file_path}")
        print("\nMake sure you've extracted DeepTCR_Cancer-master.zip")
        print("And update the file_path variable in main()")
    
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()


# ============================================================================
# BONUS: Helper Functions for Multiple Patients
# ============================================================================

def load_multiple_patients(data_dir='Data/yost/data', response_file='Data/yost/response.csv'):
    """
    Load and process multiple patient files
    
    Returns:
    --------
    List of dictionaries, each containing:
      - patient_id
      - tcr_data (DataFrame)
      - response (0 or 1)
    """
    import glob
    from pathlib import Path
    
    # Load response labels
    response_df = pd.read_csv(response_file)
    response_dict = dict(zip(response_df['patient_id'], response_df['response']))
    
    # Get all pre-treatment tumor files (BCC or SCC)
    pattern = str(Path(data_dir) / '*_[BS]CC_pre*_TCRB.tsv')
    files = glob.glob(pattern)
    
    print(f"Found {len(files)} patient files")
    
    patients_data = []
    
    for file_path in files:
        # Extract patient ID
        filename = Path(file_path).name
        patient_id = filename.split('_')[0]
        
        # Load and clean
        df = pd.read_csv(file_path, sep='\t')
        productive = df[df['frame_type'] == 'In']
        df_clean = clean_tcr_data(productive)
        
        # Get label
        response = response_dict.get(patient_id, 'Unknown')
        binary_label = 1 if response in ['CR', 'PR'] else 0 if response in ['SD', 'PD'] else -1
        
        patients_data.append({
            'patient_id': patient_id,
            'tcr_data': df_clean,
            'response': response,
            'binary_label': binary_label
        })
        
        print(f"  ✓ Loaded {patient_id}: {len(df_clean):,} sequences, response={response}")
    
    return patients_data


def compare_responders_vs_nonresponders(patients_data):
    """
    Compare statistics between responders and non-responders
    """
    # Separate by response
    responders = [p for p in patients_data if p['binary_label'] == 1]
    non_responders = [p for p in patients_data if p['binary_label'] == 0]
    
    print(f"\n{'='*70}")
    print("RESPONDERS vs NON-RESPONDERS COMPARISON")
    print('='*70)
    
    print(f"\nResponders (CR/PR): {len(responders)} patients")
    print(f"Non-responders (SD/PD): {len(non_responders)} patients")
    
    # Calculate average repertoire size
    resp_sizes = [len(p['tcr_data']) for p in responders]
    non_resp_sizes = [len(p['tcr_data']) for p in non_responders]
    
    print(f"\nRepertoire Size:")
    print(f"  Responders: {np.mean(resp_sizes):.0f} ± {np.std(resp_sizes):.0f} sequences")
    print(f"  Non-responders: {np.mean(non_resp_sizes):.0f} ± {np.std(non_resp_sizes):.0f} sequences")
    
    # Could add more comparisons here...


# ============================================================================
# USAGE EXAMPLES
# ============================================================================

"""
EXAMPLE 1: Run the main analysis
=================================
python tcr_explorer.py

EXAMPLE 2: Load multiple patients in Python
============================================
from tcr_explorer import load_multiple_patients, compare_responders_vs_nonresponders

patients = load_multiple_patients()
compare_responders_vs_nonresponders(patients)

EXAMPLE 3: Encode a specific patient's data
============================================
from tcr_explorer import load_tcr_file, clean_tcr_data, encode_amino_acid_sequence

df = load_tcr_file('Data/yost/data/su001_BCC_pre1_TCRB.tsv')
productive = df[df['frame_type'] == 'In']
df_clean = clean_tcr_data(productive)

# Encode all sequences
encoded_sequences = []
for seq in df_clean['amino_acid']:
    encoded = encode_amino_acid_sequence(seq)
    encoded_sequences.append(encoded)

encoded_array = np.array(encoded_sequences)
print(f"Encoded shape: {encoded_array.shape}")  # (num_sequences, 40, 20)
"""
