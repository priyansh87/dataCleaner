import streamlit as st
import json
import time
from utils import load_data, extract_schema, analyze_results
from models import get_ollama_models, process_with_ollama, process_with_groq, generate_schema_from_sample_ollama, generate_schema_from_sample_groq

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
    schema_file = st.file_uploader("Upload Structure Reference (Excel/CSV/JSON)", type=['xlsx', 'xls', 'csv', 'json'], key="schema_file")
    if schema_file:
        schema_template = extract_schema(schema_file)
        if schema_template:
            st.json(schema_template, expanded=False)
            st.caption("Extracted Schema Structure")
    
    # Auto-Schema Generation Logic
    else:
        st.divider()
        st.write("OR")
        if st.button("✨ Auto-Generate Schema from Data"):
            if input_df is not None:
                # Take first 4 rows
                sample_data = input_df.head(4).to_dict(orient='records')
                
                with st.spinner("Analyzing data to generate schema..."):
                    generated_schema_str = ""
                    if model_provider == "Ollama (Local)":
                        generated_schema_str = generate_schema_from_sample_ollama(sample_data, model_name)
                    else:
                        if not api_key:
                             st.error("Groq API Key required for generation.")
                        else:
                             generated_schema_str = generate_schema_from_sample_groq(sample_data, api_key, model_name)
                    
                    if generated_schema_str:
                         # Try to parse
                         try:
                             # Clean markdown
                             if "```json" in generated_schema_str:
                                 generated_schema_str = generated_schema_str.split("```json")[1].split("```")[0].strip()
                             elif "```" in generated_schema_str:
                                 generated_schema_str = generated_schema_str.split("```")[1].split("```")[0].strip()
                             
                             st.session_state['generated_schema'] = json.loads(generated_schema_str)
                             # Reset confirmed schema if new generation happens
                             if 'confirmed_schema' in st.session_state:
                                 del st.session_state['confirmed_schema']
                         except Exception as e:
                             st.error(f"Failed to parse generated schema: {e}")
                             st.text(generated_schema_str)

            else:
                st.warning("Please upload Input Data (Column 1) first.")

    # Display Generated Schema if available
    if 'generated_schema' in st.session_state:
        st.success("Schema Generated!")
        st.json(st.session_state['generated_schema'])
        
        if st.button("Use Processed Schema"):
             st.session_state['confirmed_schema'] = st.session_state['generated_schema']
             st.rerun()

    if 'confirmed_schema' in st.session_state and not schema_file:
         schema_template = st.session_state['confirmed_schema']
         st.info("Using Auto-Generated Schema")
         st.json(schema_template, expanded=False)

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
            
            # --- Post-Processing & Results ---
            st.divider()
            st.subheader("4. Post-Processing & Results")
            
            valid_results, flagged_results = analyze_results(results)
            
            col_res1, col_res2 = st.columns(2)
            col_res1.metric("Total Processed", len(results))
            col_res2.metric("Valid Objects", len(valid_results))
            
            final_data = results # Default to all
            
            if flagged_results:
                st.warning(f"⚠️ {len(flagged_results)} Possibly Invalid/Empty Objects Detected")
                
                with st.expander("View Flagged Items"):
                    for item in flagged_results:
                        st.markdown(f"**Row {item['index']}**: {item['reason']}")
                        st.json(item['data'])
                
                exclude_flagged = st.checkbox("Exclude flagged items from final download", value=True)
                if exclude_flagged:
                    final_data = valid_results
                    st.success(f"Filtering applied. Download will contain {len(final_data)} valid objects.")
                else:
                    st.info("Including all items (processed and flagged) in download.")
            else:
                 st.success("✅ All items processed successfully with no quality issues detected.")
            
            st.subheader("Final Output")
            st.json(final_data)
            
            json_string = json.dumps(final_data, indent=2)
            st.download_button(
                label="Download JSON",
                data=json_string,
                file_name="converted_data.json",
                mime="application/json"
            )

else:
    st.divider()
    st.info("👆 Please upload both an Input File and a Reference Schema to enable the conversion.")
