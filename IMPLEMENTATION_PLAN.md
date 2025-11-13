# Implementation Plan - Based on LEARNING_ROADMAP.md

## Mapping: Roadmap Weeks → Day-by-Day Notebooks

### Week 1: Data Familiarization → Days 1-2

**Day 1: Setup & First Look**
- Setup environment
- Download/extract data
- Load first TSV file
- Understand file structure

**Day 2: Explore Data**
- Load multiple patient files (5 different patients)
- Calculate average repertoire size
- Find most common V genes across all patients
- Plot sequence length distributions
- Understand columns: CDR3 sequences, V/D/J genes, read counts, frequencies

### Week 2: From Pandas to Arrays → Days 3-4

**Day 3: Clean & Preprocess**
- Filter to productive sequences
- Remove invalid amino acids
- Aggregate duplicates
- Prepare clean data

**Day 4: Encoding Sequences**
- Implement one-hot encoding for amino acids
- Encode V/D/J genes as one-hot vectors
- Combine all features for one TCR
- Encode one patient's entire repertoire
- Understand shape transformations: (50k, 4) → (50k, 40, 20) → (50k, 2192)

### Week 3: Multiple Instance Learning → Days 5-6

**Day 5: Understand MIL Concept**
- Compare traditional ML vs MIL
- Understand bag of sequences concept
- Implement mean pooling baseline
- Implement max pooling baseline
- Try sklearn baseline with mean pooling

**Day 6: Why Simple Pooling Fails**
- Compare mean/max pooling to random prediction
- Understand why simple averaging isn't enough
- Understand need for attention/weighting
- Repertoire-level vs sequence-level concepts

### Week 4: Understanding DeepTCR Architecture → Days 7-8

**Day 7: Architecture Components**
- Study architecture diagram
- Understand embedding layer
- Understand attention layer (KEY INNOVATION)
- Understand aggregation layer
- Understand classification layer

**Day 8: Trace Through Architecture**
- Draw architecture yourself
- Trace one sequence through network
- Understand what "concept" means
- Calculate number of parameters

### Week 5: Install and Run DeepTCR → Days 9-10

**Day 9: DeepTCR Setup**
- Install DeepTCR package
- Understand DeepTCR API
- Load data in DeepTCR format
- Understand data loading format

**Day 10: Train & Predict**
- Train model on Yost data
- Understand training hyperparameters
- Make predictions
- Interpret results

### Week 6: Reproducing Paper Results → Day 11 (Optional/Advanced)

**Day 11: Advanced Analysis**
- Evaluate AUC (target ~0.82)
- Extract attention weights
- Identify predictive sequences
- Compare responders vs non-responders
- Visualize results

---

## Notebook Structure for Each Day

Each notebook should have:

1. **Markdown Header**
   - Day number and title
   - Goal for the day
   - Time estimate
   - Difficulty level

2. **Questions to Think About**
   - Questions before starting
   - Build logical thinking

3. **Step-by-Step Exercises**
   - Each step has:
     - Markdown explanation
     - Code cell with TODO
     - Hints (not solutions!)
     - Expected output description

4. **Summary**
   - What was learned
   - Key concepts
   - Next steps

5. **Notes Section**
   - Space for student notes

---

## Key Principles

1. **Students write code themselves** - No complete solutions, only TODOs
2. **Follow roadmap exercises** - Each notebook covers roadmap tasks
3. **Progressive difficulty** - Each day builds on previous
4. **Clear explanations** - Simple language, relate to pandas/numpy
5. **Hands-on learning** - Learn by doing, not copying

---

## Validation Checklist

For each notebook:
- [ ] Covers roadmap tasks for that week/day
- [ ] Has TODO sections (not complete code)
- [ ] Has clear explanations
- [ ] Has questions to think about
- [ ] Has hints (not solutions)
- [ ] Builds on previous days
- [ ] Uses simple language
- [ ] Relates to pandas/numpy concepts
