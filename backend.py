from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
from google.oauth2 import service_account
import google.auth.transport.requests
import requests

# Configuración
SERVICE_ACCOUNT_FILE = 'service_account.json'
PROJECT_ID = 'gen-lang-client-0438257778'
LOCATION = 'us-central1'  # Ajustar si es necesario

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/synthesize-numerology':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data)
                
                # 1. Autenticación con Google (Vertex AI)
                import vertexai
                from vertexai.generative_models import GenerativeModel, SafetySetting

                # Inicializar Vertex AI
                vertexai.init(project=PROJECT_ID, location=LOCATION)
                
                # 2. Construir Prompt para Gemini
                card_name = data.get('cardName', 'Carta Desconocida')
                definitions = data.get('definitions', {})
                examples = data.get('examples', {})
                
                prompt = f"""
                Actúa como un oráculo místico y numerólogo experto.
                Analiza la carta "{card_name}" y la siguiente configuración numerológica única para esta lectura:
                
                CONTEXTO:
                - Arquetipo (Ejemplo {examples.get('arquetipo', '?')}/22): "{definitions.get('arquetipo', '')}"
                - Sombra (Ejemplo {examples.get('sombra', '?')}/22): "{definitions.get('sombra', '')}"
                - Misticismo (Ejemplo {examples.get('misticismo', '?')}/22): "{definitions.get('misticismo', '')}"
                
                TAREA:
                Sintetiza una lectura breve (max 50 palabras) que conecte estos números de ejemplo específicos con el significado de la carta. 
                ¿Qué significa que le haya tocado precisamente el ejemplo {examples.get('sombra', '?')} en la Sombra?
                Usa un tono esotérico, profundo y directo.
                Responde en formato HTML simple (puedes usar <strong> o <em>).
                """

                # 3. Llamar a Gemini API (Vertex AI)
                # Using Gemini 2.5 Pro - State-of-the-art thinking model
                model = GenerativeModel("gemini-2.5-pro")
                
                responses = model.generate_content(
                    [prompt],
                    generation_config={
                        "max_output_tokens": 256,
                        "temperature": 0.7,
                        "top_p": 0.95,
                    },
                    stream=False,
                )

                response_text = responses.text

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'reading': response_text}).encode('utf-8'))

            except Exception as e:
                print(f"Error en backend: {e}")
                self.send_response(500)
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Backend de Star Loop activo. Usa POST /api/synthesize-numerology")

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Iniciando backend en puerto {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
