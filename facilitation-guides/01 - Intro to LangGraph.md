## LangGraph 101 (`langgraph_101.ipynb`)

**Goal:** Introduce the fundamental concepts of LangChain, LangGraph, tool calling, and basic agent/workflow construction.

### Introduction
- Start by explaining that this notebook covers the basics of LangGraph, which is a framework for building applications with LLMs.
- Mention that it will show how LangGraph works with LangChain and LangSmith.
- Show the "ecosystem.png" image to visually place LangGraph.

### 1. Chat Models
- **Concept:** Introduce Chat Models as the foundation of LLM applications. They take a list of messages as input and return a message as output.
- **LangChain Interface:**
	- Explain that LangChain provides a standardized interface for chat models, making it easy to use different providers.
	- **Code Reference:**
		```python
        from dotenv import load_dotenv
        load_dotenv("../.env", override=True)
        ```
		```python
        from langchain.chat_models import init_chat_model
        llm = init_chat_model("openai:gpt-4.1", temperature=0)
        ```
	- **Talking Point:** Emphasize how `init_chat_model` simplifies connecting to various LLMs.
- **Running the Model:**
	- Explain the `invoke()` method for a single input-output transformation. Mention `stream()` for streaming outputs.
	- **Code Reference:**
		```python
        result = llm.invoke("What is LangGraph?")
        ```
	- **Emphasis:** Show the `type(result)` (AIMessage) and `result.content` to demonstrate the model's response.

### 2. Tools
- **Concept:** Introduce Tools as utilities that can be called by a chat model.
- **Creating Tools in LangChain:**
	- Explain the `@tool` decorator, which transforms Python functions into callable tools. It infers the tool's name, description, and arguments.
	- **Code Reference (Tool Definition):**
		```python
        from langchain.tools import tool

        @tool
        def write_email(to: str, subject: str, content: str) -> str:
            """Write and send an email."""
            # Placeholder response - in real app would send email
            return f"Email sent to {to} with subject '{subject}' and content: {content}"
        ```
	- **Emphasis:**
		- Show `type(write_email)` (StructuredTool).
		- Show `write_email.args` and `write_email.description` to demonstrate how LangChain infers these from the function definition.
		- **Talking Point:** "This is how we create a tool very easily from any Python function."

### 3. Tool Calling
- **Concept:** Explain that LLMs can choose to call tools by returning a structured output with tool arguments. This is a central principle for agents.
- **Binding Tools:**
	- Use the `bind_tools` method to augment an LLM with tools.
	- Show the "tool_call_detail.png" image.
	- Mention parameters like `tool_choice` (e.g., "any" to select at least one tool) and `parallel_tool_calls=False` (to call one tool at a time).
	- **Code Reference (Binding and Invoking):**
		```python
        # Connect tools to a chat model
        model_with_tools = llm.bind_tools([write_email], tool_choice="any", parallel_tool_calls=False)

        # The model will now be able to call tools
        output = model_with_tools.invoke("Draft a response to my boss about tomorrow's meeting")
        ```
- **Executing Tool Calls:**
	- Show how to extract arguments from `output.tool_calls[0]['args']`.
	- **Code Reference (Executing the tool):**
		```python
        # Call the tool
        result = write_email.invoke(args)
        print(result)
        ```
	- **Key Talking Point:** "LLMs produce tool calls. That tool call is a structured output. We can pass that tool call to the tool itself to run the tool. This `write_email` tool in the real world... could be like the Gmail API."
	- Show the "tool_call.png" image.

### 4. Workflows vs. Agents
- **Workflows:**
	- **Concept:** Pre-defined code paths where LLMs make decisions at certain steps. Useful when control flow can be defined in advance.
	- Show the "workflow_example.png" image.
	- **Talking Point:** "If you can easily draw ahead of time the control flow that you want, workflow's fine. You don't need an agent."
- **Agents:**
	- **Concept:** LLMs dynamically direct their own tool usage in a loop. The output of each tool call informs the next action. Good for open-ended problems where steps aren't predictable.
	- Show the "agent_example.png" image.
	- **Talking Point:** "Agents are good if you actually need more flexible decision making at run time. You can't predict what actually you need in terms of tool calls."
- Show the "workflow_v_agent.png" image comparing agency and predictability.

### 5. What is LangGraph?
- **Concept:** LangGraph is a framework to help build applications with LLMs. It provides low-level supporting infrastructure.
- **Benefits:**
	1. **Control:** Define and combine agents/workflows.
	2. **Persistence:** Persist graph state (for memory, human-in-the-loop).
	3. **Testing, Debugging, and Deployment:** Easy onramp.
- **LangChain, LangGraph, LangSmith Connection:**
	- **LangChain:** Standard interfaces for components (e.g., chat models).
	- **LangGraph:** Orchestration; can use LangChain abstractions within nodes.
	- **LangSmith:** Observability and testing for any workflow.
	- **Talking Point:** "Within these nodes [in LangGraph], you can very easily have, for example, a LangChain chat model."

### 6. LangGraph: Control
- **Core Components:**
	1. **State:** Information to track. (Typically a dictionary, dataclass, or Pydantic object).
	2. **Nodes:** Units of work (Python functions) that modify the state.
	3. **Edges:** Transitions between nodes.
- Show the "nodes_edges.png" image.
- **Simple Graph Example:**
	- **State Definition:**
		```python
        from typing import TypedDict
        from langgraph.graph import StateGraph, START, END

        class StateSchema(TypedDict):
            request: str
            email: str

        workflow = StateGraph(StateSchema)
        ```
	- **Node Definition:**
		- Explain that nodes receive the current state and return a dictionary to update the state. By default, state keys are overwritten.
		```python
        def write_email_node(state: StateSchema) -> StateSchema:
            # Imperative code that processes the request
            output = model_with_tools.invoke(state["request"])
            args = output.tool_calls[0]['args']
            email = write_email.invoke(args)
            return {"email": email}
        ```
	- **Adding Nodes and Edges:**
		```python
        workflow = StateGraph(StateSchema)
        workflow.add_node("write_email_node", write_email_node)
        workflow.add_edge(START, "write_email_node")
        workflow.add_edge("write_email_node", END)

        app = workflow.compile()
        ```
	- **Invoking the Graph:**
		```python
        app.invoke({"request": "Draft a response to my boss about tomorrow's meeting"})
        ```
		- **Emphasis:** Show the initial state (`request`) and how the `email` key is populated in the final state.
- **Conditional Edges:**
	- **Concept:** Allow routing between nodes based on a condition. The function returns the name of the next node.
	- **Modifying State:** Introduce `MessagesState` (pre-built state that appends messages to a `messages` key).
	- **Node Definitions (Split into `call_llm` and `run_tool`):**
		```python
        from typing import Literal
        from langgraph.graph import MessagesState
        # ...
        def call_llm(state: MessagesState) -> MessagesState: # ...
        def run_tool(state: MessagesState): # ...
        ```
		- **Talking Point:** Explain how `call_llm` appends the AI message (with tool call) and `run_tool` appends the Tool message to the `messages` list in the state.
	- **Conditional Edge Function:**
		```python
        def should_continue(state: MessagesState) -> Literal["run_tool", END]:
            # ... checks last_message.tool_calls ...
            if last_message.tool_calls:
                return "run_tool"
            return END
        ```
	- **Building the Graph with Conditional Edge:**
		```python
        workflow = StateGraph(MessagesState)
        workflow.add_node("call_llm", call_llm)
        # ... add_node("run_tool", run_tool) ...
        workflow.add_conditional_edges("call_llm", should_continue, {"run_tool": "run_tool", END: END})
        # ... add_edge("run_tool", END) ...
        app = workflow.compile()
        ```
	- **Visualization:**
		```python
        from email_assistant.utils import show_graph # Assuming this is in the repo
        show_graph(app)
        ```
		- **Emphasis:** Point out the conditional branch in the visualized graph.
	- **Invoking and Inspecting Messages:**
		```python
        result = app.invoke({"messages": [{"role": "user", "content": "Draft a response to my boss..."}]})
        for m in result["messages"]:
            m.pretty_print()
        ```
		- **Emphasis:** Walk through the `messages` list (Human, AI with tool_call, Tool) to show the flow.
- **Pre-built Agent (`create_react_agent`):**
	- **Concept:** LangGraph provides a pre-built abstraction for common agent patterns (ReAct).
	- **Code Reference:**
		```python
        from langgraph.prebuilt import create_react_agent

        agent = create_react_agent(
            model=llm,
            tools=[write_email],
            prompt="Respond to the user's request using the tools provided."
        )
        result = agent.invoke({"messages": [{"role": "user", "content": "Draft a response..."}]})
        # ... pretty_print messages ...
        ```
	- **Key Difference:** "Previously, we sent [the tool result and] then we end. Now the tool message is sent back to the LLM. The LLM looks and says tool call is made and responds with a message... They continue calling tools until no tool is called, and they end."

### 7. LangGraph: Persistence
- **Concept:** Allows agents to pause, save state, and resume. Useful for long-running tasks and human-in-the-loop.
- **Checkpointers:** Save a checkpoint of the graph state at every step to a thread.
- Show the "checkpoints.png" image.
- **Example with `InMemorySaver`:**
	- **Code Reference (Compiling with checkpointer):**
		```python
        from langgraph.checkpoint.memory import InMemorySaver

        agent = create_react_agent(
            model=llm,
            tools=[write_email],
            prompt="...",
            checkpointer=InMemorySaver()
        )
        ```
	- **Using Thread ID for Conversation:**
		```python
        config = {"configurable": {"thread_id": "1"}}
        result = agent.invoke({"messages": [...]}, config)
        # ...
        state = agent.get_state(config) # Show current state
        # ...
        result = agent.invoke({"messages": [{"role": "user", "content": "Good, let's use lesson 3..."}]}, config) # Continue conversation
        ```
		- **Emphasis:** Show how the conversation history is maintained across invocations using the same `thread_id`.
- **Interrupts:**
	- **Concept:** Stop graph execution at specific points, often to collect user input.
	- **Code Reference (Graph with Interrupt):**
		```python
        from langgraph.types import Command, interrupt
        # ...
        class State(TypedDict): # ... input, user_feedback
        def human_feedback(state):
            print("---human_feedback---")
            feedback = interrupt("Please provide feedback:")
            return {"user_feedback": feedback}
        # ... build graph with step_1, human_feedback, step_3 nodes ...
        graph = builder.compile(checkpointer=memory)
        ```
	- **Visualizing:** `show_graph(graph)`
	- **Running to Interrupt:**
		```python
        # Run the graph until the first interruption
        for event in graph.stream(initial_input, thread, stream_mode="updates"):
            print(event)
        ```
		- **Emphasis:** Show the output indicating the graph is waiting for feedback.
	- **Resuming from Interrupt:**
		- Use the `Command` object with `resume`.
		```python
        # Continue the graph execution
        for event in graph.stream(
            Command(resume="go to step 3!"),
            thread,
            stream_mode="updates",
        ):
            print(event)
        ```
		- **Emphasis:** Show how the provided feedback is incorporated. "This interrupt resume mechanism... is a very simple, powerful way to stop our graph... and say, hey. Give me feedback."

### 8. LangGraph: Testing, Debugging, and Deployment
- **LangSmith Integration:**
	- **Setup:** Explain that setting `LANGSMITH_TRACING=true` and `LANGSMITH_API_KEY` enables out-of-the-box tracing.
	- **Demonstration:**
		- Open the provided LangSmith trace URL (e.g., `https://smith.langchain.com/public/6f77014f-d054-44ed-aa2c-8b06ceab689f/r`).
		- **Walkthrough:**
			- Show the overall agent trace.
			- Click into the `call_model` node.
			- Inspect the LLM call: show the tools bound, the full message history input to the model, and the resulting tool call.
			- Show the tool execution node and the final agent output.
			- **Talking Point:** "I like this model [of debugging]. I use this all the time."
- **LangGraph Platform (Local Deployment & Studio):**
	- **Concept:** Easily deploy LangGraph applications.
	- **Project Structure:** Briefly explain the required structure (`my-app/`, `src/`, `langgraph.json`, `pyproject.toml`).
	- `langgraph.json`: Specifies graphs to include.
	- **Local Deployment:**
		- Explain running `langgraph dev` in the repo's root directory.
		- This starts a local server and LangGraph Studio.
	- **LangGraph Studio:**
		- Navigate to the `langgraph101` graph in Studio (if `langgraph dev` is running).
		- Input a message (e.g., "Draft a response to my boss...").
		- **Emphasis:**
			- Show each node lighting up as it executes.
			- On the right, show the state at each step.
			- **Talking Point:** "I use this all the time for debugging and for inspecting my graphs. You can see very nicely in Studio. You get a good visualization of what happened."
		- Show the "langgraph_studio.png" image.

### Conclusion of LangGraph 101
- **Recap:** Briefly summarize the key learnings:
	- Chat models and tool calling.
	- Workflows vs. Agents.
	- LangGraph basics: State, Nodes, Edges, Conditional Edges.
	- Building agents with pre-built abstractions.
	- Persistence and Interrupts.
	- LangSmith for observability.
	- LangGraph Studio for local development and debugging.
- **Transition:** "This sets up everything we need... to build everything else we're gonna build in this workshop."

