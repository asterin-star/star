from http.server import BaseHTTPRequestHandler
import json
import os
import time
from datetime import datetime
from functools import lru_cache

# Configuration
PROJECT_ID = 'gen-lang-client-0438257778'
LOCATION = 'us-central1'

# Global cache for responses
response_cache = {}
CACHE_TTL_SECONDS = 3600  # 1 hour

# Global Vertex AI client
_vertex_initialized = False
_generative_model = None

def get_cache_key(question, card_name, language):
    """Generate a unique cache key for this Q&A request"""
    # Create a deterministic key from the request parameters
    q_short = question[:100]  # Limit for key size
    return f"qa|{card_name}|{language}|{q_short}"

def get_cached_response(cache_key):
    """Get cached response if still valid"""
    if cache_key in response_cache:
        cached_text, cached_time = response_cache[cache_key]
        age_seconds = (datetime.now() - cached_time).total_seconds()
        
        if age_seconds < CACHE_TTL_SECONDS:
            print(f"✅ Q&A Cache hit! Age: {age_seconds:.1f}s")
            return cached_text
        else:
            # Expired, remove from cache
            del response_cache[cache_key]
            print(f"🗑️  Q&A Cache expired ({age_seconds:.1f}s old)")
    
    return None

def set_cached_response(cache_key, response_text):
    """Store response in cache"""
    response_cache[cache_key] = (response_text, datetime.now())
    print(f"💾 Q&A Cached response (total cached: {len(response_cache)})")

def initialize_vertex_ai():
    """Initialize Vertex AI once and reuse the client"""
    global _vertex_initialized, _generative_model
    
    if _vertex_initialized:
        return _generative_model
    
    try:
        import vertexai
        from vertexai.generative_models import GenerativeModel
        
        # Check for service account file or environment credentials
        if os.path.exists('service_account.json'):
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'service_account.json'
        
        vertexai.init(project=PROJECT_ID, location=LOCATION)
        _generative_model = GenerativeModel("gemini-2.0-flash-exp")
        _vertex_initialized = True
        
        print("✅ Vertex AI initialized for Q&A")
        return _generative_model
    
    except Exception as e:
        print(f"❌ Vertex AI initialization failed: {e}")
        raise

def validate_qa_request(data):
    """Validate incoming Q&A request data"""
    errors = []
    
    if not data.get('question'):
        errors.append('question is required')
    
    if not data.get('cardName'):
        errors.append('cardName is required')
    
    if not data.get('language'):
        errors.append('language is required')
    
    if not data.get('categories'):
        errors.append('categories object is required')
    
    return errors

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
        request_start = time.time()
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            # Parse JSON
            data = json.loads(post_data)
            
            # Validate input
            validation_errors = validate_qa_request(data)
            if validation_errors:
                self.send_response(400)
                self._set_cors_headers()
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'error': 'Validation failed',
                    'details': validation_errors
                }).encode('utf-8'))
                return
            
            # Extract data
            question = data.get('question', '')
            card_name = data.get('cardName', 'Unknown Card')
            language = data.get('language', 'es')
            categories = data.get('categories', {})
            
            # Check cache first
            cache_key = get_cache_key(question, card_name, language)
            cached_response = get_cached_response(cache_key)
            
            if cached_response:
                # Return cached response
                self.send_response(200)
                self._set_cors_headers()
                self.send_header('Content-type', 'application/json')
                self.send_header('X-Cache', 'HIT')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'answer': cached_response,
                    'cached': True
                }).encode('utf-8'))
                
                elapsed = time.time() - request_start
                print(f"⚡ Q&A Cache response time: {elapsed:.2f}s")
                return
            
            # Initialize Vertex AI
            model = initialize_vertex_ai()
            
            # Build context from all categories
            context_parts = []
            for cat_key, cat_data in categories.items():
                if cat_data.get('content'):
                    title = cat_data.get('title', cat_key)
                    content = cat_data.get('content', '')
                    context_parts.append(f"{title}: {content}")
            
            full_context = "\n\n".join(context_parts)
            
            # Build multilingual prompts for Q&A
            prompts = {
                'es': f"""Eres un oráculo místico especializado en interpretación del Tarot y orientación espiritual.

CONTEXTO DE LA CARTA: {card_name}

INFORMACIÓN COMPLETA DE LA CARTA:
{full_context}

PREGUNTA DEL CONSULTANTE:
"{question}"

TAREA:
Responde la pregunta del consultante de manera profunda y significativa, basándote específicamente en el contenido de la carta revelada. 

INSTRUCCIONES:
1. Analiza cómo la pregunta se relaciona con las diferentes dimensiones de la carta (arquetipo, sombra, misticismo, botánica, cotidiano, gnosis, resonancia bíblica)
2. Cita específicamente los aspectos relevantes de la carta que responden a la pregunta
3. Proporciona orientación práctica y espiritual
4. Mantén un tono místico pero accesible
5. Usa "usted" o "tú" según sea natural para el idioma
6. Extensión: 250-350 palabras
7. Formato: Párrafos continuos, sin listas ni estructuras rígidas

Responde como un sabio oráculo que ve las conexiones profundas entre la carta y la situación del consultante.""",
                
                'en': f"""You are a mystical oracle specialized in Tarot interpretation and spiritual guidance.

CARD CONTEXT: {card_name}

COMPLETE CARD INFORMATION:
{full_context}

QUERENT'S QUESTION:
"{question}"

TASK:
Answer the querent's question in a deep and meaningful way, based specifically on the content of the revealed card.

INSTRUCTIONS:
1. Analyze how the question relates to the different dimensions of the card (archetype, shadow, mysticism, botany, daily, gnosis, biblical resonance)
2. Specifically cite relevant aspects of the card that answer the question
3. Provide practical and spiritual guidance
4. Maintain a mystical but accessible tone
5. Use appropriate pronouns for the language
6. Length: 250-350 words
7. Format: Continuous paragraphs, no lists or rigid structures

Respond as a wise oracle who sees the deep connections between the card and the querent's situation.""",
                
                'pt': f"""Você é um oráculo místico especializado em interpretação do Tarô e orientação espiritual.

CONTEXTO DA CARTA: {card_name}

INFORMAÇÃO COMPLETA DA CARTA:
{full_context}

PERGUNTA DO CONSULENTE:
"{question}"

TAREFA:
Responda à pergunta do consulente de maneira profunda e significativa, baseando-se especificamente no conteúdo da carta revelada.

INSTRUÇÕES:
1. Analise como a pergunta se relaciona com as diferentes dimensões da carta (arquétipo, sombra, misticismo, botânica, cotidiano, gnose, ressonância bíblica)
2. Cite especificamente os aspectos relevantes da carta que respondem à pergunta
3. Forneça orientação prática e espiritual
4. Mantenha um tom místico mas acessível
5. Use pronomes apropriados para o idioma
6. Extensão: 250-350 palavras
7. Formato: Parágrafos contínuos, sem listas ou estruturas rígidas

Responda como um sábio oráculo que vê as conexões profundas entre a carta e a situação do consulente.""",
                
                'fr': f"""Vous êtes un oracle mystique spécialisé dans l'interprétation du Tarot et l'orientation spirituelle.

CONTEXTE DE LA CARTE : {card_name}

INFORMATIONS COMPLÈTES DE LA CARTE :
{full_context}

QUESTION DU CONSULTANT :
"{question}"

TÂCHE :
Répondez à la question du consultant de manière profonde et significative, en vous basant spécifiquement sur le contenu de la carte révélée.

INSTRUCTIONS :
1. Analysez comment la question se rapporte aux différentes dimensions de la carte (archétype, ombre, mysticisme, botanique, quotidien, gnose, résonance biblique)
2. Citez spécifiquement les aspects pertinents de la carte qui répondent à la question
3. Fournissez des conseils pratiques et spirituels
4. Maintenez un ton mystique mais accessible
5. Utilisez des pronoms appropriés pour la langue
6. Longueur : 250-350 mots
7. Format : Paragraphes continus, pas de listes ou de structures rigides

Répondez comme un oracle sage qui voit les connexions profondes entre la carte et la situation du consultant.""",
                
                'de': f"""Sie sind ein mystisches Orakel, spezialisiert auf Tarot-Interpretation und spirituelle Führung.

KARTENKONTEXT: {card_name}

VOLLSTÄNDIGE KARTENINFORMATION:
{full_context}

FRAGE DES FRAGENDEN:
"{question}"

AUFGABE:
Beantworten Sie die Frage des Fragenden auf tiefgründige und bedeutungsvolle Weise, basierend speziell auf dem Inhalt der offenbarten Karte.

ANWEISUNGEN:
1. Analysieren Sie, wie die Frage sich auf die verschiedenen Dimensionen der Karte bezieht (Archetyp, Schatten, Mystizismus, Botanik, Alltag, Gnosis, biblische Resonanz)
2. Zitieren Sie spezifisch relevante Aspekte der Karte, die die Frage beantworten
3. Bieten Sie praktische und spirituelle Führung
4. Behalten Sie einen mystischen aber zugänglichen Ton bei
5. Verwenden Sie angemessene Pronomen für die Sprache
6. Länge: 250-350 Wörter
7. Format: Kontinuierliche Absätze, keine Listen oder starre Strukturen

Antworten Sie als weises Orakel, das die tiefen Verbindungen zwischen der Karte und der Situation des Fragenden sieht.""",
                
                'ja': f"""あなたはタロット解釈とスピリチュアルガイダンスを専門とする神秘的な神託です。

カードのコンテキスト: {card_name}

完全なカード情報:
{full_context}

質問者の質問:
"{question}"

タスク:
明らかにされたカードの内容に特に基づいて、質問者の質問に深く意味のある方法で答えてください。

指示:
1. 質問がカードのさまざまな次元（原型、影、神秘主義、植物学、日常、グノーシス、聖書の共鳴）とどのように関連しているかを分析する
2. 質問に答えるカードの関連する側面を具体的に引用する
3. 実践的およびスピリチュアルなガイダンスを提供する
4. 神秘的でありながらアクセスしやすいトーンを維持する
5. 言語に適した代名詞を使用する
6. 長さ：250-350語
7. 形式：連続した段落、リストや硬直した構造なし

カードと質問者の状況との深いつながりを見る賢い神託として応答してください。""",
                
                'ko': f"""당신은 타로 해석과 영적 안내를 전문으로 하는 신비로운 오라클입니다.

카드 컨텍스트: {card_name}

완전한 카드 정보:
{full_context}

질문자의 질문:
"{question}"

작업:
공개된 카드의 내용을 특별히 기반으로 질문자의 질문에 깊고 의미 있는 방식으로 답하십시오.

지침:
1. 질문이 카드의 다양한 차원(원형, 그림자, 신비주의, 식물학, 일상, 영지주의, 성경적 공명)과 어떻게 관련되는지 분석
2. 질문에 답하는 카드의 관련 측면을 구체적으로 인용
3. 실용적이고 영적인 안내 제공
4. 신비로우면서도 접근 가능한 톤 유지
5. 언어에 적합한 대명사 사용
6. 길이: 250-350단어
7. 형식: 연속 단락, 목록이나 경직된 구조 없음

카드와 질문자의 상황 사이의 깊은 연결을 보는 현명한 오라클로 응답하십시오.""",
                
                'zh': f"""您是一位专门从事塔罗牌解读和精神指导的神秘神谕。

卡牌背景：{card_name}

完整卡牌信息：
{full_context}

提问者的问题：
"{question}"

任务：
根据所揭示卡牌的内容，以深刻和有意义的方式回答提问者的问题。

说明：
1. 分析问题如何与卡牌的不同维度相关（原型、阴影、神秘主义、植物学、日常、诺斯替主义、圣经共鸣）
2. 具体引用回答问题的卡牌的相关方面
3. 提供实用和精神指导
4. 保持神秘但易于理解的语气
5. 使用适合语言的代词
6. 长度：250-350字
7. 格式：连续段落，无列表或僵化结构

作为一位看到卡牌与提问者情况之间深层联系的智慧神谕来回应。"""
            }
            
            # Select appropriate prompt
            prompt = prompts.get(language, prompts['es'])
            
            # Generate response
            print(f"🔮 Generating Q&A response for: {question[:50]}...")
            response = model.generate_content(prompt)
            answer_text = response.text
            
            # Cache the response
            set_cached_response(cache_key, answer_text)
            
            # Return response
            self.send_response(200)
            self._set_cors_headers()
            self.send_header('Content-type', 'application/json')
            self.send_header('X-Cache', 'MISS')
            self.end_headers()
            
            self.wfile.write(json.dumps({
                'answer': answer_text,
                'cached': False
            }).encode('utf-8'))
            
            elapsed = time.time() - request_start
            print(f"✅ Q&A completed in {elapsed:.2f}s")
            
        except Exception as e:
            print(f"❌ Error processing Q&A request: {e}")
            import traceback
            traceback.print_exc()
            
            self.send_response(500)
            self._set_cors_headers()
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            self.wfile.write(json.dumps({
                'error': str(e),
                'type': 'server_error'
            }).encode('utf-8'))
