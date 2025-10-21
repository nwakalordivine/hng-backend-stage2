# app/crud.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
from typing import Optional, List, Dict, Any

from . import models, schemas, analyzer

async def create_analyzed_string(
    db: AsyncSession, 
    string_data: schemas.StringCreate
) -> Optional[models.AnalyzedString]:
    """
    Analyzes a string, creates a new record in the database,
    and returns the new object.
    
    Returns None if a string with the same value already exists.
    """
    properties = analyzer.analyze_string(string_data.value)

    db_string = models.AnalyzedString(
        value=string_data.value,
        sha256_hash=properties["sha256_hash"],
        length=properties["length"],
        is_palindrome=properties["is_palindrome"],
        unique_characters=properties["unique_characters"],
        word_count=properties["word_count"],
        character_frequency_map=properties["character_frequency_map"]
    )
    
    db.add(db_string)
    try:
        await db.commit()
        await db.refresh(db_string)
        return db_string
    except IntegrityError:
        await db.rollback()
        return None

async def get_string_by_value(
    db: AsyncSession, 
    string_value: str
) -> Optional[models.AnalyzedString]:
    """
    Fetches a single analyzed string by its 'value' field.
    """
    query = select(models.AnalyzedString).where(models.AnalyzedString.value == string_value)
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def delete_string_by_value(db: AsyncSession, string_value: str) -> bool:
    """
    Deletes a string by its 'value'. 
    Returns True if deleted, False if not found.
    """
    db_string = await get_string_by_value(db, string_value)
    
    if db_string:
        await db.delete(db_string)
        await db.commit()
        return True
    return False

async def get_filtered_strings(
    db: AsyncSession, 
    filters: Dict[str, Any]
) -> List[models.AnalyzedString]:
    """
    Fetches a list of strings based on applied filters.
    """
    query = select(models.AnalyzedString)
    
    # Applied filters dynamically
    if filters.get("is_palindrome") is not None:
        query = query.where(models.AnalyzedString.is_palindrome == filters["is_palindrome"])
        
    if filters.get("min_length") is not None:
        query = query.where(models.AnalyzedString.length >= filters["min_length"])
        
    if filters.get("max_length") is not None:
        query = query.where(models.AnalyzedString.length <= filters["max_length"])
        
    if filters.get("word_count") is not None:
        query = query.where(models.AnalyzedString.word_count == filters["word_count"])
    
    if filters.get("contains_character") is not None:
        char = filters["contains_character"]
        query = query.where(models.AnalyzedString.character_frequency_map.has_key(char))

    result = await db.execute(query)
    return result.scalars().all()