import os
from typing import List, Tuple

import pytest

from session0.employee_matcher import find_employee_matches, SYSTEM_PROMPT

# -----------------------------------------------------------------------------
# Shared test data (small CSV so calls remain cheap)
# -----------------------------------------------------------------------------
_EMPLOYEES_CSV: str = (
    "empId,empName\n"
    "1,\"Corn, John\"\n"
    "2,\"Johnson, Casey\"\n"
    "3,\"Cheddar, Joe\"\n"
    "4,\"Oliver, Jacen\"\n"
    "5,\"Bacon, Patrick\"\n"
)

# A list of (target string, expected top-rank employee id)
_TOP_MATCH_CASES: List[Tuple[str, int]] = [
    ("JC", 1),   # initials, clear winner - John Corn not Casey Johnson
    ("JCo", 1),  # disambiguated initials (should NOT pick Cheddar, Joe)
    ("pb", 5),   # lowercase initials should map to Bacon, Patrick
    ("CJ", 2),   # initials for Casey Johnson
    ("JO", 4),   # initials for Jacen Oliver
]

# -----------------------------------------------------------------------------
# Skip logic – avoids failing CI when prompt not yet filled or no API key.
# -----------------------------------------------------------------------------
_SKIP_PROMPT = SYSTEM_PROMPT.strip().lower().startswith("todo")
_SKIP_APIKEY = "OPENAI_API_KEY" not in os.environ


@pytest.mark.skipif(_SKIP_PROMPT, reason="Student has not yet filled in the SYSTEM_PROMPT")
@pytest.mark.skipif(_SKIP_APIKEY, reason="OPENAI_API_KEY not set; skipping live LLM calls")
@pytest.mark.parametrize("target,expected_id", _TOP_MATCH_CASES)
def test_top_match(target: str, expected_id: int):
    """The highest-ranked match should be *expected_id* for each target input."""
    matches = find_employee_matches(target, _EMPLOYEES_CSV)
    assert matches, "find_employee_matches returned an empty list"
    assert matches[0][0] == expected_id, (
        f"Expected empId {expected_id} as best match for '{target}', got {matches[0]}"
    )


@pytest.mark.skipif(_SKIP_PROMPT, reason="Student has not yet filled in the SYSTEM_PROMPT")
@pytest.mark.skipif(_SKIP_APIKEY, reason="OPENAI_API_KEY not set; skipping live LLM calls")
def test_ambiguous_input_includes_multiple_candidates():
    """The ambiguous lowercase input 'jco' should list multiple plausible matches."""
    matches = find_employee_matches("jco", _EMPLOYEES_CSV)
    ids = [emp_id for emp_id, _ in matches]
    names = [name for _, name in matches]
    
    # Should include both John Corn (1) and Jacen Oliver (4) somewhere in list
    for expected_id in (1, 4):
        assert (
            expected_id in ids
        ), f"Expected empId {expected_id} to appear in candidate list for 'jco'"
    
    # Verify the actual names for clarity
    assert any("Corn, John" in name for name in names), "Should include John Corn for 'jco'"
    assert any("Oliver, Jacen" in name for name in names), "Should include Jacen Oliver for 'jco'"


@pytest.mark.skipif(_SKIP_PROMPT, reason="Student has not yet filled in the SYSTEM_PROMPT")
@pytest.mark.skipif(_SKIP_APIKEY, reason="OPENAI_API_KEY not set; skipping live LLM calls")
def test_partial_name_matching():
    """Test partial name matching like 'che' for 'Cheddar'."""
    matches = find_employee_matches("che", _EMPLOYEES_CSV)
    ids = [emp_id for emp_id, _ in matches]
    
    # Should include Cheddar, Joe as a strong match
    assert 3 in ids, "Expected 'che' to match 'Cheddar, Joe' (empId: 3)"
    
    # Verify it's ranked first since it's the only clear match
    if matches:
        assert matches[0][0] == 3, "Expected 'Cheddar, Joe' to be the top match for 'che'"


@pytest.mark.skipif(_SKIP_PROMPT, reason="Student has not yet filled in the SYSTEM_PROMPT")
@pytest.mark.skipif(_SKIP_APIKEY, reason="OPENAI_API_KEY not set; skipping live LLM calls")
def test_full_name_matching():
    """Test that full names (even partial) work correctly."""
    matches = find_employee_matches("john", _EMPLOYEES_CSV)
    ids = [emp_id for emp_id, _ in matches]
    
    # Should match both John Corn and Casey Johnson
    assert 1 in ids, "Expected 'john' to match 'Corn, John'"
    assert 2 in ids, "Expected 'john' to match 'Johnson, Casey' (last name match)"
    
    # John Corn should rank higher (first name match is usually stronger)
    if len(matches) >= 2:
        # This is a heuristic - the LLM might reasonably rank them differently
        assert 1 in [m[0] for m in matches[:2]], "Expected 'Corn, John' in top 2 matches"


def test_no_matches():
    """Test behavior when no reasonable matches exist."""
    # This test is optional - it depends on how the student handles no matches
    # Some might return empty list, others might return weak matches
    # This is more for testing edge case handling
    pass  # Students can optionally implement this


if __name__ == "__main__":
    # Allow running via:  python session0/test_employee_matcher.py
    import sys
    import pytest

    # Run with verbose output to help with debugging
    sys.exit(pytest.main([__file__, "-v"])) 