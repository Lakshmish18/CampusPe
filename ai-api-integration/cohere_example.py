import os
import cohere  # type: ignore
from dotenv import load_dotenv  # type: ignore
load_dotenv()
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
MODEL_CANDIDATES = ["command-r-plus-08-2024", "command-r-plus", "command-r"]

def query_cohere(prompt: str) -> str:
    try:
        if not COHERE_API_KEY:
            raise ValueError("Missing COHERE_API_KEY in .env")
        client = cohere.Client(COHERE_API_KEY)
        last_error: Exception | None = None
        for model_id in MODEL_CANDIDATES:
            try:
                response = client.chat(
                    model=model_id,
                    message=prompt,
                    max_tokens=500,
                    temperature=0.7,
                )
                if hasattr(response, "text"):
                    return response.text
                if hasattr(response, "message"):
                    return str(response.message)
                return str(response)
            except Exception as exc:
                last_error = exc
                continue
        if last_error:
            print(f"Error querying Cohere: {last_error}")
        return ""
    except Exception as exc:
        print(f"Error querying Cohere: {exc}")
        return ""
def main() -> None:
    user_prompt = input("Enter a prompt for Cohere: ")
    print("Querying Cohere...")
    result = query_cohere(user_prompt)
    print(result)

if __name__ == "__main__":
    main()

