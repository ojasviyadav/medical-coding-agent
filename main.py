from anthropic import Anthropic
from tool_handler import ToolHandler
from tools import get_icd_10_parser_tool
from system_prompt import system_prompt
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()

ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
CLAUDE_35_SONNET = "claude-3-5-sonnet-20241022"

class LLM:
    def __init__(self):
        self.client = Anthropic(api_key=ANTHROPIC_API_KEY)

    async def get_response(self, messages: list[dict], system_prompt: str, tools: list[dict]):
        """Get response from Anthropic client"""
        response = self.client.messages.create(
            model=CLAUDE_35_SONNET,
            messages=messages,
            system=system_prompt,
            tools=tools,
            max_tokens=500,
            stream=False
        )
        return response

class AgenticLoop:
    def __init__(self, messages: list[dict], tools: list[dict], system_prompt: str):
        self.messages = messages
        self.tools = tools
        self.system_prompt = system_prompt
        self.tool_handler = ToolHandler()
        self.llm = LLM()

    async def run_tool_call(self, tool_use):
        try:
            print(f"\n=== Using {tool_use.name} tool ===")
            tool_result = self.tool_handler.process_tool_call(tool_use)
            return {
                "type": "tool_result",
                "tool_use_id": tool_use.id,
                "content": tool_result
            }
        except Exception as e:
            error_msg = f"Error executing tool {tool_use.name}: {str(e)}"
            print(error_msg)
            return {
                "type": "tool_result",
                "tool_use_id": tool_use.id,
                "content": error_msg
            }

    async def run_requested_tools(self, response):
        """Process tool calls concurrently and return the results"""
        tool_calls = [content for content in response.content if content.type == 'tool_use']
        if tool_calls:
            tool_results = await asyncio.gather(
                *[self.run_tool_call(tool_use) for tool_use in tool_calls],
                return_exceptions=False
            )
            return tool_results 
        return "No tool calls requested"

    async def generate_response(self):
        print('fetching response')
        response = await self.llm.get_response(
            messages=self.messages,
            system_prompt=self.system_prompt,
            tools=self.tools
        )
        print('response: ', response)
        print()
        
        self.messages.append({
            "role": "assistant",
            "content": response.content
        })

        tool_results = await self.run_requested_tools(response)
        
        if tool_results != "No tool calls requested":
            self.messages.append({
                "role": "user",
                "content": tool_results
            })
            return await self.generate_response()
        
        return response

async def main():
    initial_messages = [{
        "role": "user",
        "content": "Help me find ICD-10 codes related to diabetes."
    }]
    
    tools = [get_icd_10_parser_tool()]
    
    # Create and run the agent
    agent = AgenticLoop(
        messages=initial_messages,
        tools=tools,
        system_prompt=system_prompt
    )
    
    response = await agent.generate_response()
    print("Final response:", response)

if __name__ == "__main__":
    asyncio.run(main())