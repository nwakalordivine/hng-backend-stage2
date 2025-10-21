# app/schemas.py
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Dict, Any, List, Optional

# --- Nested Models ---

class StringProperties(BaseModel):
    """
    Pydantic model for the 'properties' JSON object.
    """
    length: int
    is_palindrome: bool
    unique_characters: int
    word_count: int
    sha256_hash: str
    character_frequency_map: Dict[str, int]

    # This allows us to create this model from an ORM object
    model_config = ConfigDict(from_attributes=True)


# --- Endpoint Schemas ---

class StringCreate(BaseModel):
    """
    Schema for the POST /strings request body.
    """
    value: str = Field(..., min_length=1, description="The string to be analyzed.")


class StringResponse(BaseModel):
    """
    Schema for the POST and GET /strings/{string_value} response body.
    """
    id: str = Field(..., description="The SHA256 hash of the string.")
    value: str
    properties: StringProperties
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class FilterResponse(BaseModel):
    """
    Schema for the GET /strings filter response.
    """
    data: List[StringResponse]
    count: int
    filters_applied: Dict[str, Any]


class NLFilterParsed(BaseModel):
    """
    Schema for the 'interpreted_query.parsed_filters' part.
    """
    word_count: Optional[int] = None
    is_palindrome: Optional[bool] = None
    min_length: Optional[int] = None
    contains_character: Optional[str] = None


class NLFilterInterpretedQuery(BaseModel):
    """
    Schema for the 'interpreted_query' part of the NL response.
    """
    original: str
    parsed_filters: NLFilterParsed


class NLFilterResponse(BaseModel):
    """
    Schema for the GET /strings/filter-by-natural-language response.
    """
    data: List[StringResponse]
    count: int
    interpreted_query: NLFilterInterpretedQuery