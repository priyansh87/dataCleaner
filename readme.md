# Universal Data to JSON Converter - User Instructions

## 1. Project Overview
The **Universal Data to JSON Converter** is a powerful Streamlit web application designed to intelligently convert raw data from CSV or Excel files into structured JSON formats. It leverages Large Language Models (LLMs) to map your input data to a specific schema defined by you.

This tool is flexible, offering both **Local** (Ollama) and **Cloud** (Groq) processing options to suit your privacy and performance needs.

---

## 2. Key Features
*   **Dual Inference Modes:**
    *   **Local (Ollama):** Run entirely on your machine for maximum privacy using models like `llama3`. No data leaves your system.
    *   **Cloud (Groq):** Use Groq's high-speed API for faster processing (requires an API Key).
*   **Flexible Inputs:** Supports standard `.csv`, `.xlsx`, and `.xls` files.
*   **Custom Schema Definition:** Define your output JSON structure simply by uploading a reference Excel/CSV file with your desired column headers.
*   **Batch Processing:** Automatically processes every row in your input file.
*   **Automatic JSON Validation:** Ensures the output is valid JSON, handling errors gracefully.
*   **Downloadable Results:** Export the converted data as a ready-to-use `.json` file.

---

## 3. Prerequisites

Before setting up the application, ensure you have the following:

### Software
*   **Python 3.8 or higher** installed on your system.
*   *(Optional but Recommended)* **Ollama**: If you plan to use local models. Download from [ollama.com](https://ollama.com).

### Accounts/Keys
*   *(Optional)* **Groq API Key**: If you plan to use the Cloud mode. Get it from [console.groq.com](https://console.groq.com).

---

## 4. Installation & Setup

Follow these steps to get the application running on your local machine.

### Step 1: Set up the Project Directory
Ensure you are in the project folder containing `main.py` and `requirements.txt`.

### Step 2: Create a Virtual Environment (Optional)
It's good practice to use a virtual environment to manage dependencies.
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
Install the required Python packages using pip:
```bash
pip install -r requirements.txt
```

### Step 4: Run the Application
Start the Streamlit app:
```bash
streamlit run main.py
```
The application should open automatically in your default web browser (usually at `http://localhost:8501`).

---

## 5. Usage Guide

### Section A: Configuration (Sidebar)
1.  **Select Inference Provider:**
    *   **Ollama (Local):** Choose this for offline/private processing.
        *   **Note:** You must have Ollama running in the background (`ollama serve` in a terminal).
        *   Select your model (e.g., `llama2`) from the dropdown.
    *   **Groq (Cloud):** Choose this for speed.
        *   Enter your **Groq API Key**.
        *   (Optional) Specify a model name (default is `groq/compound-mini`).

### Section B: Uploading Files
1.  **Upload Input Data (Column 1):**
    *   Click "Browse files" under **1. Upload Input Data**.
    *   Upload the CSV or Excel file containing the data you want to convert.
    *   *Preview:* A table preview of the first few rows will appear.
2.  **Upload Target Schema (Column 2):**
    *   Click "Browse files" under **2. Upload Target Schema**.
    *   Upload a reference file (Excel or CSV) where the **column headers** represent the keys you want in your final JSON.
    *   *Preview:* The extracted keys will be shown.

### Section C: Conversion
1.  Once both files are uploaded, a **"Start Conversion"** button will appear at the bottom.
2.  Click the button to begin.
3.  **Progress Tracking:**
    *   A progress bar will show the status.
    *   For **Groq**, there is a built-in 10-second delay between rows to respect free-tier rate limits.
    *   For **Ollama**, speed depends on your local hardware.

### Section D: Results
1.  When complete, the JSON output will be displayed on the screen.
2.  Click the **"Download JSON"** button to save the file to your computer.

---

## 6. Troubleshooting

| Issue | Possible Cause | Solution |
| :--- | :--- | :--- |
| **"Could not connect to Ollama"** | Ollama is not running. | Open a terminal and run `ollama serve`. |
| **"Invalid JSON" in output** | The LLM failed to produce strictly formatted JSON. | Try using a more capable model (e.g., `llama3` instead of `llama2`) or check if your input data is very messy. |
| **API Errors (Groq)** | Invalid API Key or Rate Limit Exceeded. | Check your API Key. If rate limited, wait a few minutes before trying again. |
| **Application Crash** | Missing dependencies. | Run `pip install -r requirements.txt` again. |
