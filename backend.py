from flask import Flask, request, jsonify
import openai
import os
from dotenv import load_dotenv

# Cargar las variables del archivo .env
load_dotenv()

# Configura tu clave API de OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

# Contexto del asistente para cada marca
assistant_contexts = {
    "Cumlaude": "Eres un experto en productos Cumlaude. Proporciona respuestas claras y detalladas sobre los productos de esta marca.",
    "Rilastil": "Eres un experto en productos Rilastil. Proporciona respuestas claras y detalladas sobre los productos de esta marca.",
    "Sensilis": "Eres un experto en productos Sensilis. Proporciona respuestas claras y detalladas sobre los productos de esta marca."
}

@app.route('/')
def home():
    return "El backend está funcionando correctamente.", 200

@app.route('/ask', methods=['POST'])
def ask_gpt():
    try:
        # Obtener datos de la solicitud
        data = request.get_json()
        prompt = data.get("prompt", "").strip()
        brand = data.get("brand", "").strip()

        if not prompt or not brand:
            return jsonify({"error": "Faltan 'prompt' o 'brand' en la solicitud"}), 400

        if brand not in assistant_contexts:
            return jsonify({"error": f"Marca no válida: {brand}"}), 400

        # Contexto del sistema para la marca seleccionada
        system_message = {"role": "system", "content": assistant_contexts[brand]}

        # Crear la solicitud a OpenAI usando el modelo gpt-4
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                system_message,
                {"role": "user", "content": prompt}
            ]
        )

        # Extraer la respuesta del asistente
        assistant_response = response["choices"][0]["message"]["content"]
        return jsonify({"response": assistant_response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
