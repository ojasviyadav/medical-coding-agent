from typing import Dict, TypedDict
from enum import Enum

class ToolNames(Enum):
    """Enum for tool names to avoid string literals"""
    ICD_10_PARSER = "icd_10_parser_tool"

class Tool(TypedDict):
    """Type definition for a tool"""
    name: str
    description: str
    input_schema: Dict

def get_icd_10_parser_tool() -> Tool:
    """Returns the tool definition for ICD-10 parsing"""
    return {
        "name": ToolNames.ICD_10_PARSER.value,
        "description": "Shows subterms at any specified level for given search terms.",
        "input_schema": {
            "type": "object",
            "properties": {
                "filename": {"type": "string", "description": "Path to the ICD-10 XML file"},
                "search_terms": {"type": "array", "description": "List of search terms"},
                "target_level": {"type": "integer", "description": "Level at which to show detailed information (0-9)"},
                "main_terms": {"type": "array", "description": "Main term(s) to start from (required for levels > 0)"},
                "current_path": {"type": "array", "description": "Keeps track of the term hierarchy path (internal use)"}
            },
            "required": ["filename", "search_terms", "target_level", "main_terms", "current_path"]
        }
    }