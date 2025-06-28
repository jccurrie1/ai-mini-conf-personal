from typing import TypedDict, List, Optional, cast
from langchain.tools import tool
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
import numpy as np

class AgentState(TypedDict):
    messages: List[dict]
    tool_result: Optional[str]
    tool_name: Optional[str]  # Track which tool was used

# Initialize embeddings model for semantic similarity
embeddings_model = OpenAIEmbeddings()

def get_semantic_similarity(text1: str, text2: str) -> float:
    """Calculate semantic similarity between two texts using embeddings."""
    embeddings = embeddings_model.embed_documents([text1, text2])
    # Calculate cosine similarity
    vec1, vec2 = np.array(embeddings[0]), np.array(embeddings[1])
    similarity = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
    return float(similarity)

def classify_intent_semantic(user_message: str, threshold: float = 0.7) -> str:
    """Classify user intent using semantic similarity instead of keyword matching."""
    
    # Define intent examples (more natural than keywords)
    calendar_examples = [
        "I need to schedule a meeting",
        "What's my availability tomorrow?", 
        "Are you free for a call?",
        "Let's set up an appointment",
        "Check my calendar for next week"
    ]
    
    search_examples = [
        "Can you find information about Python?",
        "Search for tutorials on machine learning",
        "Look up the latest news on AI",
        "Find me resources about web development",
        "I need to research this topic"
    ]
    
    # Calculate similarity scores for each intent
    calendar_scores = [get_semantic_similarity(user_message, example) for example in calendar_examples]
    search_scores = [get_semantic_similarity(user_message, example) for example in search_examples]
    
    max_calendar_score = max(calendar_scores)
    max_search_score = max(search_scores)
    
    print(f"🧠 Semantic Analysis:")
    print(f"   Calendar similarity: {max_calendar_score:.3f}")
    print(f"   Search similarity: {max_search_score:.3f}")
    print(f"   Threshold: {threshold}")
    
    # Determine intent based on highest similarity above threshold
    if max_calendar_score >= threshold and max_calendar_score > max_search_score:
        return "calendar"
    elif max_search_score >= threshold and max_search_score > max_calendar_score:
        return "search"
    else:
        return "chat"

def classify_intent_llm(user_message: str) -> str:
    """Classify user intent using LLM reasoning instead of keyword matching or embeddings."""
    
    classification_prompt = f"""
    Analyze the following user message and classify the intent into one of these categories:
    
    1. "calendar" - User wants to schedule something, check availability, or manage time
    2. "search" - User wants to find information, research something, or look up content  
    3. "chat" - General conversation, questions not requiring tools, or casual interaction
    
    User message: "{user_message}"
    
    Respond with ONLY the category name (calendar, search, or chat). No explanation needed.
    """
    
    response = llm.invoke(classification_prompt)
    # Extract content properly from the response
    if hasattr(response, 'content'):
        intent = str(response.content).strip().lower()
    else:
        intent = str(response).strip().lower()
    
    print(f"🤖 LLM Classification: '{intent}' for message: '{user_message[:50]}...'")
    
    # Validate the response
    if intent in ["calendar", "search", "chat"]:
        return intent
    else:
        print(f"⚠️  Unknown classification '{intent}', defaulting to 'chat'")
        return "chat"

@tool
def check_calendar(day: str) -> str:
    """Return dummy availability for demo purposes."""
    return f"Available slots on {day}: 9 AM, 2 PM, 4 PM"

@tool
def search_web(query: str) -> str:
    """Pretend to search the web."""
    return f"Top result for '{query}': ... (stub)"
    
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def triage(state: AgentState) -> AgentState:
    """Decide whether we need a tool call using semantic similarity."""
    user_message = state["messages"][-1]["content"]
    
    # Use semantic classification instead of keyword matching
    intent = classify_intent_semantic(user_message)
    
    if intent == "calendar":
        print("🔧 Triage: Semantic analysis detected calendar intent → routing to calendar tool")
        return {"messages": state["messages"], "tool_result": "calendar", "tool_name": "check_calendar"}
    elif intent == "search":
        print("🔧 Triage: Semantic analysis detected search intent → routing to web search tool")
        return {"messages": state["messages"], "tool_result": "search", "tool_name": "search_web"}
    else:
        print("🔧 Triage: Semantic analysis detected general chat intent → routing directly to chat")
        return {"messages": state["messages"], "tool_result": "no_tool", "tool_name": None}

def run_tool(state: AgentState) -> AgentState:
    # Determine which tool to run based on the tool_result from triage
    if state["tool_result"] == "calendar":
        print(f"⚡ Running tool: {state['tool_name']}")
        result = check_calendar("tomorrow")
    elif state["tool_result"] == "search":
        print(f"⚡ Running tool: {state['tool_name']}")
        # Extract search query from the user message
        user_message = state["messages"][-1]["content"]
        result = search_web(user_message)
    else:
        result = "No tool specified"
    
    print(f"✅ Tool result: {result[:50]}..." if len(result) > 50 else f"✅ Tool result: {result}")
    return {"messages": state["messages"], "tool_result": result, "tool_name": state["tool_name"]}

def chat(state: AgentState) -> AgentState:
    if state["tool_result"] and state["tool_result"] != "no_tool":
        print(f"💬 Chat: Generating response with {state['tool_name']} tool data")
        prompt = f"User asked: {state['messages'][-1]['content']}\nTool says: {state['tool_result']}"
    else:
        print("💬 Chat: Generating direct response (no tool data)")
        prompt = state["messages"][-1]["content"]
    reply = llm.invoke(prompt)
    new_messages = state["messages"] + [{"role": "assistant", "content": reply.content}]
    return {"messages": new_messages, "tool_result": state["tool_result"], "tool_name": state["tool_name"]}

# Alternative triage function using LLM classification
def triage_llm_based(state: AgentState) -> AgentState:
    """Decide whether we need a tool call using LLM-based classification."""
    user_message = state["messages"][-1]["content"]
    
    # Use LLM classification instead of keyword matching or embeddings
    intent = classify_intent_llm(user_message)
    
    if intent == "calendar":
        print("🔧 Triage: LLM detected calendar intent → routing to calendar tool")
        return {"messages": state["messages"], "tool_result": "calendar", "tool_name": "check_calendar"}
    elif intent == "search":
        print("🔧 Triage: LLM detected search intent → routing to web search tool")
        return {"messages": state["messages"], "tool_result": "search", "tool_name": "search_web"}
    else:
        print("🔧 Triage: LLM detected general chat intent → routing directly to chat")
        return {"messages": state["messages"], "tool_result": "no_tool", "tool_name": None}

from langgraph.graph import StateGraph, START, END

# Choose which classification method to use
CLASSIFICATION_METHOD = "llm"  # Options: "keywords", "semantic", "llm"

builder = StateGraph(AgentState)

# Use different triage functions based on method
if CLASSIFICATION_METHOD == "llm":
    builder.add_node("triage", triage_llm_based)
else:
    builder.add_node("triage", triage)  # semantic-based triage

builder.add_node("run_tool", run_tool)
builder.add_node("chat", chat)

# Edges
builder.add_edge(START, "triage")

# More explicit conditional edges with proper routing function
def route_after_triage(state: AgentState) -> str:
    """Route after triage based on tool_result."""
    if state["tool_result"] in ["calendar", "search"]:
        return "run_tool"
    else:
        return "chat"

builder.add_conditional_edges(
    "triage",
    route_after_triage,
    {
        "run_tool": "run_tool",
        "chat": "chat"
    }
)
builder.add_edge("run_tool", "chat")
builder.add_edge("chat", END)

agent = builder.compile()

def run_interactive():
    """Run the agent in interactive mode."""
    print("🤖 Personal Agent Interactive Mode")
    print("Type 'quit' to exit")
    print("-" * 40)
    
    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("Goodbye! 👋")
            break
            
        if not user_input:
            continue
            
        # Run the agent
        state = {"messages": [{"role": "user", "content": user_input}], "tool_result": None, "tool_name": None}
        result = agent.invoke(state)
        
        print(f"🤖 Agent: {result['messages'][-1]['content']}")

def show_execution_summary(final_state: AgentState):
    """Display a summary of the agent's execution path."""
    print("\n" + "="*30)
    print("📊 EXECUTION SUMMARY")
    print("="*30)
    
    if final_state["tool_name"]:
        print(f"🔧 Tool Used: {final_state['tool_name']}")
        tool_result = final_state['tool_result'] or ""
        print(f"📝 Tool Result: {tool_result[:100]}..." if len(tool_result) > 100 else f"📝 Tool Result: {tool_result}")
        print(f"🛤️  Execution Path: triage → run_tool → chat")
    else:
        print("🔧 Tool Used: None (direct chat)")
        print(f"🛤️  Execution Path: triage → chat")
    
    print(f"💬 Messages in conversation: {len(final_state['messages'])}")
    print("="*30)

def compare_classification_methods(user_message: str):
    """Compare all three classification methods on the same input."""
    print(f"\n🔬 CLASSIFICATION COMPARISON for: '{user_message}'")
    print("="*60)
    
    # Method 1: Keyword-based (recreated for comparison)
    calendar_keywords = ["availability", "schedule", "free", "available", "meeting", "appointment", "calendar"]
    search_keywords = ["search", "internet", "web", "find", "lookup", "google"]
    
    lower_msg = user_message.lower()
    if any(keyword in lower_msg for keyword in calendar_keywords):
        keyword_result = "calendar"
    elif any(keyword in lower_msg for keyword in search_keywords):
        keyword_result = "search"
    else:
        keyword_result = "chat"
    print(f"1️⃣ Keyword-based:  {keyword_result}")
    
    # Method 2: Semantic similarity
    semantic_result = classify_intent_semantic(user_message, threshold=0.7)
    print(f"2️⃣ Semantic-based: {semantic_result}")
    
    # Method 3: LLM-based
    llm_result = classify_intent_llm(user_message)
    print(f"3️⃣ LLM-based:      {llm_result}")
    
    print("="*60)

def visualize_graph():
    """Create a visual representation of the agent graph."""
    try:
        # Try to create a visualization
        from IPython.display import Image, display
        import io
        import base64
        
        # Get the graph visualization
        graph_image = agent.get_graph().draw_mermaid_png()
        
        # Save to file
        with open("personal_agent_graph.png", "wb") as f:
            f.write(graph_image)
        print("📊 Graph visualization saved as 'personal_agent_graph.png'")
        
        return graph_image
    except ImportError:
        print("📊 Visualization requires additional dependencies. Install with: pip install pygraphviz")
        return None
    except Exception as e:
        print(f"📊 Could not create visualization: {e}")
        # Fallback: print text representation
        print("\n🔗 GRAPH STRUCTURE (Text):")
        print("="*40)
        print("START → triage")
        if CLASSIFICATION_METHOD == "llm":
            print("triage → [LLM classifies intent]")
        else:
            print("triage → [Semantic classifies intent]")
        print("  ├─ calendar intent → run_tool → chat → END")
        print("  ├─ search intent → run_tool → chat → END") 
        print("  └─ chat intent → chat → END")
        print("="*40)
        return None

def debug_graph_structure():
    """Print detailed information about the graph structure."""
    print("\n🔍 DETAILED GRAPH STRUCTURE DEBUG")
    print("="*50)
    
    # Get the compiled graph
    graph = agent.get_graph()
    
    print("📊 Nodes:")
    for node in graph.nodes:
        print(f"   • {node}")
    
    print("\n🔗 Edges:")
    for edge in graph.edges:
        print(f"   • {edge}")
    
    print(f"\n⚙️  Classification Method: {CLASSIFICATION_METHOD}")
    print(f"🎯 Triage Function: {'triage_llm_based' if CLASSIFICATION_METHOD == 'llm' else 'triage'}")
    
    print("\n🛤️  Expected Flow:")
    print("   START → triage")
    print("   triage → route_after_triage() → [run_tool | chat]")
    print("   run_tool → chat") 
    print("   chat → END")
    print("="*50)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        run_interactive()
    elif len(sys.argv) > 1 and sys.argv[1] == "--compare":
        # Comparison mode - show how different methods classify the same inputs
        print("🔬 CLASSIFICATION METHOD COMPARISON")
        print("="*50)
        
        test_messages = [
            "Are you free tomorrow?",
            "What's your favorite color?", 
            "I need to learn about Python",
            "Can you help me organize my day?",
            "Schedule a meeting with John",
            "Find information about climate change",
            "How are you doing today?",
            "Look up the weather forecast",
            "Set up a call for next week"
        ]
        
        for msg in test_messages:
            compare_classification_methods(msg)
        
        print(f"\n💡 Current agent uses: {CLASSIFICATION_METHOD.upper()} classification")
        print("   Change CLASSIFICATION_METHOD variable to switch methods")
        
    elif len(sys.argv) > 1 and sys.argv[1] == "--visualize":
        print("🎨 PERSONAL AGENT GRAPH VISUALIZATION")
        print("="*50)
        visualize_graph()
        print("\n💡 To see this in LangGraph Studio:")
        print("   1. Run: langgraph up")
        print("   2. Open: http://localhost:3000") 
        print("   3. Select: personal_agent")
        
    elif len(sys.argv) > 1 and sys.argv[1] == "--debug":
        print("🔍 PERSONAL AGENT DEBUG MODE")
        print("="*50)
        debug_graph_structure()
        visualize_graph()
        
    else:
        # Test 1: Calendar query (natural language)
        print("=== Test 1: Calendar Query (Natural Language) ===")
        init_state = {"messages": [{"role": "user", "content": "Do you have any openings this week for a quick chat?"}],
                      "tool_result": None, "tool_name": None}
        out = agent.invoke(init_state)
        print("User:", init_state["messages"][0]["content"])
        print("Agent:", out["messages"][-1]["content"])
        show_execution_summary(cast(AgentState, out))
        print()
        
        # Test 2: Web search query (natural language)
        print("=== Test 2: Web Search Query (Natural Language) ===")
        init_state2 = {"messages": [{"role": "user", "content": "I need to learn more about machine learning algorithms"}],
                       "tool_result": None, "tool_name": None}
        out2 = agent.invoke(init_state2)
        print("User:", init_state2["messages"][0]["content"])
        print("Agent:", out2["messages"][-1]["content"])
        show_execution_summary(cast(AgentState, out2))
        print()
        
        # Test 3: General chat
        print("=== Test 3: General Chat ===")
        init_state3 = {"messages": [{"role": "user", "content": "What's your favorite color?"}],
                       "tool_result": None, "tool_name": None}
        out3 = agent.invoke(init_state3)
        print("User:", init_state3["messages"][0]["content"])
        print("Agent:", out3["messages"][-1]["content"])
        show_execution_summary(cast(AgentState, out3))
        
        # Test 4: Edge case - ambiguous query
        print("\n=== Test 4: Edge Case - Ambiguous Query ===")
        init_state4 = {"messages": [{"role": "user", "content": "Can you help me organize my day?"}],
                       "tool_result": None, "tool_name": None}
        out4 = agent.invoke(init_state4)
        print("User:", init_state4["messages"][0]["content"])
        print("Agent:", out4["messages"][-1]["content"])
        show_execution_summary(cast(AgentState, out4))
        
        print("\n" + "="*50)
        print("💡 Available modes:")
        print("   python src/email_assistant/personal_agent.py                 # Run test cases")
        print("   python src/email_assistant/personal_agent.py --interactive   # Interactive chat")
        print("   python src/email_assistant/personal_agent.py --compare       # Compare classification methods")
        print("   python src/email_assistant/personal_agent.py --visualize     # Show graph structure")
        print("   python src/email_assistant/personal_agent.py --debug         # Debug graph structure")
        print("   langgraph up                                                 # Start LangGraph Studio")