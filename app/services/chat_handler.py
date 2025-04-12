from app.services.memory_manager import fetch_user_memory, save_user_memory
from app.services.intent_classifier import classify_intent
from app.services.policy_scorer import rank_policies
from app.services.real_time_fetcher import get_live_insurance_rates
from app.config import generate_chat_response
import hashlib

# Sample mock policies for illustration
mock_policies = [
    {"name": "Secure Life", "monthly_premium": 120, "type": "whole", "has_family_coverage": True, "includes_riders": True},
    {"name": "Term Saver", "monthly_premium": 80, "type": "term", "has_family_coverage": False, "includes_riders": False},
    {"name": "Family First", "monthly_premium": 150, "type": "whole", "has_family_coverage": True, "includes_riders": True},
]

def handle_user_query(user_input: str, user_id: str):
    """
    Main handler for processing the user's query and generating a chatbot response.
    """
    # Step 1: Save current input into memory for future context
    save_user_memory(user_id=user_id, text=user_input)

    # Step 2: Retrieve relevant past memories for context
    relevant_memories = fetch_user_memory(user_id=user_id, query=user_input)
    memory_context = "\n".join(relevant_memories) if relevant_memories else "No relevant memory found."

    # Step 3: Classify the user’s intent
    intent = classify_intent(user_input)

    # Step 4: Build user profile dynamically from memory context (placeholder logic)
    user_profile = build_user_profile(user_id, relevant_memories)

    # Step 5: Rank policies based on profile
    ranked_policies = rank_policies(mock_policies, user_profile)
    top_policies_text = "\n".join([f"{i+1}. {p['name']} - Premium: ${p['monthly_premium']}" for i, p in enumerate(ranked_policies[:3])])

    # Step 6: Handle real-time info if intent requires it
    real_time_data = ""
    if intent == "real_time_info":
        live_data = get_live_insurance_rates(user_input)
        real_time_data = f"Live insurance data:\n{live_data}\n" if live_data else "Live data not available.\n"

    # Step 7: Generate LLM prompt and chatbot response
    prompt = f"""
You are a helpful and empathetic life insurance advisor bot.

User's latest query:
{user_input}

Relevant past memories:
{memory_context}

User profile insights:
{user_profile}

Top recommended policies:
{top_policies_text}

{real_time_data}

Based on the above, answer clearly and kindly to assist the user's insurance decisions.
"""

    response = generate_chat_response(prompt)
    return response

def build_user_profile(user_id: str, memories: list) -> dict:
    """
    Derive a basic user profile from memory context or other metadata (simple placeholder logic).
    """
    # In practice, use NLP on memories to extract fields like age, income, family size, etc.
    return {
        "user_id": user_id,
        "income": 40000,  # placeholder
        "family_size": 3,  # placeholder
        "preferences": memories[:2] if memories else [],
    }
