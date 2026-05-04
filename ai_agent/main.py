import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key is None: raise RuntimeError("API key not foound")
client = genai.Client(api_key=api_key)


def main():
    
    # use parser to use cli to interact with agent
    parser = argparse.ArgumentParser(description='Chatbot')
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    #create roles and record them for the model to know
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    #gemini response and different data shown outside
    gemini = client.models.generate_content(model="gemini-2.5-flash", contents=messages) # get prompt from the messages list
    
    if gemini.usage_metadata.candidates_token_count is None: raise RuntimeError("no resposnse given by model") #get number of tokens by given models response
    if args.verbose is True: # handles edge case if verbose is passed to the cli
        print(f"User prompt: {messages[0].parts[0].text}")
        print(f"Prompt tokens: {gemini.usage_metadata.prompt_token_count}") # get number of token from given question
        print(f"Response tokens: {gemini.usage_metadata.candidates_token_count}")

    print(f"Response:\n {gemini.text}") # outputs agents response
    
if __name__ == "__main__":
    main()
