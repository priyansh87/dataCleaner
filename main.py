import streamlit as st
import json
import time
from utils import load_data, extract_schema
from models import get_ollama_models, process_with_ollama, process_with_groq

st.set_page_config(page_title="Universal Data Converter", layout="wide")

st.title("📂 Universal Data to JSON Converter")
st.markdown("Convert your CSV/Excel data into a structured JSON format using Local LLMs (Ollama) or Cloud Models (Groq).")

# --- Sidebar Configuration ---
with st.sidebar:
    st.header("⚙️ Configuration")
    
    model_provider = st.radio("Select Inference Provider", ["Ollama (Local)", "Groq (Cloud)"])
    
    api_key = None
    model_name = ""
    
    if model_provider == "Groq (Cloud)":
        api_key = st.text_input("Enter Groq API Key", type="password")
        model_name = st.text_input("Model Name", value="groq/compound-mini", help="Recommended: groq/compound-mini or llama3-8b-8192")
        if not model_name:
             model_name = "groq/compound-mini" 
    else:
        available_models = get_ollama_models()
        if available_models:
            model_name = st.selectbox("Select Ollama Model", available_models, index=0)
        else:
            st.warning("Could not connect to Ollama. Make sure it's running.")
            model_name = st.text_input("Ollama Model Name", value="llama2")
        st.info("Make sure Ollama is running locally: `ollama serve`")

# --- Main Content ---
col1, col2 = st.columns(2)

input_df = None
schema_template = None

with col1:
    st.subheader("1. Upload Input Data")
    input_file = st.file_uploader("Upload CSV or Excel file", type=['csv', 'xlsx', 'xls'], key="input_file")
    if input_file:
        input_df = load_data(input_file)
        if input_df is not None:
            st.dataframe(input_df.head(), use_container_width=True)
            st.caption(f"Loaded {len(input_df)} rows.")

with col2:
    st.subheader("2. Upload Target Schema")
    schema_file = st.file_uploader("Upload Structure Reference (Excel)", type=['xlsx', 'xls', 'csv'], key="schema_file")
    if schema_file:
        schema_template = extract_schema(schema_file)
        if schema_template:
            st.json(schema_template, expanded=False)
            st.caption("Extracted Schema Structure")

# --- Conversion Logic ---
if input_df is not None and schema_template is not None:
    st.divider()
    st.subheader("3. Start Conversion")
    st.caption(f"Ready to process all {len(input_df)} rows.")
    
    if st.button("Start Conversion", type="primary"):
        if model_provider == "Groq (Cloud)" and not api_key:
            st.error("Please enter a valid Groq API Key.")
        else:
            results = []
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Process ALL rows by default
            rows_to_process = input_df
            total_rows = len(rows_to_process)
            
            for index, row in rows_to_process.iterrows():
                row_data = row.to_dict()
                status_text.text(f"Processing row {index + 1}/{total_rows}...")
                
                json_output = ""
                if model_provider == "Ollama (Local)":
                    json_output = process_with_ollama(row_data, schema_template, model_name)
                else:
                    json_output = process_with_groq(row_data, schema_template, api_key, model_name)
                    
                    # Rate limiting delay loop
                    if index < total_rows - 1:
                        for remaining in range(10, 0, -1):
                            status_text.text(f"Processing row {index + 1}/{total_rows}... Done. Waiting {remaining}s...")
                            time.sleep(1)
                
                # Validation / Parsing
                try:
                    # Clean markdown
                    if "```json" in json_output:
                        json_output = json_output.split("```json")[1].split("```")[0].strip()
                    elif "```" in json_output:
                         json_output = json_output.split("```")[1].split("```")[0].strip()
                    
                    parsed_json = json.loads(json_output)
                    results.append(parsed_json)
                except json.JSONDecodeError:
                    st.warning(f"Row {index+1} failed to generate valid JSON. Raw output saved.")
                    results.append({"error": "Invalid JSON", "raw_output": json_output, "input": row_data})
                
                progress_bar.progress((index + 1) / total_rows)
            
            status_text.success("Conversion Complete!")
            
            # --- Results & Download ---
            st.subheader("Results")
            st.json(results)
            
            json_string = json.dumps(results, indent=2)
            st.download_button(
                label="Download JSON",
                data=json_string,
                file_name="converted_data.json",
                mime="application/json"
            )

else:
    st.divider()
    st.info("👆 Please upload both an Input File and a Reference Schema to enable the conversion.")
