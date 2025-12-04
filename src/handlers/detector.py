import json
import os
import requests  # Usamos requests em vez do SDK pesado

# --- A VACINA DO ZIP (Mantemos por segurança) ---
try:
    import unzip_requirements
except ImportError:
    pass


# -----------------------

def handler(event, context):
    print(f"Processing event: {json.dumps(event)}")

    # Recupera a chave e o payload
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
    log_data = event.get('payload', {})

    # Prompt Otimizado
    prompt_text = f"""
    You are a Tier 3 Security Analyst. Analyze this log:
    {json.dumps(log_data)}

    INSTRUCTIONS:
    1. Identify if malicious (True/False).
    2. Confidence (0.0-1.0).
    3. Reasoning.

    OUTPUT JSON ONLY:
    {{ "malicious": bool, "confidence": float, "reasoning": "str", "attack_type": "str" }}
    """

    # Configuração da Chamada REST (Sem gRPC!)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GOOGLE_API_KEY}"

    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{
            "parts": [{"text": prompt_text}]
        }],
        "generationConfig": {
            "temperature": 0.0,
            "responseMimeType": "application/json"  # Força o Gemini a responder JSON limpo
        }
    }

    try:
        # Faz o POST request direto
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()

        # Parseia a resposta do Google
        result = response.json()

        # Extrai o texto da IA (que já vem em JSON graças ao mimeType)
        ai_text = result['candidates'][0]['content']['parts'][0]['text']
        analysis = json.loads(ai_text)

        return {
            **event,
            "analysis": analysis
        }

    except Exception as e:
        print(f"Error calling Google AI API: {str(e)}")
        if 'response' in locals():
            print(f"Google Error Detail: {response.text}")

        return {
            **event,
            "analysis": {
                "malicious": False,
                "confidence": 0.0,
                "error": "AI Service Unavailable",
                "details": str(e)
            }
        }