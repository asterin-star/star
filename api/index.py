from http.server import BaseHTTPRequestHandler
import json
import os
# Note: In Vercel, dependencies must be in requirements.txt

# Configuration
PROJECT_ID = 'gen-lang-client-0438257778'
LOCATION = 'us-central1'

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data)
            
            # 1. Authentication & Initialization (Vertex AI)
            # We import here to avoid cold start issues if possible, though Vercel caches imports
            import vertexai
            from vertexai.generative_models import GenerativeModel
            
            # Initialize Vertex AI
            # Note: Vercel will need GOOGLE_APPLICATION_CREDENTIALS env var or similar
            # For this implementation, we assume the environment is set up or service_account.json is available
            # However, in Vercel, file paths can be tricky. 
            # Ideally, credentials should be passed via Environment Variables (Base64 encoded)
            # But for now we will try to use the existing pattern if the file is deployed.
            
            if os.path.exists('service_account.json'):
                os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'service_account.json'
            
            vertexai.init(project=PROJECT_ID, location=LOCATION)
            
            # 2. Build Prompt (Multilingual)
            card_name = data.get('cardName', 'Carta Desconocida')
            language = data.get('language', 'es')
            definitions = data.get('definitions', {})
            examples = data.get('examples', {})
            
            # Prompts por idioma
            prompts = {
                'es': f"""
Eres un oráculo profesional especializado en orientación personal y desarrollo humano.
Analiza la carta "{card_name}" con esta configuración numerológica única:

CONTEXTO:
- Arquetipo (Var. {examples.get('arquetipo', '?')}/22): "{definitions.get('arquetipo', '')}"
- Sombra (Var. {examples.get('sombra', '?')}/22): "{definitions.get('sombra', '')}"
- Misticismo (Var. {examples.get('misticismo', '?')}/22): "{definitions.get('misticismo', '')}"

TAREA (120 palabras):
1. **Objetivo**: Principal meta a desarrollar según esta carta
2. **Acción**: Paso concreto basado en las variantes recibidas
3. **Atención**: Aspecto vital que requiere enfoque inmediato

Lenguaje formal, directo, orientado a la acción. Usa "usted" o tercera persona.

Formato:
**Objetivo**: [descripción completa]
**Acción**: [descripción completa]
**Atención**: [descripción completa]
""",
                'en': f"""
You are a professional oracle specialized in personal guidance and human development.
Analyze the card "{card_name}" with this unique numerological configuration:

CONTEXT:
- Archetype (Var. {examples.get('arquetipo', '?')}/22): "{definitions.get('arquetipo', '')}"
- Shadow (Var. {examples.get('sombra', '?')}/22): "{definitions.get('sombra', '')}"
- Mysticism (Var. {examples.get('misticismo', '?')}/22): "{definitions.get('misticismo', '')}"

TASK (120 words):
1. **Objective**: Main goal to develop according to this card
2. **Action**: Concrete step based on the specific variants received
3. **Attention**: Vital aspect requiring immediate focus

Use formal, direct, action-oriented language.

Format:
**Objective**: [complete description]
**Action**: [complete description]
**Attention**: [complete description]
""",
                'pt': f"""
Você é um oráculo profissional especializado em orientação pessoal e desenvolvimento humano.
Analise a carta "{card_name}" com esta configuração numerológica única:

CONTEXTO:
- Arquétipo (Var. {examples.get('arquetipo', '?')}/22): "{definitions.get('arquetipo', '')}"
- Sombra (Var. {examples.get('sombra', '?')}/22): "{definitions.get('sombra', '')}"
- Misticismo (Var. {examples.get('misticismo', '?')}/22): "{definitions.get('misticismo', '')}"

TAREFA (120 palavras):
1. **Objetivo**: Meta principal a desenvolver segundo esta carta
2. **Ação**: Passo concreto baseado nas variantes recebidas
3. **Atenção**: Aspecto vital que requer foco imediato

Linguagem formal, direta, orientada à ação. Use "você" ou terceira pessoa.

Formato:
**Objetivo**: [descrição completa]
**Ação**: [descrição completa]
**Atenção**: [descrição completa]
""",
                'fr': f"""
Vous êtes un oracle professionnel spécialisé dans l'orientation personnelle et le développement humain.
Analysez la carte "{card_name}" avec cette configuration numérologique unique:

CONTEXTE:
- Archétype (Var. {examples.get('arquetipo', '?')}/22): "{definitions.get('arquetipo', '')}"
- Ombre (Var. {examples.get('sombra', '?')}/22): "{definitions.get('sombra', '')}"
- Mysticisme (Var. {examples.get('misticismo', '?')}/22): "{definitions.get('misticismo', '')}"

TÂCHE (120 mots):
1. **Objectif**: But principal à développer selon cette carte
2. **Action**: Étape concrète basée sur les variantes reçues
3. **Attention**: Aspect vital nécessitant une attention immédiate

Langage formel, direct, orienté vers l'action. Utilisez "vous" ou la troisième personne.

Format:
**Objectif**: [description complète]
**Action**: [description complète]
**Attention**: [description complète]
""",
                'de': f"""
Sie sind ein professionelles Orakel, spezialisiert auf persönliche Orientierung und menschliche Entwicklung.
Analysieren Sie die Karte "{card_name}" mit dieser einzigartigen numerologischen Konfiguration:

KONTEXT:
- Archetyp (Var. {examples.get('arquetipo', '?')}/22): "{definitions.get('arquetipo', '')}"
- Schatten (Var. {examples.get('sombra', '?')}/22): "{definitions.get('sombra', '')}"
- Mystik (Var. {examples.get('misticismo', '?')}/22): "{definitions.get('misticismo', '')}"

AUFGABE (120 Wörter):
1. **Ziel**: Hauptziel, das gemäß dieser Karte zu entwickeln ist
2. **Aktion**: Konkreter Schritt basierend auf den erhaltenen Varianten
3. **Aufmerksamkeit**: Lebenswichtiger Aspekt, der sofortige Aufmerksamkeit erfordert

Formale, direkte, handlungsorientierte Sprache. Verwenden Sie "Sie" oder die dritte Person.

Format:
**Ziel**: [vollständige Beschreibung]
**Aktion**: [vollständige Beschreibung]
**Aufmerksamkeit**: [vollständige Beschreibung]
""",
                'ja': f"""
あなたは個人的な指導と人間開発を専門とする プロのオラクルです。
このユニークな数秘術的配置でカード「{card_name}」を分析してください:

コンテキスト:
- アーキタイプ (変形 {examples.get('arquetipo', '?')}/22): "{definitions.get('arquetipo', '')}"
- シャドウ (変形 {examples.get('sombra', '?')}/22): "{definitions.get('sombra', '')}"
- 神秘主義 (変形 {examples.get('misticismo', '?')}/22): "{definitions.get('misticismo', '')}"

タスク (120文字):
1. **目的**: このカードに従って開発すべき主な目標
2. **行動**: 受け取った特定の変形に基づいた具体的なステップ
3. **注意**: 即座の集中が必要な重要な側面

フォーマル、直接的、 行動指向の言語を使用してください。

形式:
**目的**: [完全な説明]
**行動**: [完全な説明]
**注意**: [完全な説明]
""",
                'ko': f"""
당신은 개인 지도와 인간 개발을 전문으로 하는 전문 오라클입니다.
이 고유한 수비학적 구성으로 카드 "{card_name}"를 분석하십시오:

컨텍스트:
- 원형 (변형 {examples.get('arquetipo', '?')}/22): "{definitions.get('arquetipo', '')}"
- 그림자 (변형 {examples.get('sombra', '?')}/22): "{definitions.get('sombra', '')}"
- 신비주의 (변형 {examples.get('misticismo', '?')}/22): "{definitions.get('misticismo', '')}"

과제 (120단어):
1. **목표**: 이 카드에 따라 개발해야 할 주요 목표
2. **행동**: 받은 특정 변형을 기반으로 한 구체적인 단계
3. **주의**: 즉각적인 집중이 필요한 중요한 측면

공식적이고 직접적이며 행동 지향적인 언어를 사용하십시오.

형식:
**목표**: [완전한 설명]
**행동**: [완전한 설명]
**주의**: [완전한 설명]
""",
                'zh': f"""
您是专门从事个人指导和人类发展的专业神谕。
用这个独特的命理学配置分析卡牌"{card_name}":

背景:
- 原型 (变体 {examples.get('arquetipo', '?')}/22): "{definitions.get('arquetipo', '')}"
- 阴影 (变体 {examples.get('sombra', '?')}/22): "{definitions.get('sombra', '')}"
- 神秘主义 (变体 {examples.get('misticismo', '?')}/22): "{definitions.get('misticismo', '')}"

任务 (120字):
1. **目标**: 根据此卡需要发展的主要目标
2. **行动**: 基于收到的特定变体的具体步骤
3. **注意**: 需要立即关注的重要方面

使用正式、直接、以行动为导向的语言。

格式:
**目标**: [完整描述]
**行动**: [完整描述]
**注意**: [完整描述]
"""
            }
            
            prompt = prompts.get(language, prompts['es'])

            # 3. Call Gemini API (Vertex AI)
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
            print(f"Error in handler: {e}")
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Star Oracle API Active")
