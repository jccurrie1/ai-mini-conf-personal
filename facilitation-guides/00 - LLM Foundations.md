## LLM Foundations & Prompt Engineering (`employee_matcher.py`)

**Goal:** Refresh participants on using Large Language Models as deterministic, test-friendly functions and on prompt-engineering best practices. By the end of the session students will make **all unit tests in `tests/test_employee_matcher.py` pass by editing ONE constant: `SYSTEM_PROMPT`**.

### Introduction

- Explain that this "Session 0" bootstraps everyone with the mental model of _LLM ≙ pure function_.
- Emphasise deterministic settings (`temperature=0`), structured output, and test-driven iteration.
- Show the project tree highlighting `session0/employee_matcher.py` and its companion test file.

### 1. Thinking of LLMs as Functions

- **Concept:** A chat model takes a _list of messages_ → returns _one_ assistant message.
- **Code walk-through:**
  ```python
  result = openai.chat.completions.create(
      model="gpt-4.1-mini",  # cost-effective tier (gpt-4.1-nano works too)
      messages=[{"role": "system", "content": SYSTEM_PROMPT}, ...],
      temperature=0,
  )
  ```
- Point out the determinism lever (`temperature`), the cost lever (`model`) and where the prompt lives.

### 2. Prompt Anatomy

| Part              | Purpose                                                   |
| ----------------- | --------------------------------------------------------- |
| **System Prompt** | Global rules, output contract, reasoning approach         |
| **User Prompt**   | Dynamic task data – the CSV employee list & target string |

Key techniques to highlight:

1. _Explicit format instructions_ → **pure JSON** with top-level key `matches`.
2. _Step-by-step reasoning_ inside a dedicated field (can be removed later).
3. _Few-shot examples_ – at least one full demonstration.
4. CAPS-lock imperatives: **_"RESPOND ONLY WITH JSON"_**.

### 3. Live Coding Flow (≈25 min)

1. Run `pytest -q` → watch it fail, inspect the raw LLM output captured by the test.
2. Open `employee_matcher.py`; locate the `SYSTEM_PROMPT = """ TODO """` placeholder.
3. Draft a first prompt (basic JSON instructions).
4. Rerun tests; observe failure modes (extra text, wrong keys, bad logic).
5. Iterate: add reasoning, tweak examples, enforce casing rules.
6. Celebrate green tests 🌱.

> **Discussion prompt:** "If the model keeps returning prose instead of JSON, how is that like getting a corrupted response from a flaky HTTP API? What defensive coding patterns would you apply?"

> **Facilitation tip:** Ask participants to _copy/paste_ the exact failing output into the discussion – it sharpens their debugging eye.

> **Facilitation tip:** If a prompt feels "almost right" but still fails edge-case tests, ask _"Would this be a good place to route the request to a Human-in-the-Loop reviewer? How could that correction feed back into our tests?"_

### 4. Conceptual Deep Dive (light-weight slides)

1. Deterministic vs. Creative settings (`temperature`, `top_p`).
2. Cost awareness and token budgeting.
3. JSON Schema coercion via `response_format` in the OpenAI SDK.
4. Why _structured output_ is the bedrock for agents & LangGraph.

### 5. Common Pitfalls & Fixes

| Symptom                    | Likely Cause                 | Quick Fix                                             |
| -------------------------- | ---------------------------- | ----------------------------------------------------- |
| Model returns prose + JSON | Output instructions too weak | Repeat **ONLY JSON** at end; add negative examples    |
| Order of matches is wrong  | Ambiguous matching rules     | Add explicit tie-break instructions                   |
| Capitalisation errors      | Case-sensitivity confusion   | State _"matching must be case-insensitive"_ in prompt |

### 6. Learning Objectives Recap

Participants should now be able to:

- Treat an LLM call as a deterministic function in code.
- Craft prompts that yield structured, parseable results.
- Use tests to iteratively refine prompt behaviour.
- Articulate why structured output is critical for later LangGraph sessions.

### 7. Transition to Session 1

Finish with the journey diagram:

```
Session 0: LLM as a Function
    ↓
Session 1: Orchestrating Multiple Functions (LangGraph)
    ↓
Session 2: Dynamic Tool Selection (Agents)
    ↓
Session 3: Evaluation & HITL
    ↓
Session 4: Stateful Systems & Memory
```

Explain that tomorrow the _same_ structured-output mindset will underpin tool calling and graph orchestration in LangGraph.
