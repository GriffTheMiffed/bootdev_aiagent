import os
import argparse 
import json
from prompts import system_prompt

from dotenv import load_dotenv
from openai import OpenAI
from functions.call_function import available_functions
from functions.call_function import call_function
from generate_content import generate_content


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
    for _ in range(20):
        result = generate_content(client, messages, args)
        messages.append(result[0].choices[0].message)
        messages.append(result[1])
        if result[1]["content"][-11:] == "END OF LOOP":
            print(result[1]["content"])
            return
        continue
    print("---------------------")
    print("LOOP ITER MAX REACHED")
    print("---------------------")
    exit(1)



if __name__ == "__main__":
    main()

