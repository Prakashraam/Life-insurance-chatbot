import os
import hashlib
import time
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer

# Initialize Pinecone and embedding model
PINECONE_API_KEY = "pcsk_8uT6V_HWJ9MKoCXKVJHStMNhpFLGH6WhyTcCQTQG1QPZhLNm8ChXPGoVjHiUQ7zUvFc3u"
INDEX_NAME = "user-memory"
VECTOR_DIMENSION = 384  # Match this with the dimension of the model
CLOUD = "aws"
REGION = "us-east-1"

# --- Initialize Pinecone client ---
pc = Pinecone(api_key=PINECONE_API_KEY)

# Check if index exists, if not, create it
if INDEX_NAME not in pc.list_indexes().names():
    try:
        pc.create_index(
            name=INDEX_NAME,
            dimension=VECTOR_DIMENSION,
            metric="cosine",
            spec=ServerlessSpec(cloud=CLOUD, region=REGION)
        )
        print(f"[memory_manager] Index '{INDEX_NAME}' created successfully.")
    except Exception as e:
        print(f"[memory_manager] Failed to create index: {e}")

index = pc.Index(INDEX_NAME)

# --- Load embedding model ---
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# --- Save memory chunk for user-specific memory ---
def save_user_memory(user_id: str, text: str, metadata: dict = {}):
    try:
        # Add timestamp for memory decay/aging
        timestamp = int(time.time())
        
        # Generate the embedding for the memory
        vector = embedder.encode(text).tolist()
        
        # Unique ID based on user_id and text hash
        unique_id = f"{user_id}-{hashlib.md5(text.encode()).hexdigest()}"
        
        # Prepare memory data with metadata
        memory_data = {
            "id": unique_id,
            "values": vector,
            "metadata": {
                "user_id": user_id,
                "text": text,
                "timestamp": timestamp,  # New field for memory decay
                **metadata
            }
        }

        # Upsert memory to Pinecone index
        index.upsert(vectors=[memory_data])
        print(f"[memory] Saved memory for user '{user_id}'")
    except Exception as e:
        print(f"[save_user_memory] Error: {e}")

# --- Retrieve top-k relevant memories based on user context ---
def fetch_user_memory(user_id: str, query: str, top_k: int = 5, min_score: float = 0.75):
    try:
        # Get recent chat context (this could be the last N chat messages or recent memory)
        context = get_recent_user_messages(user_id)  # Replace with actual method to get context
        query_vector = embedder.encode(f"{context} {query}").tolist()

        # Perform semantic search using Pinecone
        response = index.query(
            vector=query_vector,
            top_k=top_k,
            include_metadata=True,
            filter={"user_id": user_id}
        )

        # Extract and filter matches based on a minimum score threshold
        matches = response.get("matches", [])
        filtered_matches = [match["metadata"]["text"] for match in matches if match["score"] >= min_score]
        
        # Return relevant memories
        return filtered_matches
    except Exception as e:
        print(f"[fetch_user_memory] Error: {e}")
        return []

# --- Fetch recent user messages (for context) ---
def get_recent_user_messages(user_id: str, num_messages: int = 3):
    # Simulate fetching recent messages from a database or memory
    # Example return format: ["Message 1", "Message 2", "Message 3"]
    # Replace this with an actual implementation of fetching recent user messages
    return ["Example message 1", "Example message 2", "Example message 3"]

# --- Memory decay: remove outdated memories based on user ---
def remove_old_memories(user_id: str, max_age_in_days: int = 30):
    try:
        current_time = int(time.time())
        cutoff_time = current_time - (max_age_in_days * 86400)  # Convert days to seconds

        # Query to find memories older than the cutoff
        response = index.query(
            vector=[0] * VECTOR_DIMENSION,  # Dummy vector as we only care about metadata
            top_k=1000,  # Limit the query to a reasonable number of results
            include_metadata=True,
            filter={"user_id": user_id}
        )

        # Find memories to remove based on timestamp
        memories_to_remove = [
            match["id"] for match in response["matches"] if match["metadata"]["timestamp"] < cutoff_time
        ]

        # Delete old memories
        if memories_to_remove:
            index.delete(ids=memories_to_remove)
            print(f"[memory_manager] Removed {len(memories_to_remove)} outdated memories for user '{user_id}'")
        else:
            print(f"[memory_manager] No outdated memories to remove for user '{user_id}'")
    except Exception as e:
        print(f"[remove_old_memories] Error: {e}")

