from app import db

from datetime import datetime
from sqlalchemy.types import Integer, String, Text, DateTime, Boolean

class User(db.Model):
    """
    user info
    """
    id = db.Column(Integer, primary_key=True)
    address = db.Column(String(100), nullable=False, unique=True)
    domain = db.Column(String(100), nullable=True, unique=True)
    created_at = db.Column(DateTime(timezone=True), default=datetime.now)
    updated_at = db.Column(DateTime(timezone=True), onupdate=datetime.now)
    is_deleted = db.Column(Boolean, default=False)

class ChatRecord(db.Model):
    """
    Chat Record
    """
    id = db.Column(Integer, primary_key=True)
    address = db.Column(String(100), nullable=False)
    session_id = db.Column(String(100), nullable=False, unique=True)
    content = db.Column(Text, nullable=False)
    created_at = db.Column(DateTime(timezone=True), default=datetime.now)
    updated_at = db.Column(DateTime(timezone=True), onupdate=datetime.now)
    is_deleted = db.Column(Boolean, default=False)

class Score(db.Model):
    """
    Score
    """
    id = db.Column(Integer, primary_key=True)
    address = db.Column(String(100), nullable=False)
    score_json = db.Column(Text, nullable=False)
    created_at = db.Column(DateTime(timezone=True), default=datetime.now)
    updated_at = db.Column(DateTime(timezone=True), onupdate=datetime.now)
    is_deleted = db.Column(Boolean, default=False)

class ScoreRecord(db.Model):
    """
    Score Record
    """
    id = db.Column(Integer, primary_key=True)
    score_id = db.Column(Integer, nullable=False)
    chat_id = db.Column(Integer, nullable=False)
    score_json = db.Column(Text, nullable=False)
    created_at = db.Column(DateTime(timezone=True), default=datetime.now)
    updated_at = db.Column(DateTime(timezone=True), onupdate=datetime.now)
    is_deleted = db.Column(Boolean, default=False)