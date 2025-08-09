from enum import Enum
from openai import OpenAI
import os

class Agents(Enum):
    OpenAI = 1,
    Gemini = 2,
    DeepSeek = 3


class chatAssitant:
    
    def __init__(self, agent: Agents, key: str) -> None:
        self.agent = agent
        self.client = OpenAI(api_key=key)
    
    def reply(self, userMessage, tools=None) -> str:
        #messages = [{"role": "system", "content": system_prompt()}] + history + [{"role": "user", "content": message}]
        messages = [{"role": "user", "content": userMessage}]
        response = self.client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages, tools=tools)
        return response.choices[0].message.content


