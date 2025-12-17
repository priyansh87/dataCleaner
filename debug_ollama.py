import requests

try:
    print("Checking Ollama connection...")
    response = requests.get("http://localhost:11434/")
    print(f"Server Status: {response.status_code}")
    print(f"Server Response: {response.text}")

    print("\nChecking Tags...")
    tags_response = requests.get("http://localhost:11434/api/tags")
    if tags_response.status_code == 200:
        models = [model['name'] for model in tags_response.json().get('models', [])]
        print(f"Available Models: {models}")
    else:
        print(f"Failed to get tags: {tags_response.status_code}")

except Exception as e:
    print(f"Connection Failed: {e}")
