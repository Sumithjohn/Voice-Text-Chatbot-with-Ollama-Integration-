import streamlit as st
import requests

# 🧐 System prompt for vehicle-related responses only
system_prompt = (
    "You are an expert on vehicles (cars, bikes, trucks, EVs, engines, etc.). "
    "Only answer questions related to vehicles. "
    "If someone asks something unrelated to vehicles, respond with: "
    "'I'm only able to answer questions about vehicles.'"
)

# 🔌 Function to call Ollama's local API
def chat_with_ollama(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2:1b",
                "prompt": f"{system_prompt}\n\nUser: {prompt}\nAssistant:",
                "stream": False
            }
        )
        result = response.json()
        return result.get("response") or result.get("error", "No response found.")
    except Exception as e:
        return f"[Error] {e}"

# 🧠 Initialize session state variables
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 🚀 Page config
st.set_page_config(page_title="Vehicle Chatbot", page_icon="🚗")
st.title("🚗 Vehicle Expert Chatbot")
st.write("Ask me anything about cars, bikes, EVs, engines, and more!")

# 💬 Show chat history
for role, message in st.session_state.chat_history:
    if role == "You":
        st.markdown(f"**🧑 You:** {message}")
    else:
        st.markdown(f"**🤖 Bot:** {message}")

# 📥 Input field (temporary key for safe clearing)
user_input = st.text_input("You:", key="temp_input").strip()

# ✉️ Handle input
if user_input:
    st.session_state.chat_history.append(("You", user_input))
    bot_reply = chat_with_ollama(user_input)
    st.session_state.chat_history.append(("Bot", bot_reply))

    # Clear input field by deleting key
    del st.session_state["temp_input"]
    st.experimental_rerun()
