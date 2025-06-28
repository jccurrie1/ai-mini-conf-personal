"""
Recipe Request Triage Agent

This agent takes user input and uses an LLM to determine if it's a food recipe request or not.
It also maintains memory of user food preferences.
"""

from typing import Literal, List, Dict, Any, Optional
from pydantic import BaseModel, Field

from langchain.chat_models import init_chat_model
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage

from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.store.base import BaseStore

# ===============================
# SCHEMAS AND STATE
# ===============================

class FoodPreferences(BaseModel):
    """Updated user food preferences based on user's interactions."""
    chain_of_thought: str = Field(description="Reasoning about which food preferences need to add/update if required")
    food_preferences: str = Field(description="Updated user food preferences including dietary restrictions, favorite cuisines, ingredients they like/dislike, cooking skill level, etc.")

class TriageState(MessagesState):
    """State for the triage workflow."""
    classification: str
    user_input: str  
    triage_result: str

# ===============================
# MEMORY MANAGEMENT
# ===============================

def get_food_preferences(store: BaseStore, namespace, default_content=None):
    """Get food preferences from the store or initialize with default if it doesn't exist.
    
    Args:
        store: LangGraph BaseStore instance to search for existing memory
        namespace: Tuple defining the memory namespace, e.g. ("recipe_assistant", "food_preferences")
        default_content: Default content to use if memory doesn't exist
        
    Returns:
        str: The content of the food preferences, either from existing memory or the default
    """
    # Search for existing memory with namespace and key
    user_food_prefs = store.get(namespace, "food_preferences")
    
    # If memory exists, return its content (the value)
    if user_food_prefs:
        return user_food_prefs.value
    
    # If memory doesn't exist, add it to the store and return the default content
    else:
        # Namespace, key, value
        store.put(namespace, "food_preferences", default_content or "")
        user_food_prefs = default_content or ""
    
    # Return the default content
    return user_food_prefs

def update_food_preferences(store: BaseStore, namespace, messages, current_preferences):
    """Update food preferences in the store.
    
    Args:
        store: LangGraph BaseStore instance to update memory
        namespace: Tuple defining the memory namespace, e.g. ("recipe_assistant", "food_preferences")
        messages: List of messages to update the memory with
        current_preferences: Current food preferences to build upon
    """
    # Create the memory update prompt
    memory_update_prompt = f"""
    Based on the user's interaction, update their food preferences profile.
    
    Current food preferences: {current_preferences}
    
    Instructions:
    1. Analyze the conversation to identify any food preferences, dietary restrictions, or cooking preferences
    2. Update the food preferences profile to include new information
    3. Keep existing preferences unless they are contradicted by new information
    4. Include information about:
       - Favorite cuisines and dishes
       - Dietary restrictions or allergies
       - Ingredients they like or dislike
       - Cooking skill level and preferences
       - Meal types they prefer (quick meals, elaborate dishes, etc.)
    
    Return the updated food preferences as a comprehensive profile.
    """
    
    # Update the memory using structured output
    llm = init_chat_model("gpt-4.1", temperature=0.0).with_structured_output(FoodPreferences)
    result = llm.invoke(
        [
            {"role": "system", "content": memory_update_prompt},
        ] + messages
    )
    
    # Save the updated memory to the store
    # Handle the structured output result properly
    if hasattr(result, 'food_preferences'):
        updated_preferences = result.food_preferences
    elif isinstance(result, dict) and 'food_preferences' in result:
        updated_preferences = result['food_preferences']
    else:
        updated_preferences = str(result)
    
    store.put(namespace, "food_preferences", updated_preferences)

# Default food preferences
DEFAULT_FOOD_PREFERENCES = """
User food preferences: Not yet established. 
Dietary restrictions: None specified.
Favorite cuisines: None specified.
Cooking skill level: Not specified.
Preferred meal types: Not specified.
"""

# ===============================
# TRIAGE NODE
# ===============================

def triage_request(state: TriageState, store: BaseStore):
    """Analyze user input and determine if it's a food recipe request."""
    
    # Initialize the LLM
    llm = init_chat_model("gpt-4.1", temperature=0)
    
    # Get food preferences from memory
    food_preferences = get_food_preferences(
        store, 
        ("recipe_assistant", "food_preferences"), 
        DEFAULT_FOOD_PREFERENCES
    )
    
    user_message = None
    for message in reversed(state["messages"]):
        if isinstance(message, HumanMessage):
            user_message = message.content
            break
    
    if not user_message:
        return {
            "classification": "not_recipe_request",
            "triage_result": "No user input found",
        }
    
    print(f"DEBUG: User message: {user_message}")
    print(f"DEBUG: Current food preferences: {food_preferences}")
    
    # Create triage prompt with food preferences context
    triage_prompt = f"""
    Analyze the following user input and determine if it is a food recipe request:
    
    User Input: "{user_message}"
    
    User's Food Preferences: {food_preferences}
    
    Determine if this is a food recipe request. This includes:
    - Asking for a specific recipe
    - Requesting cooking instructions
    - Asking for meal suggestions or recommendations
    - Requesting cooking advice or tips
    - Asking about ingredients or cooking methods
    - Any food-related cooking request
    - Expressing food preferences or dietary needs
    
    Respond with:
    Category: recipe_request OR not_recipe_request
    Analysis: [brief explanation of why you classified it this way]
    """
    
    # Get LLM response
    response = llm.invoke([HumanMessage(content=triage_prompt)])
    
    # Convert response content to string
    response_text = str(response.content)
    print(f"DEBUG: LLM triage response: {response_text}")
    
    # Extract category from response - improved logic
    category = "not_recipe_request"  # Default to not a recipe request
    
    # More robust classification - check for recipe-related keywords
    recipe_keywords = [
        'recipe', 'cook', 'bake', 'prepare', 'ingredients', 'meal', 'dish', 
        'food', 'kitchen', 'eat', 'dinner', 'lunch', 'breakfast', 'dessert',
        'sauce', 'soup', 'salad', 'bread', 'cake', 'cookies', 'pasta',
        'vegetarian', 'vegan', 'gluten-free', 'allergic', 'diet', 'cuisine'
    ]
    
    # Check the user message directly for recipe keywords
    user_lower = str(user_message).lower() if user_message else ""
    has_recipe_keywords = any(keyword in user_lower for keyword in recipe_keywords)
    
    # Also check the LLM response
    response_lower = response_text.lower()
    llm_says_recipe = 'recipe_request' in response_lower and 'not_recipe_request' not in response_lower
    
    # Classify as recipe request if either condition is met
    if has_recipe_keywords or llm_says_recipe:
        category = "recipe_request"
        
        # Update food preferences if this is a recipe request
        update_food_preferences(
            store,
            ("recipe_assistant", "food_preferences"),
            [{"role": "user", "content": user_message}],
            food_preferences
        )
    
    print(f"DEBUG: Has recipe keywords: {has_recipe_keywords}")
    print(f"DEBUG: LLM says recipe: {llm_says_recipe}")
    print(f"DEBUG: Final classification: {category}")
    
    return {
        "classification": category,
        "user_input": user_message,
        "triage_result": response_text,
        "messages": [AIMessage(content=f"Triage complete. Category: {category}\n\nAnalysis: {response_text}")]
    }

# ===============================
# RECIPE GENERATION NODE
# ===============================

def generate_recipe(state: TriageState, store: BaseStore):
    """Generate a recipe based on the user's request and their food preferences."""
    
    # Initialize the LLM
    llm = init_chat_model("gpt-4.1", temperature=0)
    
    # Get the user's original message
    user_message = state.get("user_input", "")
    
    # Get food preferences from memory
    food_preferences = get_food_preferences(
        store, 
        ("recipe_assistant", "food_preferences"), 
        DEFAULT_FOOD_PREFERENCES
    )
    
    # Create recipe generation prompt with personalized preferences
    recipe_prompt = f"""
    The user has requested a food recipe. Please provide a helpful, detailed recipe response that takes into account their preferences.
    
    User Request: "{user_message}"
    
    User's Food Preferences: {food_preferences}
    
    Please provide:
    1. A clear recipe title
    2. List of ingredients with measurements
    3. Step-by-step cooking instructions
    4. Cooking time and serving information
    5. Any helpful tips or variations
    6. Consider the user's dietary restrictions and preferences when suggesting the recipe
    
    Make your response friendly, clear, and easy to follow. Personalize the recipe based on their known preferences.
    """
    
    # Get LLM response
    response = llm.invoke([HumanMessage(content=recipe_prompt)])
    print(response)
    
    # Update food preferences based on the recipe interaction
    update_food_preferences(
        store,
        ("recipe_assistant", "food_preferences"),
        [
            {"role": "user", "content": user_message},
            {"role": "assistant", "content": str(response.content)}
        ],
        food_preferences
    )
    
    return {
        "messages": [AIMessage(content=str(response.content))]
    }

# ===============================
# CONDITIONAL ROUTING
# ===============================

def route_after_triage(state: TriageState) -> Literal["generate_recipe", "__end__"]:
    """Route based on triage classification."""
    classification = state.get("classification", "not_recipe_request")
    
    if classification == "recipe_request":
        return "generate_recipe"
    else:
        return "__end__"

# ===============================
# WORKFLOW CONSTRUCTION
# ===============================

def create_triage_agent():
    """Create and compile the triage agent with memory support."""
    
    # Create the workflow
    workflow = StateGraph(TriageState)
    
    # Add nodes (store parameter will be passed automatically by LangGraph)
    workflow.add_node("triage", triage_request)
    workflow.add_node("generate_recipe", generate_recipe)
    
    # Set up the flow with conditional routing
    workflow.add_edge(START, "triage")
    workflow.add_conditional_edges(
        "triage",
        route_after_triage,
        {
            "generate_recipe": "generate_recipe",
            "__end__": END,
        },
    )
    workflow.add_edge("generate_recipe", END)
    
    # Compile with memory support (store will be injected by LangGraph)
    return workflow.compile()

# Create the agent instance for LangGraph dev
email_assistant = create_triage_agent()

