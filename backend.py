from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
import time
from datetime import datetime

# Configuration
SERVICE_ACCOUNT_FILE = 'service_account.json'
PROJECT_ID = 'gen-lang-client-0438257778'
LOCATION = 'us-central1'

# Simple in-memory cache for local testing
response_cache = {}
CACHE_TTL_SECONDS = 3600

# Global client
_vertex_initialized = False
_generative_model = None

def get_cache_key(card_name, language, definitions):
    """Generate cache key"""
    arquetipo = definitions.get('arquetipo', '')[:50]
    sombra = definitions.get('sombra', '')[:50]
    misticismo = definitions.get('misticismo', '')[:50]
    return f"{card_name}|{language}|{arquetipo}|{sombra}|{misticismo}"

def get_cached_response(cache_key):
    """Get cached response if valid"""
    if cache_key in response_cache:
        cached_text, cached_time = response_cache[cache_key]
        age = (datetime.now() - cached_time).total_seconds()
        if age < CACHE_TTL_SECONDS:
            print(f"✅ Cache hit! Age: {age:.1f}s")
            return cached_text
        del response_cache[cache_key]
    return None

def set_cached_response(cache_key, response_text):
    """Cache response"""
    response_cache[cache_key] = (response_text, datetime.now())
    print(f"💾 Cached (total: {len(response_cache)})")

def initialize_vertex_ai():
    """Initialize Vertex AI once"""
    global _vertex_initialized, _generative_model
    
    if _vertex_initialized:
        return _generative_model
    
    import vertexai
    from vertexai.generative_models import GenerativeModel
    
    vertexai.init(project=PROJECT_ID, location=LOCATION)
    _generative_model = GenerativeModel("gemini-2.0-flash-exp")
    _vertex_initialized = True
    
    print("✅ Vertex AI initialized")
    return _generative_model

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_POST(self):
        if self.path == '/api/synthesize-numerology':
            request_start = time.time()
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data)
                
                # Extract data
                card_name = data.get('cardName', 'Unknown Card')
                language = data.get('language', 'es')
                definitions = data.get('definitions', {})
                examples = data.get('examples', {})
                
                # Check cache
                cache_key = get_cache_key(card_name, language, definitions)
                cached = get_cached_response(cache_key)
                
                if cached:
                    self.send_response(200)
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.send_header('Content-type', 'application/json')
                    self.send_header('X-Cache', 'HIT')
                    self.end_headers()
                    self.wfile.write(json.dumps({
                        'reading': cached,
                        'cached': True
                    }).encode('utf-8'))
                    print(f"⚡ Cache response: {time.time() - request_start:.2f}s")
                    return
                
                # Initialize and call Gemini
                model = initialize_vertex_ai()
                
                # Spanish prompt (simplified for local testing)
                prompt = f"""Eres un oráculo profesional especializado en orientación personal.
Analiza la carta "{card_name}" con esta configuración:

CONTEXTO:
- Arquetipo: "{definitions.get('arquetipo', '')}"
- Sombra: "{definitions.get('sombra', '')}"
- Misticismo: "{definitions.get('misticismo', '')}"

Genera una lectura fluida y profunda de 400 palabras que integre estos aspectos.
Usa párrafos continuos, lenguaje formal y directo."""
                
                api_start = time.time()
                responses = model.generate_content(
                    [prompt],
                    generation_config={
                        "max_output_tokens": 800,
                        "temperature": 1.0,
                        "top_p": 0.95,
                        "top_k": 40,
                    },
                    stream=False,
                )
                
                api_time = time.time() - api_start
                response_text = responses.text
                
                print(f"✅ Generated {len(response_text)} chars in {api_time:.2f}s")
                
                # Cache it
                set_cached_response(cache_key, response_text)
                
                self.send_response(200)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Content-type', 'application/json')
                self.send_header('X-Cache', 'MISS')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'reading': response_text,
                    'cached': False
                }).encode('utf-8'))
                
                print(f"⚡ Total: {time.time() - request_start:.2f}s")

            except Exception as e:
                print(f"❌ Error: {e}")
                self.send_response(500)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({
            'status': 'active',
            'service': 'Star Oracle Backend (Local)',
            'vertex_initialized': _vertex_initialized,
            'cached': len(response_cache)
        }).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'🚀 Star Oracle Backend running on port {port}')
    print(f'   Access: http://localhost:{port}')
    print(f'   Endpoint: POST /api/synthesize-numerology')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
