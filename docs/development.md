# Development Guide

## Setup

### Prerequisites
- Python 3.11+
- Git
- AWS CLI (optional, for Bedrock integration)

### Local Development
```bash
# Clone repository
git clone https://github.com/your-username/paper2repo.git
cd paper2repo

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests
python -m pytest

# Test with sample paper
python pdf_to_code.py sample_paper.pdf
```

### AWS Integration (Optional)
```bash
# Configure AWS credentials
aws configure
# or export AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY

# Enable Bedrock models in AWS Console
# - Claude 3 Sonnet
# - Claude 3 Haiku

# Test AWS integration
python pdf_to_code.py sample_paper.pdf
```

## Code Structure

```
paper2repo/
├── pdf_to_code.py          # Main conversion script
├── requirements.txt        # Dependencies
├── docs/                   # Documentation
├── tests/                  # Test files
├── examples/               # Sample papers and outputs
└── future/                 # Planned components
    ├── backend/            # FastAPI backend
    ├── frontend/           # React frontend
    └── infrastructure/     # Docker, K8s configs
```

## Key Classes

### `DemoPaper2Code`
Main conversion class with methods:
- `extract_pdf_text()`: PDF text extraction
- `analyze_paper()`: Content analysis
- `generate_repo_structure()`: Module planning
- `generate_code()`: Code generation
- `generate_tests()`: Test creation
- `save_output()`: File export

## Testing

### Unit Tests
```bash
# Run all tests
python -m pytest

# Run specific test
python -m pytest tests/test_pdf_extraction.py

# Run with coverage
python -m pytest --cov=pdf_to_code
```

### Integration Tests
```bash
# Test with sample papers
python pdf_to_code.py examples/sample_paper.pdf

# Verify generated code works
cd generated_sample_paper/
python model.py
python test_model.py
```

## Contributing

### Code Style
- Use Black for formatting: `black pdf_to_code.py`
- Use flake8 for linting: `flake8 pdf_to_code.py`
- Add type hints where possible
- Write docstrings for all functions

### Pull Request Process
1. Fork the repository
2. Create feature branch: `git checkout -b feature/new-feature`
3. Make changes and add tests
4. Run tests: `python -m pytest`
5. Format code: `black .`
6. Commit: `git commit -m "Add new feature"`
7. Push: `git push origin feature/new-feature`
8. Create Pull Request

### Adding New Features

#### New AI Provider
1. Create new service class in `ai_services/`
2. Implement standard interface methods
3. Add configuration options
4. Update main converter to use new provider

#### New Output Format
1. Add format option to `save_output()`
2. Create format-specific templates
3. Update CLI arguments
4. Add tests for new format

## Debugging

### Common Issues
1. **PDF parsing fails**: Try different PDF library (pdfplumber, pymupdf)
2. **AWS credentials**: Check `aws sts get-caller-identity`
3. **Generated code errors**: Review paper analysis quality
4. **Import errors**: Verify all dependencies installed

### Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Profiling
```bash
# Profile performance
python -m cProfile -o profile.stats pdf_to_code.py paper.pdf
python -c "import pstats; pstats.Stats('profile.stats').sort_stats('cumulative').print_stats(10)"
```

## Roadmap

### Phase 1: Core MVP ✅
- [x] PDF text extraction
- [x] Basic code generation
- [x] Test suite creation
- [x] Repository export

### Phase 2: AI Integration 🚧
- [ ] AWS Bedrock integration
- [ ] Improved paper analysis
- [ ] Better code quality
- [ ] Provenance tracking

### Phase 3: Web Interface 📋
- [ ] React frontend
- [ ] Three-pane layout
- [ ] Real-time processing
- [ ] Interactive debugging

### Phase 4: Production 📋
- [ ] Sandboxed execution
- [ ] Multi-user support
- [ ] API endpoints
- [ ] Cloud deployment
