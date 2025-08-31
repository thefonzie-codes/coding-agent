import os
import sys
from dotenv import load_dotenv
from google import genai

def call_api(prompt):
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    print(f"Asking Gemini... '{prompt}'")
    res = client.models.generate_content(
        model='gemini-2.0-flash-001', contents=f'{prompt}'
    )
    # print(res)
    return res

def main():
    if not sys.argv[1]:
        sys.exit("Error: Prompt Required")
    prompt = sys.argv[1]
    print("Hello from the cli-coding-agent!")
    #res = call_api("Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.")
    res = call_api(prompt)
    print(res.text)
    print(f"Prompt tokens: {res.usage_metadata.prompt_token_count}\nResponse tokens: {res.usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    main()
