# database.py
import sqlite3

DATABASE = "library_management.db"


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Enables dictionary-like row access
    return conn


def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('librarian', 'member'))
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            isbn TEXT NOT NULL UNIQUE,
            available BOOLEAN NOT NULL DEFAULT 1,
            borrowed_by INTEGER,
            return_date DATE,
            FOREIGN KEY (borrowed_by) REFERENCES members (id)
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS borrowed_books (
            member_id INTEGER NOT NULL,
            book_id INTEGER NOT NULL,
            borrow_date DATE NOT NULL,
            return_date DATE,
            FOREIGN KEY (member_id) REFERENCES members(id),
            FOREIGN KEY (book_id) REFERENCES books(id)
        );
    ''')

    conn.commit()
    conn.close()


# Run table creation on import
create_tables()
