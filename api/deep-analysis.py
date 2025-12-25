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
PRO_MODEL = genai.GenerativeModel('gemini-2.5-pro')

# ============================================================================
# ANTIGRAVITY SYSTEM MANIFESTO - FOUNDATIONAL CONTEXT
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

def get_user_context_from_cards(collected_cards):
    """Extract symbolic patterns from collected cards"""
    if not collected_cards:
        return "Sin cartas colectadas aún"
    
    card_names = [card.get('name', '') for card in collected_cards]
    card_count = len(collected_cards)
    
    return f"Cartas colectadas ({card_count}): {', '.join(card_names)}"

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self._set_cors_headers()
        self.end_headers()
    
    def _set_cors_headers(self):
        """Set CORS headers for cross-origin requests"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
    
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data)
            analysis_type = data.get('type')
            collected_cards = data.get('collectedCards', [])
            
            # Context que se comparte entre todos los análisis
            user_context = get_user_context_from_cards(collected_cards)
            
            if analysis_type == 'brain':
                result = self._analyze_brain(user_context, collected_cards)
            elif analysis_type == 'body':
                result = self._analyze_body(user_context, collected_cards)
            elif analysis_type == 'personality':
                result = self._analyze_personality(user_context, collected_cards)
            elif analysis_type == 'complete':
                result = self._analyze_complete(user_context, collected_cards, data)
            else:
                raise ValueError(f"Unknown analysis type: {analysis_type}")
            
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
            self.wfile.write(json.dumps({
                'error': str(e)
            }).encode('utf-8'))
    
    def _analyze_brain(self, context, cards):
        """Prompt 1: Análisis Cerebral y Neuronal"""
        prompt = f"{SYSTEM_CONTEXT}

===== SOLICITUD ESPECÍFICA: ANÁLISIS CEREBRAL =====

CONTEXTO DEL USUARIO:
{context}

Basándote en las cartas del tarot que ha colectado, proporciona un análisis detallado de aproximadamente 300 palabras que incluya:

1. **Estado Cerebral Actual**
   - Actividad hemisférica dominante (izquierdo/derecho)
   - Patrones de pensamiento identificados a partir de los arquetipos de las cartas
   - Áreas de desarrollo neuronal sugeridas

2. **Desarrollo de la Glándula Pineal**
   - Estado estimado de activación (1-10)
   - Bloqueos energéticos potenciales según las cartas
   - Prácticas recomendadas para optimización

3. **Sugerencias de Neuro-Optimización**
   - Ejercicios mentales específicos basados en los arquetipos
   - Hábitos para equilibrio cerebral
   - Meditaciones recomendadas

Responde en español, con un tono profesional pero accesible. Sé específico y conecta los arquetipos de las cartas con estados neuronales y espirituales reales. IMPORTANTE: Opera desde el NIVEL 7, no des respuestas genéricas de horóscopo."""

        response = FLASH_MODEL.generate_content(prompt)
        return {
            'analysis': response.text,
            'type': 'brain'
        }
    
    def _analyze_body(self, context, cards):
        """Prompt 2: Análisis Corporal (Hemisferios)"""
        prompt = f"{SYSTEM_CONTEXT}

===== SOLICITUD ESPECÍFICA: ANÁLISIS CORPORAL =====

CONTEXTO DEL USUARIO:
{context}

Basándote en las cartas del tarot que ha colectado, proporciona un análisis de aproximadamente 250 palabras sobre:

1. **Hemisferio Izquierdo (Cuerpo Derecho - Lógica/Análisis)**
   - Porcentaje estimado de activación
   - Fortalezas identificadas en las cartas
   - Áreas que requieren desarrollo

2. **Hemisferio Derecho (Cuerpo Izquierdo - Intuición/Creatividad)**
   - Porcentaje estimado de activación
   - Dones naturales según los arquetipos
   - Potencial sin explotar

3. **Recomendaciones de Armonización**
   - Prácticas físicas específicas (yoga, tai chi, etc.)
   - Ejercicios de integración hemisférica
   - Técnicas de equilibrio energético

Responde en español, conectando los arquetipos de las cartas con estados corporales y energéticos. Recuerda que el usuario es 'zurdo contrariado' - esto es relevante para el análisis de hemisferios."""

        response = FLASH_MODEL.generate_content(prompt)
        return {
            'analysis': response.text,
            'type': 'body'
        }
    
    def _analyze_personality(self, context, cards):
        """Prompt 3: Perfil de Personalidad (Stats)"""
        # Calcular stats básicos
        card_count = len(cards)
        stats = {
            'fuerza': min(20, 8 + card_count * 2),
            'inteligencia': min(20, 10 + card_count),
            'sabiduria': min(20, 12 + card_count),
            'carisma': min(20, int(9 + card_count * 1.5)),
            'constitucion': min(20, 11 + card_count),
            'destreza': min(20, 7 + card_count * 2)
        }
        
        prompt = f"{SYSTEM_CONTEXT}

===== SOLICITUD ESPECÍFICA: PERFIL DE PERSONALIDAD =====

CONTEXTO DEL USUARIO:
{context}

STATS CALCULADOS (escala 1-20):
- Fuerza: {stats['fuerza']}/20
- Inteligencia: {stats['inteligencia']}/20
- Sabiduría: {stats['sabiduria']}/20
- Carisma: {stats['carisma']}/20
- Constitución: {stats['constitucion']}/20
- Destreza: {stats['destreza']}/20

Basándote en las cartas colectadas y estos stats, genera un análisis de aproximadamente 300 palabras que incluya:

1. **Perfil Dominante**
   - Tipo de personalidad según los stats más altos
   - Arquetipos dominantes en su psique

2. **Fortalezas y Debilidades**
   - Qué stats son excepcionales y qué implican
   - Áreas de desarrollo prioritarias

3. **Conclusión de Personalidad**
   - Resumen de quién es esta persona
   - Camino de desarrollo sugerido
   - Potencial sin explotar

Responde en español, integrando los arquetipos del tarot con los stats RPG para crear un perfil coherente y profundo. Este no es un juego: es un espejo para el autoconocimiento."""

        response = FLASH_MODEL.generate_content(prompt)
        return {
            'analysis': response.text,
            'stats': stats,
            'type': 'personality'
        }
    
    def _analyze_complete(self, context, cards, data):
        """Prompt 4: Análisis Completo (Carta Natal + Síntesis)"""
        birth_data = data.get('birthData', {})
        birth_date = birth_data.get('date', '')
        birth_time = birth_data.get('time', '')
        birth_location = birth_data.get('location', '')
        latitude = birth_data.get('latitude', 0)
        longitude = birth_data.get('longitude', 0)
        
        prompt = f"{SYSTEM_CONTEXT}

===== SOLICITUD ESPECÍFICA: SÍNTESIS HOLÍSTICA COMPLETA =====

Este es el análisis más profundo. Integra TODOS los aspectos previos (cerebral, corporl, personalidad) con la carta natal para crear una visión unificada transformadora.

CONTEXTO DEL USUARIO:
{context}

DATOS DE NACIMIENTO:
- Fecha: {birth_date}
- Hora: {birth_time}
- Ubicación: {birth_location}
- Coordenadas: {latitude}, {longitude}

Genera un análisis completo de aproximadamente 400 palabras que integre:

1. **Carta Natal Interpretada**
   - Signo solar probable
   - Influencias lunares
   - Ascendente estimado basado en hora y ubicación
   - Aspectos planetarios relevantes

2. **Integración con las Cartas del Tarot**
   - Cómo los arquetipos colectados resuenan con la carta natal
   - Patrones que se refuerzan mutuamente
   - Sincronicidades identificadas

3. **Síntesis Holística**
   - Unificación de análisis cerebral, corporal y de personalidad
   - Visión completa del estado actual del usuario
   - Camino de evolución personalizado

4. **Recomendaciones Finales**
   - Prácticas espirituales específicas
   - Momentos astrológicos propicios próximos
   - Intenciones recomendadas

Responde en español, creando una narrativa cohesiva que una astrología, tarot y análisis personal. Este es el RITUAL FINAL - debe ser transformador, no informativo."""

        response = PRO_MODEL.generate_content(prompt)
        return {
            'analysis': response.text,
            'natal_chart': {
                'birth_date': birth_date,
                'birth_time': birth_time,
                'location': birth_location,
                'coordinates': {
                    'lat': latitude,
                    'lng': longitude
                }
            },
            'type': 'complete'
        }
    
    def do_GET(self):
        """Health check endpoint"""
        self.send_response(200)
        self._set_cors_headers()
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        self.wfile.write(json.dumps({
            'status': 'active',
            'service': 'Star Oracle Deep Analysis API',
            'version': '1.0',
            'models': {
                'flash': 'gemini-2.5-flash',
                'pro': 'gemini-2.5-pro'
            }
        }).encode('utf-8'))
