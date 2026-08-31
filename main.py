import os
import argparse 
import json
from prompts import system_prompt

from dotenv import load_dotenv
from openai import OpenAI
from functions.call_function import available_functions
from functions.call_function import call_function


def main() -> None:
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY environement variable not set")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]
    generate_content(client, messages, args)
 

def generate_content(client, messages, args):
    response = client.chat.completions.create(
        model="openrouter/free",
        messages = messages,
        temperature=0,
        tools=available_functions,
    )
    if response.usage == None:
        raise RuntimeError("API failed to return a response to the chat completion request")

    if args.verbose == True:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")
    message = response.choices[0].message
    if message.tool_calls != None:
        for tool_call in message.tool_calls:
            if tool_call.type != "function":
                continue
            function_args = json.loads(tool_call.function.arguments or "{}")
            print(f"Calling function: {tool_call.function.name}({function_args})")
            result_message = call_function(tool_call, args.verbose)
            if result_message["content"] == None or "":
                raise Exception(f'Error: tool_call of {tool_call.fucntion.name}({tool_call.function.arguments} returned empty conent')
            print(result_message["content"])

    if message.tool_calls == None:
        print("Response:")
        print(message.content)
        return


if __name__ == "__main__":
    main()

