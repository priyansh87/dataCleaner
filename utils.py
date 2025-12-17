import pandas as pd
import streamlit as st

def analyze_results(results):
    """
    Analyzes list of JSON results.
    Returns:
        valid_list: List of good objects
        flagged_list: List of objects with issues (index, reason, object)
        stats: Dictionary with counts
    """
    valid_list = []
    flagged_list = []
    
    for idx, obj in enumerate(results):
        # Check for error / invalid JSON
        if "error" in obj:
            flagged_list.append({
                "index": idx + 1,
                "reason": "Invalid JSON / Parsing Error",
                "data": obj
            })
            continue
            
        # Check for null density
        if isinstance(obj, dict):
            total_keys = len(obj)
            null_keys = 0
            for key, value in obj.items():
                if value is None or value == "" or str(value).lower() == "null":
                    null_keys += 1
            
            # Threshold: If > 50% keys are null explain
            if total_keys > 0 and (null_keys / total_keys) > 0.5:
                flagged_list.append({
                    "index": idx + 1,
                    "reason": f"High Null Density ({null_keys}/{total_keys} fields empty)",
                    "data": obj
                })
            else:
                valid_list.append(obj)
        else:
            # Should be a dict, if list or other, pass but maybe flag? 
            # For now assume valid if it's a valid object
            valid_list.append(obj)
            
    return valid_list, flagged_list

def load_data(uploaded_file):
    """Loads CSV or Excel file into a Pandas DataFrame."""
    try:
        if uploaded_file.name.endswith('.csv'):
            return pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(('.xls', '.xlsx')):
            return pd.read_excel(uploaded_file)
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None

def extract_schema(uploaded_file):
    """Extracts fields from the reference file (CSV, Excel, or JSON)."""
    try:
        if uploaded_file.name.endswith('.csv'):
             df = pd.read_csv(uploaded_file)
             fields = list(df.columns)
        elif uploaded_file.name.endswith('.json'):
             import json
             data = json.load(uploaded_file)
             if isinstance(data, list):
                 if data:
                    fields = list(data[0].keys())
                 else:
                    fields = []
             elif isinstance(data, dict):
                 fields = list(data.keys())
             else:
                 fields = []
        else:
             df = pd.read_excel(uploaded_file)
             fields = list(df.columns)
        
        schema_template = {field: "Data Type/Description" for field in fields}
        return schema_template
    except Exception as e:
        st.error(f"Error extracting schema: {e}")
        return None
