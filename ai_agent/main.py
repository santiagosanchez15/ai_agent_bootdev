import os
from dotenv import load_dotenv
from google import genai
import argparse


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key is None: raise RuntimeError("API key not foound")
client = genai.Client(api_key=api_key)


def main():

    parser = argparse.ArgumentParser(description='Chatbot')
    parser.add_argument("user_prompt", type=str, help="User prompt")
    args = parser.parse_args()

    gemini = client.models.generate_content(model="gemini-2.5-flash", contents=args.user_prompt)
    
    print(f"Prompt tokens: {gemini.usage_metadata.prompt_token_count}") # get number of token from given question

    if gemini.usage_metadata.candidates_token_count is None: raise RuntimeError("no resposnse given by model") #get number of tokens by given models response
    print(f"Response tokens: {gemini.usage_metadata.candidates_token_count}")

    print(f"Response:\n {gemini.text}")
    
if __name__ == "__main__":
    main()
