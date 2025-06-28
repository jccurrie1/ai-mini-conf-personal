## Memory and Advanced Features (`memory.ipynb`)

**Goal:** Transform the email assistant into a self-improving system that learns from user feedback, creating personalized experiences that get better over time.

### Introduction
- Start by explaining that we'll add long-term memory to our email assistant, enabling it to learn from HITL feedback
- Emphasize that this transforms a reactive system into one that actively improves and personalizes itself
- Show the "overview_memory.png" image to visualize the complete system

### 1. Memory Types in LangGraph
- **Thread-Scoped vs. Long-term Memory:**
  - **Thread-scoped (Short-term)**: Conversation history within a single thread, managed automatically
  - **Long-term (Across-thread)**: Persistent knowledge that spans sessions, stored in memory store
  - Show the "short-vs-long.png" image to illustrate the difference
- **Key Concept:** "Thread-scoped memory enables coherent conversations, while long-term memory enables learning and personalization."

### 2. LangGraph Store Implementation
- **Store Options:**
  1. **InMemoryStore**: Python dict, no persistence (notebooks)
  2. **Local dev**: Pickled to filesystem (langgraph dev)
  3. **Production**: PostgreSQL with pgvector
- **Memory Organization:**
  ```python
  # Namespaces are tuples that organize memories
  namespace = (user_id, "memories")
  namespace = ("email_assistant", "triage_preferences")
  ```
- **Basic Operations:**
  ```python
  # Save memory with UUID
  memory_id = str(uuid.uuid4())
  store.put(namespace, memory_id, {"preference": "value"})
  
  # Or save with fixed key (used in our implementation)
  store.put(namespace, "user_preferences", "preference content")
  
  # Retrieve memory
  memory = store.get(namespace, "user_preferences")
  if memory:
      memory_value = memory.value
  ```
- **Talking Point:** "Namespaces are like folders - they help organize different types of memories for efficient retrieval."

### 3. Memory Categories for Email Assistant
- **Three Memory Types:**
  1. **Triage Preferences**: Which emails to respond/notify/ignore
  2. **Calendar Preferences**: Meeting duration, timing preferences
  3. **Response Preferences**: Email tone, style, structure
- **Show defaults for each category:**
  - Display `default_triage_instructions`, `default_cal_preferences`, `default_response_preferences`
  - **Emphasis:** "These defaults are starting points - the system will personalize them based on user feedback."

### 4. Memory Management Functions
- **Helper Functions:**
  ```python
  def get_memory(store, namespace, default_content=None):
      """Get memory or initialize with default"""
      user_preferences = store.get(namespace, "user_preferences")
      if user_preferences:
          return user_preferences.value
      else:
          store.put(namespace, "user_preferences", default_content)
          return default_content
  ```
- **Key Design Decision:** Start with string-based memory for simplicity
- **Talking Point:** "We fetch existing memory or create it with defaults - this ensures the system always has preferences to work with."

### 5. Intelligent Memory Updates
- **The Challenge:** How to update memory based on user feedback without overwriting everything
- **Solution:** Use LLM with careful prompting
- **Show `MEMORY_UPDATE_INSTRUCTIONS` prompt:**
  - Emphasize the key instructions: "NEVER overwrite entire profile", "ONLY targeted additions"
  - Point out the XML delimiters and structured reasoning steps
- **Update Function:**
  ```python
  def update_memory(store, namespace, messages):
      # Get existing memory
      current = store.get(namespace, "user_preferences")
      
      # Use LLM to intelligently update
      llm = init_chat_model("openai:gpt-4.1").with_structured_output(UserPreferences)
      result = llm.invoke([system_prompt] + messages)
      
      # Save updated memory
      store.put(namespace, "user_preferences", result.user_preferences)
  ```
- **Talking Point:** "The LLM analyzes the feedback and current preferences to make surgical updates - adding new information while preserving existing knowledge."

### 6. Memory Integration Points
- **Triage Router:**
  - Retrieves triage preferences to inform classification decisions
  - Updates when user overrides classifications
- **LLM Call Node:**
  - Injects calendar and response preferences into system prompt
  - Ensures all responses align with learned preferences
- **Interrupt Handlers:**
  - Capture user feedback (edits, natural language, ignores)
  - Trigger appropriate memory updates based on feedback type

### 7. Memory Update Triggers
- **Four Types of Feedback → Memory Updates:**
  1. **Triage Override**: User responds to "notify" → Update triage preferences
  2. **Tool Edits**: User modifies proposals → Update relevant preferences
  3. **Natural Language**: User provides text feedback → Parse and update
  4. **Ignore Actions**: User ignores proposals → Learn what to avoid
- **Code Example (Edit Handler):**
  ```python
  if response["type"] == "edit":
      # Execute with edited args
      observation = tool.invoke(edited_args)
      
      # Update memory based on what was edited
      if tool_call["name"] == "schedule_meeting":
          update_memory(store, ("email_assistant", "cal_preferences"), [{
              "role": "user",
              "content": f"User edited: {initial} → {edited}. Extract preferences."
          }])
  ```

### 8. Testing Memory Learning
- **Three Test Scenarios:**
  1. **Accept without changes**: No memory updates (no learning signal)
  2. **Edit tool calls**: Specific changes → Generalizable preferences
  3. **Natural language feedback**: Unstructured input → Structured preferences
- **Demonstration Flow:**
  - Run same email through multiple times
  - Show memory state after each interaction
  - Highlight how preferences evolve
- **Key Examples:**
  - Edit 45→30 minutes: Learns "prefer 30-minute meetings"
  - Feedback "after 2pm": Adds "afternoon meetings preferred"
  - Edit to shorter email: Learns communication style preference

### 9. Viewing Memory Evolution
- **Helper Function:**
  ```python
  def display_memory_content(store, namespace=None):
      # Shows current memory state
      memory = store.get(namespace, "user_preferences")
      if memory:
          print(f"--- {namespace[1]} ---")
          print(memory.value)
  ```
- **Live Demo:** Show how memory changes with each interaction type
- **Talking Point:** "Watch how the system doesn't just record your edits - it extracts the underlying preferences and generalizes them."

### 10. Local Deployment with Memory
- **LangGraph Studio Memory Tab:**
  - Show the "memory-studio.png" image
  - Navigate to Memory tab in Studio
  - Demonstrate real-time memory updates
  - **Emphasis:** "You can see exactly what the system is learning about you."
- **Testing Email:**
  ```json
  {
    "author": "Alice Smith <alice.smith@company.com>",
    "subject": "Quick question about API documentation",
    "email_thread": "Could you help clarify if missing endpoints were intentional?"
  }
  ```

### 11. Production Deployment
- **Gmail Integration:**
  - Real email processing with `email_assistant_hitl_memory_gmail.py`
  - OAuth setup for Gmail access
  - Cron scheduling for automated checking
- **LangGraph Platform:**
  - One-click deployment from GitHub
  - Built-in task queues for scaling
  - Persistent PostgreSQL storage
  - **Live Demo:** Deploy and test with actual email

### 12. Advanced Memory Patterns
- **Namespace Design:**
  - Work backwards from where memory is needed
  - Separate namespaces for different preference types
  - Enable multi-user support with user-specific namespaces
- **Memory Search:**
  - Configure semantic search with embeddings
  - Enable similarity-based retrieval
  - Reference LangMem for advanced patterns
- **Best Practices:**
  - Never overwrite entire memories
  - Test with diverse interaction patterns
  - Monitor for preference drift
  - Consider privacy implications

### Conclusion
- **Recap the transformation:**
  - Started with stateless email assistant
  - Added evaluation for quality assurance
  - Integrated HITL for human oversight
  - Now added memory for continuous learning
- **The Complete System:**
  - Learns from every interaction
  - Personalizes behavior per user
  - Improves accuracy over time
  - Maintains user control
- **Key Takeaway:** "Memory transforms AI from a tool that follows instructions to a partner that learns your preferences."

### Practical Exercise (Optional)
If time permits, have participants:
1. Run the email assistant with different feedback patterns
2. Observe memory updates in real-time
3. Test how learned preferences affect future interactions
4. Discuss: "What other types of preferences could the system learn?"

### Q&A Topics to Prepare For
- How to handle conflicting preferences
- Privacy and data retention policies
- Scaling to thousands of users
- Integration with existing preference systems
- Memory decay and forgetting old preferences