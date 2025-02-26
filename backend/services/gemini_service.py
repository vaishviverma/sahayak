import google.generativeai as genai
from .predictions import sales_forecast, predict_demand

API_KEY = os.getenv("GEMINI_API_KEY")


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
    

    if "sales forecast" in user_message.lower() or "predict sales" in user_message.lower():
        forecast = sales_forecast()  
        user_message += f"\n\nAlso, analyze this sales forecast and give insights. Mention that you received these info from the customer sales data: {forecast}"

    if "demand" in user_message.lower():
        words = user_message.split()
        product_line = None
        date = datetime.today().strftime('%Y-%m-%d')  # Default to today's date

        for i, word in enumerate(words):
            if word.lower() in ["for", "of"] and i + 1 < len(words):
                product_line = words[i + 1]  # Assume next word is product line
            if word.lower() == "on" and i + 1 < len(words):
                date = words[i + 1]  # Assume next word is date

        if product_line:
            predicted_quantity = predict_demand(product_line, date)
            demand_response = f"Based on past sales, we expect to sell approximately {predicted_quantity} units of {product_line} on {date}."
        else:
            demand_response = "Please specify the product line for demand prediction."

        return demand_response


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