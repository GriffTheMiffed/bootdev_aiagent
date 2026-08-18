import os
import argparse 

from dotenv import load_dotenv
from openai import OpenAI


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
        {"role": "user", "content": args.user_prompt},
    ]
    generate_content(client, messages, args)
 

def generate_content(client, messages, args):
    response = client.chat.completions.create(
        model="openrouter/free",
        messages = messages,
    )
    if response.usage == None:
        raise RuntimeError("API failed to return a response to the chat completion request")

    if args.verbose == True:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")
    print("Response:")
    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()

