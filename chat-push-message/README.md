# AI Practice Project

A Python-based AI chatbot application that integrates with OpenAI's GPT-4o-mini model and Pushover notification service.

## Features

- **AI Chat Interface**: Interactive chat interface built with Gradio
- **OpenAI Integration**: Uses GPT-4o-mini model for intelligent responses
- **Pushover Notifications**: Can send messages to Pushover account via API
- **Function Calling**: Supports tool/function execution for external actions
- **Conversation History**: Maintains chat history for contextual conversations

## Project Structure

```
practice/
├── main.py          # Main application with chat interface
├── pyproject.toml   # Project dependencies and configuration
├── README.md        # This file
└── uv.lock          # Lock file for dependency versions
```

## Dependencies

- **openai**: OpenAI API client for GPT-4o-mini integration
- **gradio**: Web interface framework for the chat application
- **python-dotenv**: Environment variable management
- **requests**: HTTP library for Pushover API calls
- **ruff**: Python linter and formatter

## Setup Instructions

1. **Install Dependencies**:
   ```bash
   uv sync
   ```

2. **Environment Variables**:
   Create a `.env` file with the following variables:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   PUSHOVER_URL=https://api.pushover.net/1/messages.json
   PUSHOVER_TOKEN=your_pushover_app_token
   PUSHOVER_USER=your_pushover_user_key
   ```

3. **Run the Application**:
   ```bash
   uv shell
   python main.py
   ```

## How It Works

1. **Chat Interface**: Users interact through a Gradio web interface
2. **AI Processing**: Messages are sent to GPT-4o-mini with system prompts
3. **Function Calling**: When users request admin contact, the AI can trigger Pushover notifications
4. **Tool Execution**: The system supports executing external functions (like SendMessage)
5. **Response Generation**: AI generates contextual responses based on conversation history

## Key Functions

- `chat_with_openai()`: Main chat function that handles AI interactions
- `SendMessage()`: Sends notifications via Pushover API
- `system_prompt()`: Defines the AI assistant's behavior and capabilities

## Technical Details

- **Model**: GPT-4o-mini (fast, cost-effective GPT-4o variant)
- **Framework**: Gradio 5.x for web interface
- **Package Manager**: UV for fast Python package management
- **Python Version**: Requires Python 3.12+

## Usage

1. Start the application
2. Open the provided web interface URL
3. Chat with the AI assistant
4. Request admin contact to trigger Pushover notifications

The AI assistant can answer questions, help with tasks, and send notifications when requested.
