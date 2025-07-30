# ergodspy

Ergonomic DSPy signatures - write DSPy signatures with minimal boilerplate and maximum clarity.

## Installation

```bash
pip install ergodspy
```

## Quick Start

```python
from ergodspy import make_sig
import dspy

# Simple Q&A signature
qa_sig = make_sig("question", "answer")

# With system prompt
medical_qa = make_sig(
    "question", 
    "answer", 
    "You are a medical expert assistant"
)

# Use with DSPy modules
qa_module = dspy.Predict(qa_sig)
medical_expert = dspy.ChainOfThought(medical_qa)
```

## Features

- **Minimal syntax** - Start with just `make_sig("input", "output")`
- **Progressive complexity** - Add types and descriptions only when needed
- **Flexible formats** - Strings, lists, or tuples - your choice
- **Type safety** - Full support for Python type hints
- **DSPy compatible** - Creates standard DSPy signatures

## Examples

### Simple Single Input/Output

```python
# Just field names (defaults to str type)
sig = make_sig("question", "answer")
```

### Multiple Fields

```python
# String format with comma separation
sig = make_sig(
    "query, context", 
    "answer, confidence: float"
)

# List format for clarity
sig = make_sig(
    inputs=["query", "context"],
    outputs=["answer", "confidence: float"]
)
```

### With Types and Descriptions

```python
# Using semicolon to separate type and description
sig = make_sig(
    inputs=[
        "topic",                               # Just name (str type)
        "tags: list[str]",                     # With type annotation
        "query: str; What to ask about?",      # Type and description
        ("limit", int, "Max results")          # Tuple format
    ],
    outputs=[
        "results: list[dict]",
        ("score", float, "Relevance score 0-1"),
        "explanation: str; Why these results?"
    ],
    system="You are a helpful search assistant"
)
```

### Using with DSPy

```python
import dspy
from ergodspy import make_sig

# Configure DSPy
dspy.configure(lm=dspy.LM('openai/gpt-4o-mini'))

# Create a signature
joke_sig = make_sig(
    inputs=["topic", "audience: str; Who is this joke for?"],
    outputs=["setup", "punchline", "rating: float; Score from 1-10"],
    system="You are a comedian"
)

# Use with any DSPy module
joke_maker = dspy.ChainOfThought(joke_sig)
result = joke_maker(topic="programming", audience="developers")
print(f"{result.setup}\n{result.punchline}")
```

## Field Format Reference

Each field can be specified in multiple ways:

1. **Just the name**: `"field_name"` → defaults to `str` type
2. **With type**: `"field_name: type"` → e.g., `"count: int"`, `"tags: list[str]"`
3. **With type and description**: `"field_name: type; description"` → e.g., `"query: str; The user's question"`
4. **Tuple with type**: `("field_name", type)` → e.g., `("embedding", list[float])`
5. **Tuple with description**: `("field_name", "description")` → e.g., `("query", "What to search for")`
6. **Full tuple**: `("field_name", type, "description")` → e.g., `("limit", int, "Max items to return")`

## Comparison with Vanilla DSPy

Instead of:
```python
# Vanilla DSPy
import dspy

class QASignature(dspy.Signature):
    """You are a helpful assistant"""
    question: str = dspy.InputField()
    context: str = dspy.InputField(description="Background information")
    answer: str = dspy.OutputField()
    confidence: float = dspy.OutputField(description="Confidence score")
```

Write:
```python
# With ergodspy
from ergodspy import make_sig

sig = make_sig(
    inputs=["question", "context: str; Background information"],
    outputs=["answer", "confidence: float; Confidence score"],
    system="You are a helpful assistant"
)
```

## Contributing

This is a minimal library with a focused scope. If you'd like to contribute or have suggestions, please open an issue!

## License

MIT License - see LICENSE file for details.
