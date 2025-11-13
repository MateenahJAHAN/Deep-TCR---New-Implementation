# Clean Project Structure

## 📁 Directory Organization

```
DeepTCR_Learning/
│
├── README.md                          ⭐ Main guide - START HERE!
├── START_HERE.md                      📍 Quick start guide
├── LEARNING_ROADMAP.md                📚 Original learning roadmap
├── requirements.txt                   📦 Python packages needed
│
├── Day_00_Getting_Started/            📅 Day 0: Absolute beginner setup
│   └── Day_00_Getting_Started.ipynb   📓 How to use Jupyter/Colab
│
├── Day_01_Setup/                      📅 Day 1: Set up Python packages
│   └── Day_01_Setup.ipynb             📓 Install packages, verify setup
│
├── Day_02_Explore_Data/               📅 Day 2: Explore TCR data
│   └── Day_02_Explore_Data.ipynb      📓 Load files, understand structure
│
├── Day_03_Clean_Data/                 📅 Day 3: Clean data
│   └── Day_03_Clean_Data.ipynb        📓 Filter, validate, aggregate
│
├── Day_04_Understand_Data/            📅 Day 4: Statistics & visualization
│   └── Day_04_Understand_Data.ipynb   📓 Calculate stats, make plots
│
├── Day_05_Encode_Sequences/           📅 Day 5: Encode sequences
│   └── Day_05_Encode_Sequences.ipynb  📓 Convert strings to numbers
│
├── Day_06_Multiple_Patients/          📅 Day 6: Work with multiple patients
│   └── Day_06_Multiple_Patients.ipynb 📓 Load all patients, create batches
│
├── Day_07_Simple_ML/                  📅 Day 7: Simple ML baselines
│   └── Day_07_Simple_ML.ipynb         📓 Mean/max pooling, sklearn baseline
│
├── Day_08_Understand_MIL/             📅 Day 8: Multiple Instance Learning
│   └── Day_08_Understand_MIL.ipynb    📓 Understand MIL concept
│
├── Day_09_DeepTCR_Setup/              📅 Day 9: Install DeepTCR
│   └── Day_09_DeepTCR_Setup.ipynb     📓 Install package, understand API
│
├── Day_10_Run_DeepTCR/                📅 Day 10: Train DeepTCR model
│   └── Day_10_Run_DeepTCR.ipynb       📓 Train, predict, evaluate
│
├── data/                              📊 All data files
│   └── DeepTCR_Cancer-master/
│       └── Data/
│           └── yost/
│               ├── data/              (37 patient TSV files)
│               └── response.csv       (Patient labels)
│
├── scripts/                           🔧 Utility scripts
│   ├── setup_project.py               (Setup helper)
│   └── tcr_explorer.py                (Example exploration)
│
└── docs/                              📚 Documentation
    ├── IMPLEMENTATION_PLAN.md          (Roadmap mapping)
    ├── PROJECT_STRUCTURE_CLEAN.md      (This file)
    ├── STATUS.md                      (What's done/needed)
    ├── pandas_to_deeptcr_guide.md     (Learning guides)
    ├── dataset_exploration_guide.md
    ├── deeptcr_architecture.md
    └── data_shapes_walkthrough.md
```

## 🎯 Key Points

1. **Day folders** - Each day has one notebook (.ipynb)
2. **Data folder** - All data files organized here
3. **Scripts folder** - Helper scripts (optional)
4. **Docs folder** - All documentation and guides

## 📝 File Naming

- Notebooks: `Day_XX_Topic/Day_XX_Topic.ipynb`
- Data: `data/DeepTCR_Cancer-master/Data/...`
- Docs: `docs/filename.md`

## 🚀 Getting Started

1. Read `README.md`
2. Start with `Day_00_Getting_Started/Day_00_Getting_Started.ipynb`
3. Work through days 0-10 in order
4. Each notebook has TODOs - you write the code!
