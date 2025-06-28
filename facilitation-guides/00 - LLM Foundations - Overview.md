# Session 0 – LLM Foundations & Prompt Engineering – Overview

## Session Purpose and Context

Before we dive into LangGraph and agents, participants need a **hands-on refresher on working with Large Language Models as a developer**. This kick-off session bridges the gap between _asking an LLM for help_ and **writing precise code (prompts) that drive a probabilistic function**, ready to be composed inside real software.

The concrete objective is to implement a _name-matching micro-service_ powered by the OpenAI Chat Completions API. Students will:

1. Call the OpenAI API directly with the `openai` Python SDK.
2. Craft an effective **system prompt** using modern prompting patterns (step-by-step reasoning, **JSON structured output**, etc.).
3. Parse the structured response and return deterministic Python objects.
4. Make the provided unit test (`tests/test_employee_matcher.py`) pass by filling in just one constant – the `SYSTEM_PROMPT`.

This small but complete workflow—prompt → LLM call → structured output → parse → return—gives learners the baseline mental model required for the later LangGraph sessions.

### Why Start Here?

Many developers have used LLMs through chat interfaces or AI-assisted coding tools, but building **reliable systems** with LLMs requires a different mindset:

- **Deterministic Behavior**: Using `temperature=0` and structured outputs for predictable results
- **Test-Driven Development**: Writing prompts that pass unit tests, not just "look good"
- **Cost Consciousness**: Understanding model selection and token usage
- **Error Handling**: Dealing with malformed outputs and API failures
- **Iterative Refinement**: Systematically improving prompts based on test failures

---

## Core Conceptual Framework

### 1. Thinking of LLMs as Functions

```
result = openai.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[{"role": "system", "content": SYSTEM_PROMPT}, …],
    temperature=0,
)
```

- **Inputs**: a list of messages (system / user / assistant).
- **Output**: exactly **one** assistant message.
- **Determinism lever**: `temperature=0` for test-friendly behaviour.
- **Cost lever**: choose a cheap model (`gpt-4.1-mini` is the default).

### 2. Prompt Anatomy

1. **System prompt** – sets global rules, required format, reasoning approach.
2. **User prompt** – contains dynamic task data (CSV list + target string).

Key prompting techniques introduced here:

- _Explicit format instructions_ → demand a **pure JSON object** with top-level key `matches` (array of `{empId, empName}`) — enforced via the JSON Schema passed to `response_format`.
- _Step-by-step reasoning_ → bullet or numbered reasoning inside a dedicated tag.
- _Few-shot examples_ → at least one full demonstration showing input ⟶ output.
- _Caps-lock imperatives_ to prevent drifting: "**Respond ONLY with the JSON object – no extra text**".

### 3. Structured-Output Contracts

Why we prefer XML / JSON over plain text:

- reliable parsing ⇒ robust software
- easier evaluation ⇒ simple unit tests
- future-proofing ⇒ can swap LLM without changing downstream code

### 4. Minimal Parsing Logic

The supplied scaffold shows a **tiny `json.loads` parser**. Behind the scenes, the call passes a **full JSON Schema** in `response_format` so the model is _constrained_ to emit:

```jsonc
{
  "matches": [
    { "empId": 27, "empName": "Bacon, Patrick" }
    // ... more candidates
  ]
}
```

See the [OpenAI Structured Outputs deep-dive](https://community.openai.com/t/structured-outputs-deep-dive/930169) for details.

---

## Pedagogical Approach

### Why Name Matching?

This exercise was carefully chosen because it:

1. **Requires Precise Understanding**: The LLM must parse instructions about name order correctly
2. **Has Clear Success Criteria**: Tests pass or fail – no ambiguity
3. **Introduces Real Challenges**:
   - Ambiguous inputs ("jco" could match multiple people)
   - Format constraints (JSON-only output)
   - Edge cases (case sensitivity, partial matches)
4. **Mirrors Real-World Tasks**: Many business applications need fuzzy matching
5. **Scales in Complexity**: From simple exact matches to sophisticated fuzzy logic

### Learning Through Failure

The exercise is designed so that students' first attempts will likely fail. This is intentional:

- **First attempt**: Often outputs explanatory text alongside JSON
- **Second attempt**: May get the JSON format right but logic wrong
- **Third+ attempts**: Progressively refine based on test feedback

This mirrors real prompt engineering workflows where iteration is essential.

## Hands-On Exercise – Name-Matching Service

### Problem Statement

Given:

- A CSV list of employees `(empId, empName)` in _last-name, first-name_ order.
- A user-supplied _target string_ (free-form).

Return:

- A **list of candidate matches** `List[Tuple[int, str]]`, ordered best-to-worst.

Rules (enforced by the test):

- Initials like "JC" should match "Corn, John" not "Johnson, Casey".
- Case-insensitive.
- 100 % JSON output (no extra commentary).
- All potential matches must be listed (not just the winner).

### Provided Files

| Path                                | Purpose                                               |
| ----------------------------------- | ----------------------------------------------------- |
| `session0/employee_matcher.py`      | Scaffold with TODO `SYSTEM_PROMPT` constant.          |
| `session0/test_employee_matcher.py` | Pytest that calls your function with a small dataset. |

Students **only edit the `SYSTEM_PROMPT` string**. Everything else (OpenAI call & JSON parsing) is handled for them.

---

## Live Coding Flow

1. Inspect the failing test – observe assertion error.
2. Open `employee_matcher.py`, read the TODOs.
3. Draft a first pass of the system prompt (basic instructions + JSON format).
4. Run tests; inspect LLM output on failure.
5. Iteratively refine prompt (add reasoning steps, constraints, few-shot).
6. When `pytest -q` passes, commit the prompt.

This mirrors real-world prompt iteration while emphasising **observable, testable development**.

---

## Learning Objectives

By the end of Session 0 participants can:

### Technical Skills

1. **API Interaction**: Call the OpenAI API directly using the Python SDK, understanding the message-based interface
2. **Prompt Engineering**: Write effective system prompts that produce reliable, structured outputs
3. **Structured Output**: Use JSON schemas and response formatting to constrain LLM outputs
4. **Parsing & Validation**: Convert LLM responses into typed Python objects with proper error handling
5. **Test-Driven Prompting**: Use unit tests to iteratively improve prompt quality

### Conceptual Understanding

1. **LLMs as Functions**: Think of LLMs as deterministic functions with inputs and outputs
2. **Prompt Anatomy**: Understand the roles of system vs. user messages and how they influence behavior
3. **Temperature Control**: Know when to use `temperature=0` for consistency vs. higher values for creativity
4. **Cost-Performance Tradeoffs**: Select appropriate models based on task complexity and budget
5. **Limitations**: Recognize what LLMs can't do well without proper orchestration (sets up Session 1)
6. **Resilience Mindset**: Treat LLM calls like network requests—validate outputs, retry on failure, and know when to route to Human-in-the-Loop review (sets up Session 3)

### Development Practices

1. **Iterative Development**: Refine prompts through systematic testing and observation
2. **Debugging Techniques**: Analyze LLM outputs to diagnose prompt issues
3. **Version Control**: Treat prompts as code that should be versioned and tested
4. **Documentation**: Write clear instructions that LLMs can follow consistently

---

## Common Pitfalls & Tips

### Pitfalls to Avoid

1. **Over-Engineering Initial Prompts**

   - Start simple, test, then add complexity
   - Don't try to handle every edge case upfront

2. **Ignoring Test Feedback**

   - Read the actual LLM output when tests fail
   - The model might be interpreting your instructions differently than expected

3. **Mixing Instructions and Examples**

   - Keep instructions clear and separate from examples
   - Use consistent formatting throughout

4. **Forgetting About Case Sensitivity**
   - Be explicit about case-insensitive matching
   - Test with various input cases

### Success Tips

1. **Use the LLM to Debug Itself**

   - If output is wrong, ask the LLM to explain its reasoning
   - Add a "reasoning" field to the JSON output during development

2. **Leverage Few-Shot Examples**

   - One good example is worth many lines of instructions
   - Show edge cases in your examples

3. **Be Explicit About Output Format**

   - Use CAPS for critical instructions: "ONLY output JSON"
   - Repeat format requirements at the end of the prompt

4. **Test Incrementally**
   - Get one test passing before tackling the next
   - Each test failure teaches you something about the LLM's behavior

## Facilitation Notes

### Time Management (45-60 minutes)

- **5 min**: Introduction and context setting
- **10 min**: Walk through the provided code structure
- **5 min**: Run failing tests together, analyze output
- **20-30 min**: Iterative prompt development (live coding)
- **5 min**: Discuss what worked and why
- **5 min**: Preview how this connects to LangGraph

### Key Teaching Moments

1. **First Test Failure**: When students see the raw LLM output vs. expected JSON
2. **Ambiguous Matches**: When "jco" needs to return multiple candidates
3. **Success**: When all tests pass – celebrate the iterative process

### Discussion Prompts

- "What surprised you about the LLM's behavior?"
- "How is this different from using ChatGPT?"
- "What would happen if we set temperature to 0.7?"
- "How would you extend this to handle misspellings?"

## Connection to Future Sessions

This session establishes critical foundations:

1. **Session 1 (LangGraph)**: These prompt engineering skills directly apply to agent development

   - Agents need clear, structured prompts to make decisions
   - Tool calling requires similar JSON output formatting
   - State management builds on structured data concepts

2. **Session 2 (Building Agents)**: Understanding structured outputs is crucial for tool calling

   - Tools require specific parameter formats (like our JSON output)
   - Agents must parse and validate tool responses
   - Error handling patterns established here scale to agent systems

3. **Session 3 (Evaluation)**: Test-driven development extends to agent evaluation

   - Unit tests for prompts evolve into integration tests for agents
   - Systematic debugging approaches remain essential
   - Performance metrics build on the pass/fail paradigm

4. **Session 4 (Memory)**: Structured data formats enable persistent memory systems
   - JSON/structured outputs facilitate storage and retrieval
   - Consistent formatting enables memory search and updates
   - Schema design skills transfer directly

### The Journey from Functions to Agents

```
Session 0: LLM as a Function
    ↓
Session 1: Orchestrating Multiple Functions (LangGraph)
    ↓
Session 2: Dynamic Function Selection (Agents)
    ↓
Session 3: Validating Complex Behaviors (Evaluation)
    ↓
Session 4: Stateful, Learning Systems (Memory)
```

Each session builds on the previous, with this foundational session ensuring everyone has the core skills needed for the journey ahead.

## Further Reading & References

### Essential Resources

- [OpenAI Python SDK Documentation](https://platform.openai.com/docs/python)
- [OpenAI Structured Outputs Guide](https://platform.openai.com/docs/guides/structured-outputs)
- [Anthropic Prompt Engineering Interactive Tutorial](https://docs.anthropic.com/claude/docs/prompt-engineering)

### Deep Dives

- [DeepLearning.AI - ChatGPT Prompt Engineering for Developers](https://www.deeplearning.ai/short-courses/chatgpt-prompt-engineering-for-developers/)
- [Lilian Weng - Prompt Engineering](https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/)
- [DSPy: Programming—not prompting—Foundation Models](https://github.com/stanfordnlp/dspy)

### Community Resources

- [Awesome Prompt Engineering](https://github.com/promptslab/Awesome-Prompt-Engineering)
- [Learn Prompting](https://learnprompting.org/)

---

Happy prompting! 🚀
