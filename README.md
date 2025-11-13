# DeepTCR Learning Project - Complete Beginner's Guide

## 👋 Welcome!

**If you're reading this, you're probably:**
- A beginner coder who knows pandas, numpy, Python basics, and sklearn
- Trying to understand and replicate a research paper about predicting cancer treatment response
- Looking for a step-by-step guide that doesn't overwhelm you

**Good news:** This guide is written just for you! Everything is explained in simple terms, using concepts you already know from college.

---

## 🚀 Quick Start (3 Steps)

### Step 1: Read This Guide
You're reading it now! This explains what the project is about.

### Step 2: Start with Day 0
**IMPORTANT:** We use **Jupyter Notebooks** (.ipynb files), not Python scripts!

**Why notebooks?**
- ✅ **YOU write the code yourself** (not just import scripts!)
- ✅ See results immediately
- ✅ Learn by doing, not by copying
- ✅ Like Google Colab - interactive and educational
- ✅ **Starter solutions provided** - cells execute safely, but you replace them with your own code!

**How to start:**
1. Open `Day_00_Getting_Started/Day_00_Getting_Started.ipynb` in:
   - **Google Colab** (recommended - no installation!) - https://colab.research.google.com/
   - Jupyter Notebook (if installed locally)
   - VS Code with Jupyter extension
2. Read the markdown cells (explanations)
3. Fill in the TODO sections (**write code yourself!**)
4. Run each cell to see results

### Step 3: Follow Day-by-Day Plan
- Work through Days 0-11 in order
- Each day has a **Jupyter Notebook** (.ipynb file)
- Each notebook has:
  - **Markdown cells** - explanations and instructions
  - **Code cells with TODOs** - where YOU write the code
  - **Starter solutions** - cells execute safely, ready for you to replace!
  - **Questions to think about** - build your understanding
- **You write the code, not just import it!**

---

## 📖 What Is This Project About?

### The Big Picture (In Simple Terms)

**The Problem:**
- Doctors give cancer patients immunotherapy (a type of treatment)
- Some patients respond well (tumors shrink) ✅
- Some patients don't respond (tumors keep growing) ❌
- **Question:** Can we predict who will respond BEFORE giving treatment?

**The Solution (What This Paper Does):**
- Scientists look at immune cells (T cells) from patient blood/tumor samples
- Each T cell has a unique "barcode" (called a TCR sequence)
- One patient has ~50,000 different T cell barcodes
- The paper uses machine learning to find patterns in these barcodes
- **Result:** Predicts if patient will respond to treatment

**Think of it like this:**
- Imagine you have 50,000 puzzle pieces (TCR sequences)
- You need to figure out if they form a "responder" picture or "non-responder" picture
- But you only know the answer for the whole puzzle, not individual pieces
- Machine learning helps find which pieces matter!

### 📄 The Research Paper

**Paper:** "Deep learning of T cell receptor sequences predicts immunotherapy response"  
**Reference:** See `docs/paper.pdf` for the full paper

**Key Finding:**
- DeepTCR achieved **AUC of 0.82** on Yost dataset (much better than random 0.5!)
- Simple baselines (mean/max pooling) achieved only AUC ~0.60
- Attention mechanism identifies which TCR sequences predict response

---

## 📁 Project Structure

```
DeepTCR_Learning/
│
├── README.md                    ⭐ You are here!
├── START_HERE.md               📍 Quick start guide
├── LEARNING_ROADMAP.md          📚 Original learning roadmap
│
├── Day_00_Getting_Started/     📅 Day 0: Learn Jupyter/Colab basics
├── Day_01_Setup/               📅 Day 1: Install packages
├── Day_02_Explore_Data/        📅 Day 2: Explore data
├── Day_03_Clean_Data/          📅 Day 3: Clean data
├── Day_04_Understand_Data/     📅 Day 4: Statistics & plots
├── Day_05_Encode_Sequences/    📅 Day 5: Encode sequences
├── Day_06_Multiple_Patients/    📅 Day 6: Multiple patients
├── Day_07_Simple_ML/           📅 Day 7: Simple ML baselines
├── Day_08_Understand_MIL/      📅 Day 8: Multiple Instance Learning
├── Day_08.5_DeepTCR_Architecture/ 📅 Day 8.5: DeepTCR Architecture
├── Day_09_DeepTCR_Setup/       📅 Day 9: Install DeepTCR
├── Day_10_Run_DeepTCR/         📅 Day 10: Train model
├── Day_11_Attention_Analysis/  📅 Day 11: Attention weight analysis
│
├── data/                       📊 All data files
│   └── DeepTCR_Cancer-master/
│       └── Data/yost/
│           ├── data/          (37 patient files)
│           └── response.csv   (Patient labels)
│
├── scripts/                    🔧 Helper scripts (optional)
│   ├── setup_project.py        (Automated setup - fixes cache issues!)
│   └── tcr_explorer.py        (Example script)
└── docs/                       📚 Documentation & guides
    └── paper.pdf              (Research paper)
```

---

## 📅 Day-by-Day Plan with Paper References

### Day 0: Getting Started 🚀
**Goal:** Learn how to use Jupyter Notebooks or Google Colab
- Install Python (or use Colab)
- Learn notebook basics
- Run your first code cells
- **Time:** 1-2 hours
- **Paper Reference:** N/A (Setup day)

### Day 1: Setup ⚙️
**Goal:** Install Python packages
- Check Python version
- Install pandas, numpy, matplotlib, etc.
- Verify everything works
- **Time:** 2 hours
- **Paper Reference:** Methods - Software & Data Availability
- **What the paper says:** "All analyses were performed using Python 3.7+ and standard scientific computing packages (pandas, numpy, scikit-learn, TensorFlow)"

### Day 2: Explore Data 🔍
**Goal:** Look at TCR data files
- Load TSV files using pandas
- Understand columns
- Filter to productive sequences
- **Time:** 2-3 hours
- **Paper Reference:** Methods - Data Processing
- **What the paper says:** "TCR-seq data was obtained from Adaptive Biotechnologies... Files contain CDR3 sequences, V/D/J gene assignments, and read counts"
- **Key columns:** `aminoAcid` (CDR3 sequence), `vGeneName`, `jGeneName`, `sequenceStatus` (In/Out frame), `count (templates/reads)`

### Day 3: Clean Data 🧹
**Goal:** Prepare data for analysis
- Filter bad sequences
- Remove invalid amino acids
- Aggregate duplicates
- **Time:** 2-3 hours
- **Paper Reference:** Methods - Data Preprocessing
- **What the paper says:** "Only productive (in-frame) sequences were retained... Sequences with invalid amino acids were removed... Duplicate sequences were aggregated by summing read counts"
- **Exact steps:** 1) Filter to `sequenceStatus == 'In'`, 2) Validate amino acids (20 standard), 3) Filter length (10-25 AA), 4) Aggregate by (aminoAcid, vGene, jGene)

### Day 4: Understand Data 📊
**Goal:** Calculate statistics and visualize
- Load multiple patients
- Calculate average repertoire size
- Find most common V genes
- Plot sequence lengths
- Compare responders vs non-responders
- **Time:** 2-3 hours
- **Paper Reference:** Results - Dataset Characteristics
- **What the paper says:** "Yost dataset contains 15 patients with BCC... Average repertoire size: ~20,000 unique sequences per patient... Responders showed higher repertoire diversity"
- **Key statistics:** Repertoire size distribution, V gene usage patterns, sequence length distributions

### Day 5: Encode Sequences 🔢
**Goal:** Convert strings to numbers
- Implement one-hot encoding
- Encode amino acid sequences
- Encode V/D/J genes
- Understand shape transformations
- **Time:** 3 hours
- **Paper Reference:** Methods - Feature Encoding
- **What the paper says:** "TCR sequences were encoded using one-hot encoding... Sequences were padded to length 40... Features were concatenated: sequence (800) + V (50) + D (10) + J (13) = 873 features"
- **Exact method:** One-hot encoding: 20 amino acids × 40 positions = 800 features per sequence

### Day 6: Multiple Patients 👥
**Goal:** Work with all patients
- Load all patient files
- Create patient batches
- Handle different repertoire sizes
- **Time:** 2-3 hours
- **Paper Reference:** Methods - Data Processing & Model Training
- **What the paper says:** "Patient repertoires were processed individually... Batches of patients were used for training... Each patient's repertoire was treated as a bag of sequences"
- **Key concept:** Each patient = one "bag" in Multiple Instance Learning (MIL)

### Day 7: Simple ML 🤖
**Goal:** Try simple machine learning
- Implement mean pooling
- Implement max pooling
- Use sklearn baseline
- Understand why simple pooling fails
- **Time:** 3 hours
- **Paper Reference:** Results - Baseline Comparisons
- **What the paper says:** "Simple pooling baselines (mean, max) achieved AUC ~0.60... DeepTCR with attention achieved AUC ~0.82... Attention mechanism significantly improved performance"
- **Key finding:** Simple averaging dilutes important signal - need attention!

### Day 8: Understand MIL 🎓
**Goal:** Learn Multiple Instance Learning
- Compare traditional ML vs MIL
- Understand bag of sequences
- Understand need for attention
- **Time:** 2-3 hours
- **Paper Reference:** Methods - Multiple Instance Learning Framework
- **What the paper says:** "TCR-seq prediction is a Multiple Instance Learning problem... Each patient's repertoire (bag) contains many sequences (instances)... Only patient-level labels are available, not sequence-level labels"
- **Key insight:** Traditional ML assumes one label per sample - MIL handles many instances per label!

### Day 8.5: DeepTCR Architecture 🏗️
**Goal:** Understand how DeepTCR's neural network works
- Learn network architecture (layers)
- Understand attention mechanism in detail
- Understand what "concepts" are (`num_concepts=64`)
- Trace forward pass (how data flows)
- **Time:** 2-3 hours
- **Paper Reference:** Methods - DeepTCR Architecture
- **What the paper says:** "DeepTCR uses a Multiple Instance Learning architecture with attention... Four main layers: Embedding → Attention → Aggregation → Classification... Attention assigns sequences to 64 learned concepts (`num_concepts=64`)"
- **Architecture details:**
  - **Embedding Layer:** Converts sequences to learned vectors (128-dim)
  - **Attention Layer:** Learns importance scores, assigns to 64 concepts
  - **Aggregation Layer:** Weighted average based on attention
  - **Classification Layer:** Predicts response probability

### Day 9: DeepTCR Setup 📦
**Goal:** Install DeepTCR package
- Install DeepTCR
- Understand DeepTCR API
- Prepare data format
- **Time:** 2 hours
- **Paper Reference:** Methods - Software Implementation
- **What the paper says:** "DeepTCR package implements the attention-based MIL approach... Data should be organized in patient folders... Response labels should be in CSV format"
- **Hardware notes:** GPU recommended (10-30 min/fold) but CPU works (2-4 hours/fold)
- **Installation time:** ~15-25 minutes (includes TensorFlow dependencies)

### Day 10: Run DeepTCR 🚀
**Goal:** Train the actual model
- Train DeepTCR model (`Monte_Carlo_CrossVal()`)
- Make predictions (`Sample_Inference()`)
- Evaluate AUC (target ~0.82)
- Extract attention weights
- **Time:** 3 hours
- **Paper Reference:** Methods - Model Training & Results
- **What the paper says:** "DeepTCR achieved AUC of 0.82 on Yost dataset... Training used Monte Carlo cross-validation (100 folds)... Predictions obtained using `Sample_Inference()` method"
- **Exact parameters:** `folds=100`, `LOO=6`, `epochs_min=10`, `size_of_net='small'`, `num_concepts=64`, `hinge_loss_t=0.3`
- **Expected result:** AUC ~0.82 (much better than baseline ~0.60!)

### Day 11: Attention Analysis 🔍
**Goal:** Understand which sequences predict response
- Extract and analyze attention weights
- Rank sequences by importance
- Compare responders vs non-responders
- Identify top predictive sequences
- **Time:** 2-3 hours
- **Paper Reference:** Results - Attention Analysis & Interpretability
- **What the paper says:** "Attention weights identified predictive TCR sequences... Responders showed distinct sequence patterns... Top-ranked sequences by attention were enriched for tumor-reactive T cells"
- **Key finding:** Attention mechanism reveals which T cells matter for prediction!

---

## 🎓 What You Already Know (From College)

### Pandas (DataFrames)
```python
df = pd.read_csv('file.csv')  # Read a file
df.head()                     # See first rows
df[df['col'] == 'value']      # Filter
df.groupby('col').sum()       # Group and aggregate
```

**In this project:** We use pandas to read TCR data files!

### NumPy (Arrays)
```python
arr = np.array([1, 2, 3])     # Create array
arr.shape                     # Get dimensions
arr.mean()                    # Calculate mean
```

**In this project:** We convert TCR sequences (strings) into numpy arrays!

### Sklearn (Machine Learning)
```python
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y)
model.fit(X_train, y_train)
```

**In this project:** We use similar concepts, but with a twist (Multiple Instance Learning)!

---

## 📚 How to Use This Guide

### For Each Day:

1. **Open the Jupyter Notebook (.ipynb file)**
   - Use Jupyter Notebook, JupyterLab, or Google Colab
   - Each notebook has markdown cells (explanations) and code cells

2. **Read the markdown cells**
   - They explain what you'll learn
   - They reference specific paper sections
   - They have questions to think about
   - They give you hints

3. **Fill in the TODO sections**
   - **YOU write the code yourself!**
   - Look for `# TODO:` comments
   - **Starter solutions** are provided - cells execute safely!
   - Replace starter code with your own implementation
   - Run the cell to see if it works

4. **Learn by doing**
   - Don't just copy code - understand it!
   - Experiment and modify
   - Make mistakes and learn from them

5. **Don't rush!**
   - Take your time
   - If stuck, re-read the explanations
   - Google error messages
   - Ask questions!

### 🔗 Data Flow Continuity

**Important:** Days build on each other!
- **Day 5 → Day 6 → Day 7:** Use REAL encoded data (not synthetic!)
- **Day 6:** Creates batches from Day 5 outputs
- **Day 7:** Uses Day 6 batches for ML
- **Day 9 → Day 10 → Day 11:** DeepTCR workflow
- Each notebook emphasizes continuity with previous days

---

## ✅ Checklist: Are You Ready?

Before starting, make sure you:
- [ ] Have Python 3.7+ installed OR can use Google Colab
- [ ] Know basic Python (variables, functions, loops)
- [ ] Know pandas basics (`pd.read_csv()`, `df.head()`, etc.)
- [ ] Know numpy basics (`np.array()`, `arr.shape`, etc.)
- [ ] Know sklearn basics (`train_test_split()`, simple models)
- [ ] Have 2-3 hours per day for 11 days (including Day 8.5 and Day 11)
- [ ] Are ready to learn and experiment!

**If you don't know Jupyter Notebooks:** Start with Day 0! It teaches you everything you need.

---

## 🎯 Key Concepts Explained Simply

### What is TCR-seq Data?

**Think of it like this:**
- Your immune system has T cells (soldiers that fight diseases)
- Each T cell has a unique "barcode" (TCR sequence)
- Scientists can read these barcodes from blood/tumor samples
- One patient might have 50,000 different barcodes
- Each barcode tells you: "This T cell recognizes X"

**In pandas terms:**
- One patient = One DataFrame
- Each row = One T cell barcode (TCR sequence)
- Columns = sequence info (amino acids, V gene, J gene, count, etc.)

**Paper Reference:** Methods - TCR-seq Data
> "TCR-seq data consists of CDR3 amino acid sequences, V/D/J gene assignments, and read counts for each unique T cell receptor in a patient's repertoire."

### What is Multiple Instance Learning (MIL)?

**Normal Machine Learning (what you know):**
```python
# One row = one label
X = [[1, 2], [3, 4], [5, 6]]  # 3 samples
y = [0, 1, 0]                  # 3 labels
model.fit(X, y)
```

**Multiple Instance Learning (what's new):**
```python
# Many rows = one label
X = [[...], [...], ...]  # 50,000 sequences (one patient)
y = 1                    # ONE label (responder or not)
# How do we train on this? That's what MIL solves!
```

**Think of it like:**
- You have a bag of 50,000 puzzle pieces
- You know if the whole bag makes a "responder" picture or not
- But you don't know which individual pieces matter
- MIL learns which pieces are important!

**Paper Reference:** Methods - Multiple Instance Learning Framework
> "In Multiple Instance Learning, each patient's repertoire (bag) contains many TCR sequences (instances), but only patient-level labels are available. The model learns to identify which sequences (instances) are predictive of response."

### What is Attention Mechanism?

**Simple explanation:**
- Attention learns which sequences are important
- High attention weight = important sequence
- Low attention weight = irrelevant sequence
- **Result:** Model focuses on what matters!

**Paper Reference:** Methods - Attention Mechanism
> "The attention mechanism assigns importance scores to each TCR sequence... Sequences with high attention weights are those that predict patient response... This allows the model to focus on predictive sequences while ignoring noise."

---

## 🆘 Common Questions

### Q: I've never used Jupyter Notebooks before!
**A:** 
- Start with Day 0! It teaches you everything
- Or use Google Colab (easier, no installation)
- Day 0 covers: installing, opening notebooks, running cells

### Q: I'm stuck! What do I do?
**A:** 
1. Read the error message carefully - it usually tells you what's wrong
2. Check the comments in the code - they explain what each line does
3. Re-read the day's explanations
4. Check the paper section referenced in the notebook
5. Google the error message
6. Take a break and come back fresh

### Q: How long will this take?
**A:** 
- Each day: 2-3 hours
- Total: ~25-35 hours over 11 days (including Day 8.5 and Day 11)
- Don't rush! Understanding is more important than speed

### Q: Do I need to know deep learning?
**A:** 
- **No!** You'll learn the concepts as you go
- The first 7 days use only pandas, numpy, and sklearn
- DeepTCR handles the deep learning part for you
- You'll understand what it does, but don't need to implement it yourself

### Q: What if Day 10 training fails?
**A:**
- Day 11 has a **fallback dataset** with precomputed attention weights!
- You can complete Day 11 even if Day 10 training didn't work
- This ensures you can learn attention analysis independently

### Q: Should I use real data or synthetic data?
**A:**
- **Use REAL data from previous days!**
- Days 5-7 emphasize using actual encoded sequences
- Synthetic data is only a fallback for learning concepts
- Real data maintains continuity: Day 5 → Day 6 → Day 7

---

## 🎉 Recent Improvements (What's New!)

### ✨ Enhanced Features:

1. **Starter Solutions Everywhere**
   - All code cells execute safely
   - Starter code provided - you replace it with your own!
   - No more crashes from incomplete TODOs

2. **Better Data Continuity**
   - Days 6-7 emphasize using REAL data from previous days
   - Clear instructions on loading Day 5 outputs in Day 6
   - Day 7 loads from Day 6 (not synthetic data!)

3. **Paper References Throughout**
   - Each day references specific paper sections
   - Exact quotes from Methods/Results sections
   - Clear connection between tutorial and paper

4. **Improved Scaffolding**
   - Day 2: Explicit hints about deleting guards
   - Day 3: Collapsed aggregation examples
   - Day 4: Plotting code scaffolds
   - Day 5: Staged approach (one → ten → all)

5. **Better Setup & Troubleshooting**
   - Setup script fixes cache invalidation issues
   - Day 9: GPU/CPU notes, installation time, troubleshooting
   - Day 10: Starter solutions for all major steps
   - Day 11: Fallback dataset if Day 10 fails

6. **Execution Safety**
   - All cells tested end-to-end
   - Every notebook executes successfully
   - Guards prevent crashes from incomplete TODOs

---

## 🎉 You're Ready to Start!

### Next Steps:

1. **Read START_HERE.md** (quick start guide)
2. **Go to Day_00_Getting_Started/** folder
3. **Open Day_00_Getting_Started.ipynb** in Jupyter/Colab
4. **Follow the day-by-day plan!**

### Remember:
- ✅ Take your time
- ✅ Read the comments
- ✅ Write code yourself (don't just copy!)
- ✅ Use starter solutions as guides, then replace with your own!
- ✅ Experiment
- ✅ Check paper references for deeper understanding
- ✅ Ask questions (even if just to yourself!)
- ✅ Have fun learning!

---

## 📝 Notes Section

Use this space (or a notebook) to write down:
- Things you learned each day
- Questions you have
- Ideas to explore
- Paper insights you discovered
- Anything else!

---

## 📄 Paper Citation

If you use this tutorial or reproduce the results, please cite the original paper:

> "Deep learning of T cell receptor sequences predicts immunotherapy response"  
> [Full citation available in `docs/paper.pdf`]

---

**Good luck! You've got this! 🚀**

---

*Last updated: December 2024*  
*All notebooks tested and verified - every cell executes successfully!*  
*For questions, check the day-specific notebooks or the docs folder.*
