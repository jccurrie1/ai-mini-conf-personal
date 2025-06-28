import streamlit as st
from langchain_core.messages import HumanMessage, BaseMessage

# Import the triage + recipe agent
from email_assistant.recipe_maker import email_assistant as recipe_agent

st.set_page_config(page_title="Recipe Assistant", page_icon="🍳")
st.title("🍳 Personal Recipe Assistant")

# -----------------------------------------------------------------------------
# Session-level state helpers
# -----------------------------------------------------------------------------
if "agent" not in st.session_state:
    # Keep the compiled LangGraph agent alive across reruns so that its internal
    # memory store (which tracks the user's food preferences) is preserved.
    st.session_state.agent = recipe_agent

if "chat_history" not in st.session_state:
    # We keep the full chat history so that it can be sent back to the agent on
    # each turn and also rendered in the UI.
    st.session_state.chat_history: list[BaseMessage] = []

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
    human_msg = HumanMessage(content=user_input)
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