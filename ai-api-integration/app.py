import time  # Measure response time in seconds.
import html  # Escape response text for safe HTML injection.
import threading  # Parallel API calls in Compare mode.
import re  # Word count / reading time calculations.
import streamlit as st  # Streamlit UI framework.
from dotenv import load_dotenv  # Load environment variables from .env.

from cohere_example import query_cohere  # Import Cohere query function.
from gemini_example import query_gemini  # Import Gemini query function.
from groq_example import query_groq  # Import Groq query function.
from huggingface_example import query_huggingface  # Import Hugging Face query function.
from ollama_example import query_ollama  # Import Ollama query function.
from openai_example import query_openai  # Import OpenAI query function.


load_dotenv(override=True)  # Ensure the app uses the latest .env values.


st.set_page_config(  # Basic page configuration.
    page_title="AI API Integration Dashboard",  # Browser tab title.
    page_icon="🤖",  # Icon displayed in the browser tab.
    layout="centered",  # Center the main content for nicer mobile behavior.
)


# --- Theme (Dark UI) ---
st.markdown(  # Inject custom CSS to force a clean dark theme.
    """
    <style>
      :root { color-scheme: dark; }
      body { background-color: #0b0f14; }
      .stApp { background: #0b0f14; }
      .sidebar .sidebar-content { background: #0f172a; }
      .card {
        background: #111827;
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 14px;
        padding: 16px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.35);
      }
      .card-blue { border-color: rgba(59,130,246,0.65) !important; }
      .card-green { border-color: rgba(16,185,129,0.65) !important; }
      .card-purple { border-color: rgba(147,51,234,0.65) !important; }
      .card-orange { border-color: rgba(249,115,22,0.65) !important; }
      .card-yellow { border-color: rgba(234,179,8,0.75) !important; }
      .card-red { border-color: rgba(239,68,68,0.65) !important; }
      .pill { padding: 4px 10px; border-radius: 999px; background: rgba(255,255,255,0.06); }
      .muted { color: rgba(255,255,255,0.70); }
      textarea { background: #0b1220 !important; color: #e5e7eb !important; }
      input { background: #0b1220 !important; color: #e5e7eb !important; }
      .btn-copy { border-radius: 10px; background: #1d4ed8; color: white; padding: 8px 12px; border: none; cursor: pointer; }
      .btn-clear { border-radius: 10px; background: #ef4444; color: white; padding: 8px 12px; border: none; cursor: pointer; }
      div[data-testid="stSpinner"] > div { background-color: #1f2937; }
    </style>
    """,
    unsafe_allow_html=True,
)


st.title("AI API Integration Dashboard")  # App title.
st.caption("Query multiple AI models at once")  # App subtitle.


# --- Sidebar ---
compare_all = st.sidebar.checkbox("Compare All APIs", value=False)  # Enable parallel comparison mode.
theme_dark = st.sidebar.toggle("Dark mode", value=True)  # UI theme toggle.

if not compare_all:  # Show the single API selector only in normal mode.
    api_choice = st.sidebar.radio(
        "Select API",
        options=["Groq", "OpenAI", "Gemini", "Cohere", "Hugging Face", "Ollama"],
        index=0,
    )
else:  # Keep api_choice defined for later branching logic.
    api_choice = None

# Light theme override when the toggle is off.
if not theme_dark:
    st.markdown(
        """
        <style>
          body { background-color: #f5f7fb; }
          .stApp { background: #f5f7fb; }
          .sidebar .sidebar-content { background: #ffffff; }
          .card { background: #ffffff; border-color: rgba(0,0,0,0.08); }
          textarea { background: #ffffff !important; color: #111827 !important; }
          input { background: #ffffff !important; color: #111827 !important; }
          .muted { color: rgba(0,0,0,0.65); }
        </style>
        """,
        unsafe_allow_html=True,
    )

st.sidebar.markdown(  # App info block (logo + short description).
    """
    ## 🤖 AI API Dashboard
    <div class="muted">Modern, simple UI for trying multiple model providers.</div>
    """,
    unsafe_allow_html=True,
)

st.sidebar.markdown(  # About section.
    """
    ### About
    This app routes your prompt to the selected provider and shows the response along with status and response time.
    """
)

st.sidebar.markdown(  # Small footer in sidebar.
    "<div class='muted'>Tip: Keep your `.env` private.</div>",
    unsafe_allow_html=True,
)


# --- Session State ---
if "prompt" not in st.session_state:  # Store the prompt in session state.
    st.session_state.prompt = ""  # Initial prompt value.
if "response" not in st.session_state:  # Store the response text.
    st.session_state.response = ""  # Initial response value.
if "status" not in st.session_state:  # Store status: success/error.
    st.session_state.status = None  # No status yet.
if "model_used" not in st.session_state:  # Store which model is used.
    st.session_state.model_used = ""  # Initial model label.
if "elapsed" not in st.session_state:  # Store response time.
    st.session_state.elapsed = None  # No elapsed time yet.
if "compare_results" not in st.session_state:  # Store compare mode results per API.
    st.session_state.compare_results = {}  # Empty until first compare run.
if "compare_fastest" not in st.session_state:  # Store fastest API provider name.
    st.session_state.compare_fastest = None  # None until compare completes.
if "compare_best" not in st.session_state:  # Store best response provider name.
    st.session_state.compare_best = None  # None until compare completes.
if "ratings" not in st.session_state:  # Store thumbs up/down per API.
    st.session_state.ratings = {}  # Example: {"Groq": "up"}.
# Prompt templates removed (keep raw prompt as-is).


def reset_all() -> None:  # Reset app state.
    st.session_state.prompt = ""  # Clear prompt.
    st.session_state.response = ""  # Clear response.
    st.session_state.status = None  # Clear status.
    st.session_state.model_used = ""  # Clear model label.
    st.session_state.elapsed = None  # Clear timer.
    st.session_state.compare_results = {}  # Clear compare results.
    st.session_state.compare_fastest = None  # Clear fastest.
    st.session_state.compare_best = None  # Clear best.
    st.session_state.ratings = {}  # Clear thumbs ratings.
    # Prompt templates removed (nothing to reset here).


# --- Helpers ---
def apply_prompt_template(raw_prompt: str) -> str:
    return raw_prompt


def word_count_and_read_time(text: str) -> tuple[int, float]:
    words = re.findall(r"\b\w+\b", text or "")
    count = len(words)
    # Average reading speed ~200 WPM; reading time in minutes.
    reading_time_min = round(count / 200.0, 2) if count else 0.0
    return count, reading_time_min


def safe_html_text(text: str) -> str:
    return html.escape(text or "")


def try_toast(message: str, kind: str = "success") -> None:
    # Keep it compatible across Streamlit versions.
    if hasattr(st, "toast"):
        if kind == "error":
            st.toast(message, icon="⚠️")
        else:
            st.toast(message, icon="✅")
    else:
        if kind == "error":
            st.error(message)
        else:
            st.success(message)


def copy_button(response_id: str, response_text: str) -> None:
    safe_response = safe_html_text(response_text)
    st.components.v1.html(
        f"""
        <button class="btn-copy" onclick="navigator.clipboard.writeText(document.getElementById('{response_id}').value)">
          Copy response
        </button>
        <textarea id="{response_id}" style="position:absolute;left:-9999px;top:-9999px;width:1px;height:1px;">{safe_response}</textarea>
        """,
        height=50,
    )


# --- Main UI ---
with st.form("query_form", clear_on_submit=False):  # Form prevents partial reruns.
    prompt_text = st.text_area(  # Prompt input area.
        "Enter your prompt",  # Field label.
        value=st.session_state.prompt,  # Keep session value.
        height=140,  # Make it mobile friendly.
        placeholder="Ask a question or send a prompt...",  # Placeholder.
    )

    st.caption(f"Characters: {len(prompt_text)}")  # Character counter for prompt input.

    col_submit, col_clear = st.columns([1, 1])  # Two buttons side-by-side.
    with col_submit:  # Submit column.
        submitted = st.form_submit_button("Submit", type="primary")  # Submit trigger.
    with col_clear:  # Clear column.
        clear_clicked = st.form_submit_button("Clear", use_container_width=True)  # Clear trigger.


if clear_clicked:  # If clear button pressed.
    reset_all()  # Reset everything.
    st.rerun()  # Refresh UI immediately.


if submitted:  # If submit pressed.
    st.session_state.prompt = prompt_text  # Save prompt to session.
    st.session_state.response = ""  # Reset response before call.
    st.session_state.status = None  # Reset status.
    st.session_state.elapsed = None  # Reset elapsed.
    st.session_state.model_used = ""  # Reset model label.
    st.session_state.compare_results = {}  # Reset compare results.
    st.session_state.compare_fastest = None  # Reset fastest.
    st.session_state.compare_best = None  # Reset best.
    st.session_state.ratings = {}  # Reset ratings.

    final_prompt = apply_prompt_template(prompt_text)  # Build prompt using the selected template.
    start = time.time()  # Start timer.
    try:  # Wrap provider call in try/except.
        if compare_all:  # Compare All APIs Mode.
            providers = [
                ("Groq", "🟦", "llama-3.1-8b-instant", query_groq),
                ("OpenAI", "🟩", "gpt-3.5-turbo", query_openai),
                ("Gemini", "🟪", "gemini (auto)", query_gemini),
                ("Cohere", "🟧", "command-r-plus-08-2024 (fallbacks)", query_cohere),
                ("Hugging Face", "🟨", "Qwen/Qwen3.5-27B (your enabled Router models)", query_huggingface),
                ("Ollama", "🟥", "ollama:llama3", query_ollama),
            ]
            results = {}

            def run_one(provider_name: str, model_label: str, fn) -> None:
                t0 = time.time()
                err = ""
                try:
                    out = fn(final_prompt)
                except Exception as exc:
                    out = ""
                    err = str(exc)
                elapsed = time.time() - t0
                ok = out is not None and isinstance(out, str) and out.strip() != ""
                results[provider_name] = {
                    "status": "success" if ok else "error",
                    "response": out if ok else "",
                    "error": err,
                    "elapsed": round(elapsed, 2),
                    "model_used": model_label,
                }

            with st.spinner(f"Calling APIs: {', '.join([p[0] for p in providers])} ..."):
                threads = []
                for provider_name, _, model_label, fn in providers:
                    th = threading.Thread(target=run_one, args=(provider_name, model_label, fn))
                    threads.append(th)
                    th.start()
                for th in threads:
                    th.join()

            st.session_state.compare_results = results
            successes = [k for k, v in results.items() if v.get("status") == "success"]
            fastest = min(successes, key=lambda k: results[k]["elapsed"]) if successes else None
            best = None
            best_words = -1
            for k in successes:
                wc, _ = word_count_and_read_time(results[k]["response"])
                if wc > best_words:
                    best_words = wc
                    best = k
            st.session_state.compare_fastest = fastest
            st.session_state.compare_best = best
            if fastest:
                try_toast(f"{fastest} finished fastest!", kind="success")
        else:  # Single API Mode (existing behavior).
            with st.spinner(f"Calling {api_choice}..."):
                if api_choice == "Groq":
                    st.session_state.model_used = "llama-3.1-8b-instant"
                    result = query_groq(final_prompt)
                elif api_choice == "OpenAI":
                    st.session_state.model_used = "gpt-3.5-turbo"
                    result = query_openai(final_prompt)
                elif api_choice == "Gemini":
                    st.session_state.model_used = "gemini-1.5-flash (auto)"
                    result = query_gemini(final_prompt)
                elif api_choice == "Cohere":
                    st.session_state.model_used = "command-r-plus-08-2024 (fallbacks)"
                    result = query_cohere(final_prompt)
                elif api_choice == "Hugging Face":
                    st.session_state.model_used = "Qwen/Qwen3.5-27B (your enabled Router models)"
                    result = query_huggingface(final_prompt)
                else:
                    st.session_state.model_used = "ollama:llama3"
                    result = query_ollama(final_prompt)

            elapsed = time.time() - start
            st.session_state.elapsed = round(elapsed, 2)
            if result is None or (isinstance(result, str) and result.strip() == ""):
                st.session_state.status = "error"
                st.session_state.response = "No response returned. Check provider logs or your API credentials."
                st.error(st.session_state.response)
                try_toast("Request failed (check credentials/quota).", kind="error")
            else:
                st.session_state.status = "success"
                st.session_state.response = result
                st.success("Request successful!")
                try_toast("Request successful!", kind="success")

    except Exception as exc:  # Handle unexpected crashes.
        st.session_state.status = "error"  # Mark error.
        st.session_state.response = f"An unexpected error occurred: {exc}"  # Show error.
        st.session_state.elapsed = round(time.time() - start, 2)  # Still show approximate elapsed time.
        st.error(st.session_state.response)  # Show error.


# --- Response Card ---
if st.session_state.response:  # Only show response area when we have something.
    st.markdown("<div class='card'>", unsafe_allow_html=True)  # Card open.
    st.markdown(  # Metadata line: model + time.
        f"<div class='muted'>Model: <b>{st.session_state.model_used}</b> · Response time: <b>{st.session_state.elapsed}s</b></div>",
        unsafe_allow_html=True,
    )
    st.text_area(  # Display response.
        "Response",  # Label.
        value=st.session_state.response,  # Response text.
        height=220,  # Reasonable height.
    )

    # Copy button (JS copy to clipboard).
    response_id = "hf_response_box"  # Fixed id is fine for single-user run.
    safe_response = html.escape(st.session_state.response)  # Escape for safe HTML rendering.
    st.components.v1.html(  # Inject copy-to-clipboard UI.
        f"""
        <button class="btn-copy" onclick="navigator.clipboard.writeText(document.getElementById('{response_id}').value)">
          Copy response
        </button>
        <script>
          const el = document.getElementById('{response_id}');
          if (el) {{
            el.setAttribute('readonly', 'true');
          }}
        </script>
        """,
        height=50,
    )

    # Hidden textarea used only for copying.
    st.markdown(  # Hidden helper for copy.
        f"""
        <textarea id="{response_id}" style="position:absolute;left:-9999px;top:-9999px;width:1px;height:1px;">{safe_response}</textarea>
        """,
        unsafe_allow_html=True,
    )

    wc, rt = word_count_and_read_time(st.session_state.response)  # Word count + reading time.
    st.caption(f"{wc} words · ~{rt} min read")  # Show reading info.

    # Syntax-highlighted view when the model returns code blocks.
    if "```" in st.session_state.response:
        with st.expander("Syntax highlighted view"):
            st.markdown(st.session_state.response)

    # Thumbs up/down rating for the single response.
    rate_col1, rate_col2 = st.columns([1, 1])  # Rate buttons.
    with rate_col1:
        if st.button("👍", key="rate_up_single"):
            st.session_state.ratings["single"] = "up"
            try_toast("Thanks!", kind="success")
    with rate_col2:
        if st.button("👎", key="rate_down_single"):
            st.session_state.ratings["single"] = "down"
            try_toast("Noted.", kind="error")

    st.markdown("</div>", unsafe_allow_html=True)  # Card close.


# --- Compare All APIs Mode UI ---
if compare_all and st.session_state.compare_results:  # Render compare grid only in compare mode.
    provider_order = ["Groq", "OpenAI", "Gemini", "Cohere", "Hugging Face", "Ollama"]  # Fixed order for consistent layout.
    card_class_by_provider = {  # Map provider -> card border color.
        "Groq": "card-blue",
        "OpenAI": "card-green",
        "Gemini": "card-purple",
        "Cohere": "card-orange",
        "Hugging Face": "card-yellow",
        "Ollama": "card-red",
    }
    icon_by_provider = {  # Provider icons for readability.
        "Groq": "🟦",
        "OpenAI": "🟩",
        "Gemini": "🟪",
        "Cohere": "🟧",
        "Hugging Face": "🟨",
        "Ollama": "🟥",
    }

    st.subheader("Compare All APIs")  # Section header.
    grid_cols = st.columns(2)  # Two-column grid for mobile friendliness.

    for idx, provider_name in enumerate(provider_order):  # Render one card per provider.
        col = grid_cols[idx % 2]  # Alternate columns.
        with col:
            item = st.session_state.compare_results.get(provider_name, {})  # Fetch card data.
            response_text = item.get("response", "")  # Response text.
            status = item.get("status", "error")  # success/error.
            elapsed = item.get("elapsed", None)  # Response time.
            model_used = item.get("model_used", "")  # Model label.
            is_fastest = st.session_state.compare_fastest == provider_name  # Fastest badge check.
            wc, rt = word_count_and_read_time(response_text)  # Word count + reading time.
            card_class = card_class_by_provider.get(provider_name, "card")  # Card color class.
            response_id = f"copy_{provider_name.replace(' ', '_')}"  # Unique copy id.

            st.markdown(f"<div class='card {card_class}'>", unsafe_allow_html=True)  # Card open.

            top_line = f"{icon_by_provider.get(provider_name,'')} <b>{provider_name}</b>"  # Header left.
            if is_fastest:  # Add fastest pill.
                top_line += " <span class='pill'>Fastest</span>"  # Fastest badge.
            st.markdown(f"<div class='muted'>{top_line}</div>", unsafe_allow_html=True)  # Provider header.

            st.caption(f"Model: {model_used}")  # Show model name used.
            st.caption(f"Response time: {elapsed}s" if elapsed is not None else "Response time: —")  # Show elapsed.
            st.caption(f"{wc} words · ~{rt} min read")  # Word count + reading time.

            if status == "success":  # Show status.
                st.success("Success")  # Status success.
            else:
                st.error("Error")  # Status error.

            if response_text:  # Show response body.
                st.markdown(response_text)  # Syntax highlight via markdown code fences.
            else:
                err_text = item.get("error", "")  # Stored exception message if any.
                if err_text:  # Print crash details if available.
                    st.caption(f"Error details: {err_text}")
                else:
                    st.caption("No response returned (check provider logs / credentials).")

            copy_button(response_id, response_text)  # Copy response button (required).

            rate_col1, rate_col2 = st.columns([1, 1])  # Thumbs up/down buttons.
            with rate_col1:
                if st.button("👍", key=f"rate_up_{provider_name}"):  # Rate up.
                    st.session_state.ratings[provider_name] = "up"  # Save rating.
                    try_toast(f"{provider_name}: Thanks!", kind="success")  # Toast feedback.
            with rate_col2:
                if st.button("👎", key=f"rate_down_{provider_name}"):  # Rate down.
                    st.session_state.ratings[provider_name] = "down"  # Save rating.
                    try_toast(f"{provider_name}: Noted.", kind="error")  # Toast feedback.

            st.markdown("</div>", unsafe_allow_html=True)  # Card close.

    # Best Response section at bottom.
    if st.session_state.compare_best:  # Ensure we have a best provider.
        best_provider = st.session_state.compare_best  # Best provider name.
        best_item = st.session_state.compare_results.get(best_provider, {})  # Best data.
        best_text = best_item.get("response", "")  # Best response content.
        st.divider()  # Divider before best section.
        st.subheader(f"Best Response: {best_provider}")  # Best response header.
        st.markdown(f"**Model:** {best_item.get('model_used','')}")  # Best model info.
        st.markdown(f"**Response time:** {best_item.get('elapsed','—')}s")  # Best time info.
        st.markdown(best_text)  # Render best response with formatting.


# --- Footer ---
st.divider()  # Visual separator.
st.caption("Built by Your Name")  # Replace with your name.

