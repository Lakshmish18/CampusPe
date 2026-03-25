import os
from dotenv import load_dotenv  # type: ignore  # Load variables from the local .env file.
from google import genai
load_dotenv()  # Populate process environment from .env (in this folder).
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")  # Read the Gemini API key.
MODEL_CANDIDATES = ["gemini-1.5-flash", "gemini-1.5-flash-latest"]

def query_gemini(prompt: str) -> str:
    try:
        if not GOOGLE_API_KEY:
            raise ValueError("Missing GOOGLE_API_KEY in .env")
        client = genai.Client(api_key=GOOGLE_API_KEY)
        last_error: Exception | None = None

        def model_to_string(model_obj: object) -> str:
            candidate = getattr(model_obj, "name", None)
            if candidate:
                return str(candidate)
            candidate = getattr(model_obj, "model", None)
            if candidate:
                return str(candidate)
            candidate = getattr(model_obj, "id", None)
            if candidate:
                return str(candidate)
            return str(model_obj)

        def attempt_generate(model_id: str) -> str | None:
            response = client.models.generate_content(
                model=model_id,
                contents=prompt,
            )
            if hasattr(response, "text") and response.text:
                return str(response.text)
            return str(response)

        for model_id in MODEL_CANDIDATES:
            try:
                result = attempt_generate(model_id)
                if result:
                    return result
                return result
            except Exception as exc:
                last_error = exc
                continue

        try:
            available_models = client.models.list()
            model_ids: list[str] = []
            for m in available_models:
                model_ids.append(model_to_string(m))
            preferred_flash = None
            for mid in model_ids:
                if "gemini" in mid and "flash" in mid and "1.5" in mid:
                    preferred_flash = mid
                    break
            chosen = preferred_flash or (model_ids[0] if model_ids else None)
            if chosen:
                return attempt_generate(chosen)
        except Exception as list_exc:
            print(f"Gemini model listing failed: {list_exc}")

        if last_error:
            print(f"Error querying Gemini: {last_error}")
        return ""
    except Exception as exc:
        print(f"Error querying Gemini: {exc}")
        return ""


def main() -> None:
    user_prompt = input("Enter a prompt for Gemini: ")
    print("Querying Gemini...")
    result = query_gemini(user_prompt)
    print(result)


if __name__ == "__main__":
    main()
