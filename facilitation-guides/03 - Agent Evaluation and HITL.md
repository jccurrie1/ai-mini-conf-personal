## Agent Evaluation and Human-in-the-Loop (`evaluation.ipynb` and `hitl.ipynb`)

**Goal:** Learn how to systematically evaluate agent performance and implement human oversight for sensitive actions in production AI systems.

### Introduction
- Start by explaining that we'll cover two critical aspects of production agent systems:
  1. **Evaluation**: How to test and validate agent behavior
  2. **Human-in-the-Loop (HITL)**: How to add human oversight for sensitive operations
- Emphasize that these are essential for building trustworthy AI systems in production

## Part 1: Agent Evaluation (`evaluation.ipynb`)

### 1. Why Evaluate Agents?
- **Talking Point:** "When building agents, we need quantifiable metrics to ensure they're working correctly."
- **Key Metrics to Track:**
  - Response quality
  - Token usage and costs
  - Latency
  - Classification accuracy
  - Tool call correctness
- **Concept:** Different types of outputs require different evaluation strategies:
  - Structured outputs (classifications, tool calls) → Exact match comparisons
  - Unstructured outputs (email responses) → LLM-as-judge evaluation

### 2. Evaluation Approaches
- **Two Main Methods with LangSmith:**
  1. **Pytest Integration**: For developers familiar with traditional testing
  2. **LangSmith Datasets**: For collaborative team evaluation
- Show the "eval.png" image to visualize the evaluation flow

### 3. Setting Up Test Cases
- **Dataset Structure** (`eval/email_dataset.py`):
  ```python
  test_case = {
      "email_input": "The actual email content...",
      "classification": "Respond",  # Expected: Respond/Notify/Ignore
      "tool_calls": ["check_calendar_availability", "schedule_meeting"],
      "success_criteria": "What makes a good response..."
  }
  ```
- **Talking Point:** "We need diverse test cases covering different email types and expected behaviors."

### 4. Pytest Integration
- **Code Reference (Basic Structure):**
  ```python
  @pytest.mark.langsmith
  @pytest.mark.parametrize("email_input, expected_calls", test_data)
  def test_email_dataset_tool_calls(email_input, expected_calls):
      # Run the agent
      result = email_assistant.invoke({"messages": messages})
      
      # Extract tool calls
      tool_calls = extract_tool_calls(result['messages'])
      
      # Verify expectations
      missing_calls = [call for call in expected_calls 
                      if call.lower() not in tool_calls]
      
      # Log to LangSmith
      t.log_outputs({"tool_calls": tool_calls})
      
      assert len(missing_calls) == 0
  ```
- **Key Point:** "The `@pytest.mark.langsmith` decorator automatically logs results to LangSmith for tracking."

### 5. Unit Testing Specific Components
- **Testing the Triage Router:**
  ```python
  def target_triage_router(inputs: dict) -> dict:
      response = email_assistant.nodes['triage_router'].invoke({
          "email_input": inputs["email_input"]
      })
      return {"classification_decision": response.update['classification_decision']}
  
  def classification_evaluator(outputs: dict, reference_outputs: dict) -> bool:
      return outputs["classification_decision"].lower() == reference_outputs["classification"].lower()
  ```
- **Talking Point:** "We can test individual nodes in isolation for more granular evaluation."

### 6. LLM-as-Judge Evaluation
- **Concept:** Use an LLM to evaluate subjective qualities of responses
- Show the "eval_detail.png" image
- **Code Reference (Structured Evaluation):**
  ```python
  class CriteriaGrade(BaseModel):
      justification: str = Field(description="The justification")
      grade: bool = Field(description="Does it meet criteria?")
  
  # Create evaluator
  criteria_llm = llm.with_structured_output(CriteriaGrade)
  
  # Evaluate response
  eval_result = criteria_llm.invoke([
      {"role": "system", "content": CRITERIA_PROMPT},
      {"role": "user", "content": f"Criteria: {success_criteria}..."}
  ])
  ```
- **Key Point:** "This allows us to evaluate subjective qualities like tone, completeness, and appropriateness."

### 7. Running Full Test Suites
- **LangSmith Dataset Evaluation:**
  ```python
  experiment_results = client.evaluate(
      target_email_assistant,
      data=dataset_name,
      evaluators=[classification_evaluator, tool_evaluator],
      experiment_prefix="Email assistant v2"
  )
  ```
- **Viewing Results:**
  - Show how to access experiment results in LangSmith UI
  - Demonstrate comparing different versions
  - **Talking Point:** "LangSmith gives us a dashboard to track performance over time and compare experiments."

### 8. Evaluation Best Practices
- **Key Takeaways:**
  1. Test at multiple levels (unit and integration)
  2. Use exact match for structured outputs
  3. Use LLM-as-judge for subjective evaluation
  4. Create diverse, realistic test cases
  5. Track metrics over time
- Show the "test_result.png" image

## Part 2: Human-in-the-Loop (`hitl.ipynb`)

### 1. Why HITL?
- **Talking Point:** "Even well-tested agents need human oversight for sensitive actions."
- **Scenarios Requiring HITL:**
  - Sending emails on behalf of users
  - Scheduling meetings
  - Making financial transactions
  - Any irreversible action
- Show the "hitl_schematic.png" image

### 2. HITL Architecture Overview
- **Two Interrupt Points:**
  1. **After Triage**: When emails are classified as "notify"
  2. **Before Tool Execution**: For sensitive tools
- Show the "HITL_flow.png" image
- **Key Concept:** "We interrupt the graph at specific points and wait for human input."

### 3. Implementing Interrupts
- **Basic Interrupt Pattern:**
  ```python
  from langgraph.types import interrupt
  
  # Create interrupt request
  request = {
      "action_request": {
          "action": "schedule_meeting",
          "args": {
              "attendees": ["boss@company.com"],
              "duration": 30,
              "topic": "Project update"
          }
      },
      "config": {
          "allow_accept": True,
          "allow_edit": True,
          "allow_ignore": True,
          "allow_respond": True
      },
      "description": "Schedule a meeting with your boss"
  }
  
  # Interrupt and wait for response
  response = interrupt([request])[0]
  ```
- **Talking Point:** "The interrupt gives users four options: accept, edit, ignore, or respond with feedback."

### 4. HITL Tools vs Safe Tools
- **Categorization:**
  ```python
  HITL_TOOLS = ["write_email", "schedule_meeting", "Question"]
  SAFE_TOOLS = ["check_calendar_availability", "Done"]
  ```
- **Interrupt Handler Logic:**
  ```python
  def interrupt_handler(state):
      for tool_call in state["messages"][-1].tool_calls:
          if tool_call["name"] in HITL_TOOLS:
              # Create interrupt
              response = interrupt([create_request(tool_call)])
              # Process response...
          else:
              # Execute immediately
              result = tools[tool_call["name"]].invoke(tool_call["args"])
  ```

### 5. Response Types
- **Accept**: Execute tool as-is
  ```python
  graph.stream(Command(resume=[{"type": "accept"}]), config)
  ```
- **Edit**: Modify arguments
  ```python
  graph.stream(Command(resume=[{
      "type": "edit", 
      "args": {"args": {"duration": 60}}  # Changed from 30
  }]), config)
  ```
- **Ignore**: Skip tool execution
  ```python
  graph.stream(Command(resume=[{"type": "ignore"}]), config)
  ```
- **Respond**: Provide feedback
  ```python
  graph.stream(Command(resume=[{
      "type": "response", 
      "args": {"response": "Make it 2 hours and more formal"}
  }]), config)
  ```

### 6. The Question Tool
- **Concept:** Allow agents to ask clarifying questions
- **Implementation:**
  ```python
  @tool
  class Question(BaseModel):
      """Question to ask user."""
      content: str
  ```
- **Talking Point:** "This creates a bidirectional conversation when the agent needs more information."

### 7. LangGraph Studio Integration
- **Demonstrate in Studio:**
  1. Run the HITL agent with an email requiring action
  2. Show the graph pausing at interrupt points
  3. Demonstrate different response types
  4. Show state updates after each response
- Show the "studio-interrupt.png" image
- **Key Point:** "Studio makes it easy to test and debug HITL flows during development."

### 8. Agent Inbox UI
- **Concept:** Production UI for managing interrupts
- Show the "agent-inbox.png", "agent-inbox-draft.png", and "agent-inbox-edit.png" images
- **Features:**
  - Queue of pending approvals
  - Edit interface for tool arguments
  - Feedback mechanism
  - Thread history view
- **Talking Point:** "In production, users interact through a dedicated UI, not through code."

### 9. HITL Best Practices
1. **Minimize Interrupts**: Only for truly sensitive actions
2. **Clear Descriptions**: Help users understand what they're approving
3. **Sensible Defaults**: Pre-populate with agent's suggestions
4. **Feedback Loop**: Allow users to guide the agent
5. **Audit Trail**: Log all human decisions

### Conclusion
- **Recap Key Concepts:**
  - Evaluation ensures agents work correctly before deployment
  - HITL adds necessary human oversight for sensitive actions
  - Both are essential for production AI systems
- **Integration:** "These concepts work together - good evaluation identifies where HITL is needed."
- **Next Steps:** "Now we'll add memory to help agents learn from human feedback over time."

### Practical Exercise (Optional)
If time permits, have participants:
1. Write a test case for a new email scenario
2. Add a new tool that requires HITL
3. Test the interrupt flow in LangGraph Studio
4. Discuss: "What other actions in your applications would need human approval?"