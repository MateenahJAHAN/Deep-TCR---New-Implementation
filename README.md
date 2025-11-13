# DeepTCR Learning Project - Complete Beginner's Guide

## 👋 Welcome!

**If you're reading this, you're probably:**
- A beginner coder who knows pandas, numpy, Python basics, and sklearn
- Trying to understand and replicate a research paper about predicting cancer treatment response
- Looking for a step-by-step guide that doesn't overwhelm you

**Good news:** This guide is written just for you! Everything is explained in simple terms, using concepts you already know from college.

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

## 🎓 What You Already Know (From College)

### Pandas (DataFrames)
```python
# You know this:
df = pd.read_csv('data.csv')  # Read a file
df.head()                     # See first rows
df['column'].value_counts()   # Count values
```

**In this project:** We'll use pandas to read TCR data files (they're like CSV files but with tabs instead of commas)

### NumPy (Arrays)
```python
# You know this:
arr = np.array([1, 2, 3])     # Create array
arr.shape                     # Get dimensions
arr.mean()                    # Calculate mean
```

**In this project:** We'll convert TCR sequences (strings) into numpy arrays so computers can work with them

### Sklearn (Machine Learning)
```python
# You know this:
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y)
model.fit(X_train, y_train)
```

**In this project:** We'll use similar concepts, but with a twist - one patient = many sequences = one label (this is called "Multiple Instance Learning")

---

## 📁 Project Structure (What's Where?)

```
DeepTCR_Learning/
│
├── README.md                          ⭐ START HERE - This file!
│
├── Day_01_Setup/                     📅 Day 1: Set up everything
│   ├── README.md                     (What to do today)
│   ├── setup_project.py              (Run this first!)
│   └── test_setup.py                 (Check if everything works)
│
├── Day_02_Explore_Data/              📅 Day 2: Look at the data
│   ├── README.md                     (What to do today)
│   ├── load_one_file.py              (Load one patient's data)
│   └── explore_dataframe.py          (See what's in the data)
│
├── Day_03_Clean_Data/                📅 Day 3: Clean the data
│   ├── README.md                     (What to do today)
│   ├── filter_sequences.py           (Remove bad data)
│   └── aggregate_data.py             (Combine duplicates)
│
├── Day_04_Understand_Data/           📅 Day 4: Understand what you have
│   ├── README.md                     (What to do today)
│   ├── calculate_statistics.py       (Basic stats)
│   └── visualize_data.py             (Make plots)
│
├── Day_05_Encode_Sequences/           📅 Day 5: Convert strings to numbers
│   ├── README.md                     (What to do today)
│   ├── encode_one_sequence.py       (One sequence → array)
│   └── encode_all_sequences.py       (All sequences → arrays)
│
├── Day_06_Multiple_Patients/          📅 Day 6: Work with many patients
│   ├── README.md                     (What to do today)
│   ├── load_multiple_patients.py     (Load all patients)
│   └── compare_patients.py           (Compare responders vs non-responders)
│
├── Day_07_Simple_ML/                  📅 Day 7: Try simple machine learning
│   ├── README.md                     (What to do today)
│   ├── mean_pooling_baseline.py      (Simple approach)
│   └── sklearn_baseline.py           (Use sklearn)
│
├── Day_08_Understand_MIL/             📅 Day 8: Learn Multiple Instance Learning
│   ├── README.md                     (What to do today)
│   └── mil_explained.py              (What is MIL?)
│
├── Day_09_DeepTCR_Setup/              📅 Day 9: Set up DeepTCR package
│   ├── README.md                     (What to do today)
│   └── install_deeptcr.py            (Install the package)
│
├── Day_10_Run_DeepTCR/                📅 Day 10: Run the actual model
│   ├── README.md                     (What to do today)
│   └── train_model.py                (Train DeepTCR model)
│
├── data/                              📊 All the data files
│   └── DeepTCR_Cancer-master/
│       └── Data/
│           └── yost/
│               ├── data/              (37 patient files)
│               └── response.csv       (Who responded?)
│
├── guides/                             📚 Learning guides (read as needed)
│   ├── pandas_to_deeptcr_guide.md    (Connect pandas to DeepTCR)
│   ├── dataset_exploration_guide.md  (Understand the data)
│   ├── deeptcr_architecture.md       (How the model works)
│   └── data_shapes_walkthrough.md    (Array dimensions explained)
│
└── requirements.txt                    📦 Python packages needed
```

---

## 🚀 Quick Start (3 Steps)

### Step 1: Set Up (Day 1)
```bash
# Go to Day 1 folder
cd Day_01_Setup

# Read what to do
cat README.md

# Run setup script
python3 setup_project.py
```

### Step 2: Explore Data (Day 2)
```bash
# Go to Day 2 folder
cd Day_02_Explore_Data

# Read what to do
cat README.md

# Run the script
python3 load_one_file.py
```

### Step 3: Follow Day-by-Day Plan
- Each day has its own folder
- Each folder has a README.md explaining what to do
- Each folder has Python scripts with detailed comments
- Work through them one day at a time!

---

## 📅 Day-by-Day Plan (2-3 Hours Per Day)

### Day 1: Setup ⚙️
**Goal:** Get everything installed and working
- Install Python packages
- Download data (already done!)
- Test that everything works
- **Time:** 2 hours

**Questions to Think About:**
- What Python packages do I need? Why?
- What is the data file format? (TSV vs CSV)
- How do I check if something is installed correctly?

---

### Day 2: Explore Data 🔍
**Goal:** Look at one patient's data file
- Load a TSV file using pandas
- See what columns exist
- Understand what each column means
- **Time:** 2-3 hours

**Questions to Think About:**
- What does `pd.read_csv()` do? (Hint: TSV files use `sep='\t'`)
- What is a TCR sequence? (It's a string of amino acids)
- What does "productive" mean? (In-frame sequences that work)
- How many sequences does one patient have?

---

### Day 3: Clean Data 🧹
**Goal:** Remove bad data and prepare for analysis
- Filter to only productive sequences
- Remove sequences with invalid characters
- Aggregate duplicate sequences
- **Time:** 2-3 hours

**Questions to Think About:**
- Why do we filter to "productive" sequences only?
- What does `df.groupby().sum()` do? (Hint: combines duplicates)
- Why might the same sequence appear multiple times?

---

### Day 4: Understand Data 📊
**Goal:** Calculate statistics and visualize
- Calculate basic statistics (mean, median, etc.)
- Make plots (histograms, bar charts)
- Understand the distribution of sequences
- **Time:** 2-3 hours

**Questions to Think About:**
- What is "diversity" in TCR data? (More unique sequences = more diverse)
- What is "clonality"? (Opposite of diversity - few sequences dominate)
- How do responders differ from non-responders?

---

### Day 5: Encode Sequences 🔢
**Goal:** Convert strings to numbers (for machine learning)
- Understand one-hot encoding (like `pd.get_dummies()`)
- Encode one amino acid sequence
- Encode all sequences for one patient
- **Time:** 3 hours

**Questions to Think About:**
- Why do we need to convert strings to numbers? (Computers work with numbers!)
- What is one-hot encoding? (One 1, rest 0s - like `pd.get_dummies()`)
- What shape will the encoded array be? (sequences × positions × amino_acids)

---

### Day 6: Multiple Patients 👥
**Goal:** Work with all patients at once
- Load multiple patient files
- Compare responders vs non-responders
- Calculate statistics across all patients
- **Time:** 2-3 hours

**Questions to Think About:**
- How do I loop through multiple files? (Use `glob` or `os.listdir()`)
- How do I merge patient data with response labels? (Use `pd.merge()`)
- What patterns do I see between responders and non-responders?

---

### Day 7: Simple ML 🤖
**Goal:** Try simple machine learning approaches
- Mean pooling (average all sequences)
- Max pooling (take strongest sequence)
- Use sklearn to train a simple classifier
- **Time:** 3 hours

**Questions to Think About:**
- Why can't I just use `model.fit(X, y)` directly? (One patient = many sequences = one label!)
- What is "pooling"? (Combining many things into one)
- Why might simple averaging not work well?

---

### Day 8: Understand MIL 🎓
**Goal:** Learn about Multiple Instance Learning
- Understand the "bag of instances" concept
- Learn why normal ML doesn't work here
- Understand what attention mechanism does
- **Time:** 2-3 hours

**Questions to Think About:**
- What is Multiple Instance Learning? (Many instances → one label)
- Why is this different from normal ML? (Normal: one instance → one label)
- What does "attention" mean? (Learning which sequences matter)

---

### Day 9: DeepTCR Setup 📦
**Goal:** Install and set up the DeepTCR package
- Install DeepTCR (may take time!)
- Understand what DeepTCR does
- Load data using DeepTCR format
- **Time:** 2 hours

**Questions to Think About:**
- What does DeepTCR package do? (It's the actual model from the paper!)
- How is DeepTCR different from sklearn? (It handles MIL automatically)
- What format does DeepTCR expect?

---

### Day 10: Run DeepTCR 🚀
**Goal:** Train the actual model from the paper
- Load data in DeepTCR format
- Train the model
- Make predictions
- Evaluate results
- **Time:** 3 hours

**Questions to Think About:**
- How do I train the model? (Use `model.Train_Supervised_Repertoire()`)
- How do I make predictions? (Use `model.Predict_Repertoire()`)
- How do I evaluate if it worked? (Calculate AUC, accuracy, etc.)

---

## 📚 How to Use This Guide

### For Each Day:

1. **Read the README.md in that day's folder**
   - Explains what you'll learn
   - Lists what to do
   - Has questions to think about

2. **Open the Python scripts**
   - Read the comments (they explain everything!)
   - Run the scripts
   - Modify them to experiment

3. **Answer the questions**
   - Think about them before coding
   - Write down your answers
   - Discuss with others if possible

4. **Don't rush!**
   - Take your time
   - If something doesn't make sense, re-read
   - Experiment and play around

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

### What Does This Paper Do?

1. **Input:** Patient's TCR sequences (50,000 sequences)
2. **Process:** 
   - Convert sequences to numbers (encoding)
   - Use neural network to find important sequences (attention)
   - Combine information from all sequences (aggregation)
3. **Output:** Prediction (will patient respond? Yes/No + probability)

**In simple terms:**
- Look at all T cell barcodes
- Find patterns that predict response
- Use those patterns to predict for new patients

---

## 🛠️ What Tools Will You Use?

### Python (You know this!)
- Basic Python syntax
- Functions, loops, conditionals
- File I/O

### Pandas (You know this!)
```python
pd.read_csv()        # Read files
df.head()            # Preview data
df.groupby()         # Group and aggregate
df.merge()           # Combine DataFrames
```

### NumPy (You know this!)
```python
np.array()           # Create arrays
arr.shape           # Get dimensions
arr.mean()          # Calculate statistics
```

### Matplotlib (You might know this!)
```python
plt.plot()          # Make line plots
plt.hist()          # Make histograms
plt.bar()           # Make bar charts
```

### Sklearn (You know this!)
```python
train_test_split()  # Split data
RandomForestClassifier()  # Simple ML model
```

### DeepTCR (New!)
- Package from the paper
- Handles Multiple Instance Learning automatically
- You'll learn this in Days 9-10

---

## ❓ Common Questions

### Q: I'm stuck! What do I do?
**A:** 
1. Read the error message carefully - it usually tells you what's wrong
2. Check the comments in the code - they explain what each line does
3. Re-read the day's README.md
4. Google the error message (someone else probably had the same problem!)
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

### Q: What if I don't understand something?
**A:** 
- That's normal! Research papers are hard
- Re-read the explanation
- Try the code yourself
- Experiment and see what happens
- Each day builds on the previous, so make sure you understand Day 1 before Day 2

### Q: Can I skip days?
**A:** 
- **Not recommended!** Each day builds on the previous
- If you're really stuck on one day, you can review previous days
- But try to complete them in order

---

## 📖 Additional Resources

### Guides (in `guides/` folder):
- **pandas_to_deeptcr_guide.md**: Connects pandas concepts to DeepTCR
- **dataset_exploration_guide.md**: Detailed data structure explanation
- **deeptcr_architecture.md**: How the model works (more advanced)
- **data_shapes_walkthrough.md**: Understanding array dimensions

### When to Read These:
- Read guides as you need them
- Don't read everything at once!
- Each day's README will tell you if you need a specific guide

---

## ✅ Checklist: Are You Ready?

Before starting, make sure you:
- [ ] Have Python 3.7+ installed (`python3 --version`)
- [ ] Know basic Python (variables, functions, loops)
- [ ] Know pandas basics (`pd.read_csv()`, `df.head()`, etc.)
- [ ] Know numpy basics (`np.array()`, `arr.shape`, etc.)
- [ ] Know sklearn basics (`train_test_split()`, simple models)
- [ ] Have 2-3 hours per day for 10 days
- [ ] Are ready to learn and experiment!

---

## 🎉 You're Ready to Start!

**Next Step:** Go to `Day_01_Setup/` folder and read `README.md`

**Remember:**
- Take your time
- Read the comments
- Experiment
- Ask questions (even if just to yourself!)
- Have fun learning!

**Good luck! You've got this! 🚀**

---

## 📝 Notes Section

Use this space to write down:
- Things you learned each day
- Questions you have
- Ideas to explore
- Anything else!

---

*Last updated: [Date]*
*For questions or issues, check the day-specific README files or the guides folder.*
