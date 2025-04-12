from nicegui import ui
import httpx
from datetime import datetime
import asyncio

BACKEND_URL = "http://localhost:8000/save-memory"
USER_ID = "user_123"

# === Dark Mode CSS Styling ===
ui.add_head_html('''
    <style>
        body {
            background: #1f2937;
            color: #f4f4f5;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
        }
        .chat-container {
            height: 70vh;
            overflow-y: auto;
            padding: 1.5rem;
            background: #2d3748;
            border-radius: 16px;
            margin: 0 auto;
            max-width: 800px;
            box-shadow: 0 6px 24px rgba(0, 0, 0, 0.1);
            animation: fadeIn 0.6s ease;
        }
        .chat-bubble {
            max-width: 75%;
            margin-bottom: 0.75rem;
            padding: 1rem 1.25rem;
            border-radius: 1.5rem;
            display: inline-block;
            word-wrap: break-word;
            font-size: 0.95rem;
            line-height: 1.4;
            animation: fadeIn 0.4s ease;
            white-space: pre-wrap;
        }
        .user-msg {
            background-color: #4c51bf;
            color: white;
            margin-left: auto;
        }
        .bot-msg {
            background-color: #4a5568;
            color: #edf2f7;
            margin-right: auto;
        }
        .timestamp {
            font-size: 0.7rem;
            color: gray;
            margin-top: 0.2rem;
        }
        .title {
            text-align: center;
            font-size: 2.25rem;
            font-weight: bold;
            color: #edf2f7;
            margin-top: 30px;
            margin-bottom: 6px;
        }
        .subtitle {
            text-align: center;
            color: #e2e8f0;
            font-size: 1.1rem;
            margin-bottom: 25px;
        }
        .send-button {
            background-color: #38b2ac;
            color: white;
            border-radius: 10px;
            font-weight: bold;
        }
        .typing {
            color: white;
            background-color: #2d3748;
            font-style: italic;
            padding-left: 10px;
            padding-right: 10px;
            border-radius: 1.5rem;
        }
        @keyframes fadeIn {
            from {opacity: 0; transform: translateY(10px);}
            to {opacity: 1; transform: translateY(0);}
        }
        @keyframes typing {
            0% { content: ''; }
            100% { content: '...'; }
        }
        .input-box input {
            color: white !important; /* Text inside the input box will be white */
            background-color: #2d3748 !important; /* Background of the input box is dark */
            padding-left: 20px !important; /* Shifts the text 5 spaces (20px) to the right */
        }
    </style>
''')

ui.label("💬 Life Insurance Chatbot").classes("title")
ui.label("Your friendly AI assistant — Let's find the right plan for you!").classes("subtitle")

chat_area = ui.column().classes("chat-container flex flex-col").props('class=scroll-area')

def display_message(msg: str, sender: str, typing=False):
    timestamp = datetime.now().strftime("%H:%M")
    bubble_class = "chat-bubble user-msg" if sender == "user" else "chat-bubble bot-msg"
    avatar = "👤" if sender == "user" else "🤖"

    with chat_area:
        with ui.row().classes("w-full"):
            if sender == "bot":
                ui.label(avatar)
            with ui.column().classes("max-w-[75%]"):
                message_label = ui.label(msg).classes(bubble_class)
                ui.label(timestamp).classes("timestamp")
            if sender == "user":
                ui.label(avatar)

    ui.run_javascript("document.querySelector('.scroll-area').scrollTop = document.querySelector('.scroll-area').scrollHeight")

    if typing:
        # Simulate typing animation
        asyncio.create_task(typing_animation(message_label))

async def typing_animation(label):
    # Add typing effect with a grey placeholder animation
    label.set_text("...")
    label.classes("typing")
    for _ in range(3):
        await asyncio.sleep(0.5)
        label.set_text(label.text + '.')
    label.set_text(label.text[:-3])  # Remove the dots to finalize the typing

# === MAIN FUNCTION ===
async def send_message(text: str):
    if not text.strip():
        return
    display_message(text, "user")
    user_input.value = ""

    loading_label = ui.label("🤖 Typing...").classes("bot-msg")
    ui.run_javascript("document.querySelector('.scroll-area').scrollTop = document.querySelector('.scroll-area').scrollHeight")

    try:
        async with httpx.AsyncClient() as client:
            payload = {"user_id": USER_ID, "text": text}
            response = await client.post(BACKEND_URL, json=payload, timeout=60)
            data = response.json()
            ai_reply = data.get("ai_response", "Sorry, I couldn't process that.")
    except Exception as e:
        ai_reply = f"⚠️ Error: {e}"

    loading_label.delete()
    display_message(ai_reply, "bot")

# === INPUT AREA ===
with ui.row().classes("w-full mt-4 input-box"):
    user_input = ui.input(placeholder="Type your message...").classes("w-full text-white bg-gray-700").on("keydown.enter", lambda e: send_message(user_input.value))
    ui.button("Send", on_click=lambda: send_message(user_input.value), icon="send").classes("send-button")

# === Default Welcome Message ===
ui.timer(0.1, lambda: display_message(
    "👋 Welcome! I'm your life insurance assistant. What kind of plan are you looking for? Feel free to share your age, income goals, and preferences.",
    "bot"
), once=True)

ui.run(port=8080)
