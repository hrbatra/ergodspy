"""ergodspy - Ergonomic DSPy signatures

Write DSPy signatures with minimal boilerplate and maximum clarity.
"""

__version__ = "0.1.2"

import re
from typing import Any, Union, List, Type
import dspy

def make_sig(inputs: Union[str, List[Union[str, tuple]]], 
             outputs: Union[str, List[Union[str, tuple]]] = None,
             system: str = "") -> Type[dspy.Signature]:
    """
    Create a DSPy signature with ergonomic syntax.
    
    Args:
        inputs: Input field definitions (str or list)
        outputs: Output field definitions (str or list)
        system: Optional system prompt/instructions
    
    Field formats:
        - "name" - just the field name (defaults to str type)
        - "name: type" - field with type annotation (e.g. "count: int")
        - "name: type; description" - field with type and description
        - ("name", type) - tuple with actual type object
        - ("name", "description") - tuple with description
        - ("name", type, "description") - full specification
        
    Examples:
        # Simple Q&A
        make_sig("question", "answer")
        
        # With system prompt
        make_sig("question", "answer", "You are a helpful assistant")
        
        # Multiple fields - use a list
        make_sig(
            inputs=["topic", "tags: list[str]", "query: str; The user's question"],
            outputs=["joke", "confidence: float; Confidence score 0-1"]
        )
        
        # Full complexity
        make_sig(
            inputs=[
                "query",
                ("context", str, "Background information"),
                "style: str; Either 'casual' or 'formal'"
            ],
            outputs=[
                ("answer", str, "The response"),
                "confidence: float; How certain the model is"
            ],
            system="You are an expert assistant"
        )
    """
    # Handle the case where outputs is None (positional args)
    if outputs is None:
        raise ValueError("Both inputs and outputs are required")
    
    # Normalize inputs and outputs to lists
    def normalize_to_list(field_spec):
        if isinstance(field_spec, str):
            # Single string = single field
            return [field_spec]
        return field_spec
    
    inputs = normalize_to_list(inputs)
    outputs = normalize_to_list(outputs)
    
    # Parse a single field specification
    def parse_field(field):
        """Parse various field formats into (name, description, type)"""
        
        # Handle tuple formats
        if isinstance(field, tuple):
            if len(field) == 2:
                name, second = field
                # (name, type)
                if isinstance(second, type) or hasattr(second, '__origin__'):
                    return name, None, second
                # (name, description)
                elif isinstance(second, str):
                    return name, second, str
            elif len(field) == 3:
                # (name, type, description)
                name, typ, desc = field
                return name, desc, typ
            else:
                raise ValueError(f"Invalid tuple format: {field}")
        
        # Handle string formats
        elif isinstance(field, str):
            # Check if field contains semicolon (type; description format)
            if ';' in field:
                # Split on first semicolon
                type_part, desc = field.split(';', 1)
                type_part = type_part.strip()
                desc = desc.strip()
                
                # Now parse the type part
                if ':' in type_part:
                    name, type_str = type_part.split(':', 1)
                    name = name.strip()
                    type_str = type_str.strip()
                    typ = parse_type_string(type_str)
                    return name, desc, typ
                else:
                    # Just name; description (type defaults to str)
                    return type_part, desc, str
            
            # No semicolon - check for colon (name: type or name: 'description' format)
            elif ':' in field:
                name, rest = field.split(':', 1)
                name = name.strip()
                rest = rest.strip()
                
                # Check if it's a quoted description
                desc_match = re.match(r"^['\"](.+)['\"]$", rest)
                if desc_match:
                    return name, desc_match.group(1), str
                else:
                    # It's a type - try to parse it
                    typ = parse_type_string(rest)
                    return name, None, typ
            else:
                # Just a name
                return field.strip(), None, str
        
        raise ValueError(f"Cannot parse field: {field}")
    
    # Parse type annotations from strings
    def parse_type_string(type_str):
        """Convert string type annotations to actual types"""
        type_str = type_str.strip()
        
        # Simple built-in types
        simple_types = {
            'str': str,
            'int': int,
            'float': float,
            'bool': bool,
            'bytes': bytes,
        }
        
        if type_str in simple_types:
            return simple_types[type_str]
        
        # Handle list[T] syntax
        list_match = re.match(r'^list\[(.+)\]$', type_str)
        if list_match:
            inner_type = parse_type_string(list_match.group(1))
            return list[inner_type]
        
        # Handle dict[K, V] syntax
        dict_match = re.match(r'^dict\[(.+),\s*(.+)\]$', type_str)
        if dict_match:
            key_type = parse_type_string(dict_match.group(1))
            val_type = parse_type_string(dict_match.group(2))
            return dict[key_type, val_type]
        
        # Default to str for unknown types
        # (In a real implementation, might want to handle more cases or raise an error)
        return str
    
    # Build the signature class
    namespace = {}
    annotations = {}
    
    # Process inputs
    for field in inputs:
        name, desc, typ = parse_field(field)
        namespace[name] = dspy.InputField(description=desc)
        annotations[name] = typ
    
    # Process outputs
    for field in outputs:
        name, desc, typ = parse_field(field)
        namespace[name] = dspy.OutputField(description=desc)
        annotations[name] = typ
    
    # Add annotations and docstring
    namespace['__annotations__'] = annotations
    if system:
        namespace['__doc__'] = system
    
    # Create and return the signature class
    return type("DynamicSignature", (dspy.Signature,), namespace)

# Export
__all__ = ['make_sig']
