from __future__ import annotations

"""Session 0 Exercise – Name-Matching via OpenAI ChatCompletions

Participants should ONLY edit the ``SYSTEM_PROMPT`` constant.  The rest of the file
is provided so that the unit tests in ``session0/test_employee_matcher.py`` can
run without any modifications.
"""

from typing import List, Tuple
import os
import textwrap
import json

import openai

# -------------------------------------------------------------------------------------
# Participants –– replace the string below with your carefully-crafted system prompt.
# -------------------------------------------------------------------------------------
SYSTEM_PROMPT: str = """
You’re given a two-letter string of initials (e.g. "PB"), where the first letter is the employee’s first-name initial and the second is the last-name initial. You also have a CSV of employees whose “Name” column is in the format:

    Last,First

Write code that:

1. Reads the CSV.
2. For each row, splits the “Name” field into Last and First.
3. Performs a case-insensitive match so that:
   - the first letter of First equals the first input initial, and
   - the first letter of Last equals the second input initial.
4. Returns all matching rows (if none, return an empty list).
5. Preserves order and does not match swapped initials (e.g. input “PB” must match “Bookie,Pawn” but not “Pawn,Bookie”).

Example:
- Input: `"PB"`
- CSV rows:
  - `Pawn,Bookie`  → Last Pawn (P) / First Bookie (B)  ✗
  - `Bookie,Pawn`  → Last Bookie (B) / First Pawn (P)  ✔
"""

_USER_TEMPLATE = textwrap.dedent(
    """
    <User input>
        <Employees>
{employees_csv}
        </Employees>
        <target string>{target}</target string>
    </User input>
    """
)

# -------------------------------------------------------------------------------------
# Internal helpers – nothing to change below this line
# -------------------------------------------------------------------------------------

def _initialise_openai() -> None:
    """Initialise the OpenAI client using the ``OPENAI_API_KEY`` env var."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "OPENAI_API_KEY environment variable not found.  Set it before running."
        )
    openai.api_key = api_key



# JSON schema that constrains the LLM to the desired structure
_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "matches": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "empId": {"type": "integer", "description": "Employee ID"},
                    "empName": {"type": "string", "description": "Employee name in 'Last, First' format"},
                },
                "required": ["empId", "empName"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["matches"],
    "additionalProperties": False,
}


def _call_llm(employees_csv: str, target: str, model: str = "gpt-4.1") -> str:
    """Send the prompt to OpenAI and return the assistant's raw JSON text.

    The function relies on the caller having set a valid ``OPENAI_API_KEY``.
    The JSON schema in ``response_format`` ensures that the model produces
    output we can parse deterministically.
    """
    _initialise_openai()

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": _USER_TEMPLATE.format(employees_csv=employees_csv, target=target),
        },
    ]

    response = openai.chat.completions.create(
        model=model,
        messages=messages,  # type: ignore[arg-type]
        temperature=0,
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "employee_matches",
                "schema": _RESPONSE_SCHEMA,
            },
        },
    )
    return response.choices[0].message.content  # type: ignore[attr-defined]


# -----------------------------------------------------------------------------
# JSON helper
# -----------------------------------------------------------------------------

def _parse_json_output(text: str) -> List[Tuple[int, str]]:
    """Parse the JSON response into a list of ``(empId, empName)`` tuples.

    Expected JSON structure::

        {
            "matches": [
                {"empId": 27, "empName": "Bacon, Patrick"},
                ...
            ]
        }
    """

    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError("Response was not valid JSON:\n" + text) from exc

    if not isinstance(data, dict) or "matches" not in data:
        raise ValueError("JSON does not contain a 'matches' key: " + text)

    matches = data["matches"]
    if not isinstance(matches, list):
        raise ValueError("'matches' is not a list in JSON output: " + text)

    results: List[Tuple[int, str]] = []
    for item in matches:
        if not isinstance(item, dict):
            continue
        try:
            emp_id = int(item["empId"])
            emp_name = str(item["empName"]).strip()
            results.append((emp_id, emp_name))
        except (KeyError, TypeError, ValueError):
            # Skip malformed parts but continue processing others
            continue

    if not results:
        raise ValueError("No valid matches extracted from JSON: " + text)

    return results


# -------------------------------------------------------------------------------------
# Public API – this is what the tests import.
# -------------------------------------------------------------------------------------

def find_employee_matches(target: str, employees_csv: str) -> List[Tuple[int, str]]:
    """Return a list of candidate (empId, empName) tuples for *target*.

    Parameters
    ----------
    target : str
        Free-form user input that identifies an employee (name, initials, …).
    employees_csv : str
        CSV string containing *empId,empName* records – one per line.

    Returns
    -------
    List[Tuple[int, str]]
        Ordered best-to-worst candidate matches as parsed from the LLM's JSON
        structured output.
    """
    raw_response = _call_llm(employees_csv=employees_csv, target=target)
    return _parse_json_output(raw_response)


__all__ = ["find_employee_matches", "SYSTEM_PROMPT"] 