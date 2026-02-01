import argparse
import os
import sys 
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt 
from call_function import available_functions, call_function

def main():
  load_dotenv()

  api_key = os.environ.get("GEMINI_API_KEY")
  if not api_key:
    raise RuntimeError("GEMINI_API_KEY environment variable not set")
  
  client = genai.Client(api_key=api_key)

  #asking for arguments at execution in the cli 
  parser = argparse.ArgumentParser(description="ai agent")
  parser.add_argument("user_prompt", type=str, help="User prompt")
  parser.add_argument("--verbose",action="store_true", help="Enable verbose output" )
  args = parser.parse_args()

  messages=[types.Content(role="user",parts=[types.Part(text=args.user_prompt)])]
  functions_responses = []
  response = client.models.generate_content(model="gemini-2.5-flash",
                                            contents=messages,
                                            config=types.GenerateContentConfig(
                                              tools=[available_functions],
                                              system_instruction=system_prompt, 
                                              temperature=0)
                                            )
  if response.usage_metadata == None:
    raise RuntimeError("Failed api request")

  if args.verbose:
    print(f"User prompt: {args.user_prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}") 
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}") 
  if response.function_calls:
    for function_call in response.function_calls:
      if args.verbose:
        function_call_response = call_function(function_call,True)
      else:
        function_call_response = call_function(function_call)
      if not function_call_response.parts:
        raise Exception("empty parts object")
      if not function_call_response.parts[0].function_response:
        raise Exception("not function response")
      if not function_call_response.parts[0].function_response.response:
        raise Exception("not response")
      functions_responses.append(function_call_response.parts[0])
      if args.verbose:
        print(f"-> {function_call_response.parts[0].function_response.response}")
  else:
    print(response.text)

  

if __name__ == "__main__":
  main()