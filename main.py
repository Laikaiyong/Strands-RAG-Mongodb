"""Interactive CLI for Malaysian Food Agent with thought process visibility."""

import os
import sys
import asyncio
from dotenv import load_dotenv
from strands.models import BedrockModel
from services.bedrock import BedrockService
from services.mongodb import MongoDBFoodKnowledgeService
from agent.malaysian_food_agent import MalaysianFoodAgent

# Load environment variables
load_dotenv(override=True)

# ANSI color codes for better visibility
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def print_header(text):
    """Print header with formatting."""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'═' * 80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'═' * 80}{Colors.END}\n")


def print_section(title, content="", color=Colors.YELLOW):
    """Print a section with title."""
    print(f"\n{color}{Colors.BOLD}▶ {title}{Colors.END}")
    if content:
        print(f"{color}{content}{Colors.END}")


def print_thinking(text):
    """Print thinking process."""
    print(f"{Colors.YELLOW}💭 Thinking: {text}{Colors.END}")


def print_tool_call(tool_name, args=None):
    """Print tool call information."""
    print(f"\n{Colors.CYAN}🔧 Tool Call: {Colors.BOLD}{tool_name}{Colors.END}")
    if args:
        print(f"{Colors.CYAN}   Parameters: {args}{Colors.END}")


def print_response(text):
    """Print agent response."""
    print(f"\n{Colors.GREEN}{Colors.BOLD}Assistant:{Colors.END} {text}")


def print_error(text):
    """Print error message."""
    print(f"\n{Colors.RED}❌ Error: {text}{Colors.END}")


def print_separator():
    """Print separator line."""
    print(f"{Colors.BLUE}{'─' * 80}{Colors.END}")


async def interactive_mode(agent):
    """
    Run agent in interactive mode with thought process visibility.

    This mode shows:
    - User queries
    - Agent's thinking process
    - Tool calls being made
    - Final responses
    """
    print_header("🍜 Malaysian Food Agent - Interactive Mode")

    print(f"{Colors.GREEN}I'm your Malaysian food expert! I can help you with:{Colors.END}")
    print(f"{Colors.GREEN}  • Information about Malaysian dishes and ingredients{Colors.END}")
    print(f"{Colors.GREEN}  • Finding restaurants serving specific dishes{Colors.END}")
    print(f"{Colors.GREEN}  • Dietary information (halal, vegetarian, etc.){Colors.END}")
    print(f"{Colors.GREEN}  • Cultural significance and regional origins{Colors.END}")

    print(f"\n{Colors.YELLOW}Type 'quit', 'exit', or press Ctrl+C to end the conversation.{Colors.END}")
    print(f"{Colors.YELLOW}I'll show you my thought process as I work!{Colors.END}")

    conversation_count = 0

    while True:
        try:
            # Get user input
            print(f"\n{Colors.BOLD}{Colors.BLUE}{'─' * 80}{Colors.END}")
            user_input = input(f"{Colors.BOLD}You: {Colors.END}").strip()

            # Check for exit commands
            if user_input.lower() in ['quit', 'exit', 'q', 'bye']:
                print(f"\n{Colors.GREEN}Thank you for exploring Malaysian cuisine! Selamat makan! 🍜{Colors.END}")
                break

            # Skip empty input
            if not user_input:
                continue

            conversation_count += 1
            print_separator()
            print_section(f"Processing Query #{conversation_count}", color=Colors.CYAN)

            # Process the query and capture the response
            print_thinking("Analyzing your question and determining the best approach...")

            # Run the agent query (async version shows thinking)
            response = await agent.query_async(user_input, verbose=True)

            # Print the final response
            print_separator()
            print_response(response)

        except KeyboardInterrupt:
            print(f"\n\n{Colors.GREEN}Interrupted. Thank you for using Malaysian Food Agent!{Colors.END}")
            break
        except EOFError:
            print(f"\n{Colors.GREEN}Thank you for using Malaysian Food Agent!{Colors.END}")
            break
        except Exception as e:
            print_error(f"An error occurred: {str(e)}")
            import traceback
            traceback.print_exc()


def main():
    """Run the Malaysian Food Agent in interactive CLI mode."""
    print(f"{Colors.BOLD}{Colors.HEADER}")
    print("╔════════════════════════════════════════════════════════════════════════════╗")
    print("║                     🍜 Malaysian Food Agent 🍜                             ║")
    print("║                  Interactive CLI with Thought Process                      ║")
    print("╚════════════════════════════════════════════════════════════════════════════╝")
    print(Colors.END)

    try:
        print(f"{Colors.YELLOW}Initializing services...{Colors.END}")

        # Initialize Bedrock service (for embeddings)
        bedrock_service = BedrockService(
            region=os.getenv("AWS_REGION", "us-east-1"),
            embedding_model=os.getenv("BEDROCK_EMBEDDING_MODEL", "amazon.titan-embed-text-v2:0"),
            inference_model=os.getenv("BEDROCK_INFERENCE_MODEL", "amazon.nova-pro-v1:0"),
            access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        )
        print(f"{Colors.GREEN}✓ AWS Bedrock service initialized{Colors.END}")

        # Initialize MongoDB service (Food Knowledge)
        mongo_service = MongoDBFoodKnowledgeService(
            uri=os.getenv("MONGODB_URI", "mongodb://localhost:27017"),
            database=os.getenv("MONGODB_DATABASE", "food_places_db"),
            collection=os.getenv("MONGODB_COLLECTION", "dishes"),
            bedrock_service=bedrock_service,
        )
        print(f"{Colors.GREEN}✓ MongoDB service initialized{Colors.END}")

        # Create BedrockModel for Amazon Nova Pro
        bedrock_model = BedrockModel(
            model_id=os.getenv("BEDROCK_INFERENCE_MODEL", "amazon.nova-pro-v1:0"),
            region_name=os.getenv("AWS_REGION", "us-east-1"),
            temperature=0.3,
        )
        print(f"{Colors.GREEN}✓ Amazon Nova Pro model configured{Colors.END}")

        # Create agent
        agent = MalaysianFoodAgent(
            mongo_service=mongo_service,
            model=bedrock_model
        )

        # Initialize agent
        agent.initialize()
        print(f"{Colors.GREEN}✓ Agent initialized with dual skills{Colors.END}")
        print(f"{Colors.GREEN}  - Food Knowledge Skill (MongoDB vector search){Colors.END}")
        print(f"{Colors.GREEN}  - Restaurant Finder Skill (Tavily web search){Colors.END}")

        # Run interactive mode
        asyncio.run(interactive_mode(agent))

    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Interrupted by user.{Colors.END}")
        return 1
    except Exception as e:
        print_error(f"Failed to initialize: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        try:
            agent.shutdown()
            print(f"\n{Colors.GREEN}✓ Agent shutdown complete{Colors.END}")
        except:
            pass

    return 0


if __name__ == "__main__":
    exit(main())
