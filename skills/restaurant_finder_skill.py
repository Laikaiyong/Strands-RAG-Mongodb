"""Restaurant Finder Skill - Finds restaurant locations using Tavily tools."""

from strands import tool
from strands_tools.tavily import tavily_search, tavily_extract, tavily_crawl, tavily_map


class RestaurantFinderSkill:
    """
    Skill for finding restaurant locations using Tavily tools.

    Tavily Tools:
    - tavily_search: Real-time web search optimized for AI agents
    - tavily_extract: Extract clean content from restaurant web pages
    - tavily_crawl: Crawl restaurant websites for detailed information
    - tavily_map: Map website structure to discover all pages
    """

    def __init__(self):
        """Initialize restaurant finder skill."""
        pass

    @tool
    async def find_restaurants(
        self,
        dish_name: str,
        location: str,
        additional_criteria: str | None = None
    ) -> str:
        """
        Find restaurants serving a specific Malaysian dish in a location.

        This tool searches the web for current restaurant information including
        names, locations, reviews, and contact details.

        Args:
            dish_name: Name of Malaysian dish (e.g., "Nasi Lemak", "Char Koay Teow")
            location: Location in Malaysia (city, state, area - e.g., "Kuala Lumpur", "Georgetown Penang")
            additional_criteria: Additional requirements (e.g., "halal", "best rated", "affordable")

        Returns:
            Search results with restaurant information
        """
        query = f"best {dish_name} restaurants in {location} Malaysia"
        if additional_criteria:
            query += f" {additional_criteria}"

        return await tavily_search(
            query=query,
            search_depth="advanced",
            max_results=8,
            topic="general"
        )

    @tool
    async def find_halal_restaurants(self, dish_name: str, location: str) -> str:
        """
        Find halal restaurants serving a specific dish.

        Args:
            dish_name: Name of the dish
            location: Location in Malaysia

        Returns:
            Search results for halal restaurants
        """
        query = f"halal {dish_name} restaurants in {location} Malaysia"

        return await tavily_search(
            query=query,
            search_depth="advanced",
            max_results=8,
            topic="general"
        )

    @tool
    async def find_restaurants_by_cuisine(self, cuisine_type: str, location: str) -> str:
        """
        Find restaurants by Malaysian cuisine type in a location.

        Args:
            cuisine_type: Type of Malaysian cuisine (Malay, Chinese Malaysian, Indian Malaysian, Nyonya, Mamak)
            location: Location in Malaysia

        Returns:
            Search results for restaurants
        """
        query = f"best authentic {cuisine_type} restaurants in {location} Malaysia"

        return await tavily_search(
            query=query,
            search_depth="advanced",
            max_results=8,
            topic="general"
        )

    @tool
    async def get_restaurant_reviews(
        self,
        restaurant_name: str,
        location: str | None = None
    ) -> str:
        """
        Get reviews and current information about a specific restaurant.

        Args:
            restaurant_name: Name of the restaurant
            location: Optional location to narrow down search

        Returns:
            Search results with reviews and restaurant information
        """
        query = f"{restaurant_name} restaurant reviews"
        if location:
            query += f" {location}"
        query += " Malaysia"

        return await tavily_search(
            query=query,
            search_depth="advanced",
            max_results=5,
            topic="general"
        )

    @tool
    async def find_best_area_for_food(self, dish_or_cuisine: str, city: str) -> str:
        """
        Find the best areas/neighborhoods in a city for specific food or cuisine.

        Args:
            dish_or_cuisine: Dish name or cuisine type
            city: City in Malaysia (e.g., "Kuala Lumpur", "Penang")

        Returns:
            Information about best food areas and neighborhoods
        """
        query = f"best neighborhoods and areas for {dish_or_cuisine} in {city} Malaysia food guide"

        return await tavily_search(
            query=query,
            search_depth="advanced",
            max_results=6,
            topic="general"
        )

    @tool
    async def search_food_blogs(self, dish_name: str, location: str) -> str:
        """
        Search Malaysian food blogs and review sites for recommendations.

        Args:
            dish_name: Name of the dish
            location: Location in Malaysia

        Returns:
            Blog posts and articles about the dish
        """
        query = f"{dish_name} {location} Malaysia food blog review"

        return await tavily_search(
            query=query,
            search_depth="advanced",
            max_results=5,
            topic="general"
        )

    @tool
    async def extract_restaurant_details(self, urls: list[str]) -> str:
        """
        Extract detailed information from restaurant websites or review pages.

        Use this to get clean, structured content from specific restaurant URLs,
        including menus, hours, locations, and reviews.

        Args:
            urls: List of restaurant URLs to extract content from

        Returns:
            Extracted content from the URLs
        """
        return await tavily_extract(
            urls=urls,
            extract_depth="advanced"
        )

    @tool
    async def crawl_restaurant_website(
        self,
        url: str,
        max_depth: int = 2,
        instructions: str | None = None
    ) -> str:
        """
        Crawl a restaurant website to find specific information like menus, locations, or contact details.

        Args:
            url: Base URL of the restaurant website
            max_depth: How many levels deep to crawl (default: 2)
            instructions: Optional instructions for what to find (e.g., "Find menu and prices")

        Returns:
            Crawled content from the website
        """
        return await tavily_crawl(
            url=url,
            max_depth=max_depth,
            instructions=instructions or "Find restaurant information, menu, location, and contact details"
        )

    @tool
    async def map_restaurant_website(
        self,
        url: str,
        max_depth: int = 2
    ) -> str:
        """
        Map out the structure of a restaurant website to discover all available pages.

        Args:
            url: Base URL of the restaurant website
            max_depth: How many levels deep to map (default: 2)

        Returns:
            List of discovered URLs on the website
        """
        return await tavily_map(
            url=url,
            max_depth=max_depth,
            instructions="Discover all pages on this restaurant website"
        )
