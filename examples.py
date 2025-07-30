"""Example usage of ergodspy"""

from ergodspy import make_sig
import dspy

# Configure DSPy (you'll need to add your API key)
dspy.configure(lm=dspy.LM('openai/gpt-4o-mini'))

# Example 1: Simple Q&A
print("=== Example 1: Simple Q&A ===")
qa_sig = make_sig("question", "answer")
qa = dspy.Predict(qa_sig)

result = qa(question="What is the capital of France?")
print(f"Q: What is the capital of France?")
print(f"A: {result.answer}\n")

# Example 2: Joke generator with types
print("=== Example 2: Joke Generator ===")
joke_sig = make_sig(
    inputs=["topic", "audience: 'Target audience'"],
    outputs=["setup", "punchline", "rating: float"],
    system="You are a professional comedian"
)
comedian = dspy.ChainOfThought(joke_sig)

result = comedian(topic="programming", audience="software developers")
print(f"Topic: programming")
print(f"Setup: {result.setup}")
print(f"Punchline: {result.punchline}")
print(f"Rating: {result.rating}\n")

# Example 3: Complex analysis task
print("=== Example 3: Data Analysis ===")
analysis_sig = make_sig(
    inputs=[
        "data: list[float]", 
        "threshold: float",
        ("operation", str, "What analysis to perform")
    ],
    outputs=[
        "mean: float",
        "above_threshold: list[float]",
        ("summary", str, "Brief summary of findings")
    ],
    system="You are a data analyst. Analyze the provided data."
)
analyzer = dspy.ChainOfThought(analysis_sig)

result = analyzer(
    data=[1.5, 3.2, 4.8, 2.1, 5.5, 3.9],
    threshold=3.0,
    operation="statistical summary"
)
print(f"Mean: {result.mean}")
print(f"Above threshold: {result.above_threshold}")
print(f"Summary: {result.summary}")
