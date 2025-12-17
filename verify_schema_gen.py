import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

from models import generate_schema_prompt

sample_data = [
    {"name": "Alice", "age": 30, "city": "New York"},
    {"name": "Bob", "age": 25, "city": "Los Angeles"}
]

try:
    prompt = generate_schema_prompt(sample_data)
    print("✅ Prompt generation successful.")
    print("--- Prompt Preview ---")
    print(prompt[:100] + "...")
except Exception as e:
    print(f"❌ Verification failed: {e}")
