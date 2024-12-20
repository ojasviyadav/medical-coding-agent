import json
from tools import ToolNames
from parser import view_subterms_at_level

class ToolHandler:
    def __init__(self):
        self.tools = {
            ToolNames.ICD_10_PARSER.value: self.parse_icd_10
        }

    def process_tool_call(self, tool_call: dict):
        """Process incoming tool calls and route to appropriate handler"""
        try:
            print(f"\n\n\n\ntool_call: {tool_call}\n\n\n\n")
            tool_name = tool_call.name
            tool_input = tool_call.input
            
            if not isinstance(tool_input, dict):
                # Handle case where input might be a JSON string
                tool_input = json.loads(tool_input)
            
            if tool_name not in self.tools:
                raise ValueError(f"Unknown tool: {tool_name}")
            
            return self.tools[tool_name](tool_input)
        except Exception as e:
            print(f"Error processing tool call: {e}")
            return None

    def parse_icd_10(self, input_data: dict) -> dict:
        """Handler for ICD-10 parser tool"""
        # Extract required parameters from input_data
        filename = input_data.get('filename')
        search_terms = input_data.get('search_terms')
        target_level = input_data.get('target_level', 0)
        main_terms = input_data.get('main_terms')
        current_path = input_data.get('current_path')


        # Call the parser function
        results = view_subterms_at_level(
            filename=filename,
            search_terms=search_terms,
            target_level=target_level,
            main_terms=main_terms,
            current_path=current_path
        )

        return results
