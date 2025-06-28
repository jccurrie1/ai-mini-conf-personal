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
    augmented_user_input = (
        f"{user_input}\n\nMy preferred grocery store is {store_info}. Please use typical prices from this store when estimating costs."
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