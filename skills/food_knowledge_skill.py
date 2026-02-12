"""Food Knowledge Skill - Provides information about Malaysian dishes from MongoDB."""

import json
from typing import Any, Dict, List
from strands import tool
from services.mongodb import MongoDBFoodKnowledgeService


class FoodKnowledgeSkill:
    """Skill for Malaysian food knowledge using MongoDB vector search."""

    def __init__(self, mongo_service: MongoDBFoodKnowledgeService):
        """
        Initialize food knowledge skill.

        Args:
            mongo_service: MongoDB service for food knowledge
        """
        self.mongo_service = mongo_service

    @tool
    def search_dishes(
        self,
        query: str,
        cuisine_type: str | None = None,
        category: str | None = None,
        halal: bool | None = None,
        vegetarian: bool | None = None,
        limit: int = 5
    ) -> str:
        """
        Search for Malaysian dishes and food information.

        Use this tool to find information about Malaysian dishes, ingredients,
        cooking methods, cultural significance, and taste profiles.

        Args:
            query: Natural language query about Malaysian food (e.g., "spicy coconut milk dishes", "breakfast foods")
            cuisine_type: Filter by cuisine (Malay, Chinese Malaysian, Indian Malaysian, Nyonya, Mamak)
            category: Filter by category (Main course, Dessert, Beverage, Snack)
            halal: Filter by halal status (True/False/None)
            vegetarian: Filter by vegetarian status (True/False/None)
            limit: Maximum number of results (default 5)

        Returns:
            JSON string with dish information including ingredients, cooking methods, taste profiles, cultural significance
        """
        filters = {}
        if cuisine_type:
            filters["cuisine_type"] = cuisine_type
        if category:
            filters["category"] = category
        if halal is not None:
            filters["halal"] = halal
        if vegetarian is not None:
            filters["vegetarian"] = vegetarian

        results = self.mongo_service.vector_search(query, limit, filters)

        # Format results for the agent
        formatted_results = []
        for r in results:
            formatted_results.append({
                "name": r["name"],
                "cuisine_type": r["cuisine_type"],
                "category": r["category"],
                "description": r["description"],
                "ingredients": r["ingredients"],
                "cooking_method": r.get("cooking_method"),
                "taste_profile": r["taste_profile"],
                "dietary_info": r["dietary_info"],
                "cultural_significance": r.get("cultural_significance"),
                "typical_meal_time": r["typical_meal_time"],
                "regional_origin": r.get("regional_origin"),
                "common_pairings": r["common_pairings"],
                "relevance_score": r.get("score", 0),
            })

        return json.dumps(formatted_results, indent=2)

    @tool
    def get_dish_ingredients(self, dish_name: str) -> str:
        """
        Get ingredients for a specific Malaysian dish.

        Args:
            dish_name: Name of the dish (e.g., "Nasi Lemak", "Rendang")

        Returns:
            JSON string with detailed ingredient list and cooking method
        """
        results = self.mongo_service.vector_search(dish_name, limit=1)

        if not results:
            return json.dumps({"error": f"No information found for {dish_name}"})

        dish = results[0]
        return json.dumps({
            "name": dish["name"],
            "ingredients": dish["ingredients"],
            "cooking_method": dish.get("cooking_method", "Not specified")
        }, indent=2)

    @tool
    def get_dietary_info(self, dish_name: str) -> str:
        """
        Get dietary information for a Malaysian dish.

        Args:
            dish_name: Name of the dish

        Returns:
            JSON string with dietary information (halal, vegetarian, vegan, gluten-free)
        """
        results = self.mongo_service.vector_search(dish_name, limit=1)

        if not results:
            return json.dumps({"error": f"No information found for {dish_name}"})

        dish = results[0]
        return json.dumps({
            "name": dish["name"],
            "dietary_info": dish["dietary_info"],
            "ingredients": dish["ingredients"]
        }, indent=2)

    @tool
    def explore_cuisine_type(self, cuisine_type: str) -> str:
        """
        Explore dishes from a specific Malaysian cuisine type.

        Args:
            cuisine_type: Type of cuisine (Malay, Chinese Malaysian, Indian Malaysian, Nyonya, Mamak)

        Returns:
            JSON string with dishes from that cuisine type
        """
        results = self.mongo_service.vector_search(
            cuisine_type,
            limit=10,
            filters={"cuisine_type": cuisine_type}
        )

        formatted_results = []
        for r in results:
            formatted_results.append({
                "name": r["name"],
                "description": r["description"],
                "category": r["category"],
                "typical_meal_time": r["typical_meal_time"]
            })

        return json.dumps(formatted_results, indent=2)
