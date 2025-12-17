import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

from utils import analyze_results

# Test Data
test_results = [
    # 1. Valid
    {"name": "Alice", "age": 30, "city": "NY"},
    # 2. Error
    {"error": "Invalid JSON", "raw_output": "...", "input": {}},
    # 3. High Null Density (3/4 = 75%)
    {"name": "Bob", "age": None, "city": "", "country": "null"},
    # 4. Borderline (2/4 = 50%) - Should be Valid based on > 0.5 logic
    {"name": "Charlie", "age": 25, "city": None, "country": ""}
]

valid, flagged = analyze_results(test_results)

print(f"Total: {len(test_results)}")
print(f"Valid: {len(valid)}")
print(f"Flagged: {len(flagged)}")

print("\n--- Flagged Items ---")
for item in flagged:
    print(f"Index {item['index']}: {item['reason']}")

# Assertions
assert len(valid) == 2, f"Expected 2 valid items, got {len(valid)}"
assert len(flagged) == 2, f"Expected 2 flagged items, got {len(flagged)}"
assert flagged[0]['index'] == 2 # The error one
assert flagged[1]['index'] == 3 # The null heavy one

print("\n✅ Verification Successful!")
