import os
import requests
from dotenv import load_dotenv  # type: ignore

load_dotenv(override=True)
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
API_URL = "https://router.huggingface.co/v1/chat/completions"
MODEL = "Qwen/Qwen3.5-27B"
MODELS_URL = "https://router.huggingface.co/v1/models"
HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}", "Content-Type": "application/json"}


def list_suggested_mistral_models(max_results: int = 5) -> list[str]:
    try:
        resp = requests.get(
            MODELS_URL,
            headers={"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"},
            timeout=60,
        )
        data = resp.json()
        if isinstance(data, dict) and isinstance(data.get("data"), list):
            ids: list[str] = []
            for m in data["data"]:
                if isinstance(m, dict) and isinstance(m.get("id"), str):
                    mid = m["id"]
                    lower_mid = mid.lower()
                    if ("mistral" in lower_mid) or ("mixtral" in lower_mid) or ("nemo" in lower_mid):
                        ids.append(mid)
                        if len(ids) >= max_results:
                            return ids
        return []
    except Exception:
        return []


def list_supported_model_ids(max_results: int = 5) -> list[str]:
    try:
        resp = requests.get(
            MODELS_URL,
            headers={"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"},
            timeout=60,
        )
        data = resp.json()
        if isinstance(data, dict) and isinstance(data.get("data"), list):
            ids: list[str] = []
            for m in data["data"]:
                if isinstance(m, dict) and isinstance(m.get("id"), str):
                    ids.append(m["id"])
                    if len(ids) >= max_results:
                        return ids
        return []
    except Exception:
        return []


def query_huggingface(prompt: str) -> str:
    try:
        if not HUGGINGFACE_API_KEY:
            raise ValueError("Missing HUGGINGFACE_API_KEY in .env")

        payload = {
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 500,
            "temperature": 0.7,
        }

        resp = requests.post(API_URL, headers=HEADERS, json=payload, timeout=60)
        data = resp.json()

        if resp.status_code == 403:
            message = ""
            if isinstance(data, dict) and isinstance(data.get("error"), dict):
                message = str(data["error"].get("message", ""))
            print("Hugging Face 403: permission error calling Inference Providers.")
            print("Fix: create/refresh your HF token with 'Make calls to Inference Providers' permission.")
            if message:
                print(f"Details: {message}")
            return ""

        if resp.status_code == 400:
            message = ""
            if isinstance(data, dict) and isinstance(data.get("error"), dict):
                message = str(data["error"].get("message", ""))
            if "not supported by any provider" in (message or "").lower():
                print(f"Error querying Hugging Face: model '{MODEL}' is not supported by your enabled providers.")
                suggested = list_suggested_mistral_models()
                if suggested:
                    print("Try one of these supported model IDs instead:")
                    for s in suggested:
                        print(f"- {s}")
                else:
                    supported = list_supported_model_ids()
                    if supported:
                        print("This token/provider setup can access these model IDs:")
                        for s in supported:
                            print(f"- {s}")
                    else:
                        print("Fix: enable providers that support this model in Hugging Face Inference Providers settings (and ensure your token has 'Make calls to Inference Providers' permission).")
                print("Fix: enable providers that serve this model, or change `MODEL` in this script to one of the supported IDs above.")
                return ""
            resp.raise_for_status()

        resp.raise_for_status()

        if isinstance(data, dict) and isinstance(data.get("choices"), list) and data["choices"]:
            choice0 = data["choices"][0]
            if isinstance(choice0, dict) and isinstance(choice0.get("message"), dict):
                message = choice0["message"]
                content = str(message.get("content", ""))
                if content:
                    return content
                reasoning = message.get("reasoning")
                if reasoning:
                    return str(reasoning)
                return ""

        return str(data)
    except Exception as exc:
        print(f"Error querying Hugging Face: {exc}")
        return ""


def main() -> None:
    user_prompt = input("Enter a prompt for Hugging Face: ")
    print("Querying Hugging Face...")
    result = query_huggingface(user_prompt)
    print(result)


if __name__ == "__main__":
    main()

