# models.py
from pydantic import BaseModel
from typing import Optional
from datetime import date


class Book(BaseModel):
    title: str
    author: str
    isbn: str


class Member(BaseModel):
    name: str
    password: str
    role: str  # Either 'librarian' or 'member'


class BorrowBook(BaseModel):
    member_id: int
    return_date: Optional[date]  # Optional return date
