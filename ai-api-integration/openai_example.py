import os
from openai import OpenAI  # type: ignore
from dotenv import load_dotenv  # type: ignore

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None


def query_openai(prompt: str) -> str:
    try:
        if client is None:
            raise ValueError("Missing OPENAI_API_KEY in .env")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.7,
        )
        return response.choices[0].message.content or ""
    except Exception as exc:
        if "insufficient_quota" in str(exc).lower():
            print("Error querying OpenAI: insufficient_quota. Check your OpenAI billing/quota in the OpenAI dashboard.")
        else:
            print(f"Error querying OpenAI: {exc}")
        return ""


def main() -> None:
    user_prompt = input("Enter a prompt for OpenAI: ")
    print("Querying OpenAI...")
    result = query_openai(user_prompt)
    print(result)


if __name__ == "__main__":
    main()

