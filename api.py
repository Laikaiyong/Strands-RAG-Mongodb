"""FastAPI web interface for Malaysian Food Agent."""

import os
import asyncio
from typing import Dict, List, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv

from strands.models import BedrockModel
from services.bedrock import BedrockService
from services.mongodb import MongoDBFoodKnowledgeService
from agent.malaysian_food_agent import MalaysianFoodAgent

# Load environment variables
load_dotenv(override=True)

# Global agent instance
agent: Optional[MalaysianFoodAgent] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize and cleanup resources."""
    global agent

    print("🍜 Starting Malaysian Food Agent API...")

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

    # Create BedrockModel for Amazon Nova Pro
    bedrock_model = BedrockModel(
        model_id=os.getenv("BEDROCK_INFERENCE_MODEL", "amazon.nova-pro-v1:0"),
        region_name=os.getenv("AWS_REGION", "us-east-1"),
        temperature=0.3,
    )

    # Create agent
    agent = MalaysianFoodAgent(
        mongo_service=mongo_service,
        model=bedrock_model
    )

    # Initialize agent
    agent.initialize()
    print("✓ Malaysian Food Agent API ready!")

    yield

    # Cleanup
    if agent:
        agent.shutdown()
    print("✓ Malaysian Food Agent API stopped")


# Create FastAPI app
app = FastAPI(
    title="Malaysian Food Agent API",
    description="AI-powered Malaysian food expert with MongoDB vector search and Tavily web search",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response models
class QueryRequest(BaseModel):
    """Query request model."""
    query: str

    class Config:
        json_schema_extra = {
            "example": {
                "query": "What is Nasi Lemak and where can I find it in Kuala Lumpur?"
            }
        }


class QueryResponse(BaseModel):
    """Query response model."""
    response: str
    query: str


class HistoryResponse(BaseModel):
    """Conversation history response."""
    history: List[Dict[str, str]]


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    message: str
    mongodb_connected: bool
    agent_ready: bool


# API Endpoints
@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the web interface."""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Malaysian Food Agent</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }

            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }

            .container {
                max-width: 900px;
                margin: 0 auto;
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                overflow: hidden;
            }

            .header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                text-align: center;
            }

            .header h1 {
                font-size: 2.5em;
                margin-bottom: 10px;
            }

            .header p {
                font-size: 1.1em;
                opacity: 0.9;
            }

            .chat-container {
                height: 500px;
                overflow-y: auto;
                padding: 20px;
                background: #f8f9fa;
            }

            .message {
                margin-bottom: 20px;
                animation: fadeIn 0.3s;
            }

            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(10px); }
                to { opacity: 1; transform: translateY(0); }
            }

            .message.user {
                text-align: right;
            }

            .message-content {
                display: inline-block;
                max-width: 80%;
                padding: 15px 20px;
                border-radius: 15px;
                word-wrap: break-word;
            }

            .message.user .message-content {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border-bottom-right-radius: 5px;
            }

            .message.assistant .message-content {
                background: white;
                color: #333;
                border: 1px solid #e0e0e0;
                border-bottom-left-radius: 5px;
                text-align: left;
            }

            .input-container {
                padding: 20px;
                background: white;
                border-top: 1px solid #e0e0e0;
            }

            .input-row {
                display: flex;
                gap: 10px;
            }

            #queryInput {
                flex: 1;
                padding: 15px 20px;
                border: 2px solid #e0e0e0;
                border-radius: 25px;
                font-size: 16px;
                outline: none;
                transition: border-color 0.3s;
            }

            #queryInput:focus {
                border-color: #667eea;
            }

            button {
                padding: 15px 30px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                border-radius: 25px;
                font-size: 16px;
                font-weight: 600;
                cursor: pointer;
                transition: transform 0.2s, box-shadow 0.2s;
            }

            button:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
            }

            button:active {
                transform: translateY(0);
            }

            button:disabled {
                opacity: 0.6;
                cursor: not-allowed;
                transform: none;
            }

            .loading {
                text-align: center;
                padding: 20px;
                color: #666;
            }

            .examples {
                padding: 20px;
                background: #f8f9fa;
                border-top: 1px solid #e0e0e0;
            }

            .examples h3 {
                margin-bottom: 10px;
                color: #333;
            }

            .example-chips {
                display: flex;
                flex-wrap: wrap;
                gap: 10px;
            }

            .example-chip {
                padding: 8px 16px;
                background: white;
                border: 1px solid #667eea;
                color: #667eea;
                border-radius: 20px;
                cursor: pointer;
                font-size: 14px;
                transition: all 0.2s;
            }

            .example-chip:hover {
                background: #667eea;
                color: white;
            }

            .buttons-row {
                display: flex;
                gap: 10px;
                margin-top: 10px;
            }

            .secondary-btn {
                background: #6c757d;
            }

            .secondary-btn:hover {
                box-shadow: 0 5px 15px rgba(108, 117, 125, 0.4);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🍜 Malaysian Food Agent</h1>
                <p>Your AI-powered guide to Malaysian cuisine</p>
            </div>

            <div class="chat-container" id="chatContainer">
                <div class="message assistant">
                    <div class="message-content">
                        <strong>Welcome to Malaysian Food Agent!</strong><br><br>
                        I'm your expert guide to Malaysian cuisine. I can help you:<br>
                        • Learn about Malaysian dishes, ingredients, and recipes<br>
                        • Find restaurants serving specific dishes<br>
                        • Get dietary information (halal, vegetarian, etc.)<br>
                        • Discover regional specialties<br><br>
                        Ask me anything about Malaysian food!
                    </div>
                </div>
            </div>

            <div class="examples">
                <h3>Try these examples:</h3>
                <div class="example-chips">
                    <span class="example-chip" onclick="sendExample('What is Nasi Lemak and what ingredients does it have?')">
                        What is Nasi Lemak?
                    </span>
                    <span class="example-chip" onclick="sendExample('Where can I find the best Char Koay Teow in Penang?')">
                        Best Char Koay Teow in Penang?
                    </span>
                    <span class="example-chip" onclick="sendExample('What are some good vegetarian Malaysian dishes?')">
                        Vegetarian dishes
                    </span>
                    <span class="example-chip" onclick="sendExample('Tell me about Rendang and where I can try it')">
                        About Rendang
                    </span>
                </div>
            </div>

            <div class="input-container">
                <div class="input-row">
                    <input
                        type="text"
                        id="queryInput"
                        placeholder="Ask me about Malaysian food..."
                        onkeypress="handleKeyPress(event)"
                    >
                    <button onclick="sendQuery()" id="sendBtn">Send</button>
                </div>
                <div class="buttons-row">
                    <button onclick="clearHistory()" class="secondary-btn">Clear History</button>
                </div>
            </div>
        </div>

        <script>
            const chatContainer = document.getElementById('chatContainer');
            const queryInput = document.getElementById('queryInput');
            const sendBtn = document.getElementById('sendBtn');

            function scrollToBottom() {
                chatContainer.scrollTop = chatContainer.scrollHeight;
            }

            function addMessage(role, content) {
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${role}`;

                const contentDiv = document.createElement('div');
                contentDiv.className = 'message-content';
                contentDiv.innerHTML = content.replace(/\n/g, '<br>');

                messageDiv.appendChild(contentDiv);
                chatContainer.appendChild(messageDiv);
                scrollToBottom();
            }

            function showLoading() {
                const loadingDiv = document.createElement('div');
                loadingDiv.className = 'loading';
                loadingDiv.id = 'loading';
                loadingDiv.innerHTML = '🤔 Thinking...';
                chatContainer.appendChild(loadingDiv);
                scrollToBottom();
            }

            function hideLoading() {
                const loading = document.getElementById('loading');
                if (loading) {
                    loading.remove();
                }
            }

            async function sendQuery() {
                const query = queryInput.value.trim();
                if (!query) return;

                // Add user message
                addMessage('user', query);
                queryInput.value = '';

                // Disable input
                sendBtn.disabled = true;
                queryInput.disabled = true;
                showLoading();

                try {
                    const response = await fetch('/api/query', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ query }),
                    });

                    if (!response.ok) {
                        throw new Error('Failed to get response');
                    }

                    const data = await response.json();
                    hideLoading();
                    addMessage('assistant', data.response);
                } catch (error) {
                    hideLoading();
                    addMessage('assistant', '❌ Sorry, I encountered an error. Please try again.');
                    console.error('Error:', error);
                } finally {
                    sendBtn.disabled = false;
                    queryInput.disabled = false;
                    queryInput.focus();
                }
            }

            function sendExample(query) {
                queryInput.value = query;
                sendQuery();
            }

            function handleKeyPress(event) {
                if (event.key === 'Enter') {
                    sendQuery();
                }
            }

            async function clearHistory() {
                try {
                    const response = await fetch('/api/clear-history', {
                        method: 'POST',
                    });

                    if (response.ok) {
                        chatContainer.innerHTML = '';
                        addMessage('assistant', '<strong>History cleared!</strong><br>Start a new conversation by asking me anything about Malaysian food.');
                    }
                } catch (error) {
                    console.error('Error:', error);
                }
            }

            // Focus input on load
            queryInput.focus();
        </script>
    </body>
    </html>
    """


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    if not agent:
        raise HTTPException(status_code=503, detail="Agent not initialized")

    mongodb_connected = agent.mongo_service.client is not None

    return HealthResponse(
        status="healthy" if mongodb_connected else "degraded",
        message="Malaysian Food Agent is running",
        mongodb_connected=mongodb_connected,
        agent_ready=True
    )


@app.post("/api/query", response_model=QueryResponse)
async def query_agent(request: QueryRequest):
    """
    Send a query to the Malaysian Food Agent.

    The agent can answer questions about:
    - Malaysian dishes, ingredients, and recipes
    - Restaurant locations and recommendations
    - Dietary information (halal, vegetarian, etc.)
    - Cultural significance and regional origins
    """
    if not agent:
        raise HTTPException(status_code=503, detail="Agent not initialized")

    try:
        # Run the agent query in the event loop
        response = agent.query(request.query)

        return QueryResponse(
            response=response,
            query=request.query
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


@app.post("/api/clear-history")
async def clear_conversation_history():
    """Clear the conversation history."""
    if not agent:
        raise HTTPException(status_code=503, detail="Agent not initialized")

    agent.clear_history()
    return {"status": "success", "message": "Conversation history cleared"}


@app.get("/api/history", response_model=HistoryResponse)
async def get_conversation_history():
    """Get the conversation history."""
    if not agent:
        raise HTTPException(status_code=503, detail="Agent not initialized")

    return HistoryResponse(history=agent.get_history())


if __name__ == "__main__":
    import uvicorn

    print("Starting Malaysian Food Agent API server...")
    print("Access the web interface at: http://localhost:8000")
    print("API documentation at: http://localhost:8000/docs")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
