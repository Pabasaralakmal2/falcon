# Librarian Agent

A library management assistant built with the Google Agent Development Kit (ADK). This agent demonstrates how to manage stateful data (like a catalog and members) through function calling.

## What it does

The `librarian_agent` acts as a virtual assistant for a public library. It can:
- **Search the catalog:** Look up books by title, author, or genre.
- **Manage checkout:** Borrow books for members and automatically calculate a 14-day due date, updating the available stock.
- **Process returns:** Accept returned books and replenish the available stock.
- **Check member status:** Provide a list of currently borrowed books and their due dates for a given member.

## How it works

This is a single-agent setup that uses four python function tools:

- `search_catalog`
- `borrow_book`
- `return_book`
- `check_member_status`

The agent uses these tools to interact with a mock in-memory database (`CATALOG` and `MEMBERS` dictionaries) to fulfill user requests accurately.

## Try it out

From the repository root, start the web interface:

```bash
adk web
```

Then try these prompts:
- *"I'm looking for a programming book by Mark Lutz. Do you have it?"*
- *"Can you check out Effective Java for member M002?"*
- *"What books does Alice Smith (M001) currently have checked out?"*
- *"I'd like to return C++ Primer for Bob Jones (M002)."*
