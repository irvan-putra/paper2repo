#!/usr/bin/env python3
"""
Demo Paper2Repo: Convert PDF to code (with fallback to heuristics)
Usage: python pdf_to_code_fixed.py 1805.10616v4.pdf
"""

import sys
import json
import os
from pathlib import Path
import PyPDF2
from typing import Dict

class DemoPaper2Code:
    def __init__(self):
        self.use_aws = self._check_aws_credentials()
        if self.use_aws:
            import boto3
            self.bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
            self.model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
    
    def _check_aws_credentials(self):
        """Check if AWS credentials are properly configured"""
        try:
            import boto3
            session = boto3.Session()
            credentials = session.get_credentials()
            if credentials is None:
                return False
            # Try to get caller identity to verify credentials work
            sts = session.client('sts')
            sts.get_caller_identity()
            return True
        except Exception as e:
            print(f"AWS credentials check failed: {e}")
            return False
    
    def extract_pdf_text(self, pdf_path: str) -> str:
        """Extract text from PDF"""
        print(f"📄 Extracting text from {pdf_path}...")
        
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
        
        print(f"✅ Extracted {len(text)} characters")
        return text
    
    def analyze_paper(self, text: str) -> Dict:
        """Analyze paper structure"""
        print("🔍 Analyzing paper structure...")
        
        if self.use_aws:
            try:
                return self._analyze_with_bedrock(text)
            except Exception as e:
                print(f"⚠️  Bedrock failed ({e}), falling back to heuristics")
                return self._analyze_with_heuristics(text)
        else:
            return self._analyze_with_heuristics(text)
    
    def _analyze_with_heuristics(self, text: str) -> Dict:
        """Simple heuristic analysis for demo"""
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        # Extract title (usually in first few lines, longer than 10 chars)
        title = "Unknown Paper"
        for line in lines[:20]:
            if 10 < len(line) < 100 and not line.lower().startswith(('abstract', 'introduction')):
                title = line
                break
        
        # Look for abstract
        abstract = ""
        for i, line in enumerate(lines):
            if "abstract" in line.lower():
                # Get next few lines as abstract
                abstract_lines = []
                for j in range(i+1, min(i+10, len(lines))):
                    if len(lines[j]) > 20:
                        abstract_lines.append(lines[j])
                        if len(' '.join(abstract_lines)) > 200:
                            break
                abstract = ' '.join(abstract_lines)[:300] + "..."
                break
        
        # Detect method keywords
        text_lower = text.lower()
        method_keywords = {
            "transformer": "Transformer",
            "attention": "Attention Mechanism", 
            "bert": "BERT",
            "gpt": "GPT",
            "neural network": "Neural Network",
            "convolution": "Convolutional Neural Network",
            "lstm": "LSTM",
            "rnn": "Recurrent Neural Network",
            "gan": "Generative Adversarial Network",
            "vae": "Variational Autoencoder",
            "reinforcement learning": "Reinforcement Learning"
        }
        
        main_method = "Neural Network"
        for keyword, method_name in method_keywords.items():
            if keyword in text_lower:
                main_method = method_name
                break
        
        # Architecture detection
        architecture = "Standard neural architecture"
        if "transformer" in text_lower:
            architecture = "Transformer-based architecture with multi-head attention"
        elif "cnn" in text_lower or "convolution" in text_lower:
            architecture = "Convolutional neural network with pooling layers"
        elif "rnn" in text_lower or "lstm" in text_lower:
            architecture = "Recurrent neural network with memory cells"
        elif "gan" in text_lower:
            architecture = "Generator-discriminator adversarial architecture"
        
        # Look for key implementation details
        implementation_hints = []
        if "pytorch" in text_lower:
            implementation_hints.append("Use PyTorch framework")
        if "tensorflow" in text_lower:
            implementation_hints.append("Use TensorFlow framework")
        if "batch" in text_lower:
            implementation_hints.append("Implement batch processing")
        if "dropout" in text_lower:
            implementation_hints.append("Include dropout for regularization")
        
        return {
            "title": title,
            "abstract": abstract,
            "main_method": main_method,
            "architecture": architecture,
            "key_equations": "Standard neural network equations with backpropagation",
            "implementation_hints": "; ".join(implementation_hints) if implementation_hints else "Use modern deep learning framework"
        }
    
    def _analyze_with_bedrock(self, text: str) -> Dict:
        """Analyze with AWS Bedrock"""
        text_sample = text[:8000]
        
        prompt = f"""
        Analyze this ML research paper and extract key information for code generation.
        
        Paper text:
        {text_sample}
        
        Return a JSON object with:
        - title: Paper title
        - abstract: Brief abstract
        - main_method: Core algorithm/method described
        - architecture: Model architecture details
        - key_equations: Important mathematical formulations
        - implementation_hints: Specific implementation details mentioned
        
        Focus on extracting information needed to implement the core method.
        """
        
        response = self._call_bedrock(prompt, max_tokens=2000)
        return self._parse_json(response)
    
    def generate_repo_structure(self, analysis: Dict) -> Dict:
        """Generate repository structure plan"""
        print("📋 Planning repository structure...")
        
        if self.use_aws:
            try:
                return self._generate_structure_with_bedrock(analysis)
            except Exception as e:
                print(f"⚠️  Bedrock failed ({e}), using heuristic structure")
                return self._generate_structure_heuristic(analysis)
        else:
            return self._generate_structure_heuristic(analysis)
    
    def _generate_structure_heuristic(self, analysis: Dict) -> Dict:
        """Generate structure with heuristics"""
        method = analysis.get('main_method', '').lower()
        
        modules = ["model.py", "train.py", "utils.py"]
        dependencies = ["torch", "numpy", "matplotlib"]
        
        if "transformer" in method or "attention" in method:
            modules.append("attention.py")
            dependencies.extend(["transformers", "tokenizers"])
        elif "cnn" in method or "convolution" in method:
            modules.append("layers.py")
            dependencies.append("torchvision")
        elif "gan" in method:
            modules.extend(["generator.py", "discriminator.py"])
        elif "reinforcement" in method:
            modules.extend(["agent.py", "environment.py"])
            dependencies.append("gym")
        
        return {
            "modules": modules,
            "main_module": "model.py",
            "dependencies": dependencies,
            "structure": {
                "model.py": "Main model implementation",
                "train.py": "Training loop and optimization",
                "utils.py": "Utility functions and data processing"
            }
        }
    
    def _generate_structure_with_bedrock(self, analysis: Dict) -> Dict:
        """Generate structure with Bedrock"""
        prompt = f"""
        Based on this paper analysis, create a Python repository structure.
        
        Paper info:
        Title: {analysis.get('title', 'Unknown')}
        Method: {analysis.get('main_method', 'Unknown')}
        Architecture: {analysis.get('architecture', 'Unknown')}
        
        Return JSON with:
        - modules: List of Python files to create (e.g., ["model.py", "train.py", "utils.py"])
        - main_module: Primary implementation file
        - dependencies: Required Python packages
        - structure: Brief description of each module's purpose
        
        Keep it simple and focused on the core implementation.
        """
        
        response = self._call_bedrock(prompt, max_tokens=1500)
        return self._parse_json(response)
    
    def generate_code(self, analysis: Dict, structure: Dict) -> Dict:
        """Generate code for the main module"""
        print("💻 Generating code...")
        
        if self.use_aws:
            try:
                return self._generate_code_with_bedrock(analysis, structure)
            except Exception as e:
                print(f"⚠️  Bedrock failed ({e}), using template")
                return self._generate_code_template(analysis, structure)
        else:
            return self._generate_code_template(analysis, structure)
    
    def _generate_code_template(self, analysis: Dict, structure: Dict) -> Dict:
        """Generate basic code template"""
        title = analysis.get('title', 'Unknown')
        method = analysis.get('main_method', 'Neural Network')
        class_name = method.replace(' ', '').replace('-', '') + 'Model'
        
        code = f'''import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np

class {class_name}(nn.Module):
    """
    Implementation of {method} from paper: {title}
    
    Architecture: {analysis.get('architecture', 'Standard neural network')}
    
    Based on the paper's methodology and implementation hints:
    {analysis.get('implementation_hints', 'Standard implementation')}
    """
    
    def __init__(self, input_dim=784, hidden_dim=256, output_dim=10, dropout_rate=0.1):
        super().__init__()
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.output_dim = output_dim
        self.dropout_rate = dropout_rate
        
        # Define layers based on the paper's architecture
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, hidden_dim)
        self.fc3 = nn.Linear(hidden_dim, output_dim)
        self.dropout = nn.Dropout(dropout_rate)
        
        # Initialize weights
        self._init_weights()
        
    def _init_weights(self):
        """Initialize model weights"""
        for module in self.modules():
            if isinstance(module, nn.Linear):
                nn.init.xavier_uniform_(module.weight)
                nn.init.zeros_(module.bias)
    
    def forward(self, x):
        """
        Forward pass implementing the method from the paper
        
        Args:
            x: Input tensor of shape (batch_size, input_dim)
            
        Returns:
            Output tensor of shape (batch_size, output_dim)
        """
        # Flatten input if needed
        if len(x.shape) > 2:
            x = x.view(x.size(0), -1)
        
        # Apply layers with activation functions
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = F.relu(self.fc2(x))
        x = self.dropout(x)
        x = self.fc3(x)
        
        return x
    
    def predict(self, x):
        """Make predictions on input data"""
        self.eval()
        with torch.no_grad():
            outputs = self.forward(x)
            predictions = torch.argmax(outputs, dim=1)
        return predictions
    
    def get_features(self, x):
        """Extract features from the penultimate layer"""
        self.eval()
        with torch.no_grad():
            if len(x.shape) > 2:
                x = x.view(x.size(0), -1)
            x = F.relu(self.fc1(x))
            x = F.relu(self.fc2(x))
        return x

def create_model(config=None):
    """Factory function to create model instance"""
    if config is None:
        config = {{'input_dim': 784, 'hidden_dim': 256, 'output_dim': 10}}
    
    return {class_name}(**config)

def train_step(model, data_loader, optimizer, criterion, device='cpu'):
    """Single training step"""
    model.train()
    total_loss = 0
    correct = 0
    total = 0
    
    for batch_idx, (data, target) in enumerate(data_loader):
        data, target = data.to(device), target.to(device)
        
        optimizer.zero_grad()
        output = model(data)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()
        
        total_loss += loss.item()
        pred = output.argmax(dim=1, keepdim=True)
        correct += pred.eq(target.view_as(pred)).sum().item()
        total += target.size(0)
    
    accuracy = 100. * correct / total
    avg_loss = total_loss / len(data_loader)
    
    return avg_loss, accuracy

def evaluate(model, data_loader, criterion, device='cpu'):
    """Evaluate model on test data"""
    model.eval()
    test_loss = 0
    correct = 0
    total = 0
    
    with torch.no_grad():
        for data, target in data_loader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            test_loss += criterion(output, target).item()
            pred = output.argmax(dim=1, keepdim=True)
            correct += pred.eq(target.view_as(pred)).sum().item()
            total += target.size(0)
    
    test_loss /= len(data_loader)
    accuracy = 100. * correct / total
    
    return test_loss, accuracy
'''

        imports = """import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np"""

        usage_example = f"""    # Create model instance
    model = create_model()
    print(f"Model: {{model}}")
    
    # Example forward pass
    x = torch.randn(32, 784)  # Batch of 32 samples
    output = model(x)
    print(f"Output shape: {{output.shape}}")
    
    # Example prediction
    predictions = model.predict(x)
    print(f"Predictions: {{predictions}}")
    
    # Extract features
    features = model.get_features(x)
    print(f"Features shape: {{features.shape}}")"""

        return {
            "code": code,
            "imports": imports,
            "usage_example": usage_example
        }
    
    def _generate_code_with_bedrock(self, analysis: Dict, structure: Dict) -> Dict:
        """Generate code with Bedrock"""
        main_module = structure.get('main_module', 'model.py')
        
        prompt = f"""
        Generate Python code for {main_module} implementing the method from this paper.
        
        Paper details:
        - Title: {analysis.get('title', '')}
        - Method: {analysis.get('main_method', '')}
        - Architecture: {analysis.get('architecture', '')}
        - Key equations: {analysis.get('key_equations', '')}
        - Implementation hints: {analysis.get('implementation_hints', '')}
        
        Requirements:
        1. Create a complete, runnable Python class/function
        2. Include detailed docstrings explaining the method
        3. Add type hints where appropriate
        4. Include basic error handling
        5. Add comments referencing paper sections
        
        Return JSON with:
        - code: Complete Python code
        - imports: Required import statements
        - usage_example: Simple example of how to use the code
        """
        
        response = self._call_bedrock(prompt, max_tokens=4000)
        return self._parse_json(response)
    
    def generate_tests(self, code_info: Dict) -> str:
        """Generate basic tests"""
        print("🧪 Generating tests...")
        
        tests = '''import pytest
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
'''
        return tests
    
    def _call_bedrock(self, prompt: str, max_tokens: int = 2000) -> str:
        """Call AWS Bedrock with Claude"""
        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
            "temperature": 0.1,
            "messages": [{"role": "user", "content": prompt}]
        }
        
        try:
            response = self.bedrock.invoke_model(
                modelId=self.model_id,
                body=json.dumps(body),
                contentType="application/json"
            )
            
            response_body = json.loads(response['body'].read())
            return response_body['content'][0]['text']
            
        except Exception as e:
            print(f"❌ Bedrock error: {e}")
            raise e
    
    def _parse_json(self, text: str) -> Dict:
        """Parse JSON from response"""
        try:
            if "```json" in text:
                start = text.find("```json") + 7
                end = text.find("```", start)
                text = text[start:end].strip()
            
            return json.loads(text)
        except Exception as e:
            print(f"⚠️  JSON parsing failed: {e}")
            return {"raw_response": text}
    
    def save_output(self, analysis: Dict, structure: Dict, code: Dict, tests: str, output_dir: str):
        """Save all generated files"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Save analysis
        with open(output_path / "analysis.json", "w") as f:
            json.dump(analysis, f, indent=2)
        
        # Save structure plan
        with open(output_path / "structure.json", "w") as f:
            json.dump(structure, f, indent=2)
        
        # Save main code
        main_module = structure.get('main_module', 'model.py')
        code_content = f"""# Generated from paper: {analysis.get('title', 'Unknown')}
# Method: {analysis.get('main_method', 'Unknown')}

{code.get('code', '')}

# Usage example:
if __name__ == "__main__":
{code.get('usage_example', '    pass')}
"""
        
        with open(output_path / main_module, "w") as f:
            f.write(code_content)
        
        # Save tests
        with open(output_path / "test_model.py", "w") as f:
            f.write(tests)
        
        # Save requirements
        deps = structure.get('dependencies', ['torch', 'numpy'])
        with open(output_path / "requirements.txt", "w") as f:
            f.write('\n'.join(deps))
        
        # Save README
        readme = f"""# {analysis.get('title', 'Generated Code')}

## Overview
Generated implementation of the method described in the paper.

**Method**: {analysis.get('main_method', 'Unknown')}

**Architecture**: {analysis.get('architecture', 'Standard neural network')}

## Files
- `{main_module}`: Main implementation
- `test_model.py`: Unit tests and smoke tests
- `requirements.txt`: Python dependencies
- `analysis.json`: Paper analysis results
- `structure.json`: Repository structure plan

## Quick Start
```bash
# Install dependencies
pip install -r requirements.txt

# Run the model
python {main_module}

# Run tests
python test_model.py
```

## Paper Information
**Title**: {analysis.get('title', 'Unknown')}

**Abstract**: {analysis.get('abstract', 'No abstract extracted')}

**Implementation Hints**: {analysis.get('implementation_hints', 'Standard implementation')}

## Generated by Paper2Repo
This code was automatically generated from the research paper using {'AWS Bedrock' if self.use_aws else 'heuristic analysis'}.

**Note**: This is a proof-of-concept implementation. Review and modify the code as needed for your specific use case.
"""
        
        with open(output_path / "README.md", "w") as f:
            f.write(readme)
        
        print(f"✅ Output saved to {output_path}/")
        print(f"📁 Generated files:")
        for file in output_path.iterdir():
            print(f"   - {file.name}")
    
    def convert_paper(self, pdf_path: str, output_dir: str = None):
        """Main conversion pipeline"""
        if not output_dir:
            output_dir = f"generated_{Path(pdf_path).stem}"
        
        print(f"🚀 Converting {pdf_path} to code...")
        if self.use_aws:
            print("✅ Using AWS Bedrock for AI generation")
        else:
            print("📝 Using heuristic analysis (demo mode)")
        
        try:
            # Step 1: Extract text
            text = self.extract_pdf_text(pdf_path)
            
            # Step 2: Analyze paper
            analysis = self.analyze_paper(text)
            print(f"📊 Found method: {analysis.get('main_method', 'Unknown')}")
            
            # Step 3: Plan structure
            structure = self.generate_repo_structure(analysis)
            print(f"📁 Planning {len(structure.get('modules', []))} modules")
            
            # Step 4: Generate code
            code = self.generate_code(analysis, structure)
            
            # Step 5: Generate tests
            tests = self.generate_tests(code)
            
            # Step 6: Save everything
            self.save_output(analysis, structure, code, tests, output_dir)
            
            print(f"🎉 Conversion complete! Check {output_dir}/ for results")
            return output_dir
            
        except Exception as e:
            print(f"❌ Conversion failed: {e}")
            return None

def main():
    if len(sys.argv) != 2:
        print("Usage: python pdf_to_code_fixed.py <pdf_file>")
        print("Example: python pdf_to_code_fixed.py 1805.10616v4.pdf")
        sys.exit(1)
    
    pdf_file = sys.argv[1]
    
    if not os.path.exists(pdf_file):
        print(f"❌ File not found: {pdf_file}")
        sys.exit(1)
    
    converter = DemoPaper2Code()
    result = converter.convert_paper(pdf_file)
    
    if result:
        print(f"\n🎯 Next steps:")
        print(f"1. cd {result}")
        print(f"2. pip install -r requirements.txt")
        print(f"3. python model.py")
        print(f"4. python test_model.py")
    else:
        print("❌ Conversion failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
