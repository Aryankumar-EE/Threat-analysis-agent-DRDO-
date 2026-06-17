from dotenv import load_dotenv
import os

load_dotenv(override=True)

print("GROQ_API_KEY =", os.getenv("GROQ_API_KEY"))