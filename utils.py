import pandas as pd
import streamlit as st

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
