"""MongoDB vector search service for Malaysian food knowledge."""

from typing import List, Optional, Dict, Any
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from pydantic import BaseModel
from services.bedrock import BedrockService


class MalaysianDish(BaseModel):
    """Malaysian dish/food model."""
    name: str
    cuisine_type: str  # Malay, Chinese Malaysian, Indian Malaysian, Nyonya, Mamak
    category: str  # Main course, Dessert, Beverage, Snack, Condiment
    description: str
    ingredients: List[str]
    cooking_method: Optional[str] = None
    taste_profile: List[str]  # Sweet, Spicy, Savory, Sour, Umami
    dietary_info: Dict[str, bool]  # halal, vegetarian, vegan, gluten_free
    cultural_significance: Optional[str] = None
    typical_meal_time: List[str]  # Breakfast, Lunch, Dinner, Snack, Anytime
    regional_origin: Optional[str] = None  # Which state/region it's from
    common_pairings: List[str]  # What it's usually served with
    embedding: Optional[List[float]] = None


class MongoDBFoodKnowledgeService:
    """Service for MongoDB vector search operations on food knowledge."""

    def __init__(
        self,
        uri: str,
        database: str,
        collection: str,
        bedrock_service: BedrockService,
    ):
        """
        Initialize MongoDB food knowledge service.

        Args:
            uri: MongoDB connection URI
            database: Database name
            collection: Collection name (e.g., 'dishes')
            bedrock_service: BedrockService instance for embeddings
        """
        self.client: Optional[MongoClient] = None
        self.db: Optional[Database] = None
        self.collection: Optional[Collection] = None
        self.uri = uri
        self.database_name = database
        self.collection_name = collection
        self.bedrock_service = bedrock_service

    def connect(self) -> None:
        """Connect to MongoDB."""
        self.client = MongoClient(self.uri)
        self.db = self.client[self.database_name]
        self.collection = self.db[self.collection_name]
        print("Connected to MongoDB")

    def disconnect(self) -> None:
        """Disconnect from MongoDB."""
        if self.client:
            self.client.close()
            print("Disconnected from MongoDB")

    def create_vector_search_index(self) -> None:
        """Create vector search index programmatically."""
        try:
            index_definition = {
                "name": "food_vector_index",
                "type": "vectorSearch",
                "definition": {
                    "fields": [
                        {
                            "type": "vector",
                            "path": "embedding",
                            "numDimensions": 1024,
                            "similarity": "cosine"
                        },
                        {
                            "type": "filter",
                            "path": "cuisine_type"
                        },
                        {
                            "type": "filter",
                            "path": "category"
                        },
                        {
                            "type": "filter",
                            "path": "dietary_info.halal"
                        },
                        {
                            "type": "filter",
                            "path": "dietary_info.vegetarian"
                        }
                    ]
                }
            }

            # Create the search index using createSearchIndexes command
            result = self.collection.create_search_index(index_definition)
            print(f"✓ Vector search index created successfully: {result}")
            print(f"  Index name: food_vector_index")
            print(f"  Note: Index may take a few minutes to become active")

        except Exception as e:
            error_msg = str(e)
            if "already exists" in error_msg.lower():
                print("✓ Vector search index 'food_vector_index' already exists")
            else:
                print(f"Error creating vector search index: {e}")
                print("\nNote: If using MongoDB Atlas, the index creation may require:")
                print("1. Atlas M10+ cluster (M0/M2/M5 free tiers don't support search indexes)")
                print("2. Or manual creation via Atlas UI")
                self.create_vector_search_index_info()

    def create_vector_search_index_info(self) -> None:
        """Display instructions for creating vector search index in Atlas."""
        index_definition = """
        ================================================================================
        IMPORTANT: Vector Search Index Setup
        ================================================================================

        You need to create a Vector Search index in MongoDB Atlas:

        Index Name: food_vector_index

        Index Definition (JSON):
        {
          "fields": [
            {
              "type": "vector",
              "path": "embedding",
              "numDimensions": 1024,
              "similarity": "cosine"
            },
            {
              "type": "filter",
              "path": "cuisine_type"
            },
            {
              "type": "filter",
              "path": "category"
            },
            {
              "type": "filter",
              "path": "dietary_info.halal"
            },
            {
              "type": "filter",
              "path": "dietary_info.vegetarian"
            }
          ]
        }

        Steps:
        1. Go to MongoDB Atlas UI
        2. Navigate to your cluster
        3. Click "Atlas Search" tab
        4. Click "Create Search Index"
        5. Choose "JSON Editor"
        6. Select database: {database}
        7. Select collection: {collection}
        8. Paste the above JSON
        9. Name it: food_vector_index
        10. Click "Create Search Index"

        ================================================================================
        """.format(database=self.database_name, collection=self.collection_name)

        print(index_definition)

    def insert_dish(self, dish_data: Dict[str, Any]) -> None:
        """
        Insert a Malaysian dish with embedding.

        Args:
            dish_data: Dish data dictionary
        """
        try:
            # Create text representation for embedding
            text_for_embedding = self._create_text_representation(dish_data)

            # Generate embedding
            embedding = self.bedrock_service.generate_embedding(text_for_embedding)

            # Add embedding to dish data
            dish_data["embedding"] = embedding

            # Insert into MongoDB
            self.collection.insert_one(dish_data)
            print(f"Inserted dish: {dish_data['name']}")

        except Exception as e:
            print(f"Error inserting dish: {e}")
            raise

    def insert_dishes(self, dishes: List[Dict[str, Any]]) -> None:
        """
        Insert multiple Malaysian dishes with embeddings.

        Args:
            dishes: List of dish data dictionaries
        """
        for dish in dishes:
            self.insert_dish(dish)

    def vector_search(
        self,
        query: str,
        limit: int = 5,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Perform vector search for Malaysian dishes/food.

        Args:
            query: Search query
            limit: Maximum number of results
            filters: Optional filters (cuisine_type, category, dietary restrictions)

        Returns:
            List of matching dishes
        """
        try:
            # Generate embedding for query
            query_embedding = self.bedrock_service.generate_embedding(query)

            # Build filter conditions
            filter_conditions = []
            if filters:
                if "cuisine_type" in filters and filters["cuisine_type"]:
                    filter_conditions.append({"cuisine_type": {"$eq": filters["cuisine_type"]}})
                if "category" in filters and filters["category"]:
                    filter_conditions.append({"category": {"$eq": filters["category"]}})
                if "halal" in filters and filters["halal"] is not None:
                    filter_conditions.append({"dietary_info.halal": {"$eq": filters["halal"]}})
                if "vegetarian" in filters and filters["vegetarian"] is not None:
                    filter_conditions.append({"dietary_info.vegetarian": {"$eq": filters["vegetarian"]}})

            # Build aggregation pipeline
            pipeline = [
                {
                    "$vectorSearch": {
                        "index": "food_vector_index",
                        "path": "embedding",
                        "queryVector": query_embedding,
                        "numCandidates": limit * 10,
                        "limit": limit,
                    }
                },
                {
                    "$project": {
                        "_id": 1,
                        "name": 1,
                        "cuisine_type": 1,
                        "category": 1,
                        "description": 1,
                        "ingredients": 1,
                        "cooking_method": 1,
                        "taste_profile": 1,
                        "dietary_info": 1,
                        "cultural_significance": 1,
                        "typical_meal_time": 1,
                        "regional_origin": 1,
                        "common_pairings": 1,
                        "score": {"$meta": "vectorSearchScore"},
                    }
                },
            ]

            # Add filter if conditions exist
            if filter_conditions:
                pipeline[0]["$vectorSearch"]["filter"] = {"$and": filter_conditions}

            results = list(self.collection.aggregate(pipeline))
            return results

        except Exception as e:
            print(f"Error performing vector search: {e}")
            raise

    def get_all_dishes(self) -> List[Dict[str, Any]]:
        """Get all dishes (for testing)."""
        return list(self.collection.find({}, {"embedding": 0}))

    def clear_all_dishes(self) -> None:
        """Clear all dishes (for testing)."""
        self.collection.delete_many({})
        print("Cleared all dishes")

    def _create_text_representation(self, dish: Dict[str, Any]) -> str:
        """
        Create text representation of dish for embedding.

        Args:
            dish: Dish data

        Returns:
            Text representation
        """
        dietary_info = []
        if dish['dietary_info'].get('halal'):
            dietary_info.append('Halal')
        if dish['dietary_info'].get('vegetarian'):
            dietary_info.append('Vegetarian')
        if dish['dietary_info'].get('vegan'):
            dietary_info.append('Vegan')

        return f"""
Malaysian Dish: {dish['name']}
Cuisine Type: {dish['cuisine_type']}
Category: {dish['category']}
Description: {dish['description']}
Ingredients: {', '.join(dish['ingredients'])}
Cooking Method: {dish.get('cooking_method', 'Not specified')}
Taste Profile: {', '.join(dish['taste_profile'])}
Dietary: {', '.join(dietary_info) if dietary_info else 'None specified'}
Cultural Significance: {dish.get('cultural_significance', 'N/A')}
Typical Meal Time: {', '.join(dish['typical_meal_time'])}
Regional Origin: {dish.get('regional_origin', 'Various regions')}
Common Pairings: {', '.join(dish['common_pairings'])}
        """.strip()
