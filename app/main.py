from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from app.routes import chat  # Make sure this matches your actual project structure

app = FastAPI()

# Allow Vite's default development origins
origins = [
    "http://localhost:5173",  # Vite dev server
    "http://127.0.0.1:5173",
    "http://localhost:8080",  # Add this
    "http://127.0.0.1:8080"
]

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,           # Only allow these frontend origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root route to avoid 404 on "/"
@app.get("/")
def root():
    return {"message": "Life Insurance Chatbot API is running 🚀"}

# Optional: Avoid 404 on /favicon.ico
@app.get("/favicon.ico")
def favicon():
    return Response(status_code=204)

# Include chat routes
app.include_router(chat.router)
