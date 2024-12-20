from anthropic import Anthropic
from tool_handler import ToolHandler
from tools import get_icd_10_parser_tool
from system_prompt import system_prompt
import asyncio
from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()

ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
CLAUDE_35_SONNET = "claude-3-5-sonnet-20241022"
ICD_10_FILE_PATH = Path("icd_datasets/icd-10-cm-index-2025.xml")

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
                "content": str(tool_result)
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
        # print('response: ', response)
        # print()
        
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
    default_note = """PATIENT NOTE
Date: 2024-03-20
RE: Initial Visit

CHIEF COMPLAINT:
Patient presents with symptoms of Type 2 diabetes mellitus with early signs of diabetic neuropathy in both feet. 
Also reports ongoing hypertension.

HISTORY OF PRESENT ILLNESS:
52-year-old male reports increased thirst, frequent urination, and numbness/tingling in feet for past 3 months. 
Blood sugar readings at home consistently above 200 mg/dL. Has family history of diabetes (mother and sister). 
Patient also notes ongoing high blood pressure despite current medication.

VITAL SIGNS:
- BP: 142/90 mmHg
- Pulse: 78
- Weight: 198 lbs
- Height: 5'10"
- BMI: 28.4

LAB RESULTS:
- Fasting Blood Glucose: 186 mg/dL
- HbA1c: 7.8%

MEDICATIONS:
- Lisinopril 10mg daily for hypertension
- No current diabetes medications

ASSESSMENT:
1. Type 2 diabetes mellitus, uncontrolled
2. Diabetic neuropathy
3. Essential hypertension

PLAN:
- Start Metformin 500mg twice daily
- Continue Lisinopril
- Diabetes education referral
- Follow-up in 2 weeks
- Recommend diet and exercise program"""

    print("\nPlease enter the patient notes (press Enter twice to use default note):")
    
    user_input = []
    while True:
        line = input()
        if line == "" and (len(user_input) == 0 or user_input[-1] == ""):
            break
        user_input.append(line)
    
    patient_note = "\n".join(user_input) if user_input and user_input != [''] else default_note

    initial_messages = [{
        "role": "user",
        "content": f"Please analyze these patient notes and identify the appropriate ICD-10 codes:\n\n{patient_note}"
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