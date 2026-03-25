import os
from dotenv import load_dotenv  # type: ignore
from groq import Groq  # type: ignore

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None
def query_groq(user_query: str) -> str | None:
    try:
        if client is None:
            raise ValueError("Missing GROQ_API_KEY in .env")
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": user_query}],
        )
        return response.choices[0].message.content
    except Exception as exc:
        print(f"Error querying Groq: {exc}")
        return None
def main() -> None:
    user_input = input("Enter a prompt for Groq: ")
    result = query_groq(user_input)
    if result is None:
        print("No response received.")
        return
    print("\nGroq response:\n")
    print(result)

if __name__ == "__main__":
    main()

