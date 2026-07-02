from dotenv import load_dotenv
import os
from groq import Groq

load_dotenv()

key = os.getenv("GROQ_API_KEY")

print("Key:", repr(key))

client = Groq(api_key=key)

print(client.models.list())