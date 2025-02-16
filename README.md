📚 Library Management System

📌 Overview

The Library Management System is a FastAPI-based application that allows librarians to manage books and members to borrow or return books. It includes features like authentication, book searching, and borrowing management.

🛠 Tech Stack

FastAPI (Backend)

SQLite (Database)

Pydantic (Data validation)

Uvicorn (Server)

Requests (API requests)

📂 Project Structure
📁 library-management-system
│-- cli.py           # Command-line interface for user interactions
│-- database.py      # Handles SQLite database operations
│-- models.py        # Pydantic models for data validation
│-- requirements.txt # Dependencies
│-- main.py          # FastAPI server setup (to be added if missing)


🚀 Setup Instructions

1️⃣ Clone the Repository

git clone https://github.com/Ganesh-Ramavath/library-management-system.git
cd library-management-system

2️⃣ Install Dependencies

pip install -r requirements.txt

3️⃣ Run the FastAPI Server

uvicorn main:app --reload

4️⃣ Use the CLI to Manage Books
python cli.py



![image](https://github.com/user-attachments/assets/56341d1c-72b7-4e4c-83b1-f15272bc507c)

📝 Features

✅ User authentication (Librarian & Member)✅ Book management (Add, Search, Borrow, Return)✅ SQLite database integration✅ Command-line interface (CLI)

📢 Contributing

Feel free to fork this repository and create pull requests! 🚀

📄 License

This project is open-source and available under the MIT license.
