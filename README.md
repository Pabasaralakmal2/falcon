# ADK Librarian Agent Demo

A beginner-friendly [Google Agent Development Kit (ADK)](https://google.github.io/adk-docs/) repository containing a Librarian Assistant agent.

| Agent | Folder | Pattern | Docs |
| --- | --- | --- | --- |
| Librarian Assistant | [`librarian_agent/`](librarian_agent/) | Single agent + stateful data | [README](librarian_agent/README.md) |

## The Agent

### Librarian Assistant - `librarian_agent/`

A stateful library management assistant. This agent uses four function tools to interact with an in-memory database of books and library members. It can search the library catalog, process book checkouts with automatic due date calculations, handle returns, and look up current member borrowing statuses.

Try: *"I'm looking for a programming book by Mark Lutz. Do you have it?"* or *"Can you check out Effective Java for member M002?"*

→ **[Full documentation](librarian_agent/README.md)** - tools, data, and usage.

## Project structure

```text
.
├── librarian_agent/
│   ├── __init__.py
│   ├── agent.py            # catalog, members, and library function tools
│   ├── .env.example        # per-agent config template
│   └── README.md
├── .env.example            # shared config template (repository root)
├── .gitignore
├── README.md
└── requirements.txt
```

Local credentials, virtual environments, Python caches, and ADK session data are excluded from Git.

## Prerequisites

Before you start, make sure you have the following. These are the minimum tools ADK needs to run an agent locally.

- **Python 3.10 or newer** - ADK is a Python framework, so you need a Python interpreter installed to run it at all. Check your version with `python3 --version`. If it's older than 3.10, install a newer Python from [python.org](https://www.python.org/downloads/) first.
- **A Google AI Studio API key or a configured Google Cloud project** - the agent's "brain" is a Gemini model, which runs on Google's servers, not on your laptop. You need credentials so your code is allowed to call that model. An [AI Studio](https://aistudio.google.com/apikey) API key is the fastest option for a workshop; a Vertex AI project is the alternative if your organization already uses Google Cloud.
- **Git** - used to download (clone) this project's code to your machine.

## Setup

Each step below explains *why* it exists, not just what to type, so you understand what's happening to your machine.

1. Clone the repository and enter its directory.

   ```bash
   git clone <your-repository-url>
   cd <repository-directory>
   ```

2. Create and activate a virtual environment, at the **repository root**.

   macOS/Linux:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

   Windows PowerShell:

   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

3. Install the dependencies.

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Create your local environment file.

   macOS/Linux:

   ```bash
   cp .env.example .env
   ```

   Windows PowerShell:

   ```powershell
   Copy-Item .env.example .env
   ```

5. Edit `.env` and provide either your Google AI Studio API key or your Vertex AI project settings. Never commit this file.

## Configuration

You can configure the agent in either of two places:

| Location | Template to copy | Use when |
| --- | --- | --- |
| Repository root `.env` | `.env.example` | Simplest, and what a workshop usually wants. |
| `librarian_agent/.env` | that folder's `.env.example` | You want the agent on its own key, project, or model. |

**When you run under `adk web` or `adk run`, the agent's own `.env` wins.** ADK searches upward
from the agent folder and stops at the first `.env` it finds, so a file inside
`librarian_agent/` takes priority over the one at the root.

Each `agent.py` also calls `load_dotenv()` itself, so the agents still work in a plain script or
notebook where ADK's CLI never runs. That call searches upward from your **current working
directory**, so from the repository root it picks up the root `.env` and does not see a per-agent
one. In short: per-agent `.env` files are honoured by ADK, and the root `.env` is the reliable
choice everywhere else.

A variable exported in your shell beats every `.env`, because `load_dotenv` never overwrites
something already set.

| Variable | Required | Default | Purpose |
| --- | --- | --- | --- |
| `GOOGLE_GENAI_USE_VERTEXAI` | Yes | `FALSE` | `FALSE` to authenticate with an API key, `TRUE` to use Vertex AI |
| `GOOGLE_API_KEY` | When not using Vertex AI | - | Your Google AI Studio / Gemini API key |
| `GOOGLE_CLOUD_PROJECT` | When using Vertex AI | - | Your GCP project ID |
| `GOOGLE_CLOUD_LOCATION` | When using Vertex AI | - | Region, e.g. `us-central1` |
| `GOOGLE_GENAI_MODEL` | No | `gemini-3.1-flash-lite` | Model the agent uses. Falls back to the default if unset |

If you set `GOOGLE_GENAI_USE_VERTEXAI=TRUE`, drop `GOOGLE_API_KEY` and set up application-default credentials first with `gcloud auth application-default login`.

## Run the agent

From the repository root, with the virtual environment active, run:

```bash
adk web
```

`adk web` is a command installed by the `google-adk` package (from step 3). It scans the current directory for agent folders like `librarian_agent/`, starts a local web server, and gives you a chat UI in the browser to talk to your agents - so you can test them interactively without writing any extra code. It prints a local URL (something like `http://localhost:8000`); open that in a browser and pick an agent from the dropdown. Stop the server anytime with `Ctrl+C` in the terminal.

You can also run a single agent straight from the terminal:

```bash
adk run librarian_agent
```

Always run these from the repository root.

### If port 8000 is already in use

```
ERROR: [Errno 48] error while attempting to bind on address ('127.0.0.1', 8000): address already in use
```

An earlier `adk web` is still running. Find it and stop it:

```bash
lsof -nP -iTCP:8000 -sTCP:LISTEN     # see what is holding the port
lsof -ti:8000 | xargs kill           # stop it
```

On Windows PowerShell the equivalent lookup is `Get-NetTCPConnection -LocalPort 8000`, then `Stop-Process -Id <pid>`.

Or just use a different port and leave the old one alone:

```bash
adk web --port 9000
```

## Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| Agent dropdown is empty in `adk web` | Started the server from the wrong directory | Run `adk web` from the repository root, which contains the agent folders |
| `ModuleNotFoundError: No module named 'librarian_agent'` | Running from inside the agent folder | `cd` to the repository root and run `adk run librarian_agent` from there |
| `command not found: adk` | Virtual environment not active | `source .venv/bin/activate` (or `.venv\Scripts\Activate.ps1`) |
| `Warning: python-dotenv not installed` | Dependencies not installed, or wrong venv | Activate the venv and run `python -m pip install -r requirements.txt` |
| `401` / `API key not valid` | Missing or wrong `GOOGLE_API_KEY` | Check your `.env`; regenerate the key at [AI Studio](https://aistudio.google.com/apikey) |
| `[Errno 48] address already in use` on port 8000 | An earlier `adk web` is still running | `lsof -ti:8000 \| xargs kill` to stop it, or start on another port with `adk web --port 9000` |

Agent-specific troubleshooting lives in each agent's own README.

## Security

Keep API keys and cloud credentials only in your local `.env` file or a secure secret manager. If a secret is ever committed, revoke or rotate it before removing it from Git history.
