import os
from dotenv import load_dotenv
from google import genai


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key is None: raise RuntimeError("API key not foound")
client = genai.Client(api_key=api_key)
gemini = client.models.generate_content(model="gemini-2.5-flash", contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.")
print(gemini.text)

def main():
    print("Hello from ai-agent!")


if __name__ == "__main__":
    main()
