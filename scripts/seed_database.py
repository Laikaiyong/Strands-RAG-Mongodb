"""Script to seed MongoDB with Malaysian dishes knowledge."""

import os
from dotenv import load_dotenv
from services.bedrock import BedrockService
from services.mongodb import MongoDBFoodKnowledgeService
from data.malaysian_dishes import MALAYSIAN_DISHES

# Load environment variables
load_dotenv(override=True)


def main():
    """Seed MongoDB with Malaysian dishes knowledge."""
    print("🍜 Starting database seeding process...\n")

    # Initialize Bedrock service
    bedrock_service = BedrockService(
        region=os.getenv("AWS_REGION", "us-east-1"),
        embedding_model=os.getenv("BEDROCK_EMBEDDING_MODEL", "amazon.titan-embed-text-v2:0"),
        inference_model=os.getenv("BEDROCK_INFERENCE_MODEL", "amazon.nova-pro-v1:0"),
        access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    # Initialize MongoDB service
    mongo_service = MongoDBFoodKnowledgeService(
        uri=os.getenv("MONGODB_URI", "mongodb://localhost:27017"),
        database=os.getenv("MONGODB_DATABASE", "food_places_db"),
        collection=os.getenv("MONGODB_COLLECTION", "dishes"),
        bedrock_service=bedrock_service,
    )

    try:
        # Connect to MongoDB
        mongo_service.connect()

        # Clear existing data (optional)
        print("Clearing existing dishes...")
        mongo_service.clear_all_dishes()

        # Insert dishes with embeddings
        print(f"\nInserting {len(MALAYSIAN_DISHES)} Malaysian dishes...\n")
        mongo_service.insert_dishes(MALAYSIAN_DISHES)

        print("\n✓ Database seeded successfully!")
        print(f"\nTotal dishes inserted: {len(MALAYSIAN_DISHES)}")

        # Display summary
        cuisine_types = list(set(d["cuisine_type"] for d in MALAYSIAN_DISHES))
        categories = list(set(d["category"] for d in MALAYSIAN_DISHES))

        print(f"\nCuisine types: {', '.join(cuisine_types)}")
        print(f"Categories: {', '.join(categories)}")

        # Create vector search index programmatically
        print("\n" + "=" * 80)
        print("Creating Vector Search Index...")
        print("=" * 80)
        mongo_service.create_vector_search_index()
        print("=" * 80)

    except Exception as e:
        print(f"Error seeding database: {e}")
        return 1
    finally:
        mongo_service.disconnect()

    return 0


if __name__ == "__main__":
    exit(main())
