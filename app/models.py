# app/models.py
from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import mapped_column
from app.db import Base

class AnalyzedString(Base):
    __tablename__ = "analyzed_strings"

    sha256_hash = mapped_column(String(64), primary_key=True)

    value = mapped_column(Text, unique=True, index=True, nullable=False)
    
    length = mapped_column(Integer, nullable=False)
    is_palindrome = mapped_column(Boolean, nullable=False)
    unique_characters = mapped_column(Integer, nullable=False)
    word_count = mapped_column(Integer, nullable=False)
    
    character_frequency_map = mapped_column(JSONB, nullable=False)
    
    created_at = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        nullable=False
    )