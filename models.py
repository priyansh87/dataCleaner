import requests
from groq import Groq

def get_ollama_models():
    """Fetches available models from local Ollama instance."""
    try:
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code == 200:
             return [model['name'] for model in response.json().get('models', [])]
        return []
    except:
        return []

def process_with_ollama(data_row, schema, model_name="llama2"):
    """Sends a prompt to local Ollama instance."""
    prompt = f"""
    You are a data conversion assistant. 
    Convert the following input data into a JSON object based on the provided target schema keys.
    
    Input Data:
    {data_row}
    
    Target Schema Keys (The output JSON must strictly use these keys):
    {list(schema.keys())}
    
    Return ONLY the valid JSON object. Do not include any explanation or markdown formatting like ```json.
    """
    
    try:
        payload = {
            "model": model_name,
            "prompt": prompt,
            "stream": False
        }
        response = requests.post("http://localhost:11434/api/generate", json=payload)
        response.raise_for_status()
        result = response.json()
        return result.get("response", "").strip()
    except Exception as e:
        return f"Error: {e}"

def process_with_groq(data_row, schema, api_key, model_name="groq/compound-mini"):
    """Sends a prompt to Groq Cloud."""
    prompt = f"""
    You are a data conversion assistant. 
    Convert the following input data into a JSON object based on the provided target schema keys.
    
    Input Data:
    {data_row}
    
    Target Schema Keys (The output JSON must strictly use these keys):
    {list(schema.keys())}
    
    Return ONLY the valid JSON object. Do not include any explanation or markdown formatting like ```json.
    """
    
    try:
        client = Groq(api_key=api_key)
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful data conversion assistant that outputs only JSON."
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=model_name,
            temperature=0, 
        )
        return chat_completion.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"
