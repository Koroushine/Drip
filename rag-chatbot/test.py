# check_env.py

from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")

if api_key:
    print(f"✅ API Key found!")
    print(f"   Starts with: {api_key[:15]}...")
    print(f"   Length: {len(api_key)}")
else:
    print("❌ No API key found in .env")