import os
import json
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr
import requests
from chatAssitant import chatAssitant, Agents

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
pushUrl = os.getenv("PUSHOVER_URL")

def SendMessage(message):
    requests.post(pushUrl, data={
        "token": os.getenv("PUSHOVER_TOKEN"),
        "user": os.getenv("PUSHOVER_USER"),
        "message": message,
    })

def inform_me():
    print("Hello from practice!")

def system_prompt():
    return """You are a helpful assistant that can answer questions and help with tasks.
        You are also able to push messages to a pushover account. If user asked to contact admin then use tool SendMessage"""
        

def chat_with_openai(message, history):
    tools = [
        {
            "type": "function",
            "function": {
                "id":1,
                "name": "SendMessage",
                "description": "Send a message to a pushover account",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "message": {
                            "type": "string",
                            "description": "The message to send"
                        }   
                    }
                }
            }
        }
    ]
    messages = [{"role": "system", "content": system_prompt()}] + history + [{"role": "user", "content": message}]
    done = False

    while not done:    
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages, tools=tools)

        if response.choices[0].finish_reason == "tool_calls":
            results = []
            message = response.choices[0].message
            tool_calls = message.tool_calls
            for tool in tool_calls:
                name = tool.function.name
                arguments = json.loads(tool.function.arguments)
                func = globals().get(name)
                result = func(**arguments) if func else {}
                results.append({"role": "tool","content": json.dumps(result),"tool_call_id": tool.id})
            messages.append(message)
            messages.extend(results)
        else:
            done = True
      
    return response.choices[0].message.content

if __name__ == "__main__":
    #gr.ChatInterface(chat_with_openai, type="messages").launch()
    ca = chatAssitant(Agents.OpenAI, os.getenv("OPENAI_API_KEY"))
    reply = ca.reply("Hi")
    print(reply)
    
