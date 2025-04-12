from fastapi import APIRouter
from pydantic import BaseModel
from app.services.memory_manager import (
    save_user_memory, fetch_user_memory, remove_old_memories
)
from app.services.intent_classifier import classify_intent
from app.services.policy_scorer import rank_policies
from app.services.real_time_fetcher import get_live_insurance_rates
from app.config import generate_chat_response
from app.utils.embeddings import embed_text, cosine_similarity

router = APIRouter()

# Request models
class MemoryRequest(BaseModel):
    user_id: str
    text: str

class FetchRequest(BaseModel):
    user_id: str
    query: str

class DeleteMemoryRequest(BaseModel):
    user_id: str
    max_age_in_days: int = 30  # Default to deleting memories older than 30 days

# --- Endpoint to save memory ---
@router.post("/save-memory")
async def save_memory(request: MemoryRequest):
    try:
        save_user_memory(request.user_id, request.text)
        ai_response = await generate_response(request.text, request.user_id)
        return {
            "message": "Memory saved successfully!",
            "ai_response": ai_response
        }
    except Exception as e:
        return {"message": f"Error saving memory: {e}"}

# --- Endpoint to fetch memory ---
@router.post("/fetch-memory")
async def fetch_memory(request: FetchRequest):
    try:
        memories = fetch_user_memory(request.user_id, request.query)
        if memories:
            most_relevant_memory = memories[0]
            ai_response = await generate_response(
                f"User's query: {request.query}\nPrevious memory: {most_relevant_memory}",
                request.user_id
            )
        else:
            ai_response = "No relevant memories found. How can I assist you?"
        return {
            "memories": memories,
            "ai_response": ai_response
        }
    except Exception as e:
        return {"message": f"Error fetching memory: {e}"}

# --- Endpoint to delete outdated memories ---
@router.post("/delete-memory")
async def delete_memory(request: DeleteMemoryRequest):
    try:
        remove_old_memories(request.user_id, request.max_age_in_days)
        return {"message": f"Memories older than {request.max_age_in_days} days deleted for user {request.user_id}."}
    except Exception as e:
        return {"message": f"Error deleting memory: {e}"}

# --- Generate chatbot response using context + intent ---
async def generate_response(user_input: str, user_id: str) -> str:
    intent = classify_intent(user_input)
    relevant_memories = fetch_user_memory(user_id, user_input)
    context = " ".join(relevant_memories) + " " + user_input if relevant_memories else user_input
    ai_response = await generate_chat_response(context)
    return ai_response
