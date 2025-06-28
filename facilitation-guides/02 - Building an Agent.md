## Building an Email Assistant (`agent.ipynb`)

**Goal:** Apply LangGraph concepts to build a more complex email assistant with routing and multiple tools.

### Introduction
-   Reiterate that you're building an email assistant from scratch, focusing on agent architecture, testing, human-in-the-loop, and memory.
-   Show the "overview.png" image.
-   **Setup:**
    -   Load environment variables.
    -   **Code Reference:**
        ```python
        from dotenv import load_dotenv
        load_dotenv("../.env")
        ```

### 1. Tool Definition
-   **Concept:** Define tools specific to the email assistant.
-   **Code Reference:**
    ```python
    from typing import Literal
    from datetime import datetime
    from pydantic import BaseModel
    from langchain_core.tools import tool

    @tool
    def write_email(to: str, subject: str, content: str) -> str: ...
    @tool
    def schedule_meeting(attendees: list[str], subject: str, ...) -> str: ...
    @tool
    def check_calendar_availability(day: str) -> str: ...
    @tool
    class Done(BaseModel):
          """E-mail has been sent."""
          done: bool
    ```
-   **Talking Point:** Explain each tool's purpose and highlight the `Done` tool as a Pydantic model for signaling completion.

### 2. Building the Email Assistant
-   Refer to the "email_workflow.png" diagram. Explain it's a combination of a router and an agent.

#### A. Router (Triage Logic)
-   **Purpose:** Handles the initial decision: ignore, notify, or respond to an email.
-   **State:**
    -   Introduce a custom `State` object that extends `MessagesState` to include `email_input` and `classification_decision`.
    -   **Code Reference:**
        ```python
        from langgraph.graph import MessagesState

        class State(MessagesState):
            email_input: dict
            classification_decision: Literal["ignore", "respond", "notify"]
        ```
-   **Triage Node (`triage_router`):**
    -   **Modular Prompts:**
        -   Explain the use of `%autoreload` to access prompts from `email_assistant`. This promotes reusability.
        -   **Code Reference (Imports):**
            ```python
            %load_ext autoreload
            %autoreload 2
            from email_assistant.prompts import triage_system_prompt, triage_user_prompt, ...
            ```
        -   Show the content of `triage_system_prompt`, `triage_user_prompt`, `default_background`, and `default_triage_instructions` to give context.
    -   **Structured Output:**
        -   Use a Pydantic model (`RouterSchema`) with `llm.with_structured_output()` for the triage decision.
        -   **Code Reference (RouterSchema):**
            ```python
            class RouterSchema(BaseModel):
                """Analyze the unread email and route it according to its content."""
                reasoning: str = Field(...)
                classification: Literal["ignore", "respond", "notify"] = Field(...)
            ```
            -   **Emphasis:** "The descriptions in the pydantic model are important because they get passed as part of JSON schema to the LLM to inform the output coercion."
    -   **Triage Function Logic:**
        -   **Code Reference (`triage_router` function):**
            ```python
            llm = init_chat_model("openai:gpt-4.1", temperature=0.0)
            llm_router = llm.with_structured_output(RouterSchema)

            def triage_router(state: State) -> Command[Literal["response_agent", "__end__"]]:
                # ... parse_email, format prompts ...
                result = llm_router.invoke([...])
                if result.classification == "respond":
                    goto = "response_agent"
                    update = { "messages": [...], "classification_decision": result.classification }
                # ... elif for "ignore" and "notify" ...
                return Command(goto=goto, update=update)
            ```
        -   **Key Point:** Explain how `Command(goto=..., update=...)` is used to direct the flow to the `response_agent` or `END`, and to update the state with the classification decision and initial message for the agent.

#### B. Agent (Response Logic)
-   **Purpose:** If the router decides to "respond," this agent handles crafting the response using tools.
-   **LLM Node (`llm_call`):**
    -   **System Prompt:**
        -   Show `AGENT_TOOLS_PROMPT` and `agent_system_prompt`.
        -   **Code Reference (Imports):**
            ```python
            from email_assistant.tools.default.prompt_templates import AGENT_TOOLS_PROMPT
            from email_assistant.prompts import agent_system_prompt, ...
            ```
        -   **Emphasis:** Highlight the placeholders in `agent_system_prompt` (e.g., `{tools_prompt}`, `{background}`).
    -   **LLM and Tool Binding:**
        -   Collect all tools: `tools = [write_email, schedule_meeting, check_calendar_availability, Done]`.
        -   Initialize LLM and bind tools with `tool_choice="any"` to enforce tool use.
        -   **Code Reference (`llm_call` function):**
            ```python
            tools_by_name = {tool.name: tool for tool in tools}
            llm = init_chat_model("openai:gpt-4.1", temperature=0.0)
            llm_with_tools = llm.bind_tools(tools, tool_choice="any")

            def llm_call(state: State):
                return { "messages": [ llm_with_tools.invoke([... + state["messages"]]) ]}
            ```
-   **Tool Handler Node (`tool_handler`):**
    -   **Purpose:** Executes the tool chosen by the `llm_call` node.
    -   **Code Reference (`tool_handler` function):**
        ```python
        def tool_handler(state: dict):
            result = []
            for tool_call in state["messages"][-1].tool_calls:
                tool = tools_by_name[tool_call["name"]]
                observation = tool.invoke(tool_call["args"])
                result.append({"role": "tool", "content" : observation, "tool_call_id": tool_call["id"]})
            return {"messages": result}
        ```
-   **Conditional Routing (`should_continue`):**
    -   **Purpose:** Determines if the agent should continue using tools or terminate (if the `Done` tool is called).
    -   **Code Reference (`should_continue` function):**
        ```python
        def should_continue(state: State) -> Literal["tool_handler", "__end__"]:
            last_message = state["messages"][-1]
            if last_message.tool_calls:
                for tool_call in last_message.tool_calls:
                    if tool_call["name"] == "Done":
                        return END
                    else:
                        return "tool_handler"
            # This case might need adjustment if LLM can respond without tool call
            # For now, with tool_choice="any", it should usually have a tool_call
        ```
-   **Agent Graph Assembly:**
    -   Combine `llm_call`, `tool_handler`, and `should_continue` into a `StateGraph`.
    -   **Code Reference:**
        ```python
        from langgraph.graph import StateGraph, START, END
        # ...
        overall_workflow = StateGraph(State)
        overall_workflow.add_node("llm_call", llm_call)
        overall_workflow.add_node("tool_handler", tool_handler)
        overall_workflow.add_edge(START, "llm_call")
        overall_workflow.add_conditional_edges("llm_call", should_continue, {"tool_handler": "tool_handler", END: END})
        overall_workflow.add_edge("tool_handler", "llm_call")
        agent = overall_workflow.compile()
        ```
    -   **Visualize:** `show_graph(agent)`

#### C. Combine Router Workflow with Response Agent
-   **Purpose:** Create the final, complete email assistant.
-   **Code Reference:**
    ```python
    overall_workflow = (
        StateGraph(State)
        .add_node("triage_router", triage_router) # Changed from direct function call to node name
        .add_node("response_agent", agent)
        .add_edge(START, "triage_router")
        # Conditional routing from triage_router is handled by its Command output
    ).compile()
    ```
   - **Note:** The `triage_router` uses `Command(goto=...)`, so explicit edges from `triage_router` to `response_agent` or `END` are not added here; LangGraph handles it.
-   **Visualize:** `show_graph(overall_workflow, xray=True)`
    -   **Emphasis:** The `xray=True` will show the internal structure of the `response_agent` subgraph.

### 3. Testing the Combined Workflow
-   **Example 1 (Notify):**
    -   **Code Reference (Email Input):**
        ```python
        email_input = {
            "author": "System Admin <sysadmin@company.com>",
            # ... (scheduled maintenance email)
        }
        response = overall_workflow.invoke({"email_input": email_input})
        # ... pretty_print messages (if any) ...
        ```
    -   **Expected Output:** `🔔 Classification: NOTIFY - This email contains important information`
-   **Example 2 (Respond):**
    -   **Code Reference (Email Input):**
        ```python
        email_input = {
          "author": "Alice Smith <alice.smith@company.com>",
          # ... (API documentation question email)
        }
        response = overall_workflow.invoke({"email_input": email_input})
        for m in response["messages"]:
            m.pretty_print()
        ```
    -   **Expected Output Walkthrough:**
        -   `📧 Classification: RESPOND - This email requires a response`
        -   Human Message (formatted input for the agent).
        -   AI Message (with `write_email` tool call).
        -   Tool Message (result of `write_email`).
        -   AI Message (with `Done` tool call).

### 4. Testing with Local Deployment (LangGraph Studio)
-   **File Location:** Point out that the agent code is in `src/email_assistant/email_assistant.py`.
-   **Running Studio:** Remind them to run `langgraph dev` in the terminal.
-   **Testing in Studio:**
    -   Use the same "API documentation question" email as input.
    -   Show the "studio.png" image as a reference.
    -   **Emphasis:** Demonstrate how Studio visualizes the graph execution, including the triage step and then the agent's internal loop.
-   **Final Invocation in Notebook (after Studio demo):**
    -   Run the same `email_input` again through `overall_workflow.invoke` and print messages to confirm behavior.

### Conclusion
-   Summarize how a sophisticated agent with routing and multiple tools was built using LangGraph.
-   Briefly mention that the next steps in a full workshop would be testing with LangSmith, human-in-the-loop, and adding memory (which are typical follow-ons but not detailed in this specific set of notebook cells/transcript for *building*).

This guide should provide a solid structure for you to facilitate the workshop. Remember to engage with participants, answer questions, and encourage them to experiment with the code.
