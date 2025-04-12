from pinecone import Pinecone, ServerlessSpec

# Initialize Pinecone client with your API key directly
pc = Pinecone(
    api_key="pcsk_8uT6V_HWJ9MKoCXKVJHStMNhpFLGH6WhyTcCQTQG1QPZhLNm8ChXPGoVjHiUQ7zUvFc3u"  # Replace this with your actual Pinecone API key
)

# Optionally, you can list available indexes
print("Available indexes:", pc.list_indexes().names())

# Define the index name and ensure it follows Pinecone's naming rules
index_name = "user-memory"

# Fetch the index from Pinecone
index = pc.Index(index_name)

# Function to fetch data for a user by metadata filter (user_id)
def fetch_user_data(user_id: str):
    try:
        # Query the index for the user_id in metadata, with empty vector and metadata filtering
        results = index.query(
            vector=[]*768,  # Empty vector, we're using metadata filter
            top_k=5,  # Get top 5 results (adjust as necessary)
            filter={"user_id": user_id},  # Filter by the user_id in metadata
            include_metadata=True  # Ensure metadata is included in the result
        )

        if results['matches']:
            print("Saved memory for user:")
            for match in results['matches']:
                print(match['metadata'])  # This will print the stored memory
            return results['matches']
        else:
            print("No data found for this user.")
            return []

    except Exception as e:
        print(f"Error fetching user data: {e}")
        return []

# Test the function by fetching data for a specific user
user_data = fetch_user_data("34")
