import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
from prompts import system_prompt
from call_function import available_functions, call_function


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
    gemini = client.models.generate_content(model="gemini-2.5-flash", contents=messages , config=types.GenerateContentConfig(tools=[available_functions],system_instruction=system_prompt),) # get prompt from the messages list
    
    if gemini.usage_metadata.candidates_token_count is None: raise RuntimeError("no resposnse given by model") #get number of tokens by given models response
    if args.verbose is True: # handles edge case if verbose is passed to the cli
        print(f"User prompt: {messages[0].parts[0].text}")
        print(f"Prompt tokens: {gemini.usage_metadata.prompt_token_count}") # get number of token from given question
        print(f"Response tokens: {gemini.usage_metadata.candidates_token_count}")
    
    if  gemini.function_calls:
        for function in gemini.function_calls:
            function_call_result = call_function(function, args.verbose)

            #handle edge cases where correct output was not fully passed to the function_call_result
            if not function_call_result.parts: raise Exception("Non-empty list found at the function_call.parts") #list is empty raise error
            if not function_call_result.parts[0].function_response: raise Exception("Function call part[0] function response is empty") #list empty reaise error
            if not function_call_result.parts[0].function_response.response: raise Exception("Function call not found in function_response.response therefore empty") # fucntion not found in response raise error
            function_result_list = []
            function_result_list.append(function_call_result.parts[0])

            if args.verbose: print(f"-> {function_call_result.parts[0].function_response.response}")
            else: print(function_call_result.parts[0].function_response.response["result"])

            # print(f"Calling function: {function.name}({function.args})")
    else: print(f"Response:\n {gemini.text}") # outputs agents response
    
if __name__ == "__main__":
    main()
