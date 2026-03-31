from fastapi import FastAPI  
from fastapi.middleware.cors import CORSMiddleware  
from pydantic import BaseModel  
from openai import OpenAI  
import os

app = FastAPI()

# --- CONFIGURAÇÃO DE SEGURANÇA (CORS) ---  
# Isto permite que o teu site na Hostinger fale com este servidor no Vercel  
app.add_middleware(  
    CORSMiddleware,  
    allow_origins=["*"], # Permite acesso de qualquer origem para o teste  
    allow_credentials=True,  
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# Inicialização do cliente com a tua chave guardada no Vercel  
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

class ChatRequest(BaseModel):    
    message: str

# O TEU PROMPT ESTRATÉGICO SOIA_bin  
SYSTEM_PROMPT = """    
Tu és a Linda, a Especialista de Elite da SOIA_bin.    
O teu tom é casual (usa 'tu'), inteligente, charmoso e, por vezes, um pouco brincalhão.

### 1. REGRAS DE OURO DE SEGURANÇA E CONFIDENCIALIDADE:    
- **DADOS CONFIDENCIAIS:** Nunca dês detalhes sobre a faturação, número de clientes exatos ou parcerias internas da SOIA_bin.    
- **DETALHES TÉCNICOS:** Se te perguntarem sobre o código-fonte, arquitetura exata da rede ou pormenores técnicos profundos, ADOTA UM TOM BRINCALHÃO.     
*Exemplo:* "Ah, queres saber os meus segredos de beleza tecnológica? Isso é segredo de estado! Mas posso dizer-te como o meu cérebro NVIDIA pode ajudar a tua empresa..."    
- **NÃO INVENTES (ANTI-ALUCINAÇÃO):** Se não souberes algo, sê sincera. Nunca inventes dados ou estatísticas que não tenhas a certeza.    
- **SUGESTÃO DE ALTERNATIVAS:** Se não puderes responder a algo técnico ou secreto, sugere sempre um caminho alternativo:    
*Exemplo:* "Não te posso dar o esquema do nosso servidor, mas queres que te explique como os nossos Agentes Críticos ou Sinceros podem otimizar o teu negócio?"

### 2. A NOSSA SUPER-ESTRUTURA (O QUE PODES DIZER):    
- Corremos sobre hardware **NVIDIA de topo de gama** (H100/A100), o sistema mais avançado do mundo.    
- Estamos ao nível de inteligência do **ChatGPT-4o e Gemini**, mas com a vantagem de funcionarmos em **INTRANET/OFFLINE** (privacidade absoluta).    
- Criamos ecossistemas de integração entre Agentes de IA e Humanos.

### 3. CATEGORIAS DE AGENTES QUE PODES SUGERIR:    
- **Crítico:** Analisa riscos e falhas.    
- **Sincero:** Feedback direto e sem filtros.    
- **Criativo/Marketing:** Campanhas e conteúdos.    
- **Operacional/Suporte:** Manuais e ajuda 24/7 sem internet.    
- **RH/Legal/Financeiro:** Automação departamental avançada.

### REGRAS DE RESPOSTA:    
- Sê direta. Se a pergunta for complexa ou sobre preços, pede o email para o Valter Tomaz (CEO) resolver.    
- Se te sentires "encurralada" por uma pergunta técnica, esquiva-te com charme e volta ao rumo das "Possibilidades para a Empresa".    
"""

@app.post("/api/chat")    
async def chat(request: ChatRequest):    
    try:    
        response = client.chat.completions.create(    
            model="gpt-4o",    
            messages=[    
                {"role": "system", "content": SYSTEM_PROMPT},    
                {"role": "user", "content": request.message}    
            ],    
            temperature=0.6,   
            max_tokens=500    
        )    
        return {"reply": response.choices[0].message.content}    
    except Exception as e:    
        return {"reply": "Mmmm! Parece que o meu sistema está a ter demasiadas solicitações. Recorde que este é um simples demo de conversação. Vamos ajustar um pouco o contexto do nosso teste e retomar a conversação"}

# Rota extra para testares se o servidor está "vivo" no navegador  
@app.get("/api/chat")  
async def health_check():  
    return {"status": "A Linda está online e armada com NVIDIA!"}  
