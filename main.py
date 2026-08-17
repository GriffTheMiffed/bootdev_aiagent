import os
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

def main():
    completion = client.chat.completions.create(
        model="openrouter/free",
        messages = [
            {
                "role": "user",
                "content": "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.",
            }
        ]
    )
    if completion.usage == None:
        raise RuntimeError("API failed to return a response to the chat completion request")
    #print(f"User prompt: {completion.messages[0].content}")
    print(f"Prompt tokens: {completion.usage.prompt_tokens}")
    print(f"Response tokens: {completion.usage.completion_tokens}")
    print("Response:")
    print(completion.choices[0].message.content)


if __name__ == "__main__":
    main()
