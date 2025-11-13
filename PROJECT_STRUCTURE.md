# Project Structure Guide

## 📁 Complete Directory Structure

```
DeepTCR_Learning/
│
├── README.md                          ⭐ START HERE - Main guide
│
├── Day_01_Setup/                      📅 Day 1: Set up everything
│   ├── README.md                      (What to do today)
│   ├── setup_project.py               (Run this first!)
│   └── test_setup.py                  (Check if everything works)
│
├── Day_02_Explore_Data/               📅 Day 2: Look at the data
│   ├── README.md                      (What to do today)
│   ├── load_one_file.py               (Load one patient's data)
│   └── explore_dataframe.py           (See what's in the data)
│
├── Day_03_Clean_Data/                 📅 Day 3: Clean the data
│   ├── README.md                      (What to do today)
│   ├── filter_sequences.py            (Remove bad data)
│   └── aggregate_data.py              (Combine duplicates)
│
├── Day_04_Understand_Data/            📅 Day 4: Understand what you have
│   ├── README.md                      (What to do today)
│   ├── calculate_statistics.py       (Basic stats)
│   └── visualize_data.py             (Make plots)
│
├── Day_05_Encode_Sequences/           📅 Day 5: Convert strings to numbers
│   ├── README.md                      (What to do today)
│   ├── encode_one_sequence.py         (One sequence → array)
│   └── encode_all_sequences.py        (All sequences → arrays)
│
├── Day_06_Multiple_Patients/          📅 Day 6: Work with many patients
│   ├── README.md                      (What to do today)
│   ├── load_multiple_patients.py      (Load all patients)
│   └── compare_patients.py            (Compare responders vs non-responders)
│
├── Day_07_Simple_ML/                  📅 Day 7: Try simple machine learning
│   ├── README.md                      (What to do today)
│   ├── mean_pooling_baseline.py       (Simple approach)
│   └── sklearn_baseline.py            (Use sklearn)
│
├── Day_08_Understand_MIL/             📅 Day 8: Learn Multiple Instance Learning
│   ├── README.md                      (What to do today)
│   └── mil_explained.py              (What is MIL?)
│
├── Day_09_DeepTCR_Setup/              📅 Day 9: Set up DeepTCR package
│   ├── README.md                      (What to do today)
│   └── install_deeptcr.py             (Install the package)
│
├── Day_10_Run_DeepTCR/                📅 Day 10: Run the actual model
│   ├── README.md                      (What to do today)
│   └── train_model.py                 (Train DeepTCR model)
│
├── data/                              📊 All the data files
│   └── DeepTCR_Cancer-master/
│       └── Data/
│           └── yost/
│               ├── data/              (37 patient files)
│               └── response.csv        (Who responded?)
│
├── guides/                             📚 Learning guides (read as needed)
│   ├── pandas_to_deeptcr_guide.md    (Connect pandas to DeepTCR)
│   ├── dataset_exploration_guide.md  (Understand the data)
│   ├── deeptcr_architecture.md        (How the model works)
│   └── data_shapes_walkthrough.md    (Array dimensions explained)
│
├── requirements.txt                    📦 Python packages needed
└── PROJECT_STRUCTURE.md               📋 This file
```

---

## 🎯 How to Navigate This Project

### For Beginners:

1. **Start with README.md** (main guide)
   - Explains what the project is about
   - Shows the day-by-day plan
   - Answers common questions

2. **Go to Day_01_Setup/**
   - Read README.md in that folder
   - Run setup_project.py
   - Run test_setup.py

3. **Follow Day-by-Day**
   - Each day has its own folder
   - Each folder has a README.md explaining what to do
   - Each folder has Python scripts with detailed comments

4. **Use Guides When Needed**
   - Don't read everything at once!
   - Each day's README will tell you if you need a specific guide
   - Guides are in the `guides/` folder

---

## 📝 File Naming Conventions

### Scripts:
- `*_setup.py` - Setup/installation scripts
- `*_test.py` - Testing scripts
- `load_*.py` - Data loading scripts
- `filter_*.py` - Data filtering scripts
- `encode_*.py` - Encoding scripts
- `train_*.py` - Model training scripts

### Documentation:
- `README.md` - Main guide for each day/folder
- `*_guide.md` - Detailed guides (in guides/ folder)
- `PROJECT_STRUCTURE.md` - This file

---

## 🔍 Finding What You Need

### "I want to..."
- **Set up the project:** → `Day_01_Setup/`
- **See what the data looks like:** → `Day_02_Explore_Data/`
- **Clean the data:** → `Day_03_Clean_Data/`
- **Understand the data:** → `Day_04_Understand_Data/`
- **Convert sequences to numbers:** → `Day_05_Encode_Sequences/`
- **Work with multiple patients:** → `Day_06_Multiple_Patients/`
- **Try machine learning:** → `Day_07_Simple_ML/`
- **Learn about MIL:** → `Day_08_Understand_MIL/`
- **Install DeepTCR:** → `Day_09_DeepTCR_Setup/`
- **Train the model:** → `Day_10_Run_DeepTCR/`
- **Understand concepts:** → `guides/` folder

---

## 📚 Guide Files Explained

### `guides/pandas_to_deeptcr_guide.md`
- **When to read:** Days 2-5
- **What it covers:** Connects pandas concepts to DeepTCR
- **Why:** Helps you understand using what you already know

### `guides/dataset_exploration_guide.md`
- **When to read:** Days 2-3
- **What it covers:** Detailed data structure explanation
- **Why:** Deep dive into what the data files contain

### `guides/deeptcr_architecture.md`
- **When to read:** Days 8-10
- **What it covers:** How the DeepTCR model works
- **Why:** Understand the model architecture

### `guides/data_shapes_walkthrough.md`
- **When to read:** Day 5
- **What it covers:** Understanding array dimensions
- **Why:** Helps with encoding sequences

---

## 🎓 Learning Path Summary

### Week 1 (Days 1-5): Data Basics
- Day 1: Setup
- Day 2: Explore data
- Day 3: Clean data
- Day 4: Understand data
- Day 5: Encode sequences

### Week 2 (Days 6-10): Machine Learning
- Day 6: Multiple patients
- Day 7: Simple ML
- Day 8: Understand MIL
- Day 9: DeepTCR setup
- Day 10: Run DeepTCR

---

## 💡 Tips for Success

1. **Work through days in order** - Each builds on the previous
2. **Read the README.md first** - It explains what to do
3. **Read the code comments** - They explain what each line does
4. **Do the exercises** - They reinforce learning
5. **Take notes** - Write down what you learn
6. **Don't rush** - Understanding is more important than speed
7. **Ask questions** - Even if just to yourself!

---

## 🆘 Getting Help

### If you're stuck:
1. Check the day's README.md
2. Read the code comments
3. Check error messages carefully
4. Google the error message
5. Review previous days

### Common issues:
- **File not found:** Check you're in the right directory
- **Import error:** Package not installed (run setup script)
- **Column error:** Column name might be different (check with df.columns)

---

*This structure is designed to help you learn step by step. Take your time and enjoy the journey! 🚀*
