# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Controller import rag_controller, chat_controller
from config import CHROMA_DIR


app = FastAPI(
    title="Local RAG API",
    description="Retrieval-Augmented Generation with Ollama + ChromaDB",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(rag_controller.router)
app.include_router(chat_controller.router)


@app.get("/")
async def root():
    return {
        "message": "Local RAG API",
        "docs": "/docs",
        "health": "/api/v1/health"
    }


if __name__ == "__main__":
    import uvicorn
    print(f"Starting server...")
    print(f"Chroma data: {CHROMA_DIR}")
    print(f"API docs: http://localhost:8000/docs")
    uvicorn.run(app, host="127.0.0.1", port=8000)