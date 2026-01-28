# check_groq_models.py
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)

# List available models
models = client.models.list()
print("Available Groq models:")
for model in models.data:
    print(f"✅ {model.id}")

# Test a few models
test_models = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant", 
    "mixtral-8x7b-instruct-v0.1",
    "llama-3.2-1b-preview",
    "gemma2-9b-it"
]

print("\nTesting models...")
for model_name in test_models:
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": "Say hello"}],
            max_tokens=10
        )
        print(f"✅ {model_name}: Working")
    except Exception as e:
        print(f"❌ {model_name}: {str(e)[:100]}")