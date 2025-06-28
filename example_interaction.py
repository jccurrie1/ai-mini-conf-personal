#!/usr/bin/env python3
"""
Example script showing how to interact with the recipe recommendation agent
"""

from src.email_assistant.recipe_maker import create_recipe_agent
from langgraph.checkpoint.memory import MemorySaver
from langgraph.store.memory import InMemoryStore

def main():
    # Create the agent with memory
    checkpointer = MemorySaver()
    store = InMemoryStore()
    
    # Note: For this example, we'd need to modify the agent to accept store/checkpointer
    # The current agent is designed for langgraph dev environment
    agent = create_recipe_agent()
    
    # Example interaction
    config = {"configurable": {"thread_id": "example_user"}}
    
    # Send a message
    initial_state = {
        "messages": [{"role": "user", "content": "I want something quick for dinner"}]
    }
    
    print("🍳 Recipe Agent Interaction Example")
    print("=" * 40)
    print("Input:", initial_state["messages"][0]["content"])
    print()
    
    try:
        # Run the agent
        result = agent.invoke(initial_state, config=config)
        print("Agent Response:")
        for message in result["messages"]:
            if message["role"] == "assistant":
                print(f"🤖 {message['content']}")
        
        print("\n✨ In the real Agent Inbox, you'd now see an interactive prompt")
        print("   where you can accept, reject, or provide feedback on the recipes!")
        
    except Exception as e:
        print(f"Note: This example requires the full LangGraph environment.")
        print(f"Error: {e}")
        print("\n🚀 To interact properly, use 'langgraph dev' + Agent Inbox!")

if __name__ == "__main__":
    main() 