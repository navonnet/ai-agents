#!/usr/bin/env python3
"""
Test script to verify imports work correctly
"""

try:
    print("Testing imports...")
    
    # Test wa_api import
    from src.wa_api import waAPiClient
    print("✓ wa_api import successful")
    
    # Test inputModels import
    from src.inputModels import CreateContactInput, RegisterForEventInput
    print("✓ inputModels import successful")
    
    # Test langchain imports
    from langchain_core import messages
    from langchain_core.tools import Tool
    from langchain.tools import StructuredTool
    print("✓ langchain imports successful")
    
    # Test langgraph imports
    from langgraph.graph import StateGraph, START, END
    from langgraph.prebuilt import tools_condition, ToolNode
    from langgraph.checkpoint.memory import MemorySaver
    print("✓ langgraph imports successful")
    
    # Test other imports
    from langchain_openai import ChatOpenAI
    from pydantic import BaseModel
    print("✓ other imports successful")
    
    print("\nAll imports successful! The AttributeError should be resolved.")
    
except ImportError as e:
    print(f"Import error: {e}")
except Exception as e:
    print(f"Other error: {e}")
    import traceback
    traceback.print_exc()

