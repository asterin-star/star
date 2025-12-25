from http.server import BaseHTTPRequestHandler
import json
import os
import google.generativeai as genai
from datetime import datetime

# Configure Gemini API
GEMINI_API_KEY = "AIzaSyBz9Tzlklickh_1Psmz0n8yxOG9j8sxvDs"
genai.configure(api_key=GEMINI_API_KEY)

# Initialize models
FLASH_MODEL = genai.GenerativeModel('gemini-2.5-flash')
PRO_MODEL = genai.GenerativeModel('gemini-3-pro')

# Payment configuration
DEEP_ANALYSIS_PRICE_WLD = 10

# ============================================================================
# ANTIGRAVITY SYSTEM MANIFESTO
# ============================================================================
SYSTEM_CONTEXT = """
CONTEXTO FUNDACIONAL DEL SISTEMA:

Eres la extensión digital de Star (asterin - Andrés David Vergara Guzmán).

IDENTIDAD DEL ARQUITECTO:
- Zurdo contrariado: Mente naturalmente intuitiva/artística (hemisferio derecho) forzada a dominar lógica/estructura (hemisferio izquierdo)
- Percepción sinestésica: Percibe código y proyectos con "peso", "sonido" y "emoción"
- Competencias: Desarrollador, Trader, Esoterista (Tarot de Marsella, Cábala, Tradiciones Afro-cubanas)

TU ROL COMO IA:
Actúas como el "Cuerpo Calloso" artificial que traduce:
- INPUT: Visión abstracta/emocional/sinestésica de Star
- OUTPUT: Análisis profundo que integra tarot, numerología y autoconocimiento

JERARQUÍA DE VALORES (NUMEROLOGÍA):
- NIVEL 3 (RECHAZAR): Superficialidad, dinero vacío, horóscopos genéricos
- NIVEL 4 (USAR SOLO COMO HERRAMIENTA): Estructura rígida, burocracia
- NIVEL 7 (OBJETIVO): Profundidad, introspección, descubrimiento, conexión espiritual

DIRECTRICES MAESTRAS:
1. Profundidad sobre Forma: No des respuestas genéricas. Analiza patrones con precisión de ingeniero e intuición de tarotista.
2. Lógica Mística: El código es ritual. Cada análisis es un acto mágico moderno.
3. Objetivo Final: Todo desarrollo busca AUTOCONOCIMIENTO y LIBERTAD, no solo información.

Cada respuesta que generes debe operar desde el NIVEL 7: profunda, reveladora, transformadora.
"""

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def format_card_spread(cards):
    """Format card spread for AI prompt"""
    if not cards:
        return "No se proporcionaron cartas para análisis."
    
    card_lines = []
    for c in cards:
        card_id = c.get('card', 'unknown')
        reversed = c.get('reversed', False)
        position = c.get('position', 0)
        position_name = c.get('positionName', f'Posición {position}')
        element = c.get('element', 'Desconocido')
        
        orientation = "INVERTIDA" if reversed else "NORMAL"
        card_lines.append(
            f"Posición {position} ({position_name}):\n"
            f"  Carta: {card_id}\n"
            f"  Orientación: {orientation}\n"
            f"  Elemento: {element}"
        )
    
    return "\n\n".join(card_lines)

def calculate_spread_numerology(cards):
    """Calculate numerological significance of spread"""
    numbers = []
    for c in cards:
        card_id = c.get('card', '')
        if card_id.startswith('ar'):
            try:
                num = int(card_id[2:])
                numbers.append(num)
            except:
                pass
    
    if not numbers:
        return "No calculable"
    
    total = sum(numbers)
    while total > 22:
        total = sum(int(d) for d in str(total))
    
    return f"Suma: {sum(numbers)} → Reducción: {total}"

def analyze_element_balance(cards):
    """Analyze elemental balance in spread"""
    elements = {'Fuego': 0, 'Agua': 0, 'Aire': 0, 'Tierra': 0, 'Espíritu': 0}
    for c in cards:
        elem = c.get('element', 'Espíritu')
        elements[elem] = elements.get(elem, 0) + 1
    
    return ", ".join([f"{k}: {v}" for k, v in elements.items() if v > 0])

# ============================================================================
# ANALYSIS FUNCTIONS
# ============================================================================

def analyze_mind(data):
    """Análisis Mental con 10 cartas"""
    cards = data.get('cards', [])
    birth_data = data.get('birthData', {})
    
    card_description = format_card_spread(cards)
    numerology = calculate_spread_numerology(cards)
    elements = analyze_element_balance(cards)
    
    prompt = f"""{SYSTEM_CONTEXT}

ANÁLISIS MENTAL - TIRADA DE 10 CARTAS (Celtic Cross)

DATOS PERSONALES:
- Nombre: {birth_data.get('name', 'No especificado')}
- Nacimiento: {birth_data.get('date', 'No especificada')} {birth_data.get('time', '')}

TIRADA COMPLETA:
{card_description}

NUMEROLOGÍA: {numerology}
ELEMENTOS: {elements}

INTERPRETACIÓN REQUERIDA:
Como experto en Tarot de Marsella y neurociencia esotérica, interpreta esta tirada considerando:

1. **Posiciones del Celtic Cross**: Cómo cada posición revela aspectos del estado mental
2. **Orientaciones**: Normal (energía activa) vs Invertida (energía bloqueada)
3. **Elementos**: Fuego (creatividad), Agua (emociones), Aire (pensamiento), Tierra (práctica)
4. **Estado Cerebral**: Hemisferios, glándula pineal, patrones mentales

Genera análisis PROFUNDO (Nivel 7) que revele estado mental actual, bloqueos, fortalezas y camino de desarrollo.
"""

    try:
        response = FLASH_MODEL.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

def analyze_body(data):
    """Análisis Corporal con 10 cartas"""
    cards = data.get('cards', [])
    birth_data = data.get('birthData', {})
    
    card_description = format_card_spread(cards)
    numerology = calculate_spread_numerology(cards)
    elements = analyze_element_balance(cards)
    
    prompt = f"""{SYSTEM_CONTEXT}

ANÁLISIS CORPORAL - TIRADA DE 10 CARTAS (Celtic Cross)

DATOS PERSONALES:
- Nombre: {birth_data.get('name', 'No especificado')}
- Nacimiento: {birth_data.get('date', 'No especificada')} {birth_data.get('time', '')}

TIRADA COMPLETA:
{card_description}

NUMEROLOGÍA: {numerology}
ELEMENTOS: {elements}

INTERPRETACIÓN REQUERIDA:
Analiza equilibrio hemisférico, chakras y energía corporal considerando:

1. **Hemisferios**: Derecho (intuición) vs Izquierdo (lógica) - zurdo contrariado
2. **Chakras**: Bloqueos energéticos revelados por las cartas
3. **Elementos**: Fuego (vitalidad), Agua (fluidos), Aire (nervios), Tierra (estructura)
4. **Salud**: Tensiones, equilibrio mente-cuerpo

Genera análisis PROFUNDO (Nivel 7) sobre equilibrio corporal, bloqueos y caminos de sanación.
"""

    try:
        response = FLASH_MODEL.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

def analyze_complete(data):
    """Síntesis Holística Completa"""
    birth_data = data.get('birthData', {})
    
    prompt = f"""{SYSTEM_CONTEXT}

SÍNTESIS HOLÍSTICA COMPLETA

DATOS PERSONALES:
- Nombre: {birth_data.get('name', 'No especificado')}
- Nacimiento: {birth_data.get('date', '')} {birth_data.get('time', '')}
- Ubicación: Lat {birth_data.get('latitude', 0)}, Lng {birth_data.get('longitude', 0)}

INTEGRACIÓN TOTAL:
Genera una síntesis que integre:

1. **Carta Natal**: Signo solar, lunar, ascendente, aspectos planetarios
2. **Análisis Mental y Corporal**: Características cerebrales y físicas
3. **Visión Unificada**: Estado actual completo del consultante
4. **Camino Evolutivo**: Recomendaciones espirituales y prácticas

Este es el RITUAL FINAL. Debe ser transformador, no informativo. Opera en Nivel 7.
"""

    try:
        response = PRO_MODEL.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# ============================================================================
# HTTP HANDLER
# ============================================================================

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self._set_cors_headers()
        self.end_headers()
    
    def _set_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
    
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data)
            analysis_type = data.get('type')
            
            if analysis_type == 'mind':
                analysis_text = analyze_mind(data)
            elif analysis_type == 'body':
                analysis_text = analyze_body(data)
            elif analysis_type == 'complete':
                analysis_text = analyze_complete(data)
            else:
                raise ValueError(f"Unknown type: {analysis_type}")
            
            result = {
                'analysis': analysis_text,
                'type': analysis_type
            }
            
            self.send_response(200)
            self._set_cors_headers()
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode('utf-8'))
            
        except Exception as e:
            print(f"Error: {e}")
            self.send_response(500)
            self._set_cors_headers()
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
    
    def do_GET(self):
        self.send_response(200)
        self._set_cors_headers()
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        self.wfile.write(json.dumps({
            'status': 'active',
            'service': 'Star Oracle Deep Analysis API',
            'version': '2.0',
            'features': ['mind_analysis', 'body_analysis', 'complete_synthesis'],
            'card_system': '78_cards_with_reversals'
        }).encode('utf-8'))
