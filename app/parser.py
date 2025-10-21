# app/parser.py
import re
from typing import Dict, Any, Optional

def parse_natural_language_query(query: str) -> Optional[Dict[str, Any]]:
    """
    Parses a natural language query into a filter dictionary.
    Returns None if the query cannot be understood.
    """
    filters: Dict[str, Any] = {}
    original_query = query
    query = query.lower().strip()

    # 1. Check for palindrome
    if "palindromic" in query or "palindrome" in query:
        filters["is_palindrome"] = True

    # 2. Check for word count
    word_count_match = re.search(r'(\d+)\s+word(s)?', query)
    if word_count_match:
        filters["word_count"] = int(word_count_match.group(1))
    elif "single word" in query:
        filters["word_count"] = 1

    # 3. Check for length (min_length)
    # "longer than 10" -> min_length = 11
    min_length_match = re.search(r'(longer|more)\s+than\s+(\d+)', query)
    if min_length_match:
        filters["min_length"] = int(min_length_match.group(2)) + 1
        
    # "at least 10" -> min_length = 10
    min_length_at_least_match = re.search(r'at\s+least\s+(\d+)', query)
    if min_length_at_least_match:
         filters["min_length"] = int(min_length_at_least_match.group(1))

    # 4. Check for length (max_length)
    # "shorter than 10" -> max_length = 9
    max_length_match = re.search(r'(shorter|less)\s+than\s+(\d+)', query)
    if max_length_match:
        filters["max_length"] = int(max_length_match.group(2)) - 1
        
    # "at most 10" -> max_length = 10
    max_length_at_most_match = re.search(r'at\s+most\s+(\d+)', query)
    if max_length_at_most_match:
         filters["max_length"] = int(max_length_at_most_match.group(1))

    # 5. Check for contains_character
    # "containing the letter z" or "contains 'z'"
    contains_match = re.search(r'contain(s|ing)\s+(the\s+letter\s+)?["\']?([a-z0-9])["\']?', query)
    if contains_match:
        filters["contains_character"] = contains_match.group(3)
        
    # Heuristic for "first vowel"
    if "first vowel" in query:
        filters["contains_character"] = "a"

    # If we couldn't parse anything, return None
    if not filters:
        return None

    return filters