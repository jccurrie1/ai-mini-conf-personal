# Session 0 – LLM Foundations & Prompt Engineering (Hands-On)

Welcome! This folder is completely **self-contained** – you only need
Python ≥ 3.11, an OpenAI API key, and `pip install -r requirements.txt` (or use the
root project environment).

The goal: implement `SYSTEM_PROMPT` inside `employee_matcher.py` so that the
unit tests pass, proving you can treat an LLM like a regular function.

---

## 1. Quick Start

```bash
# 1. Activate your virtualenv / poetry / etc.
export OPENAI_API_KEY="sk-..."

# 2. Run the tests (several options)

# Option A – plain Python
python session0/test_employee_matcher.py

# Option B – pytest (recommended)
pytest session0 -q

# Option C – run *all* top-level project tests (may take longer)
pytest -q
```

If the prompt is still the default `"TODO – replace me with your prompt"`, the
tests will be **skipped** – fill it in first.

---

## 2. What You Edit

- **`employee_matcher.py`** – change only the `SYSTEM_PROMPT` constant.
  - Keep the rules from the exercise description – **JSON-only output** with a
    `{"matches": [{"empId": ..., "empName": ...}, ...]}` structure. List **all**
    candidate matches, etc.

Everything else (OpenAI call, XML parsing, test cases) is provided.

---

## 3. Cheat-Sheet for Writing the Prompt

1. Use a **step-by-step reasoning** section.
2. Demand output as a single **JSON object** that matches the required schema –
   _and nothing else_.
3. Include a **few-shot example** – see the workshop slides.
4. Set clear **matching rules** (initials, case-insensitive, etc.).

## 4. Debugging Tips

### When Tests Fail

1. **Read the actual output**: Add a print statement to see what the LLM returned:
   ```python
   raw_response = _call_llm(employees_csv=employees_csv, target=target)
   print(f"LLM Response: {raw_response}")  # Add this temporarily
   return _parse_json_output(raw_response)
   ```

2. **Common failure modes**:
   - LLM adds text before/after JSON → Use stronger instructions like "ONLY output JSON"
   - Wrong JSON structure → Show the exact format in your prompt
   - Missing matches → Ensure your prompt asks for ALL possible matches
   - Wrong initials logic → Be explicit about first/last name order

3. **Test one case at a time**: Run specific tests:
   ```bash
   pytest session0/test_employee_matcher.py::test_top_match -v
   ```

### Iteration Strategy

1. **Start minimal**: Get basic matching working first
2. **Add complexity gradually**:
   - First: Get exact matches working
   - Then: Add initials support
   - Finally: Handle ambiguous cases

3. **Use the LLM to help debug**: If confused about why it's not matching correctly,
   temporarily add a "reasoning" field to the JSON and ask the LLM to explain its logic

4. **Key prompt patterns that help**:
   - "Think step by step"
   - "First, parse the employee list..."
   - "IMPORTANT: Return ALL possible matches"
   - "Output ONLY a JSON object, no other text"

### Example Debugging Session

```python
# If "JC" matches "Johnson, Casey" instead of "Corn, John":
# Your prompt might need to clarify:
# "Initials match in order: first initial of first name, 
#  then first initial of last name. Since names are in 
#  'Last, First' format, 'JC' matches someone with 
#  first name starting with J and last name starting with C."
```

When the tests are green ✨ you're ready for Session 1!
