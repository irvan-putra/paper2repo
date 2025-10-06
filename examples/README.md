# Examples

This directory contains sample outputs and test cases for Paper2Repo.

## Sample Output

### `sample_output/`
Generated from paper "Dynamic Network Model from Partial Observations" (arXiv:1805.10616v4)

**Generated files:**
- `model.py`: Neural network implementation (4.7KB)
- `test_model.py`: Comprehensive test suite (2.8KB)
- `requirements.txt`: Dependencies
- `README.md`: Documentation
- `analysis.json`: Paper analysis results
- `structure.json`: Repository structure plan

**Test results:**
```
✅ Model creation test passed
✅ Forward pass test passed
✅ Prediction test passed
✅ Different input sizes test passed
✅ Feature extraction test passed
🎉 All smoke tests passed!
```

**Model output:**
```python
Model: NeuralNetworkModel(
  (fc1): Linear(in_features=784, out_features=256, bias=True)
  (fc2): Linear(in_features=256, out_features=256, bias=True)
  (fc3): Linear(in_features=256, out_features=10, bias=True)
  (dropout): Dropout(p=0.1, inplace=False)
)
```

## Usage

To test with the sample:
```bash
cd examples/sample_output
pip install -r requirements.txt
python model.py
python test_model.py
```

## Adding New Examples

1. Place PDF in this directory
2. Run: `python ../pdf_to_code.py your_paper.pdf`
3. Move generated folder to `examples/`
4. Update this README with results
