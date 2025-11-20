import os
from dotenv import load_dotenv
import sys

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

    #history
    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]

    response = client.models.generate_content(
        model = "gemini-2.0-flash-001", 
        contents = messages,
    )

    if verbose:
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print(response.text)
        

if __name__ == "__main__":
    main()
