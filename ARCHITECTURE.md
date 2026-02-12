# Malaysian Food Agent - System Architecture

## Overview
AI-powered Malaysian food expert with MongoDB vector search for food knowledge and Tavily web search for restaurant recommendations.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         USER INTERFACES                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────────────────┐          ┌──────────────────────────────┐   │
│  │   Web Interface       │          │   CLI Interface              │   │
│  │   (FastAPI + HTML)    │          │   (main.py)                  │   │
│  │   Port: 8000          │          │                               │   │
│  └──────────┬───────────┘          └──────────┬───────────────────┘   │
│             │                                   │                        │
│             │ HTTP/REST                         │ Direct                 │
│             │                                   │                        │
└─────────────┼───────────────────────────────────┼────────────────────────┘
              │                                   │
              ▼                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      MALAYSIAN FOOD AGENT CORE                           │
│                   (agent/malaysian_food_agent.py)                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌────────────────────────────────────────────────────────────────┐   │
│  │  Strands Agent Framework                                        │   │
│  │  - Model: Amazon Nova Pro (via AWS Bedrock)                     │   │
│  │  - Temperature: 0.3                                              │   │
│  │  - System Instructions: Malaysian food expert                    │   │
│  └────────────────────────────────────────────────────────────────┘   │
│                                                                          │
│  ┌─────────────────────────────┐   ┌───────────────────────────────┐  │
│  │  Food Knowledge Skill        │   │  Restaurant Finder Skill       │  │
│  │  (skills/food_knowledge_     │   │  (skills/restaurant_finder_   │  │
│  │   skill.py)                  │   │   skill.py)                    │  │
│  │                               │   │                                │  │
│  │  Tools:                       │   │  Tools:                        │  │
│  │  • search_dishes             │   │  • find_restaurants            │  │
│  │  • get_dish_ingredients      │   │  • find_halal_restaurants      │  │
│  │  • get_dietary_info          │   │  • find_restaurants_by_cuisine │  │
│  │  • explore_cuisine_type      │   │  • get_restaurant_reviews      │  │
│  │                               │   │  • find_best_area_for_food     │  │
│  │                               │   │  • search_food_blogs           │  │
│  │                               │   │  • extract_restaurant_details  │  │
│  │                               │   │  • crawl_restaurant_website    │  │
│  │                               │   │  • map_restaurant_website      │  │
│  └───────────┬─────────────────┘   └───────────┬───────────────────┘  │
│              │                                   │                        │
└──────────────┼───────────────────────────────────┼────────────────────────┘
               │                                   │
               ▼                                   ▼
┌──────────────────────────────┐    ┌────────────────────────────────────┐
│  MONGODB SERVICE             │    │  TAVILY WEB SEARCH                 │
│  (services/mongodb.py)       │    │  (strands_tools/tavily.py)         │
├──────────────────────────────┤    ├────────────────────────────────────┤
│                               │    │                                     │
│  • Vector Search              │    │  • tavily_search                   │
│  • Embeddings via Bedrock     │    │    Real-time web search           │
│  • Index: food_vector_index   │    │                                     │
│  • Dimensions: 1024           │    │  • tavily_extract                  │
│  • Similarity: cosine         │    │    Extract content from URLs       │
│  • Filters: cuisine, dietary  │    │                                     │
│                               │    │  • tavily_crawl                    │
│                               │    │    Crawl websites                  │
│                               │    │                                     │
│                               │    │  • tavily_map                      │
│                               │    │    Map website structure           │
│                               │    │                                     │
└───────────┬──────────────────┘    └────────────────────────────────────┘
            │                                       │
            ▼                                       ▼
┌───────────────────────────┐        ┌────────────────────────────────────┐
│  MONGODB ATLAS            │        │  TAVILY API                        │
│                           │        │  (External Service)                │
│  Database: food_places_db │        │                                     │
│  Collection: dishes       │        │  API Key: TAVILY_API_KEY           │
│                           │        │  Endpoint: https://api.tavily.com  │
│  Data: 16 Malaysian dishes│        │                                     │
│  - Nasi Lemak             │        └────────────────────────────────────┘
│  - Rendang                │
│  - Char Koay Teow         │
│  - etc...                 │
│                           │
└───────────┬───────────────┘
            │
            ▼
┌───────────────────────────┐
│  BEDROCK SERVICE          │
│  (services/bedrock.py)    │
├───────────────────────────┤
│                           │
│  • Embedding Model:       │
│    amazon.titan-embed-    │
│    text-v2:0              │
│                           │
│  • Inference Model:       │
│    amazon.nova-pro-v1:0   │
│                           │
│  • Region: us-east-1      │
│                           │
└───────────┬───────────────┘
            │
            ▼
┌───────────────────────────┐
│  AWS BEDROCK              │
│  (External Service)       │
│                           │
│  • Amazon Titan           │
│    Embeddings             │
│  • Amazon Nova Pro        │
│    LLM Inference          │
│                           │
└───────────────────────────┘
```

## Component Details

### 1. User Interfaces

#### Web Interface (api.py)
- **Technology**: FastAPI + HTML/JavaScript
- **Port**: 8000
- **Endpoints**:
  - `GET /` - Web UI
  - `GET /health` - Health check
  - `POST /api/query` - Send query to agent
  - `POST /api/clear-history` - Clear conversation
  - `GET /api/history` - Get conversation history
- **Features**:
  - Real-time chat interface
  - Example queries
  - Conversation history
  - Responsive design

#### CLI Interface (main.py)
- **Technology**: Python command-line
- **Usage**: `python main.py`
- **Features**:
  - Batch processing of demo queries
  - Direct agent interaction

### 2. Malaysian Food Agent Core

#### Agent (agent/malaysian_food_agent.py)
- **Framework**: Strands Agent Framework
- **Model**: Amazon Nova Pro via AWS Bedrock
- **Temperature**: 0.3
- **Capabilities**:
  - Food knowledge from MongoDB
  - Restaurant search via Tavily
  - Multi-turn conversations
  - Tool orchestration

#### Skills

##### Food Knowledge Skill (skills/food_knowledge_skill.py)
**Tools**:
1. `search_dishes` - Vector search for dishes
2. `get_dish_ingredients` - Get ingredient lists
3. `get_dietary_info` - Check dietary restrictions
4. `explore_cuisine_type` - Browse by cuisine

**Data Source**: MongoDB Atlas with vector search

##### Restaurant Finder Skill (skills/restaurant_finder_skill.py)
**Tools**:
1. `find_restaurants` - Search for restaurants
2. `find_halal_restaurants` - Find halal options
3. `find_restaurants_by_cuisine` - Search by cuisine type
4. `get_restaurant_reviews` - Get reviews
5. `find_best_area_for_food` - Discover food areas
6. `search_food_blogs` - Find blog posts
7. `extract_restaurant_details` - Extract from URLs
8. `crawl_restaurant_website` - Crawl restaurant sites
9. `map_restaurant_website` - Map site structure

**Data Source**: Tavily Web Search API

### 3. Backend Services

#### MongoDB Service (services/mongodb.py)
- **Connection**: MongoDB Atlas
- **Database**: food_places_db
- **Collection**: dishes
- **Vector Index**: food_vector_index
  - Dimensions: 1024
  - Similarity: cosine
  - Filters: cuisine_type, category, dietary info
- **Operations**:
  - Vector search
  - Insert dishes with embeddings
  - Index creation

#### Bedrock Service (services/bedrock.py)
- **Provider**: AWS Bedrock
- **Embedding Model**: amazon.titan-embed-text-v2:0
- **Inference Model**: amazon.nova-pro-v1:0
- **Region**: us-east-1
- **Operations**:
  - Generate text embeddings (1024 dimensions)
  - LLM inference (via Strands)

### 4. External Services

#### MongoDB Atlas
- **Type**: Cloud MongoDB database
- **Purpose**: Store Malaysian dish knowledge
- **Data**: 16 dishes with embeddings
- **Features**: Vector search, filters

#### AWS Bedrock
- **Type**: Cloud AI service
- **Models**:
  - Amazon Titan Embeddings (text-v2:0)
  - Amazon Nova Pro (v1:0)
- **Purpose**: Embeddings + LLM inference

#### Tavily API
- **Type**: AI-optimized search engine
- **Purpose**: Real-time restaurant search
- **Features**:
  - Web search
  - Content extraction
  - Website crawling
  - Site mapping

## Data Flow

### Query Processing Flow

```
User Query
    │
    ▼
Malaysian Food Agent
    │
    ├─► Determines intent (food knowledge vs restaurant finding)
    │
    ├─► Food Knowledge Path:
    │   1. Generate query embedding (Bedrock)
    │   2. Vector search MongoDB
    │   3. Return dish information
    │
    └─► Restaurant Finding Path:
        1. Construct search query
        2. Call Tavily API
        3. Return restaurant results
    │
    ▼
Response to User
```

### Database Seeding Flow

```
Scripts/seed_database.py
    │
    ├─► Load Malaysian dishes data
    │
    ├─► For each dish:
    │   1. Create text representation
    │   2. Generate embedding (Bedrock)
    │   3. Insert into MongoDB with embedding
    │
    ├─► Create vector search index
    │   (if not exists)
    │
    └─► Complete
```

## Configuration

### Environment Variables (.env)

```bash
# AWS Bedrock
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret

# Models
BEDROCK_EMBEDDING_MODEL=amazon.titan-embed-text-v2:0
BEDROCK_INFERENCE_MODEL=amazon.nova-pro-v1:0

# MongoDB Atlas
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/
MONGODB_DATABASE=food_places_db
MONGODB_COLLECTION=dishes

# Tavily
TAVILY_API_KEY=your_tavily_key
```

## Deployment

### Local Development

```bash
# Setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Seed Database
python -m scripts.seed_database

# Run Web Interface
python api.py
# Access at http://localhost:8000

# Or Run CLI
python main.py
```

### Production Considerations

1. **Security**:
   - Use environment-specific .env files
   - Implement API rate limiting
   - Add authentication/authorization
   - Use HTTPS

2. **Scalability**:
   - Deploy on cloud (AWS/GCP/Azure)
   - Use container orchestration (Docker/K8s)
   - Implement caching layer
   - Load balancing

3. **Monitoring**:
   - Add logging (structured logs)
   - Health checks
   - Performance metrics
   - Error tracking

4. **Database**:
   - MongoDB Atlas M10+ for vector search
   - Regular backups
   - Index optimization

## Technology Stack

### Core Technologies
- **Language**: Python 3.14
- **Framework**: Strands Agent Framework
- **Web**: FastAPI + Uvicorn
- **Database**: MongoDB Atlas
- **AI Models**: Amazon Nova Pro, Amazon Titan

### Key Dependencies
```
strands-agents-tools  # Agent framework with Tavily/tools
fastapi               # Web API
uvicorn               # ASGI server
pymongo               # MongoDB driver
boto3                 # AWS SDK
python-dotenv         # Environment config
pydantic              # Data validation
```

## Access Points

### Web Interface
- **URL**: http://localhost:8000
- **Features**: Chat UI, example queries, history

### API Documentation
- **URL**: http://localhost:8000/docs
- **Type**: OpenAPI/Swagger UI
- **Features**: Interactive API testing

### CLI Interface
- **Command**: `python main.py`
- **Type**: Command-line demo

## Future Enhancements

1. **Features**:
   - Multi-language support
   - Image recognition for dishes
   - User preferences/favorites
   - Recipe generation
   - Meal planning

2. **Technical**:
   - Caching layer (Redis)
   - Async database operations
   - Streaming responses
   - User authentication
   - Rate limiting

3. **Data**:
   - More dishes (100+)
   - Regional variations
   - Restaurant partnerships
   - User-generated content
