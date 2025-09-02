import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import get_files_info, schema_get_files_info

def call_api(prompt):
    
    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """
    
    available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
    ]
)
    load_dotenv()
    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    res = client.models.generate_content(
        model='gemini-2.0-flash-001', 
        contents=f'{messages}',
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            tools=[available_functions]
            ),
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
    if (res.function_calls):
        fn_calls = res.function_calls
        for call in fn_calls:
            print(f"Calling function: {call.name}({call.args})")
    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")

if __name__ == "__main__":
    main()
