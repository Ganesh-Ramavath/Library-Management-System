import requests

BASE_URL = "http://127.0.0.1:8000"  # FastAPI server URL

# Global variables for user session
logged_in = None
user_role = None

def login():
    global logged_in, user_role
    name = input("Enter your name: ")
    password = input("Enter your password: ")
    role = input("Enter your role (librarian/member): ")

    response = requests.post(f"{BASE_URL}/login", json={"name": name, "password": password, "role": role})
    
    if response.status_code == 200:
        data = response.json()
        logged_in = data["member_id"]
        user_role = data["role"]
        print(f" Login successful! Role: {user_role.capitalize()}")
    else:
        print(" Invalid credentials. Please try again.")

def add_book():
    if logged_in and user_role == "librarian":
        title = input("Enter book title: ")
        author = input("Enter book author: ")
        isbn = input("Enter book ISBN: ")

        response = requests.post(f"{BASE_URL}/books", json={"title": title, "author": author, "isbn": isbn}, params={"member_id": logged_in, "role": user_role})
        
        print(" Book added successfully!" if response.status_code == 200 else "❌ Failed to add book.")
    else:
        print(" Only librarians can add books. Please log in as a librarian.")

def borrow_book():
    if logged_in:
        book_id = input("Enter the ID of the book to borrow: ")
        return_date = input("Enter the return date (YYYY-MM-DD): ")
        
        response = requests.post(f"{BASE_URL}/borrow/{book_id}", json={"member_id": logged_in, "return_date": return_date})
        
        print(" Book borrowed successfully!" if response.status_code == 200 else "❌ Failed to borrow book. It may be unavailable.")
    else:
        print(" Please log in first.")

def return_book():
    if logged_in:
        book_id = input("Enter the ID of the book to return: ")
        
        response = requests.post(f"{BASE_URL}/return/{book_id}", params={"member_id": logged_in})
        
        print(" Book returned successfully!" if response.status_code == 200 else "❌ Failed to return book. It may not be borrowed by you.")
    else:
        print(" Please log in first.")

def search_books():
    query = input("Enter book title or author to search: ")
    response = requests.get(f"{BASE_URL}/search", params={"query": query})
    
    if response.status_code == 200:
        books = response.json().get("books", [])
        if books:
            print("🔎 Search Results:")
            for book in books:
                print(f"📖 {book['id']}: {book['title']} by {book['author']}")
        else:
            print(" No books found.")
    else:
        print(" Error while searching.")

def list_books():
    response = requests.get(f"{BASE_URL}/books")
    
    if response.status_code == 200:
        books = response.json().get("books", [])
        if books:
            print(" Available Books:")
            for book in books:
                status = "Available" if book["available"] else "Borrowed"
                print(f"📖 {book['id']}: {book['title']} by {book['author']} ({status})")
        else:
            print("📭 No books available.")
    else:
        print(" Error fetching books.")

def main():
    while True:
        print("\n📚 Library Management System")
        print("1 Login")
        print("2 Add Book (Librarian Only)")
        print("3 Borrow Book")
        print("4 Return Book")
        print("5 Search Books")
        print("6 List All Books")
        print("7 Exit")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            login()
        elif choice == '2':
            add_book()
        elif choice == '3':
            borrow_book()
        elif choice == '4':
            return_book()
        elif choice == '5':
            search_books()
        elif choice == '6':
            list_books()
        elif choice == '7':
            print("👋 Exiting application.")
            break
        else:
            print("⚠️ Invalid choice, please try again.")

if __name__ == "__main__":
    main()
