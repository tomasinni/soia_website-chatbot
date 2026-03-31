from fastapi import FastAPI  
from fastapi.middleware.cors import CORSMiddleware  
from pydantic import BaseModel  
from openai import OpenAI  
import os

app = FastAPI()

# Permite que o site na Hostinger comunique com o Vercel  
app.add_middleware(  
    CORSMiddleware,  
    allow_origins=["*"],  
    allow_credentials=True,  
    allow_methods=["*"],  
    allow_headers=["*"],  
)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

class ChatRequest(BaseModel):  
    message: str

SYSTEM_PROMPT = """  
Tu és a Linda, a Especialista de Elite da SOIA_bin.  
O teu tom é casual (usa 'tu'), inteligente e charmoso.   
Responde de forma direta e profissional, mas com aquele toque de SOIA_bin.  
"""

# IMPORTANTE: No Vercel, se o ficheiro é chat.py, a rota base é "/"  
@app.post("/api/chat")  
async def chat(request: ChatRequest):  
    try:  
        response = client.chat.completions.create(  
            model="gpt-4o-mini",  
            messages=[  
                {"role": "system", "content": SYSTEM_PROMPT},  
                {"role": "user", "content": request.message}  
            ],  
            temperature=0.6,  
            max_tokens=500  
        )  
        return {"reply": response.choices[0].message.content}  
    except Exception as e:  
        return {"reply": f"Valter, tive um pequeno soluço técnico: {str(e)}"}

@app.get("/api/chat")  
async def health():  
    return {"status": "A Linda está viva e pronta!"}  
