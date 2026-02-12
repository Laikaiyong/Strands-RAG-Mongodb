"""Malaysian Food Agent using Strands framework with dual skills."""

import asyncio
from typing import List, Dict, Union
from strands import Agent
from strands.models import BedrockModel
from skills.food_knowledge_skill import FoodKnowledgeSkill
from skills.restaurant_finder_skill import RestaurantFinderSkill
from services.mongodb import MongoDBFoodKnowledgeService


class MalaysianFoodAgent:
    """
    Malaysian Food Agent with two specialized skills:
    1. Food Knowledge Skill - Information about dishes from MongoDB
    2. Restaurant Finder Skill - Finding restaurant locations via Strands built-in tools
    """

    def __init__(
        self,
        mongo_service: MongoDBFoodKnowledgeService,
        model: Union[BedrockModel, str] = None
    ):
        """
        Initialize Malaysian Food Agent.

        Args:
            mongo_service: MongoDB service for food knowledge
            model: BedrockModel instance or model string (BedrockModel recommended)
        """
        self.mongo_service = mongo_service

        # Initialize skills
        self.food_knowledge_skill = FoodKnowledgeSkill(mongo_service)
        self.restaurant_finder_skill = RestaurantFinderSkill()

        # Collect all skill methods
        skills = []
        skills.extend([
            self.food_knowledge_skill.search_dishes,
            self.food_knowledge_skill.get_dish_ingredients,
            self.food_knowledge_skill.get_dietary_info,
            self.food_knowledge_skill.explore_cuisine_type,
        ])
        skills.extend([
            self.restaurant_finder_skill.find_restaurants,
            self.restaurant_finder_skill.find_halal_restaurants,
            self.restaurant_finder_skill.find_restaurants_by_cuisine,
            self.restaurant_finder_skill.get_restaurant_reviews,
            self.restaurant_finder_skill.find_best_area_for_food,
            self.restaurant_finder_skill.search_food_blogs,
            self.restaurant_finder_skill.extract_restaurant_details,
            self.restaurant_finder_skill.crawl_restaurant_website,
            self.restaurant_finder_skill.map_restaurant_website,
        ])

        # Create Strands agent
        self.agent = Agent(
            name="Malaysian Food Expert",
            model=model,
            system_prompt=self._get_system_instructions(),
            tools=skills
        )

        self.conversation_history: List[Dict[str, str]] = []

    def initialize(self) -> None:
        """Initialize all services."""
        self.mongo_service.connect()
        print("Malaysian Food Agent initialized with dual skills:")
        print("  - Food Knowledge Skill (MongoDB vector search)")
        print("  - Restaurant Finder Skill (Tavily web search, extract, crawl, map)")

    def shutdown(self) -> None:
        """Shutdown all services."""
        self.mongo_service.disconnect()
        print("Malaysian Food Agent shutdown")

    def _get_system_instructions(self) -> str:
        """Get system instructions for the agent."""
        return """You are a Malaysian food expert with two specialized capabilities:

1. **Food Knowledge**: You have deep knowledge about Malaysian dishes stored in a database including:
   - Detailed ingredient lists and cooking methods
   - Cultural significance and history
   - Taste profiles and dietary information
   - Regional origins and traditional pairings
   - Cuisine types: Malay, Chinese Malaysian, Indian Malaysian, Nyonya/Peranakan, Mamak

2. **Restaurant Finder**: You can search the web using Tavily tools to find actual restaurants including:
   - Current restaurant locations and contact information
   - Reviews and ratings from food blogs and review sites
   - Best areas and neighborhoods for specific cuisines
   - Halal restaurant options

**Your Role**:
- Help users discover Malaysian dishes and understand their cultural context
- Find restaurants where users can try specific dishes
- Recommend dishes based on preferences (taste, dietary needs, meal time)
- Explain the significance of Malaysian food culture
- Guide users to authentic food experiences across Malaysia

**How to Help Users**:
1. When users ask about a DISH (what it is, ingredients, how it's made):
   - Use Food Knowledge skill to search dishes and provide detailed information
   - Explain cultural significance and typical pairings
   - Suggest similar dishes they might enjoy

2. When users ask WHERE to find food or restaurant locations:
   - Use Restaurant Finder skill to search for actual restaurants
   - Provide specific locations, areas, and current information
   - Suggest best neighborhoods or areas for specific cuisines

3. When users need both:
   - First explain the dish using Food Knowledge
   - Then find restaurants using Restaurant Finder
   - Provide a complete recommendation with context and locations

**Malaysian Cuisine Types**:
- Malay: Nasi lemak, rendang, satay
- Chinese Malaysian: Char koay teow, hokkien mee, bak kut teh
- Indian Malaysian: Roti canai, banana leaf rice
- Nyonya/Peranakan: Laksa, ayam pongteh
- Mamak: Nasi kandar, teh tarik

Be enthusiastic, knowledgeable, and helpful. Celebrate Malaysian food culture!"""

    async def query_async(self, user_query: str, verbose: bool = True) -> str:
        """
        Process a user query about Malaysian food (async version).

        Args:
            user_query: User's question or request
            verbose: Show thinking process and tool calls

        Returns:
            Agent's response
        """
        try:
            self.conversation_history.append({
                "role": "user",
                "content": user_query
            })

            # Use Strands agent to process query with both skills
            response = await self.agent.invoke_async(user_query)

            # Show thinking process if verbose
            if verbose:
                # The response from Strands contains thinking blocks and tool calls
                # Let's print them if available
                if hasattr(response, 'messages'):
                    for msg in response.messages:
                        if hasattr(msg, 'type'):
                            if msg.type == 'thinking':
                                print(f"\033[93m💭 Thinking: {msg.content}\033[0m")
                            elif msg.type == 'tool_use':
                                print(f"\033[96m🔧 Tool Call: \033[1m{msg.name}\033[0m")
                                if hasattr(msg, 'input') and msg.input:
                                    import json
                                    print(f"\033[96m   Parameters: {json.dumps(msg.input, indent=2)}\033[0m")

            # Extract response text
            response_text = str(response.content) if hasattr(response, 'content') else str(response)

            self.conversation_history.append({
                "role": "assistant",
                "content": response_text
            })

            return response_text

        except Exception as e:
            print(f"\033[91mError processing query: {e}\033[0m")
            import traceback
            traceback.print_exc()
            return f"I apologize, but I encountered an error: {str(e)}. Please try again."

    def query(self, user_query: str, verbose: bool = False) -> str:
        """
        Synchronous wrapper for query_async.

        Args:
            user_query: User's question or request
            verbose: Show thinking process and tool calls

        Returns:
            Agent's response
        """
        return asyncio.run(self.query_async(user_query, verbose))

    def clear_history(self) -> None:
        """Clear conversation history."""
        self.conversation_history = []

    def get_history(self) -> List[Dict[str, str]]:
        """Get conversation history."""
        return self.conversation_history.copy()
