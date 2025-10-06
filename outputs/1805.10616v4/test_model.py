import pytest
import torch
import sys
import os

# Add parent directory to path to import model
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from model import create_model
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure model.py is in the same directory")
    sys.exit(1)

class TestModel:
    def test_model_creation(self):
        """Test that model can be created"""
        model = create_model()
        assert model is not None
        print("✅ Model creation test passed")
        
    def test_forward_pass(self):
        """Test forward pass with sample data"""
        model = create_model()
        x = torch.randn(10, 784)
        output = model(x)
        
        # Check output shape
        assert output.shape == (10, 10)  # batch_size, output_dim
        assert not torch.isnan(output).any(), "Output contains NaN values"
        print("✅ Forward pass test passed")
        
    def test_prediction(self):
        """Test prediction method"""
        model = create_model()
        x = torch.randn(5, 784)
        predictions = model.predict(x)
        
        # Check predictions shape and type
        assert predictions.shape == (5,)
        assert predictions.dtype == torch.int64
        assert (predictions >= 0).all() and (predictions < 10).all()
        print("✅ Prediction test passed")
        
    def test_different_input_sizes(self):
        """Test model with different input sizes"""
        model = create_model({'input_dim': 512, 'hidden_dim': 128, 'output_dim': 5})
        x = torch.randn(8, 512)
        output = model(x)
        
        assert output.shape == (8, 5)
        print("✅ Different input sizes test passed")
    
    def test_feature_extraction(self):
        """Test feature extraction method"""
        model = create_model()
        x = torch.randn(3, 784)
        
        if hasattr(model, 'get_features'):
            features = model.get_features(x)
            assert features.shape[0] == 3  # batch size
            assert len(features.shape) == 2  # 2D tensor
            print("✅ Feature extraction test passed")
        else:
            print("⚠️  Model doesn't have get_features method")

def run_smoke_tests():
    """Run all smoke tests"""
    print("🧪 Running smoke tests...")
    
    test = TestModel()
    
    try:
        test.test_model_creation()
        test.test_forward_pass()
        test.test_prediction()
        test.test_different_input_sizes()
        test.test_feature_extraction()
        
        print("🎉 All smoke tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = run_smoke_tests()
    sys.exit(0 if success else 1)
