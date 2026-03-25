import os

from dotenv import load_dotenv  # type: ignore


def mask_key(value: str | None) -> str:
    """Return a masked representation of an API key without exposing fully."""
    if not value:
        return "<missing>"
    return f"{value[:5]}..." if len(value) >= 5 else f"{value}..."


def main() -> None:
    load_dotenv()

    keys = [
        "OPENAI_API_KEY",
        "GROQ_API_KEY",
        "HUGGINGFACE_API_KEY",
        "GOOGLE_API_KEY",
        "COHERE_API_KEY",
    ]

    for k in keys:
        v = os.getenv(k)
        print(f"{k}={mask_key(v)}")


if __name__ == "__main__":
    main()

