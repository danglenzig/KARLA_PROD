import re
import json
from typing import Type, TypeVar
from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)

def clean_and_validate(json_like: str, model_cls: Type[T]) -> T:
    # Extract outermost JSON object (preserves escapes inside strings)
    json_match = re.search(r'\{(?:[^{}]|(?R))*\}', json_like, re.DOTALL)
    if not json_match:
        raise ValueError("No valid JSON object found")
    
    json_str = json_match.group()
    print(f"Extracted JSON: {repr(json_str)[:200]}...")  # Debug: shows true escapes
    
    # Test json.loads first (model_validate_json uses this internally)
    data = json.loads(json_str)
    return model_cls.model_validate(data)  # Use dict directly - more reliable