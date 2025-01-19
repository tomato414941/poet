import os
import asyncio
from datetime import datetime
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from typing import Optional, Callable
from dotenv import load_dotenv

from config.prompts import PHILOSOPHER_PROMPT, DEFAULT_INITIAL_PROMPT

# Load environment variables
load_dotenv()

class Poet:
    def __init__(self, initial_prompt: str = DEFAULT_INITIAL_PROMPT):
        """
        Initialize the Poet class
        
        Args:
            initial_prompt (str): Initial prompt to start the thinking process
        """
        self.model = ChatOpenAI()  # Will automatically use OPENAI_API_KEY from environment
        self.system_message = SystemMessage(content=PHILOSOPHER_PROMPT)
        self.prompt = initial_prompt
        self._thinking = False
        self.on_thought_generated: Optional[Callable[[str], None]] = None

    async def think(self, text: str) -> str:
        """
        Think deeply about the given text and return the result
        
        Args:
            text (str): Text to contemplate on
            
        Returns:
            str: The result of contemplation
        """
        messages = [
            self.system_message,
            HumanMessage(content=text)
        ]
        response = await self.model.ainvoke(messages)
        return response.content

    async def think_forever(self):
        """
        Continuously generate thoughts every 10 minutes.
        Each thought is used as input for the next thought.
        
        The method handles errors gracefully and retries after a short delay if an error occurs.
        """
        if self._thinking:
            return
        
        self._thinking = True
        try:
            while True:
                try:
                    # Generate next thought
                    thought = await self.think(self.prompt)
                    
                    # Update prompt for next iteration
                    self.prompt = thought
                    
                    # Notify listeners
                    if self.on_thought_generated:
                        await self.on_thought_generated(thought)
                    
                    # Wait for 10 minutes
                    await asyncio.sleep(600)
                    
                except Exception as e:
                    print(f"Error during thought generation: {e}")
                    # Wait for 1 minute before retrying
                    await asyncio.sleep(60)
        
        finally:
            self._thinking = False

    def is_thinking(self) -> bool:
        """Check if the continuous thinking process is active"""
        return self._thinking

    def stop_thinking(self):
        """Stop the continuous thinking process"""
        self._thinking = False