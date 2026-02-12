# Quick Start Guide - Malaysian Food Agent

## Overview

This agent has **two separate skills**:
1. **Food Knowledge** - Malaysian dishes info from MongoDB (ingredients, culture, etc.)
2. **Restaurant Finder** - Real restaurant locations via web search

## 1. Install Dependencies

```bash
pip install -r requirements.txt
```

Required packages:
- `strands-agents-tools` - Strands agent framework
- `boto3` - AWS SDK for Bedrock
- `pymongo` - MongoDB driver
- `mcp` - Model Context Protocol
- `anthropic` - Claude API

## 2. Set Up Environment

```bash
cp .env.example .env
```

Edit `.env`:

```env
ANTHROPIC_API_KEY=sk-ant-xxx  # Required for Strands
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
BEDROCK_EMBEDDING_MODEL=amazon.titan-embed-text-v2:0
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/
MONGODB_DATABASE=food_places_db
MONGODB_COLLECTION=dishes
```

## 3. MongoDB Atlas Setup

1. Create free MongoDB Atlas cluster at https://cloud.mongodb.com
2. Create database: `food_places_db`
3. Create collection: `dishes` (NOT restaurants!)
4. Create Vector Search Index:

**Index Name**: `food_vector_index`

**JSON Definition**:
```json
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
```

## 4. AWS Bedrock Setup

1. Go to AWS Bedrock console
2. Request access to:
   - Amazon Titan Embeddings G1 - Text v2
3. Wait for approval (usually instant)

## 5. Anthropic API Setup

1. Get API key from https://console.anthropic.com/
2. Add to `.env` as `ANTHROPIC_API_KEY`

## 6. Seed the Database

```bash
python scripts/seed_database.py
```

This populates MongoDB with 15 Malaysian **dishes** (not restaurants):
- Nasi Lemak, Rendang, Satay
- Char Koay Teow, Laksa
- Roti Canai, Nasi Kandar
- And more!

## 7. Run the Agent

```bash
python main.py
```

## Example Usage

```python
from agent.malaysian_food_agent import MalaysianFoodAgent
from services.mongodb import MongoDBFoodKnowledgeService
from services.mcp_search import MCPSearchService
from services.bedrock import BedrockService

# Initialize services
bedrock = BedrockService(...)
mongo = MongoDBFoodKnowledgeService(...)
mcp = MCPSearchService()

# Create agent
agent = MalaysianFoodAgent(mongo, mcp)
agent.initialize()

# Food knowledge query (uses MongoDB skill)
response = agent.query("What is Nasi Lemak made of?")

# Restaurant finding query (uses MCP search skill)
response = agent.query("Where can I find Char Koay Teow in Penang?")

# Combined query (uses both skills)
response = agent.query("Tell me about Rendang and where to try it in KL")

agent.shutdown()
```

## Understanding the Two Skills

### Skill 1: Food Knowledge (MongoDB)
- **What it does**: Provides information about Malaysian dishes
- **Data source**: MongoDB Atlas with vector search
- **Contains**: Ingredients, cooking methods, cultural significance
- **Does NOT contain**: Restaurant locations or addresses

**Example queries**:
- "What ingredients are in Laksa?"
- "Tell me about Nyonya cuisine"
- "What are some vegetarian Malaysian dishes?"

### Skill 2: Restaurant Finder (MCP Search)
- **What it does**: Finds actual restaurant locations
- **Data source**: Web search via MCP (DuckDuckGo)
- **Contains**: Current restaurant info, locations, reviews
- **Provides**: Real-time, up-to-date information

**Example queries**:
- "Where can I find the best satay in Kajang?"
- "Find halal restaurants in Georgetown Penang"
- "What are the best areas for Malay food in KL?"

## Troubleshooting

### "No module named 'strands'"
```bash
pip install strands-agents-tools
```

### "No module named 'mcp'"
```bash
pip install mcp
```

### MongoDB Connection Error
- Check MongoDB URI in `.env`
- Ensure IP whitelist includes your IP
- Verify credentials

### Vector Search Not Working
- Ensure index name is exactly `food_vector_index`
- Wait 5-10 minutes after creating index
- Verify numDimensions is `1024`

### MCP Connection Issues
```bash
# Requires Node.js/npx
npx -y @modelcontextprotocol/server-duckduckgo
```

### AWS Bedrock Access Denied
- Verify Titan Embeddings model access in console
- Check IAM permissions for `bedrock:InvokeModel`

## Key Differences from Traditional Approach

**Traditional Approach** (DON'T DO THIS):
- Store restaurants with addresses in MongoDB
- Search database for restaurant locations

**Our Approach** (CORRECT):
- Store ONLY food knowledge in MongoDB (dishes, ingredients, culture)
- Use web search for restaurant locations (current, up-to-date info)
- Separate concerns = better accuracy and freshness

## Next Steps

- Add more Malaysian dishes to `data/malaysian_dishes.py`
- Customize agent instructions in `agent/malaysian_food_agent.py`
- Add more MCP servers (e.g., Google Search)
- Implement caching for frequently asked questions
