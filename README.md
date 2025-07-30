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

# Easy syntax for multiple fields, system prompt, and types/descriptions
medical_qa = make_sig(
    inputs=["question", "context; Background information"],
    outputs=["answer", "confidence: float; Confidence score from 0-1"], 
    system="You are a world-class medical expert"
)

# Use with DSPy modules
qa_module = dspy.Predict(qa_sig)
medical_expert = dspy.ChainOfThought(medical_qa)
```

## Comparison with Vanilla DSPy

Instead of:
```python
# Vanilla DSPy
import dspy
dspy.configure(lm=dspy.LM('openai/gpt-4o-mini'))

class JokeSignature(dspy.Signature):
    """You are a scrappy comedian filming your first Netflix special"""
    topic: str = dspy.InputField()
    style: str | None = dspy.InputField(description="Speaking style")
    setup: str = dspy.OutputField()
    punchline: str = dspy.OutputField()
    rating: float = dspy.OutputField(description="Your own rating of the joke from 1-10")
```

Write:
```python
# With ergodspy
from ergodspy import make_sig

JokeSignature = make_sig(
    inputs=["topic", "style: str; Speaking style"],
    outputs=["setup", "punchline", "rating: float; Your own rating of the joke from 1-10"],
    system="You are a scrappy comedian filming your first Netflix special"
)
```

## Field Format Reference

Each field can be specified in multiple ways:

1. **Just the name**: `"field_name"` → defaults to `str` type
2. **With type**: `"field_name: type"` → e.g., `"count: int"`, `"tags: list[str]"`
3. **With type and description**: `"field_name: type; description"` → e.g., `"query: str; The user's question"`
4. **Tuple with type**: `("field_name", type)` → e.g., `("embedding", list[float])`
5. **Tuple with description**: `("field_name", "description")` → e.g., `("query", "What to search for")`
6. **Full tuple**: `("field_name", type, "description")` → e.g., `("limit", int, "Max items to return")`

Full optionality:
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

## Contributing

This is a minimal library with a focused scope. If you'd like to contribute or have suggestions, please open an issue!

## License

MIT License - see LICENSE file for details.
