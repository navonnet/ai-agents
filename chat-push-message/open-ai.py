#openai Agent sdl
from dotenv import load_dotenv
from agents import Agent, trace, Runner, function_tool
import asyncio
from rich.console import Console
from rich.markdown import Markdown
from pushover import NotifyMe
import gradio as gr

load_dotenv(override=True)

@function_tool
def notify(email: str) -> str:
    """Send a notification with the provided email address.
    
    Args:
        email: The email address to send notification about
        
    Returns:
        A confirmation message
    """
    n = NotifyMe()
    n.notify(email)
    return f"Notification sent for email: {email}"

agent1 = Agent(name="agent1", model="gpt-4o-mini", 
                instructions="""Pretent to be math teacher for class 7th grade in INDIA.
                 Ask math question for line and angles. It is about parelle lines and transversal.
                 if user ask for contact admin then ask him email and notify with that email. use tool "notify"
                 """, tools=[notify])

async def initChat(message, history):
  with trace("math-quiz"):
        response =  await Runner.run(agent1, f"{message} {history}")
        return response.final_output

if __name__ == "__main__":
    gr.ChatInterface(initChat, type="messages").launch()