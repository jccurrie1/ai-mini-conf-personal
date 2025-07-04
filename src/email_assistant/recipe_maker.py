"""
Recipe Request Triage Agent

This agent takes user input and uses an LLM to determine if it's a food recipe request or not.
It also maintains memory of user food preferences.
"""

from typing import Literal, List, Dict, Any, Optional, cast
from pydantic import BaseModel, Field

from langchain.chat_models import init_chat_model
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage

from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.store.base import BaseStore
from langchain.storage import LocalFileStore  # NEW: lightweight on-disk store persisting to folder

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

def _compose_key(namespace: tuple, key: str) -> str:
    """Convert a namespace tuple + key into the flat string format expected by
    `LocalFileStore` (and other `BaseStore` implementations that operate on
    simple string keys). For example, `(\"recipe_assistant\", \"prefs\")` and
    ``food_preferences`` becomes ``recipe_assistant/prefs/food_preferences``.
    """
    if isinstance(namespace, (list, tuple)):
        return "/".join([*namespace, key])
    # Fallback – if the caller passed a single string as the namespace
    return f"{namespace}/{key}"

def get_food_preferences(store: BaseStore, namespace, default_content=None):
    """Get food preferences from the store or initialize with default if it doesn't exist.
    
    Args:
        store: LangGraph BaseStore instance to search for existing memory
        namespace: Tuple defining the memory namespace, e.g. ("recipe_assistant", "food_preferences")
        default_content: Default content to use if memory doesn't exist
        
    Returns:
        str: The content of the food preferences, either from existing memory or the default
    """
    if store is None:
        return default_content or ""

    # ------------------------------------------------------------------
    # Try the modern BaseStore API (mget/mset) first.  If the store happens
    # to expose the legacy `get`/`put` helpers we fall back to those so that
    # other store implementations (e.g. RedisStore) keep working unchanged.
    # ------------------------------------------------------------------
    full_key = _compose_key(namespace, "food_preferences")

    user_food_prefs = None

    if hasattr(store, "mget"):
        try:
            result_bytes = store.mget([full_key])[0]  # type: ignore[attr-defined]
            if result_bytes is not None:
                user_food_prefs = result_bytes.decode()
        except Exception:
            # Silent failure – we'll handle by initialising below
            user_food_prefs = None
    elif hasattr(store, "get"):
        # Legacy two-argument API
        try:
            pref_obj = store.get(namespace, "food_preferences")
            if pref_obj:
                user_food_prefs = pref_obj.value if hasattr(pref_obj, "value") else str(pref_obj)
        except Exception:
            user_food_prefs = None

    # If found, return it immediately
    if user_food_prefs is not None:
        return user_food_prefs

    # ------------------------------------------------------------------
    # Preference not found – initialise using the provided default.
    # ------------------------------------------------------------------
    initial = default_content or ""

    if hasattr(store, "mset"):
        try:
            store.mset([(full_key, initial.encode())])  # type: ignore[attr-defined]
        except Exception:
            pass  # Non-critical – continue without persistence
    elif hasattr(store, "put"):
        try:
            store.put(namespace, "food_preferences", initial)  # type: ignore[arg-type]
        except Exception:
            pass

    return initial

def update_food_preferences(store: BaseStore, namespace, messages, current_preferences):
    """Update food preferences in the store.
    
    Args:
        store: LangGraph BaseStore instance to update memory
        namespace: Tuple defining the memory namespace, e.g. ("recipe_assistant", "food_preferences")
        messages: List of messages to update the memory with
        current_preferences: Current food preferences to build upon
    """
    # If no store was provided, skip the update entirely.
    if store is None:
        return

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
    
    # Extract the structured field (handles both object + dict variants)
    if hasattr(result, "food_preferences"):
        updated_preferences = result.food_preferences  # type: ignore[attr-defined]
    elif isinstance(result, dict) and "food_preferences" in result:
        updated_preferences = result["food_preferences"]
    else:
        updated_preferences = str(result)
    
    # Persist the updated preferences – tolerate stores that only implement
    # the modern `mset` API.
    full_key = _compose_key(namespace, "food_preferences")

    if hasattr(store, "mset"):
        try:
            store.mset([(full_key, updated_preferences.encode())])  # type: ignore[attr-defined]
        except Exception:
            pass
    elif hasattr(store, "put"):
        try:
            store.put(namespace, "food_preferences", updated_preferences)  # type: ignore[arg-type]
        except Exception:
            pass

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
    """Analyze user input and determine if it's a weekly grocery list request or a food preference."""
    
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
            "classification": "not_grocery_list_request",
            "triage_result": "No user input found",
        }
    
    print(f"DEBUG: User message: {user_message}")
    print(f"DEBUG: Current food preferences: {food_preferences}")
    
    # Create triage prompt with food preferences context
    triage_prompt = f"""
    Analyze the following user input and determine if it is a weekly grocery list request (rather than a single recipe request).

    User Input: "{user_message}"

    User's Food Preferences: {food_preferences}

    Treat the following as a grocery list request:
    - Asking for a grocery or shopping list for the week
    - Requesting ingredients to buy for upcoming meals
    - Asking what to purchase based on dietary goals or restrictions
    - Any question focused on compiling ingredients rather than cooking instructions
    - Expressing food preferences or dietary needs and asking what to buy

    Respond with:
    Category: grocery_list_request OR not_grocery_list_request
    Analysis: [brief explanation of why you classified it this way]
    """
    
    # Get LLM response
    response = llm.invoke([HumanMessage(content=triage_prompt)])
    
    # Convert response content to string
    response_text = str(response.content)
    print(f"DEBUG: LLM triage response: {response_text}")
    
    # Extract category from response - improved logic
    category = "not_grocery_list_request"  # Default to not a grocery list request
    
    # More robust classification - check for recipe-related keywords
    recipe_keywords = [
        # Keywords indicating a grocery/shopping list request or meal planning
        'grocery', 'shopping list', 'shopping', 'grocery list', 'store list', 'buy', 'purchase',
        # Keywords retained from recipe/meal context to capture broader food planning phrasing
        'ingredients', 'meal plan', 'meal', 'dish', 'food', 'kitchen', 'eat', 'dinner',
        'lunch', 'breakfast', 'vegetarian', 'vegan', 'gluten-free', 'allergic', 'diet', 'cuisine'
    ]
    
    # Check the user message directly for recipe keywords
    user_lower = str(user_message).lower() if user_message else ""
    has_recipe_keywords = any(keyword in user_lower for keyword in recipe_keywords)
    
    # Also check the LLM response
    response_lower = response_text.lower()
    llm_says_recipe = 'grocery_list_request' in response_lower and 'not_grocery_list_request' not in response_lower
    
    # Detect explicit preference updates, e.g. "I like lemons", "I'm allergic to peanuts"
    preference_update_phrases = [
        "i like", "i love", "i prefer", "my favorite", "i hate", "i don't like",
        "i dislike", "i am allergic", "i'm allergic", "allergic to", "i cannot eat",
        "i can't eat", "i am vegan", "i'm vegan", "i am vegetarian", "i'm vegetarian",
        "gluten-free", "dairy-free", "nut-free", "egg-free"
    ]
    has_preference_update = any(phrase in user_lower for phrase in preference_update_phrases)
    
    # Classify request
    if has_recipe_keywords or llm_says_recipe:
        category = "grocery_list_request"
        # Update food preferences if this is a grocery list request
        update_food_preferences(
            store,
            ("recipe_assistant", "food_preferences"),
            [{"role": "user", "content": user_message}],
            food_preferences
        )
    elif has_preference_update:
        category = "preference_update"
        # Directly update user preferences from this statement
        update_food_preferences(
            store,
            ("recipe_assistant", "food_preferences"),
            [{"role": "user", "content": user_message}],
            food_preferences
        )
    else:
        category = "not_grocery_list_request"
    
    print(f"DEBUG: Has recipe keywords: {has_recipe_keywords}")
    print(f"DEBUG: LLM says recipe: {llm_says_recipe}")
    print(f"DEBUG: Has preference update: {has_preference_update}")
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
    """Generate a weekly grocery list based on the user's request, food preferences, and dietary goals."""
    
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
    
    # Create grocery list generation prompt with personalized preferences and meal-building framework
    recipe_prompt = f"""
    The user would like a WEEKLY GROCERY LIST. Please generate a comprehensive shopping list that aligns with their preferences, dietary restrictions, and goals.

    User Request: "{user_message}"

    User's Food Preferences & Dietary Info: {food_preferences}

    Use Ethan Chlebowski's Meal-Building Framework as guidance for ingredient selection:
    1. Base (grains, noodles, breads, greens)
    2. Protein (animal, plant, eggs)
    3. Vegetables (crisp, leafy, roasted)
    4. Aromatics (alliums, ginger/chilies, herbs & spices)
    5. Sauce / Seasoning (homemade, store-bought, DIY ratios)
    6. Garnish & Extras (fresh herbs, crunch, acid)

    Instructions:
    • Curate ingredients so the user can easily assemble balanced meals by picking one from each category above.
    • Organize the grocery list by supermarket section (Produce, Proteins, Pantry, Dairy & Eggs, Frozen, Miscellaneous).
    • Provide quantities appropriate for ONE WEEK (assume ~14 meals). Adjust based on any dietary goals or household size mentioned by the user.
    • Where possible, suggest batch-prep tactics (e.g., bulk-cook grains, freeze portions of sauce, prep proteins in advance).
    • For each ingredient, include an estimated price in USD. If the user has specified a preferred grocery store (e.g., "My preferred grocery store is Costco"), base your estimate on typical prices for that store; otherwise use a reasonable U.S. national average price.
    • After the grocery list, add an "=== Estimated Cost Summary ===" section that lists a subtotal for every grocery section and a final total estimated cost for the entire week.

    Output format:
    === Grocery List ===
    Produce:
    - …
    Proteins:
    - …
    Pantry / Dry Goods:
    - …
    (continue as needed)

    === Estimated Cost Summary ===
    Produce subtotal: $...
    Proteins subtotal: $...
    (continue as needed)
    Total estimated cost: $...

    === Meal Ideas ===
    • Base + Protein + Vegetables + Aromatics + Sauce example …
    (List at least 5 flexible meal ideas that only rely on ingredients from the grocery list.)
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

def route_after_triage(state: TriageState) -> Literal["generate_recipe", "acknowledge_preferences", "__end__"]:
    """Route based on triage classification."""
    classification = state.get("classification", "not_grocery_list_request")
    
    if classification == "grocery_list_request":
        return "generate_recipe"
    elif classification == "preference_update":
        return "acknowledge_preferences"
    else:
        return "__end__"

# ===============================
# ACKNOWLEDGEMENT NODE
# ===============================

def acknowledge_preferences(state: TriageState, store: BaseStore):
    """Simple acknowledgement after updating user preferences."""
    food_preferences = get_food_preferences(
        store,
        ("recipe_assistant", "food_preferences"),
        DEFAULT_FOOD_PREFERENCES,
    )
    return {
        "messages": [
            AIMessage(
                content=(
                    "Got it. I've updated your food preferences. "
                    "Here is your current preference profile:\n\n" + str(food_preferences)
                )
            )
        ]
    }

# ===============================
# WORKFLOW CONSTRUCTION
# ===============================

def create_triage_agent(store: BaseStore | None = None):
    """Create and compile the triage agent.

    Args:
        store: Optional persistent ``BaseStore`` implementation.  If ``None``
            (the default) we fall back to a lightweight on-disk
            ``LocalFileStore`` located in the current working directory.  This
            gives you out-of-the-box persistence without running an external
            database server.
    """

    # If no store was supplied, keep a single folder-based store alongside the
    # project so memory survives interpreter restarts.
    if store is None:
        store = cast(BaseStore, LocalFileStore(".recipe_assistant_store"))  # type: ignore[arg-type]

    # Build the graph
    workflow = StateGraph(TriageState)

    # Add nodes (LangGraph will automatically inject ``store`` into any node
    # that declares a ``store: BaseStore`` parameter)
    workflow.add_node("triage", triage_request)
    workflow.add_node("generate_recipe", generate_recipe)
    workflow.add_node("acknowledge_preferences", acknowledge_preferences)

    # Set up the flow with conditional routing
    workflow.add_edge(START, "triage")
    workflow.add_conditional_edges(
        "triage",
        route_after_triage,
        {
            "generate_recipe": "generate_recipe",
            "acknowledge_preferences": "acknowledge_preferences",
            "__end__": END,
        },
    )
    workflow.add_edge("generate_recipe", END)
    workflow.add_edge("acknowledge_preferences", END)

    # Compile with memory support
    return workflow.compile(store=store)

# Create the agent instance for LangGraph dev
email_assistant = create_triage_agent()

