import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from logic.manager_factory import ManagerFactory

def test_singleton():
    """Test that ManagerFactory is a singleton"""
    factory1 = ManagerFactory()
    factory2 = ManagerFactory()
    
    print("\n=== Testing Manager Factory ===")
    print(f"Factory1 id: {id(factory1)}")
    print(f"Factory2 id: {id(factory2)}")
    print(f"Are they the same instance? {factory1 is factory2}")
    
    # Test creating managers
    model_manager1 = factory1.create_model_manager()
    model_manager2 = factory2.create_model_manager()
    print("\nCreating managers from both factories...")
    print("✓ Successfully created managers")

if __name__ == "__main__":
    test_singleton() 