import os
from dotenv import load_dotenv
import sys
from call_function import available_functions, call_function
from prompts import system_prompt

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

from google import genai
from google.genai import types

client = genai.Client(api_key=api_key)

def main():
    
    #geen prompt = exit, len 1 want 0 van argv is script naam, niet prompt
    if len(sys.argv) == 1:
        print("Error, prompt required")
        sys.exit(1)
    
    #prompt bouwen, flag filter
    else:
        prompt_parts = []
        for i in sys.argv[1:]:
            if not i.startswith("--"):
                prompt_parts.append(i)
        prompt = " ".join(prompt_parts)
    
    #verbose ja/nee
    verbose = "--verbose" in sys.argv

    #user prompt history
    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]

    #response, max 20 rustahg
    
    for i in range(20):

        found_function_call_in_response = False

        try:
            response = client.models.generate_content(
                model = "gemini-2.0-flash-001", 
                contents = messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions],
                    system_instruction=system_prompt,
                ),
            )

            #kandidaten en function calls en alles appenden met roles en types en kkveel brackets

            candidates = response.candidates

            for candidate in candidates:
                messages.append(candidate.content)
                for part in candidate.content.parts:
                    if isinstance(part, types.FunctionCall):
                        name = part.function_name
                        args = part.args
                        messages.append(types.Content(role="user", parts=[types.Part(function_response=call_function(part, verbose=verbose))]))
                        found_function_call_in_response = True

            #klaar?

            if not found_function_call_in_response and response.text != "":
                print(response)
                break

        except Exception as e:
            return f"Error: {e}"


    """ if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    if not response.function_calls:
        print(response.text)
        return

    tool_parts = []

    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose=verbose)

        if not function_call_result.parts:
            raise Exception("Function call returned no parts")
        
        part = function_call_result.parts[0]

        if not part.function_response or not part.function_response.response:
            raise Exception("Function call result missing function_response.response")

        tool_parts.append(part)

        if verbose:
            print(f"-> {part.function_response.response}") """
        

if __name__ == "__main__":
    main()
