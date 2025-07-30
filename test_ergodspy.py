"""Quick test to ensure ergodspy works correctly"""

from ergodspy import make_sig
import dspy

def test_basic_signatures():
    """Test various signature creation patterns"""
    
    # Test 1: Simple signature
    sig1 = make_sig("question", "answer")
    assert 'question' in sig1.input_fields
    assert 'answer' in sig1.output_fields
    assert sig1.input_fields['question'].description is None
    print("✓ Test 1: Simple signature")
    
    # Test 2: With system prompt
    sig2 = make_sig("query", "response", "You are helpful")
    assert sig2.__doc__ == "You are helpful"
    print("✓ Test 2: System prompt")
    
    # Test 3: Multiple fields as string
    sig3 = make_sig("a, b, c", "x, y")
    assert 'a' in sig3.input_fields and 'b' in sig3.input_fields and 'c' in sig3.input_fields
    assert 'x' in sig3.output_fields and 'y' in sig3.output_fields
    print("✓ Test 3: Multiple fields string")
    
    # Test 4: With types
    sig4 = make_sig(
        ["topic", "count: int", "tags: list[str]"],
        ["result", "score: float"]
    )
    assert sig4.__annotations__['count'] == int
    assert sig4.__annotations__['score'] == float
    assert sig4.__annotations__['tags'] == list[str]
    print("✓ Test 4: Type annotations")
    
    # Test 5: With descriptions
    sig5 = make_sig(
        ["query: 'User question'", "context"],
        ["answer: 'The response'"]
    )
    assert sig5.input_fields['query'].description == "User question"
    assert sig5.output_fields['answer'].description == "The response"
    print("✓ Test 5: Descriptions")
    
    # Test 6: Tuple format
    sig6 = make_sig(
        [("question", str, "What to ask"), ("limit", int)],
        [("response", "The answer"), ("count", int, "Number of results")]
    )
    assert sig6.input_fields['question'].description == "What to ask"
    assert sig6.output_fields['response'].description == "The answer"
    assert sig6.output_fields['count'].description == "Number of results"
    assert sig6.__annotations__['limit'] == int
    print("✓ Test 6: Tuple format")
    
    # Test 7: Works with DSPy
    try:
        dspy.configure(lm=dspy.LM('openai/gpt-4o-mini', cache=False))
    except:
        # If no API key, just test module creation
        pass
    
    qa_sig = make_sig("question", "answer", "You are a helpful assistant")
    qa_module = dspy.Predict(qa_sig)
    
    print("✓ Test 7: DSPy compatibility (module creation)")
    
    # Test 8: Semicolon syntax for type and description
    sig7 = make_sig(
        ["query: str; The user's question", "limit: int; Maximum results"],
        ["results: list[str]; Matching items", "total: int"]
    )
    assert sig7.input_fields['query'].description == "The user's question"
    assert sig7.__annotations__['query'] == str
    assert sig7.input_fields['limit'].description == "Maximum results"
    assert sig7.__annotations__['limit'] == int
    assert sig7.output_fields['results'].description == "Matching items"
    assert sig7.__annotations__['results'] == list[str]
    assert sig7.output_fields['total'].description is None
    print("✓ Test 8: Semicolon syntax")
    
    print("\n✅ All tests passed!")

if __name__ == "__main__":
    test_basic_signatures()
