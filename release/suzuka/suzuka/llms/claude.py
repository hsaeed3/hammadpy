import os 
from typing import Optional, List, Dict 
import anthropic 

class AnthropicInstructor:
    def __init__(self, api_key: Optional[str] = None):
        self.model = None
        self.query = None
        self.system = None
        if api_key is None:
            api_key = os.getenv("ANTHROPIC_API_KEY")

        if api_key is None:
            raise ValueError("Anthropic API key is not available")

        self.client = anthropic.Anthropic(api_key=api_key)

    def chat( self, system: Optional[str] = None, query: Optional[str] = None, model: str = "claude-3-opus-20240229", max_tokens: int = 1000, temperature: float = 0):
        if system is None:
            system_prompt = "You are a helpful assistant."
        else:
            system_prompt = system
        if model is None:
            model = "claude-3-opus-20240229"
        else:
            model = model
        if query is None:
            raise ValueError("Query is required for instruct()")
        if self.client is None:
            raise ValueError("Anthropic client is not available")
        message = self.client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1000,
            temperature=0,
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": query
                        }
                    ]
                }
            ]
        )
        return message.content
    
if __name__ == "__main__":
    instructor = AnthropicInstructor()
    completion = instructor.chat(query="What is the capital of France?")
    print(completion)