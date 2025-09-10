import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function

def call_api(messages):
    
    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Run python files
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """
    
    available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
        ]
    )   
    try:
        load_dotenv()

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
        for candidate in res.candidates:
            messages.append(candidate.content)
        return res
    
    except Exception as e:
        print(f"Error during the API call: {e}")
    
def main():

    
    if not sys.argv[1]:
        sys.exit("Error: Prompt Required")
        
    user_prompt = sys.argv[1]
    verbose = False

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
        ]

    if "--verbose" in sys.argv:
        verbose = True
    
    print("Hello from the cli-coding-agent!")
    
    iterations = 0

    while iterations < 20:
        try:
            res = call_api(messages)
            prompt_tokens = res.usage_metadata.prompt_token_count
            response_tokens = res.usage_metadata.candidates_token_count
            
            if (res.function_calls):
                fn_calls = res.function_calls
                for call in fn_calls:
                    result = call_function(call, verbose=verbose)
                    if result.parts[0].function_response.response:
                        messages.append(f"user: {result.parts[0].function_response.response}")
                        print(f"-> {result.parts[0].function_response.response}")
                    else:
                        raise Exception("FATAL ERROR: No response")

            if res.text:
                print(res.candidates[0].content)
                return
            else:
                iterations += 1

            if verbose:
                print(f"User prompt: {user_prompt}")
                print(f"Prompt tokens: {prompt_tokens}")
                print(f"Response tokens: {response_tokens}")

            print(messages)

        except Exception as e:
            print(f"Error during the API call: {e}")
            iterations += 1
            


if __name__ == "__main__":
    main()
