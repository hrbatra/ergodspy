"""Minimal verification that ergodspy loads correctly"""

try:
    from ergodspy import make_sig
    print("✓ Import successful")
    
    # Test basic functionality
    sig = make_sig("input", "output")
    print("✓ Basic signature creation works")
    
    # Test that it creates proper dspy.Signature subclass
    import dspy
    assert issubclass(sig, dspy.Signature)
    print("✓ Creates proper DSPy signature")
    
    print("\n✅ ergodspy is ready to use!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
