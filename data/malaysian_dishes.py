"""Malaysian dishes and food knowledge database."""

MALAYSIAN_DISHES = [
    # Malay Cuisine
    {
        "name": "Nasi Lemak",
        "cuisine_type": "Malay",
        "category": "Main course",
        "description": "Fragrant rice cooked in coconut milk and pandan leaf, Malaysia's national dish. Traditionally served with sambal, fried anchovies (ikan bilis), peanuts, boiled egg, and cucumber.",
        "ingredients": ["Rice", "Coconut milk", "Pandan leaves", "Sambal", "Ikan bilis", "Peanuts", "Eggs", "Cucumber"],
        "cooking_method": "Rice is cooked with coconut milk and pandan leaves. Served with various accompaniments including spicy sambal, crispy fried anchovies, roasted peanuts, hard-boiled egg, and fresh cucumber slices.",
        "taste_profile": ["Savory", "Spicy", "Umami"],
        "dietary_info": {"halal": True, "vegetarian": False, "vegan": False, "gluten_free": True},
        "cultural_significance": "Malaysia's unofficial national dish, eaten at any time of day. Represents the multicultural nature of Malaysian cuisine with Malay, Chinese, and Indian influences.",
        "typical_meal_time": ["Breakfast", "Lunch", "Dinner", "Anytime"],
        "regional_origin": "Nationwide, originated from Malay communities",
        "common_pairings": ["Fried chicken", "Rendang", "Sambal sotong", "Curry"]
    },
    {
        "name": "Rendang",
        "cuisine_type": "Malay",
        "category": "Main course",
        "description": "Slow-cooked dry curry with beef or chicken, coconut milk, and a complex spice paste. Rich, tender, and intensely flavorful.",
        "ingredients": ["Beef or chicken", "Coconut milk", "Galangal", "Lemongrass", "Turmeric", "Ginger", "Garlic", "Shallots", "Chilies", "Tamarind"],
        "cooking_method": "Meat is slow-cooked for hours in coconut milk with a rich spice paste until the liquid reduces and the meat becomes tender and caramelized.",
        "taste_profile": ["Savory", "Spicy", "Umami", "Sweet"],
        "dietary_info": {"halal": True, "vegetarian": False, "vegan": False, "gluten_free": True},
        "cultural_significance": "Ceremonial dish from Minangkabau culture, often served during Eid and weddings. CNN named it the world's most delicious food.",
        "typical_meal_time": ["Lunch", "Dinner"],
        "regional_origin": "Originally from Sumatra, adopted throughout Malaysia",
        "common_pairings": ["Nasi lemak", "Ketupat", "Lemang", "Steamed rice"]
    },
    {
        "name": "Satay",
        "cuisine_type": "Malay",
        "category": "Main course",
        "description": "Skewered and grilled marinated meat (chicken, beef, or lamb) served with peanut sauce, cucumber, onions, and rice cakes.",
        "ingredients": ["Chicken/beef/lamb", "Turmeric", "Lemongrass", "Garlic", "Peanut sauce", "Cucumber", "Onions", "Rice cakes (ketupat)"],
        "cooking_method": "Meat is marinated in turmeric and spices, threaded onto bamboo skewers, and grilled over charcoal fire. Served with thick peanut sauce.",
        "taste_profile": ["Savory", "Sweet", "Umami"],
        "dietary_info": {"halal": True, "vegetarian": False, "vegan": False, "gluten_free": False},
        "cultural_significance": "Popular street food and party dish, brought by Javanese immigrants. Social eating experience.",
        "typical_meal_time": ["Lunch", "Dinner", "Snack"],
        "regional_origin": "Kajang is famous for satay",
        "common_pairings": ["Peanut sauce", "Cucumber", "Onions", "Nasi impit"]
    },

    # Chinese Malaysian Cuisine
    {
        "name": "Char Koay Teow",
        "cuisine_type": "Chinese Malaysian",
        "category": "Main course",
        "description": "Stir-fried flat rice noodles with prawns, Chinese sausage, bean sprouts, and eggs, cooked over high heat with dark soy sauce.",
        "ingredients": ["Flat rice noodles", "Prawns", "Chinese sausage", "Bean sprouts", "Eggs", "Chinese chives", "Dark soy sauce", "Chili paste"],
        "cooking_method": "Noodles are stir-fried over extremely high heat (wok hei) with ingredients in stages, creating smoky charred flavor.",
        "taste_profile": ["Savory", "Umami", "Sweet"],
        "dietary_info": {"halal": False, "vegetarian": False, "vegan": False, "gluten_free": False},
        "cultural_significance": "Iconic Penang street food, represents Chinese Malaysian culinary heritage. Requires high skill to achieve perfect wok hei.",
        "typical_meal_time": ["Lunch", "Dinner"],
        "regional_origin": "Penang",
        "common_pairings": ["Lime juice", "Pickled green chilies"]
    },
    {
        "name": "Hokkien Mee",
        "cuisine_type": "Chinese Malaysian",
        "category": "Main course",
        "description": "Thick yellow noodles braised in dark soy sauce with pork, prawns, squid, and pork lard. Two versions: KL (dark) and Penang (spicy soup).",
        "ingredients": ["Yellow noodles", "Pork", "Prawns", "Squid", "Dark soy sauce", "Cabbage", "Pork lard", "Bean sprouts"],
        "cooking_method": "Noodles are stir-fried with meat and seafood, then braised in dark soy sauce until caramelized (KL style).",
        "taste_profile": ["Savory", "Umami", "Sweet"],
        "dietary_info": {"halal": False, "vegetarian": False, "vegan": False, "gluten_free": False},
        "cultural_significance": "Introduced by Hokkien Chinese immigrants, represents adaptation of Chinese cuisine to Malaysian tastes.",
        "typical_meal_time": ["Dinner"],
        "regional_origin": "Kuala Lumpur and Penang (different styles)",
        "common_pairings": ["Sambal", "Lime", "Green chilies"]
    },
    {
        "name": "Bak Kut Teh",
        "cuisine_type": "Chinese Malaysian",
        "category": "Main course",
        "description": "Herbal pork rib soup simmered with Chinese herbs and spices. Comfort food with medicinal properties.",
        "ingredients": ["Pork ribs", "Garlic", "Star anise", "Cinnamon", "Dong quai", "Chuanxiong", "Dang shen", "Dark soy sauce"],
        "cooking_method": "Pork ribs are simmered for hours with Chinese herbs and spices until tender and flavorful.",
        "taste_profile": ["Savory", "Umami"],
        "dietary_info": {"halal": False, "vegetarian": False, "vegan": False, "gluten_free": True},
        "cultural_significance": "Created by Hokkien immigrants as nutritious breakfast for laborers. Each family has secret herb recipe.",
        "typical_meal_time": ["Breakfast", "Lunch"],
        "regional_origin": "Klang Valley",
        "common_pairings": ["White rice", "You tiao (fried dough)", "Chinese tea"]
    },

    # Nyonya/Peranakan Cuisine
    {
        "name": "Laksa",
        "cuisine_type": "Nyonya",
        "category": "Main course",
        "description": "Spicy noodle soup with rich coconut curry broth, combining Chinese and Malay flavors. Multiple regional variations exist.",
        "ingredients": ["Rice noodles", "Coconut milk", "Laksa paste", "Prawns", "Fish cake", "Bean sprouts", "Eggs", "Laksa leaves"],
        "cooking_method": "Spice paste is cooked with coconut milk to create rich curry broth, served with noodles and toppings.",
        "taste_profile": ["Spicy", "Savory", "Umami"],
        "dietary_info": {"halal": False, "vegetarian": False, "vegan": False, "gluten_free": True},
        "cultural_significance": "Represents Peranakan culture fusion of Chinese and Malay. Each region (Penang, Sarawak, Johor) has distinct version.",
        "typical_meal_time": ["Lunch", "Dinner"],
        "regional_origin": "Penang, Sarawak, Johor (different styles)",
        "common_pairings": ["Sambal belacan", "Lime"]
    },
    {
        "name": "Ayam Pongteh",
        "cuisine_type": "Nyonya",
        "category": "Main course",
        "description": "Nyonya braised chicken with fermented soybean paste (tau cheo), potatoes in sweet-savory sauce.",
        "ingredients": ["Chicken", "Tau cheo (fermented soybean)", "Potatoes", "Shallots", "Garlic", "Gula melaka", "Dark soy sauce"],
        "cooking_method": "Chicken and potatoes are braised slowly with fermented soybean paste until tender and sauce thickens.",
        "taste_profile": ["Savory", "Sweet", "Umami"],
        "dietary_info": {"halal": False, "vegetarian": False, "vegan": False, "gluten_free": False},
        "cultural_significance": "Classic Nyonya dish showcasing Chinese ingredients (tau cheo) with Malay cooking techniques.",
        "typical_meal_time": ["Lunch", "Dinner"],
        "regional_origin": "Melaka",
        "common_pairings": ["White rice", "Acar (pickles)"]
    },

    # Indian Malaysian Cuisine
    {
        "name": "Roti Canai",
        "cuisine_type": "Indian Malaysian",
        "category": "Main course",
        "description": "Flaky, layered flatbread served with curry dhal or other curries. Malaysian Indian breakfast staple.",
        "ingredients": ["Flour", "Ghee or oil", "Condensed milk", "Egg", "Salt", "Water"],
        "cooking_method": "Dough is stretched paper-thin, folded to create layers, then griddled until crispy outside and fluffy inside.",
        "taste_profile": ["Savory"],
        "dietary_info": {"halal": True, "vegetarian": True, "vegan": False, "gluten_free": False},
        "cultural_significance": "Evolved from Indian paratha, became distinctly Malaysian. Mamak stall signature item.",
        "typical_meal_time": ["Breakfast", "Anytime"],
        "regional_origin": "Nationwide, mamak stalls",
        "common_pairings": ["Dhal curry", "Fish curry", "Sambal", "Sugar (roti kosong)"]
    },
    {
        "name": "Nasi Kandar",
        "cuisine_type": "Mamak",
        "category": "Main course",
        "description": "Steamed rice served with variety of curries and side dishes, with mixed curry gravy poured over. Originated from Penang mamak shops.",
        "ingredients": ["Rice", "Various curries (chicken, mutton, fish, squid)", "Vegetables", "Fried chicken", "Boiled eggs", "Papadam"],
        "cooking_method": "Rice is served with customer's choice of curries and dishes, with mixed curry gravy ladled over everything.",
        "taste_profile": ["Spicy", "Savory", "Umami"],
        "dietary_info": {"halal": True, "vegetarian": False, "vegan": False, "gluten_free": True},
        "cultural_significance": "Created by Tamil Muslim vendors who carried rice in kandar (pole). 24-hour availability makes it iconic.",
        "typical_meal_time": ["Lunch", "Dinner", "Late night"],
        "regional_origin": "Penang",
        "common_pairings": ["Fried chicken", "Various curries", "Papadam", "Achar"]
    },
    {
        "name": "Banana Leaf Rice",
        "cuisine_type": "Indian Malaysian",
        "category": "Main course",
        "description": "Rice served on banana leaf with variety of vegetable curries, papadam, and optional meat dishes. Unlimited vegetable refills.",
        "ingredients": ["Rice", "Vegetable curries", "Papadam", "Rasam", "Yogurt", "Optional meat curry"],
        "cooking_method": "Rice and curries are served on banana leaf, eaten with hands. Vegetable curries are refillable.",
        "taste_profile": ["Spicy", "Savory", "Umami"],
        "dietary_info": {"halal": False, "vegetarian": True, "vegan": False, "gluten_free": True},
        "cultural_significance": "South Indian tradition, banana leaf is biodegradable and adds subtle flavor. Represents community dining.",
        "typical_meal_time": ["Lunch", "Dinner"],
        "regional_origin": "Brickfields, Little India areas",
        "common_pairings": ["Fish head curry", "Mutton varuval", "Rasam", "Buttermilk"]
    },

    # Desserts and Beverages
    {
        "name": "Cendol",
        "cuisine_type": "Malay",
        "category": "Dessert",
        "description": "Iced dessert with green rice flour jelly, coconut milk, palm sugar syrup, and shaved ice. Refreshing and sweet.",
        "ingredients": ["Pandan rice flour jelly", "Coconut milk", "Gula melaka (palm sugar)", "Shaved ice", "Red beans"],
        "cooking_method": "Green pandan jelly noodles are served with coconut milk, palm sugar syrup, and ice.",
        "taste_profile": ["Sweet", "Savory"],
        "dietary_info": {"halal": True, "vegetarian": True, "vegan": True, "gluten_free": True},
        "cultural_significance": "Ancient dessert predating colonial era. Each region claims to have best cendol.",
        "typical_meal_time": ["Snack", "Dessert"],
        "regional_origin": "Melaka and Penang are famous for cendol",
        "common_pairings": ["Durian (optional)", "Sweet corn"]
    },
    {
        "name": "Teh Tarik",
        "cuisine_type": "Mamak",
        "category": "Beverage",
        "description": "Pulled milk tea, Malaysia's national drink. Strong black tea with condensed milk, 'pulled' to create frothy top.",
        "ingredients": ["Black tea", "Condensed milk", "Evaporated milk"],
        "cooking_method": "Strong brewed tea is mixed with condensed and evaporated milk, then poured back and forth between containers to create froth and cool it.",
        "taste_profile": ["Sweet"],
        "dietary_info": {"halal": True, "vegetarian": True, "vegan": False, "gluten_free": True},
        "cultural_significance": "Iconic mamak stall beverage. The pulling action is an art form and creates signature frothy texture.",
        "typical_meal_time": ["Breakfast", "Anytime"],
        "regional_origin": "Nationwide",
        "common_pairings": ["Roti canai", "Nasi lemak", "Curry puff"]
    },

    # Regional Specialties
    {
        "name": "Sarawak Laksa",
        "cuisine_type": "Malay",
        "category": "Main course",
        "description": "Sarawak's iconic spicy noodle soup with sambal belacan paste, coconut milk, and unique blend of spices. Different from Peninsular laksa.",
        "ingredients": ["Rice vermicelli", "Prawns", "Shredded chicken", "Bean sprouts", "Sambal belacan paste", "Coconut milk", "Tamarind", "Lemongrass"],
        "cooking_method": "Special laksa paste is cooked with coconut milk and tamarind to create distinctive spicy-sour broth.",
        "taste_profile": ["Spicy", "Savory", "Sour"],
        "dietary_info": {"halal": True, "vegetarian": False, "vegan": False, "gluten_free": True},
        "cultural_significance": "Pride of Sarawak, created by Chinese Sarawakians. Anthony Bourdain declared it breakfast of gods.",
        "typical_meal_time": ["Breakfast", "Lunch"],
        "regional_origin": "Sarawak",
        "common_pairings": ["Lime", "Sambal belacan"]
    },
    {
        "name": "Kolo Mee",
        "cuisine_type": "Chinese Malaysian",
        "category": "Main course",
        "description": "Sarawak dry noodles tossed in lard and shallot oil, topped with char siew and minced meat.",
        "ingredients": ["Egg noodles", "Char siew", "Minced pork", "Shallot oil", "Lard", "Vinegar", "White pepper"],
        "cooking_method": "Springy egg noodles are tossed with lard and shallot oil, topped with char siew and seasoned minced meat.",
        "taste_profile": ["Savory", "Umami"],
        "dietary_info": {"halal": False, "vegetarian": False, "vegan": False, "gluten_free": False},
        "cultural_significance": "Sarawak Chinese heritage dish, breakfast staple in Kuching.",
        "typical_meal_time": ["Breakfast", "Lunch"],
        "regional_origin": "Sarawak",
        "common_pairings": ["Soup on the side", "Pickled green chilies"]
    },
    {
        "name": "Mee Rebus",
        "cuisine_type": "Malay",
        "category": "Main course",
        "description": "Yellow noodles in sweet potato-based gravy, topped with boiled egg, fried shallots, and lime.",
        "ingredients": ["Yellow noodles", "Sweet potato", "Bean sprouts", "Boiled eggs", "Fried shallots", "Green chilies", "Lime"],
        "cooking_method": "Thick gravy is made by blending sweet potato with spices, poured over noodles with toppings.",
        "taste_profile": ["Sweet", "Savory"],
        "dietary_info": {"halal": True, "vegetarian": False, "vegan": False, "gluten_free": False},
        "cultural_significance": "Johor specialty, represents Malay-Javanese culinary influence.",
        "typical_meal_time": ["Breakfast", "Lunch"],
        "regional_origin": "Johor",
        "common_pairings": ["Sambal", "Krupuk (crackers)"]
    },
]
