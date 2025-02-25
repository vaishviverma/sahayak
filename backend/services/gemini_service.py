import google.generativeai as genai

with open("./api_key.txt", "r") as file:
    API_KEY = file.read().strip()


genai.configure(api_key=API_KEY)
generation_config = {
    "temperature": 1.5,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 100,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)
chat_sessions = {}


def analyze_input(user_message: str, file_attached: bool, user_id: str, file_path: str = None) -> str:
    print(f"Processing request for user: {user_id}")

    if user_id not in chat_sessions:
        chat_sessions[user_id] = []

    with open("prompt.txt", "r") as file:
        prompt = file.read().strip()
    
    prompt += user_message

    if file_attached:
        prompt += f"\nA file has been uploaded: {file_path}"

    
    chat_history = [
        {"role": msg["role"], "parts": [{"text": msg["message"]}]}
        for msg in chat_sessions[user_id]
    ]
    chat = model.start_chat(history=chat_history)

    response = chat.send_message(prompt)

    chat_sessions[user_id].append({"role": "model", "message": response.text})

    return response.text.strip()