# Run: "ollama pull llama3" first to download the model.
# Run: "ollama serve" next to start the local Ollama server.
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3"
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_TAGS_URL = f"{OLLAMA_BASE_URL}/api/tags"

def query_ollama(prompt: str) -> str:
    try:
        try:
            requests.get(OLLAMA_TAGS_URL, timeout=5).raise_for_status()
        except Exception as diag_exc:
            print(f"Error querying Ollama: Could not reach Ollama at {OLLAMA_BASE_URL}. {diag_exc}")
            return ""
        payload = {"model": OLLAMA_MODEL, "prompt": prompt, "stream": False}
        resp = requests.post(OLLAMA_URL, json=payload, timeout=120)
        if resp.status_code == 404:
            if "model" in resp.text.lower() and "not found" in resp.text.lower():
                print(f"Error querying Ollama: Ollama is running but model '{OLLAMA_MODEL}' was not found.")
                print(f"Fix: run `ollama pull {OLLAMA_MODEL}` first, then re-run this script.")
            else:
                print(f"Error querying Ollama: 404 Not Found. Check that Ollama is running and the endpoint is correct: {OLLAMA_URL}.")
            print(f"Response body: {resp.text[:300]}")
            return ""
        resp.raise_for_status()
        data = resp.json()
        return data.get("response", "")
    except Exception as exc:
        print(f"Error querying Ollama: {exc}")
        return ""

def main() -> None:
    user_prompt = input("Enter a prompt for Ollama: ")
    print("Querying Ollama...")
    result = query_ollama(user_prompt)
    print(result)

if __name__ == "__main__":
    main()

