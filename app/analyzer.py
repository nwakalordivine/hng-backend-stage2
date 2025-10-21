# app/analyzer.py
import hashlib
from collections import Counter

def analyze_string(input_string: str) -> dict:
    """
    Computes all required properties for a given string.
    """
    
    # 1. length: Number of characters
    length = len(input_string)
    
    # 2. is_palindrome: (case-insensitive)
    normalized_string = input_string.lower()
    is_palindrome = normalized_string == normalized_string[::-1]
    
    # 3. unique_characters: Count of distinct characters
    unique_characters = len(set(input_string))
    
    # 4. word_count: Number of words separated by whitespace
    # .split() handles all whitespace (spaces, tabs, newlines)
    word_count = len(input_string.split())
    
    # 5. sha256_hash: SHA-256 hash of the string
    # The hash function requires the string to be encoded into bytes
    hash_object = hashlib.sha256(input_string.encode('utf-8'))
    sha256_hash = hash_object.hexdigest()
    
    # 6. character_frequency_map: Dictionary of character counts
    # Counter is a subclass of dict, perfect for this
    character_frequency_map = Counter(input_string)
    
    # Return all properties in a dictionary
    return {
        "length": length,
        "is_palindrome": is_palindrome,
        "unique_characters": unique_characters,
        "word_count": word_count,
        "sha256_hash": sha256_hash,
        "character_frequency_map": dict(character_frequency_map) # Convert Counter to plain dict
    }