from groq_example import query_groq
from openai_example import query_openai
from gemini_example import query_gemini
from cohere_example import query_cohere
import huggingface_example as hf
from ollama_example import query_ollama

def main() -> None:
    try:
        print("=== Multi API Query Tool ===")
        print("1. Groq")
        print("2. OpenAI")
        print("3. Gemini")
        print("4. Cohere")
        print(f"5. Hugging Face (model: {hf.MODEL})")
        print("6. Ollama")
        choice = input("Choose an option (1-6): ").strip()
        prompt = input("Enter a prompt: ").strip()
        provider_map = {
            "1": query_groq,
            "2": query_openai,
            "3": query_gemini,
            "4": query_cohere,
            "5": hf.query_huggingface,
            "6": query_ollama,
        }
        if choice not in provider_map:
            print("Invalid choice. Please enter a number from 1 to 6.")
            return
        response = provider_map[choice](prompt)
        print(response)
    except Exception as exc:
        print(f"Error running Multi API Query Tool: {exc}")

if __name__ == "__main__":
    main()

