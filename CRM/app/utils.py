import requests
from flask import current_app

# Generate AI response using Google Gemini (Direct API Method - Updated to Gemini 3.8 Flash)
def get_ai_response(user_message):
    try:
        api_key = current_app.config.get('GEMINI_API_KEY')
        if not api_key:
            return "Error: config.py mein Gemini API key nahi mili."

        # Google API Error ke mutabiq naya model: gemini-3.8-flash laga diya gaya hai
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent?key={api_key}"
        
        payload = {
            "contents": [{
                "parts": [{"text": f"You are a helpful assistant for WordbitX CRM. Reply briefly to: {user_message}"}]
            }]
        }
        
        response = requests.post(url, headers={'Content-Type': 'application/json'}, json=payload)
        data = response.json()
        
        if response.status_code == 200:
            return data['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"API Error: {data.get('error', {}).get('message', 'Unknown error')}"
            
    except Exception as e:
        return f"System Error: {str(e)}"

# Detect visitor location using a free IP API
def get_visitor_location(ip_address):
    try:
        response = requests.get(f'http://ip-api.com/json/{ip_address}').json()
        if response.get('status') == 'success':
            return f"{response['city']}, {response['country']}"
    except:
        pass
    return "Unknown Location"

# Convert deal amount using ExchangeRate API
def convert_currency(amount, from_currency, to_currency):
    if from_currency == to_currency:
        return amount
    try:
        api_key = current_app.config.get('EXCHANGE_RATE_API_KEY')
        if not api_key:
            return amount
            
        url = f"https://v6.exchangerate-api.com/v6/{api_key}/pair/{from_currency}/{to_currency}/{amount}"
        response = requests.get(url).json()
        return response.get('conversion_result', amount)
    except:
        return amount