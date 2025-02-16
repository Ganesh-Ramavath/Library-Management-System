from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import date
import sqlite3
from database import get_db_connection, create_tables
from models import Book, Member, BorrowBook

app = FastAPI()

# Ensure tables exist on startup
create_tables()

@app.post("/login")
def login(member: Member):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM members WHERE name = ? AND password = ?", (member.name, member.password))
    user = cursor.fetchone()
    conn.close()

    if user:
        return {"message": "Login successful!", "member_id": user[0], "role": user[3]}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/books")
def add_book(book: Book, member_id: int, role: str):
    if role != "librarian":
        raise HTTPException(status_code=403, detail="Only librarians can add books.")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO books (title, author, isbn, available) VALUES (?, ?, ?, 1)",
                   (book.title, book.author, book.isbn))
    conn.commit()
    conn.close()

    return {"message": "Book added successfully!"}

@app.post("/borrow/{book_id}")
def borrow_book(book_id: int, borrow_info: BorrowBook):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM books WHERE id = ? AND available = 1", (book_id,))
    book = cursor.fetchone()

    if book:
        cursor.execute('''
            INSERT INTO borrowed_books (member_id, book_id, borrow_date, return_date)
            VALUES (?, ?, ?, ?)
        ''', (borrow_info.member_id, book_id, date.today(), borrow_info.return_date))

        cursor.execute("UPDATE books SET available = 0, borrowed_by = ?, return_date = ? WHERE id = ?",
                       (borrow_info.member_id, borrow_info.return_date, book_id))

        conn.commit()
        conn.close()
        return {"message": "Book borrowed successfully!"}

    conn.close()
    raise HTTPException(status_code=404, detail="Book not available or doesn't exist.")

@app.post("/return/{book_id}")
def return_book(book_id: int, member_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM books WHERE id = ? AND borrowed_by = ?", (book_id, member_id))
    book = cursor.fetchone()

    if book:
        cursor.execute("UPDATE books SET available = 1, borrowed_by = NULL, return_date = NULL WHERE id = ?", (book_id,))
        conn.commit()
        conn.close()
        return {"message": "Book returned successfully!"}

    conn.close()
    raise HTTPException(status_code=404, detail="This book was not borrowed by this member.")

@app.get("/search")
def search_books(query: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ?", (f"%{query}%", f"%{query}%"))
    books = cursor.fetchall()
    conn.close()

    if books:
        return {"books": [{"id": book[0], "title": book[1], "author": book[2]} for book in books]}
    return {"message": "No books found."}

@app.get("/books")
def list_books():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    conn.close()

    return {"books": [{"id": book[0], "title": book[1], "author": book[2], "available": book[3]} for book in books]}
