from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv
import logging

# Configurar logs
logging.basicConfig(level=logging.INFO)

# Cargar las variables del archivo .env
load_dotenv()

# Configura tu clave API de OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
CORS(app)

# Contextos específicos para cada marca y sus asistentes
assistant_contexts = {
    "Cumlaude": {
        "context": "Asistente experto en productos Cumlaude.",
        "model": "asst_YvXWL3CSeZFLrIa9PrqLNBD2"
    },
    "Rilastil": {
        "context": "Asistente experto en productos Rilastil.",
        "model": "asst_YvXWL3CSeZFLrIa9PrqLNBD3"
    },
    "Sensilis": {
        "context": "Asistente experto en productos Sensilis.",
        "model": "asst_YvXWL3CSeZFLrIa9PrqLNBD4"
    }
}

@app.route("/", methods=["GET"])
def home():
    return "¡Bienvenido al backend de WhatsAppGPT!", 200

@app.route('/ask', methods=['POST'])
def ask_gpt():
    try:
        # Obtener datos de la solicitud
        data = request.get_json()
        prompt = data.get("prompt", "").strip()
        brand = data.get("brand", "").strip()

        # Validar que se proporcionaron los datos necesarios
        if not prompt or not brand:
            return jsonify({"error": "Faltan 'prompt' o 'brand' en la solicitud"}), 400

        # Validar que la marca es válida
        if brand not in assistant_contexts:
            return jsonify({"error": f"Marca no válida: {brand}"}), 400

        # Obtener el contexto y modelo para la marca seleccionada
        brand_context = assistant_contexts[brand]["context"]
        brand_model = assistant_contexts[brand]["model"]

        # Log de la solicitud
        logging.info(f"Usando el modelo: {brand_model} para la marca {brand}")

        # Crear la solicitud a OpenAI
        response = openai.ChatCompletion.create(
            model=brand_model,
            messages=[
                {"role": "system", "content": brand_context},
                {"role": "user", "content": prompt}
            ]
        )

        # Extraer la respuesta del asistente
        assistant_response = response["choices"][0]["message"]["content"]
        return jsonify({"response": assistant_response})

    except Exception as e:
        logging.error(f"Error en el backend: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
