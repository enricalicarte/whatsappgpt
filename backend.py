from flask import Flask, request, jsonify
import openai
import os
from dotenv import load_dotenv
import os

# Cargar las variables del archivo .env
load_dotenv()

# Configura tu clave API de OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

# Configura tu clave API de OpenAI desde una variable de entorno
openai.api_key = os.getenv("OPENAI_API_KEY")

# Contexto del asistente para cada marca
assistant_contexts = {
    "Cumlaude": "Asistente experto en productos Cumlaude.",
    "Rilastil": "Asistente experto en productos Rilastil.",
    "Sensilis": "Asistente experto en productos Sensilis."
}

@app.route('/ask', methods=['POST'])
def ask_gpt():
    try:
        # Obtener datos de la solicitud
        data = request.get_json()
        prompt = data.get("prompt", "").strip()
        brand = data.get("brand", "Cumlaude").strip()

        if not prompt or not brand:
            return jsonify({"error": "Faltan 'prompt' o 'brand' en la solicitud"}), 400

        if brand not in assistant_contexts:
            return jsonify({"error": f"Marca no válida: {brand}"}), 400

        # Contexto del sistema para la marca seleccionada
        system_message = {"role": "system", "content": assistant_contexts[brand]}

        # Crear la solicitud a OpenAI usando el modelo gpt-4o
        response = openai.ChatCompletion.create(
            model="gpt-4o",  # Usa "gpt-4o-mini" si es necesario
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
    app.run(debug=True)