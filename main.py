import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

def call_api(prompt):
    load_dotenv()
    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    res = client.models.generate_content(
        model='gemini-2.0-flash-001', 
        contents=f'{messages}'
    )
    return res

def main():
    if not sys.argv[1]:
        sys.exit("Error: Prompt Required")
    user_prompt = sys.argv[1]
    verbose = False
    if len(sys.argv) > 2:
        verbose = True
    print("Hello from the cli-coding-agent!")
    res = call_api(user_prompt)
    prompt_tokens = res.usage_metadata.prompt_token_count
    response_tokens = res.usage_metadata.candidates_token_count
    print(res.text)
    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")
    # print(f"Prompt tokens: {res.usage_metadata.prompt_token_count}\nResponse tokens: {res.usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    main()
