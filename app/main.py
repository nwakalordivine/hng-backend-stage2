# app/main.py
from fastapi import FastAPI, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List, Dict, Any
from . import crud, models, schemas, parser 
from .db import get_db, engine, Base

# Create FastAPI app
app = FastAPI(title="String Analyzer Service")

@app.on_event("startup")
async def startup():
    # This is an alternative to Alembic for simple projects:
    # It creates tables if they don't exist, but doesn't handle migrations.
    # Since we used Alembic, this isn't strictly needed, but good practice.
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# --- Endpoint 4: Natural Language Filtering ---
@app.get(
    "/strings/filter-by-natural-language",
    response_model=schemas.NLFilterResponse,
    summary="Get strings using a natural language query"
)
async def get_strings_by_natural_language(
    query: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve a list of analyzed strings based on a natural language query.

    **Example Queries:**
    - "all single word palindromic strings"
    - "strings longer than 10 characters"
    - "palindromic strings that contain the first vowel"
    - "strings containing the letter z"

    Raises **400 Bad Request** if the query cannot be parsed.
    """

    # 1. Parse the query
    parsed_filters = parser.parse_natural_language_query(query)

    if parsed_filters is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to parse natural language query."
        )

    # 2. Fetch data using the same CRUD function as /strings
    strings_list = await crud.get_filtered_strings(db, parsed_filters)

    # 3. Format the response data
    response_data = []
    for db_string in strings_list:
        response_data.append(schemas.StringResponse(
            id=db_string.sha256_hash,
            value=db_string.value,
            properties=schemas.StringProperties(
                length=db_string.length,
                is_palindrome=db_string.is_palindrome,
                unique_characters=db_string.unique_characters,
                word_count=db_string.word_count,
                sha256_hash=db_string.sha256_hash,
                character_frequency_map=db_string.character_frequency_map
            ),
            created_at=db_string.created_at
        ))

    # 4. Build the final response object
    interpreted_query = schemas.NLFilterInterpretedQuery(
        original=query,
        parsed_filters=schemas.NLFilterParsed(**parsed_filters)
    )

    return schemas.NLFilterResponse(
        data=response_data,
        count=len(response_data),
        interpreted_query=interpreted_query
    )


# --- Endpoint 1: Create/Analyze String ---
@app.post(
    "/strings", 
    response_model=schemas.StringResponse, 
    status_code=status.HTTP_201_CREATED,
    summary="Analyze and store a new string"
)
async def create_string(
    string_data: schemas.StringCreate, 
    db: AsyncSession = Depends(get_db)
):
    """
    Analyze a new string and store its properties.
    
    - **value**: The string to be analyzed.
    
    Returns the stored object on success.
    Raises **409 Conflict** if the string already exists.
    """
    db_string = await crud.create_analyzed_string(db=db, string_data=string_data)
    if db_string is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="String already exists in the system."
        )
    
    # Manually structure the response to match the 'id' and 'properties' schema
    return schemas.StringResponse(
        id=db_string.sha256_hash,
        value=db_string.value,
        properties=schemas.StringProperties(
            length=db_string.length,
            is_palindrome=db_string.is_palindrome,
            unique_characters=db_string.unique_characters,
            word_count=db_string.word_count,
            sha256_hash=db_string.sha256_hash,
            character_frequency_map=db_string.character_frequency_map
        ),
        created_at=db_string.created_at
    )

# --- Endpoint 2: Get Specific String ---
@app.get(
    "/strings/{string_value}", 
    response_model=schemas.StringResponse,
    summary="Get a specific string by its value"
)
async def get_string(string_value: str, db: AsyncSession = Depends(get_db)):
    """
    Retrieve the analysis properties for a single string.
    
    - **string_value**: The exact string to retrieve.
    
    Raises **404 Not Found** if the string does not exist.
    """
    db_string = await crud.get_string_by_value(db, string_value)
    if db_string is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="String does not exist in the system."
        )
        
    return schemas.StringResponse(
        id=db_string.sha256_hash,
        value=db_string.value,
        properties=schemas.StringProperties(
            length=db_string.length,
            is_palindrome=db_string.is_palindrome,
            unique_characters=db_string.unique_characters,
            word_count=db_string.word_count,
            sha256_hash=db_string.sha256_hash,
            character_frequency_map=db_string.character_frequency_map
        ),
        created_at=db_string.created_at
    )




# --- Endpoint 3: Get All Strings with Filtering ---
@app.get(
    "/strings", 
    response_model=schemas.FilterResponse,
    summary="Get all strings with optional filters"
)
async def get_all_strings(
    is_palindrome: Optional[bool] = Query(None),
    min_length: Optional[int] = Query(None, ge=0),
    max_length: Optional[int] = Query(None, ge=0),
    word_count: Optional[int] = Query(None, ge=0),
    contains_character: Optional[str] = Query(None, min_length=1, max_length=1),
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve a list of analyzed strings, with optional query filters.
    
    - **is_palindrome**: Filter by palindrome status (true/false).
    - **min_length**: Filter for strings with length >= value.
    - **max_length**: Filter for strings with length <= value.
    - **word_count**: Filter for strings with an exact word count.
    - **contains_character**: Filter for strings containing a specific character.
    """
    
    # Collect filters into a dictionary, removing None values
    filters_applied = {
        "is_palindrome": is_palindrome,
        "min_length": min_length,
        "max_length": max_length,
        "word_count": word_count,
        "contains_character": contains_character
    }
    # Clean dict of keys where value is None
    active_filters = {k: v for k, v in filters_applied.items() if v is not None}
    
    # Fetch data from CRUD function
    strings_list = await crud.get_filtered_strings(db, active_filters)
    
    # Format the response
    response_data = []
    for db_string in strings_list:
        response_data.append(schemas.StringResponse(
            id=db_string.sha256_hash,
            value=db_string.value,
            properties=schemas.StringProperties(
                length=db_string.length,
                is_palindrome=db_string.is_palindrome,
                unique_characters=db_string.unique_characters,
                word_count=db_string.word_count,
                sha256_hash=db_string.sha256_hash,
                character_frequency_map=db_string.character_frequency_map
            ),
            created_at=db_string.created_at
        ))
        
    return schemas.FilterResponse(
        data=response_data,
        count=len(response_data),
        filters_applied=active_filters
    )

# --- Endpoint 5: Delete String ---
@app.delete(
    "/strings/{string_value}", 
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a specific string by its value"
)
async def delete_string(string_value: str, db: AsyncSession = Depends(get_db)):
    """
    Delete a string analysis from the system.
    
    - **string_value**: The exact string to delete.
    
    Returns **204 No Content** on success.
    Raises **404 Not Found** if the string does not exist.
    """
    deleted = await crud.delete_string_by_value(db, string_value)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="String does not exist in the system."
        )
    # 204 responses have no body
    return None