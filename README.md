# Sidekick - Personal AI Co-Worker

## Overview

Sidekick is an intelligent multi-agent research assistant that combines the power of LangGraph and Gradio to deliver reliable, up-to-date answers. The system employs a unique worker-evaluator architecture where a tool-using worker agent performs tasks while an evaluator agent verifies outputs against user-defined success criteria. This approach enables cost-effective models like `gpt-4o-mini` to produce high-quality, validated results through iterative refinement.

## Features

- **Multi-Agent Architecture**: Worker agent handles task execution while evaluator agent ensures quality and completeness
- **Rich Tool Integration**: 
  - Web browsing capabilities via Playwright
  - Google search integration through Serper API
  - Wikipedia knowledge access
  - Python code execution (REPL)
  - Local file management in sandboxed environment
  - Push notifications via Pushover
- **Intelligent Evaluation Loop**: Automatic feedback and iteration until success criteria are met or clarification is needed
- **Stateful Conversations**: Persistent chat history using LangGraph checkpoints
- **Interactive Web UI**: Clean Gradio interface with chat-style interaction
- **Resource Management**: Automatic cleanup of browser sessions and resources
- **Flexible Success Criteria**: User-defined validation rules for task completion

## Tech Stack

- **Framework**: LangGraph for agent orchestration and state management
- **LLM**: OpenAI GPT-4o-mini for both worker and evaluator agents
- **UI**: Gradio for web-based chat interface
- **Browser Automation**: Playwright for headless web browsing
- **Search**: Google Serper API and Wikipedia API
- **Code Execution**: Python REPL tool
- **Notifications**: Pushover API
- **Storage**: SQLite-based memory persistence
- **Environment**: Python with UV package manager

## Project Structure

```
.
├── app.py                  # Gradio UI application entry point
├── sidekick.py            # Core Sidekick agent with LangGraph state machine
├── sidekick_tools.py      # Tool definitions and integrations
├── memory.db              # SQLite database for conversation persistence
├── agent-graph.png        # Visual representation of agent workflow
├── app-screenshot.png     # UI screenshot
├── sandbox/               # Sandboxed directory for file operations
│   ├── berlin_indian_restaurants.md
│   └── dinner.md
└── README.md              # Project documentation
```

## Agent Architecture

![Agent Graph](agent-graph.png)

The system implements a sophisticated state machine with the following flow:

1. **Worker Node**: Receives user requests and executes tasks using available tools
2. **Tool Node**: Executes specific tools (browser, search, file operations, etc.)
3. **Evaluator Node**: Validates worker output against success criteria
4. **Routing Logic**: 
   - Worker → Tools (when tool calls are needed)
   - Worker → Evaluator (when response is ready)
   - Evaluator → Worker (if criteria not met)
   - Evaluator → END (if criteria met or user input needed)

## Getting Started

### Prerequisites

- Python 3.8+
- UV package manager
- OpenAI API key

### Installation

1. Install dependencies:
   ```bash
   uv sync
   ```

2. Create a `.env` file with required environment variables:
   ```
   OPENAI_API_KEY=your_openai_api_key
   SERPER_API_KEY=your_serper_api_key  # Optional, for Google search
   PUSHOVER_TOKEN=your_pushover_token  # Optional, for notifications
   PUSHOVER_USER=your_pushover_user    # Optional, for notifications
   ```

### Running the Application

Launch the Gradio interface:
```bash
uv run app.py
```

The application will open automatically in your default browser.

### Usage

1. Enter your request in the message field
2. Optionally specify success criteria (e.g., "Include at least 3 sources" or "Provide code examples")
3. Click "Go!" or press Enter
4. The worker agent will process your request using available tools
5. The evaluator will provide feedback on the response
6. If criteria aren't met, the worker will iterate automatically
7. Use "Reset" button to start a new conversation

## Configuration

### Tool Customization

Tools are defined in `sidekick_tools.py` and can be extended or modified:

- **Playwright Tools**: Browser automation for web scraping
- **File Management**: Sandboxed file operations in `sandbox/` directory
- **Search Tools**: Google Serper and Wikipedia integration
- **Python REPL**: Execute Python code dynamically
- **Push Notifications**: Send alerts via Pushover

### Model Configuration

Both worker and evaluator use `gpt-4o-mini` by default. You can modify the model in `sidekick.py`:

```python
worker_llm = ChatOpenAI(model="gpt-4o-mini")
evaluator_llm = ChatOpenAI(model="gpt-4o-mini")
```

## Future Enhancements

- Distribute tool usage across specialized agents instead of a single worker node
- Integrate domain-specific toolkits for targeted use cases
- Add support for additional LLM providers
- Implement advanced memory and context management
- Expand tool library with more integrations
