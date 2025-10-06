# Paper2Repo

Convert ML research papers into runnable, provenance-linked repositories in <10 minutes.

## 🚀 Quick Demo

### Web Interface (Recommended)
```bash
# Clone and setup
git clone https://github.com/irvan-putra/paper2repo.git
cd paper2repo

# Start web demo
./run_demo.sh

# Visit http://localhost:5000 in your browser
# Upload a PDF and see the magic happen!
```

### Command Line
```bash
# Convert a paper to code
python pdf_to_code.py your_paper.pdf

# Results in generated_your_paper/ folder
cd generated_your_paper/
python model.py  # Run the generated model
python test_model.py  # Run tests
```

## ✨ Features

- **PDF to Code**: Extract ML methods and generate runnable Python implementations
- **Provenance Tracking**: Link generated code back to paper sections
- **Automated Testing**: Generate smoke tests for validation
- **AWS Integration**: Use Amazon Bedrock for high-quality code generation
- **Complete Repos**: Export with README, tests, and documentation

## 🎯 Goals

- >60% of papers compile and pass tests in <10 minutes
- <30 lines of user corrections needed
- Clear provenance linking between code and paper
- Support for simple to moderate ML papers

## 📊 Current Status

✅ **Proof of Concept Complete**
- PDF text extraction working
- Basic code generation functional
- Test suite generation
- Complete repository export

🚧 **In Development**
- AWS Bedrock integration for better AI
- Web UI with three-pane layout
- Advanced provenance tracking
- Sandboxed code execution

## 🏗️ Architecture

```
PDF Upload → Parser → Planner → Generator → Verifier → Export
     ↓         ↓        ↓         ↓         ↓        ↓
  Storage   Analysis  Structure  Code    Tests   Repo
```

## 🛠️ Tech Stack

- **Backend**: Python, FastAPI, PostgreSQL
- **AI**: Amazon Bedrock (Claude), AWS Q Developer
- **Frontend**: React, TypeScript, Tailwind CSS
- **Infrastructure**: Docker, AWS services

## 📝 Example Output

From paper "Dynamic Network Model from Partial Observations":

```python
class NeuralNetworkModel(nn.Module):
    """
    Implementation of Neural Network from paper: Dynamic Network Model from Partial Observations
    
    Architecture: Recurrent neural network with memory cells
    """
    
    def __init__(self, input_dim=784, hidden_dim=256, output_dim=10):
        super().__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, hidden_dim)
        self.fc3 = nn.Linear(hidden_dim, output_dim)
        # ... rest of implementation
```

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- AWS credentials (for Bedrock integration)
- Git

### Installation
```bash
git clone https://github.com/your-username/paper2repo.git
cd paper2repo
pip install -r requirements.txt
```

### Basic Usage
```bash
# Convert a paper (demo mode)
python pdf_to_code.py paper.pdf

# With AWS Bedrock (better quality)
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
python pdf_to_code.py paper.pdf
```

## 📚 Documentation

- [Architecture Overview](docs/architecture.md)
- [API Documentation](docs/api.md)
- [Development Guide](docs/development.md)
- [Deployment Guide](docs/deployment.md)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by NotebookLM's multi-panel, source-grounded UX
- Built with Amazon Q Developer assistance
- Research baselines: Paper2Code, PaperCoder

## 📞 Contact

- **Issues**: [GitHub Issues](https://github.com/your-username/paper2repo/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-username/paper2repo/discussions)

---

**Transform ML research reproducibility. From paper to runnable repo in 10 minutes.** 🎯
