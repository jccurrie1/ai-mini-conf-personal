import streamlit as st
from langchain_core.messages import HumanMessage, BaseMessage

# Import the triage + recipe agent
from email_assistant.recipe_maker import email_assistant as recipe_agent

st.set_page_config(page_title="Recipe Assistant", page_icon="🍳")
st.title("🍳 Personal Grocery List Assistant")

# -----------------------------------------------------------------------------
# Sidebar – user preferences
# -----------------------------------------------------------------------------

with st.sidebar:
    st.header("Preferences")
    default_store = st.session_state.get("grocery_store", "Walmart")

    store_options = [
        "Walmart",
        "Kroger",
        "Whole Foods",
        "Trader Joe's",
        "Costco",
        "Aldi",
        "Other",
    ]

    # Select or enter the preferred grocery store
    store_choice = st.selectbox("Preferred grocery store", store_options, index=store_options.index(default_store) if default_store in store_options else len(store_options) - 1)

    if store_choice == "Other":
        store_choice = st.text_input("Enter store name", value=st.session_state.get("grocery_store_custom", ""))
        st.session_state.grocery_store_custom = store_choice

    # Persist the chosen store across reruns
    st.session_state.grocery_store = store_choice

    # ---------------------------------------------------------------------
    # Food & nutrition preferences form
    # ---------------------------------------------------------------------

    st.subheader("Food & Nutrition Preferences")

    likes = st.text_area(
        "Foods you like (comma-separated)",
        value=st.session_state.get("likes", ""),
        placeholder="e.g., salmon, broccoli, brown rice",
        height=80,
    )
    st.session_state.likes = likes.strip()

    dislikes = st.text_area(
        "Foods you dislike (comma-separated)",
        value=st.session_state.get("dislikes", ""),
        placeholder="e.g., cilantro, mushrooms",
        height=80,
    )
    st.session_state.dislikes = dislikes.strip()

    dietary = st.text_input(
        "Dietary restrictions / lifestyle", 
        value=st.session_state.get("dietary", ""),
        placeholder="e.g., vegetarian, gluten-free, nut allergy",
    )
    st.session_state.dietary = dietary.strip()

    caloric_goal = st.number_input(
        "Daily caloric goal (kcal)",
        min_value=0,
        value=int(st.session_state.get("caloric_goal", 0)) if isinstance(st.session_state.get("caloric_goal", 0), (int, float)) else 0,
        step=50,
    )
    st.session_state.caloric_goal = int(caloric_goal)

    price_goal = st.number_input(
        "Weekly grocery budget ($)",
        min_value=0,
        value=int(st.session_state.get("price_goal", 0)) if isinstance(st.session_state.get("price_goal", 0), (int, float)) else 0,
        step=5,
    )
    st.session_state.price_goal = int(price_goal)

    # Display a quick summary so the user can see what is currently stored
    st.markdown("### Current Preferences Summary")
    st.markdown(
        f"""
        • **Likes:** {st.session_state.likes or '–'}  
        • **Dislikes:** {st.session_state.dislikes or '–'}  
        • **Dietary:** {st.session_state.dietary or '–'}  
        • **Caloric goal:** {st.session_state.caloric_goal if st.session_state.caloric_goal > 0 else '–'} kcal  
        • **Weekly budget:** {('$' + str(st.session_state.price_goal)) if st.session_state.price_goal > 0 else '–'}
        """
    )

# -----------------------------------------------------------------------------
# Session-level state helpers
# -----------------------------------------------------------------------------
if "agent" not in st.session_state:
    # Keep the compiled LangGraph agent alive across reruns so that its internal
    # memory store (which tracks the user's food preferences) is preserved.
    st.session_state.agent = recipe_agent

if "chat_history" not in st.session_state:
    # Initialize chat history list (annotation removed for compatibility with st.session_state)
    st.session_state.chat_history = []

# -----------------------------------------------------------------------------
# Display chat history so far
# -----------------------------------------------------------------------------
for msg in st.session_state.chat_history:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user"):
            st.markdown(msg.content)
    else:
        # Treat everything that is not a HumanMessage as coming from the agent
        with st.chat_message("assistant"):
            st.markdown(msg.content)

# -----------------------------------------------------------------------------
# Input box at the bottom of the chat
# -----------------------------------------------------------------------------
user_input = st.chat_input("Ask me for cooking ideas, recipes, or tips…")

if user_input:
    # -------------------------------------------------------------------------
    # 1) Add the user message to the chat history
    # -------------------------------------------------------------------------
    # Append the user's preferred grocery store to the message so the agent can
    # take it into account when generating a grocery list and pricing.
    store_info = st.session_state.get("grocery_store", "")

    # Consolidate preference details
    pref_parts = []
    if st.session_state.get("likes"):
        pref_parts.append(f"I like {st.session_state.likes}.")
    if st.session_state.get("dislikes"):
        pref_parts.append(f"I dislike {st.session_state.dislikes}.")
    if st.session_state.get("dietary"):
        pref_parts.append(f"My dietary restrictions: {st.session_state.dietary}.")
    if st.session_state.get("caloric_goal", 0) > 0:
        pref_parts.append(f"My daily caloric goal is {int(st.session_state.caloric_goal)} kcal.")
    if st.session_state.get("price_goal", 0) > 0:
        pref_parts.append(f"My weekly grocery budget is ${int(st.session_state.price_goal)}.")

    pref_text = " ".join(pref_parts)

    augmented_user_input = (
        f"{user_input}\n\nMy preferred grocery store is {store_info}. {pref_text} Please use these preferences when generating recipes and estimating costs."
    )

    human_msg = HumanMessage(content=augmented_user_input)
    st.session_state.chat_history.append(human_msg)

    # Render the user message immediately so the interface feels responsive
    with st.chat_message("user"):
        st.markdown(user_input)

    # -------------------------------------------------------------------------
    # 2) Invoke the LangGraph agent
    # -------------------------------------------------------------------------
    with st.spinner("Thinking…"):
        result = st.session_state.agent.invoke({"messages": st.session_state.chat_history})

    # The agent always returns its new messages under the "messages" key.
    assistant_messages = result.get("messages", [])

    # Safeguard for when a single BaseMessage is returned instead of a list
    if isinstance(assistant_messages, BaseMessage):
        assistant_messages = [assistant_messages]

    # -------------------------------------------------------------------------
    # 3) Append assistant messages to history and render them
    # -------------------------------------------------------------------------
    for a_msg in assistant_messages:
        st.session_state.chat_history.append(a_msg)
        with st.chat_message("assistant"):
            st.markdown(a_msg.content)

    # Optionally, show debug info such as classification / triage result
    if "classification" in result:
        with st.expander("Debug – Agent metadata", expanded=False):
            st.write({k: v for k, v in result.items() if k != "messages"}) 