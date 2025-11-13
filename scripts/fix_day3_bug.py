#!/usr/bin/env python3
"""
Fix the Day 3 bug where starting_count is used before definition.
This script fixes the notebook programmatically.
"""

import json
from pathlib import Path

# Path to the notebook
notebook_path = Path("Day_03_Clean_Data/Day_03_Clean_Data.ipynb")

# Read the notebook
with open(notebook_path, 'r', encoding='utf-8') as f:
    notebook = json.load(f)

# Find the cell with the bug (Step 1: Load Data)
# It's the second code cell (index 1)
bug_cell_idx = None
for idx, cell in enumerate(notebook['cells']):
    if cell['cell_type'] == 'code':
        source = ''.join(cell['source'])
        if 'Track starting count' in source and 'starting_count' in source:
            bug_cell_idx = idx
            break

if bug_cell_idx is None:
    print("⚠️ Could not find the bug cell!")
    exit(1)

# Get the cell
cell = notebook['cells'][bug_cell_idx]
source_lines = cell['source']

# Find the problematic section
new_source = []
i = 0
while i < len(source_lines):
    line = source_lines[i]
    
    # Check if this is the problematic if block
    if 'if df is not None:' in line:
        new_source.append(line)
        i += 1
        
        # Check if next line is empty (the bug)
        if i < len(source_lines) and source_lines[i].strip() == '':
            # Skip the empty line and add the fix
            i += 1
            new_source.append("            # Track starting count AFTER loading\n")
            new_source.append("            starting_count = len(df)\n")
            new_source.append("            print(f\"✓ Loaded {starting_count:,} sequences\")\n")
            new_source.append("            print(f\"  This is the RAW data - includes errors and duplicates\")\n")
            continue
    
    # Check if this is the problematic print statement
    if '# Track starting count' in line and 'starting_count' in ''.join(source_lines[i:i+3]):
        # This is the bug - starting_count used before definition
        # Skip these lines (they're outside the if block incorrectly)
        i += 3
        continue
    
    new_source.append(line)
    i += 1

# Update the cell
cell['source'] = new_source

# Write back
with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=1, ensure_ascii=False)

print(f"✅ Fixed bug in {notebook_path}")
print("   - starting_count is now defined inside the if df is not None block")
print("   - Added fallback to None if df is not loaded")
