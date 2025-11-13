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

**How to start:**
1. Open `Day_00_Getting_Started/Day_00_Getting_Started.ipynb` in:
   - **Google Colab** (recommended - no installation!) - https://colab.research.google.com/
   - Jupyter Notebook (if installed locally)
   - VS Code with Jupyter extension
2. Read the markdown cells (explanations)
3. Fill in the TODO sections (**write code yourself!**)
4. Run each cell to see results

### Step 3: Follow Day-by-Day Plan
- Work through Days 0-10 in order
- Each day has a **Jupyter Notebook** (.ipynb file)
- Each notebook has:
  - **Markdown cells** - explanations and instructions
  - **Code cells with TODOs** - where YOU write the code
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
├── Day_09_DeepTCR_Setup/       📅 Day 9: Install DeepTCR
├── Day_10_Run_DeepTCR/         📅 Day 10: Train model
│
├── data/                       📊 All data files
│   └── DeepTCR_Cancer-master/
│       └── Data/yost/
│           ├── data/          (37 patient files)
│           └── response.csv   (Patient labels)
│
├── scripts/                    🔧 Helper scripts (optional)
└── docs/                       📚 Documentation & guides
```

---

## 📅 Day-by-Day Plan (2-3 Hours Per Day)

### Day 0: Getting Started 🚀
**Goal:** Learn how to use Jupyter Notebooks or Google Colab
- Install Python (or use Colab)
- Learn notebook basics
- Run your first code cells
- **Time:** 1-2 hours

### Day 1: Setup ⚙️
**Goal:** Install Python packages
- Check Python version
- Install pandas, numpy, matplotlib, etc.
- Verify everything works
- **Time:** 2 hours

### Day 2: Explore Data 🔍
**Goal:** Look at TCR data files
- Load TSV files using pandas
- Understand columns
- Filter to productive sequences
- **Time:** 2-3 hours

### Day 3: Clean Data 🧹
**Goal:** Prepare data for analysis
- Filter bad sequences
- Remove invalid amino acids
- Aggregate duplicates
- **Time:** 2-3 hours

### Day 4: Understand Data 📊
**Goal:** Calculate statistics and visualize
- Load multiple patients
- Calculate average repertoire size
- Find most common V genes
- Plot sequence lengths
- Compare responders vs non-responders
- **Time:** 2-3 hours

### Day 5: Encode Sequences 🔢
**Goal:** Convert strings to numbers
- Implement one-hot encoding
- Encode amino acid sequences
- Encode V/D/J genes
- Understand shape transformations
- **Time:** 3 hours

### Day 6: Multiple Patients 👥
**Goal:** Work with all patients
- Load all patient files
- Create patient batches
- Handle different repertoire sizes
- **Time:** 2-3 hours

### Day 7: Simple ML 🤖
**Goal:** Try simple machine learning
- Implement mean pooling
- Implement max pooling
- Use sklearn baseline
- Understand why simple pooling fails
- **Time:** 3 hours

### Day 8: Understand MIL 🎓
**Goal:** Learn Multiple Instance Learning
- Compare traditional ML vs MIL
- Understand bag of sequences
- Understand need for attention
- **Time:** 2-3 hours

### Day 9: DeepTCR Setup 📦
**Goal:** Install DeepTCR package
- Install DeepTCR
- Understand DeepTCR API
- Prepare data format
- **Time:** 2 hours

### Day 10: Run DeepTCR 🚀
**Goal:** Train the actual model
- Train DeepTCR model
- Make predictions
- Evaluate AUC (target ~0.82)
- Extract attention weights
- **Time:** 3 hours

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
   - They have questions to think about
   - They give you hints

3. **Fill in the TODO sections**
   - **YOU write the code yourself!**
   - Look for `# TODO:` comments
   - Write your code in those cells
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

---

## ✅ Checklist: Are You Ready?

Before starting, make sure you:
- [ ] Have Python 3.7+ installed OR can use Google Colab
- [ ] Know basic Python (variables, functions, loops)
- [ ] Know pandas basics (`pd.read_csv()`, `df.head()`, etc.)
- [ ] Know numpy basics (`np.array()`, `arr.shape`, etc.)
- [ ] Know sklearn basics (`train_test_split()`, simple models)
- [ ] Have 2-3 hours per day for 10 days
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
4. Google the error message
5. Take a break and come back fresh

### Q: How long will this take?
**A:** 
- Each day: 2-3 hours
- Total: ~20-30 hours over 10 days
- Don't rush! Understanding is more important than speed

### Q: Do I need to know deep learning?
**A:** 
- **No!** You'll learn the concepts as you go
- The first 7 days use only pandas, numpy, and sklearn
- DeepTCR handles the deep learning part for you
- You'll understand what it does, but don't need to implement it yourself

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
- ✅ Experiment
- ✅ Ask questions (even if just to yourself!)
- ✅ Have fun learning!

---

## 📝 Notes Section

Use this space (or a notebook) to write down:
- Things you learned each day
- Questions you have
- Ideas to explore
- Anything else!

---

**Good luck! You've got this! 🚀**

---

*Last updated: [Date]*
*For questions, check the day-specific notebooks or the docs folder.*
