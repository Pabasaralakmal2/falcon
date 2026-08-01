from __future__ import annotations

import os
from typing import Literal
from datetime import date, timedelta

from google.adk.agents import Agent

try:
    from dotenv import load_dotenv
    load_dotenv()

    MODEL_NAME = os.environ.get("GOOGLE_GENAI_MODEL", "gemini-3.1-flash-lite")
except ImportError:
    print("Warning: python-dotenv not installed. Ensure API key is set")
    MODEL_NAME = "gemini-3.1-flash-lite"

# ── Data ─────────────────────────────────────────────────────────────────────

CATALOG = {
    "978-0131103627": {"title": "The C Programming Language", "author": "Brian W. Kernighan, Dennis M. Ritchie", "genre": "Programming", "total_copies": 5, "available_copies": 3},
    "978-0201896831": {"title": "The Art of Computer Programming", "author": "Donald E. Knuth", "genre": "Computer Science", "total_copies": 2, "available_copies": 0},
    "978-0321714114": {"title": "C++ Primer", "author": "Stanley B. Lippman", "genre": "Programming", "total_copies": 4, "available_copies": 4},
    "978-0134685991": {"title": "Effective Java", "author": "Joshua Bloch", "genre": "Programming", "total_copies": 6, "available_copies": 1},
    "978-1449331818": {"title": "Learning Python", "author": "Mark Lutz", "genre": "Programming", "total_copies": 7, "available_copies": 5},
}

MEMBERS = {
    "M001": {"name": "Alice Smith", "borrowed_books": [{"isbn": "978-0131103627", "due_date": "2026-08-15"}]},
    "M002": {"name": "Bob Jones", "borrowed_books": [{"isbn": "978-0201896831", "due_date": "2026-08-05"}, {"isbn": "978-0134685991", "due_date": "2026-08-10"}]},
    "M003": {"name": "Charlie Brown", "borrowed_books": []},
}

# ── Tools ─────────────────────────────────────────────────────────────────────

def search_catalog(query: str = "", genre: str = "") -> dict:
    """Search the library catalog by title, author, or genre.

    Args:
        query: Optional text to search in titles or authors.
        genre: Optional exact genre to filter by.

    Returns:
        A list of matching books and their availability.
    """
    results = []
    for isbn, book in CATALOG.items():
        if genre and book["genre"].lower() != genre.lower():
            continue
        if query:
            q = query.lower()
            if q not in book["title"].lower() and q not in book["author"].lower():
                continue
        book_info = {"isbn": isbn, **book}
        results.append(book_info)
    
    return {"status": "success", "count": len(results), "books": results}

def borrow_book(member_id: str, isbn: str) -> dict:
    """Check out a book for a library member.

    Args:
        member_id: The ID of the member (e.g., M001).
        isbn: The ISBN of the book to borrow.

    Returns:
        Success or error message regarding the checkout.
    """
    if member_id not in MEMBERS:
        return {"status": "error", "message": f"Member ID '{member_id}' not found."}
    
    if isbn not in CATALOG:
        return {"status": "error", "message": f"Book with ISBN '{isbn}' not found in catalog."}
    
    book = CATALOG[isbn]
    if book["available_copies"] <= 0:
        return {"status": "error", "message": f"No available copies for '{book['title']}'."}
    
    # Calculate due date (14 days from today)
    due_date = (date.today() + timedelta(days=14)).isoformat()
    
    # Update records
    book["available_copies"] -= 1
    MEMBERS[member_id]["borrowed_books"].append({"isbn": isbn, "due_date": due_date})
    
    return {
        "status": "success", 
        "message": f"Successfully borrowed '{book['title']}'.", 
        "due_date": due_date
    }

def return_book(member_id: str, isbn: str) -> dict:
    """Return a borrowed book to the library.

    Args:
        member_id: The ID of the member returning the book.
        isbn: The ISBN of the book being returned.

    Returns:
        Success or error message regarding the return.
    """
    if member_id not in MEMBERS:
        return {"status": "error", "message": f"Member ID '{member_id}' not found."}
    
    member = MEMBERS[member_id]
    borrowed = member["borrowed_books"]
    
    for item in borrowed:
        if item["isbn"] == isbn:
            borrowed.remove(item)
            if isbn in CATALOG:
                CATALOG[isbn]["available_copies"] += 1
            return {"status": "success", "message": f"Book '{isbn}' returned successfully."}
            
    return {"status": "error", "message": f"Member '{member_id}' does not have book '{isbn}' checked out."}

def check_member_status(member_id: str) -> dict:
    """Check a member's details and currently borrowed books.

    Args:
        member_id: The ID of the member to check.

    Returns:
        Member information including borrowed books and due dates.
    """
    if member_id not in MEMBERS:
        return {"status": "error", "message": f"Member ID '{member_id}' not found."}
    
    member = MEMBERS[member_id]
    
    # Enhance borrowed books with titles
    borrowed_details = []
    for item in member["borrowed_books"]:
        title = CATALOG.get(item["isbn"], {}).get("title", "Unknown Title")
        borrowed_details.append({
            "isbn": item["isbn"],
            "title": title,
            "due_date": item["due_date"]
        })
        
    return {
        "status": "success", 
        "member_name": member["name"], 
        "borrowed_books": borrowed_details
    }

# ── Agent ─────────────────────────────────────────────────────────────────────

root_agent = Agent(
    name="library_system_agent",
    model=MODEL_NAME,
    description="A helpful library management assistant.",
    instruction="""
You are the official virtual assistant for a public library.
You help librarians and members search the catalog, borrow books, return books, and check member statuses.

Always be polite, clear, and accurate. Never guess or make up information about books or members.
Every answer must be grounded in what the tools return.

- When asked to find a book, use `search_catalog`.
- When a member wants to borrow or check out a book, use `borrow_book`. You will need their member_id and the book's ISBN.
- When a book is being returned, use `return_book`.
- When asked about what books a member has borrowed or their due dates, use `check_member_status`.

If you don't have enough information (like a missing member ID or ISBN), ask the user for it before calling the tool.

Respond in a helpful, professional tone. Keep answers concise.
""",
    tools=[
        search_catalog,
        borrow_book,
        return_book,
        check_member_status,
    ],
)
