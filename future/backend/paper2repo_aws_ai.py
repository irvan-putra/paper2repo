# backend/app/services/ai/aws_ai_service.py
import boto3
import json
from typing import Dict, List, Optional
from app.core.config import settings

class AWSAIService:
    """AI service using Amazon Bedrock and Q Developer"""
    
    def __init__(self):
        self.bedrock = boto3.client(
            'bedrock-runtime',
            region_name=settings.AWS_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )
        
        # Model configurations
        self.code_model = "anthropic.claude-3-sonnet-20240229-v1:0"  # For code generation
        self.planning_model = "anthropic.claude-3-haiku-20240307-v1:0"  # For planning/parsing
        
    async def generate_repo_plan(self, paper_content: str) -> Dict:
        """Generate repository structure plan from paper content"""
        
        prompt = f"""
        Analyze this ML paper and propose a Python repository structure.
        
        Paper content:
        {paper_content[:4000]}  # Truncate for context limits
        
        Return a JSON structure with:
        - modules: List of Python files to create (model.py, train.py, etc.)
        - dependencies: Required packages
        - structure: Directory layout
        
        Focus on the core implementation described in the Methods section.
        """
        
        response = await self._invoke_bedrock(
            model_id=self.planning_model,
            prompt=prompt,
            max_tokens=2000
        )
        
        return self._parse_json_response(response)
    
    async def generate_module_code(self, 
                                 module_name: str, 
                                 paper_sections: List[str],
                                 context: str) -> Dict:
        """Generate code for a specific module with provenance tracking"""
        
        prompt = f"""
        Generate Python code for {module_name} based on this ML paper content.
        
        Relevant paper sections:
        {chr(10).join(paper_sections)}
        
        Context: {context}
        
        Requirements:
        1. Generate complete, runnable Python code
        2. Include detailed docstrings citing paper sections
        3. Add type hints and error handling
        4. Include basic smoke tests
        5. Mark each function/class with source paper section
        
        Return JSON with:
        - code: Complete Python code
        - imports: List of required imports
        - tests: Basic test code
        - provenance: Map of code lines to paper sections
        """
        
        response = await self._invoke_bedrock(
            model_id=self.code_model,
            prompt=prompt,
            max_tokens=4000
        )
        
        return self._parse_json_response(response)
    
    async def analyze_error_and_fix(self, 
                                  error_message: str,
                                  code: str,
                                  paper_context: str) -> Dict:
        """Analyze error and suggest fixes with paper context"""
        
        prompt = f"""
        Fix this Python code error using context from the original paper.
        
        Error: {error_message}
        
        Current code:
        {code}
        
        Paper context:
        {paper_context}
        
        Return JSON with:
        - fixed_code: Corrected Python code
        - explanation: What was wrong and how it was fixed
        - confidence: Confidence level (0-1)
        """
        
        response = await self._invoke_bedrock(
            model_id=self.code_model,
            prompt=prompt,
            max_tokens=3000
        )
        
        return self._parse_json_response(response)
    
    async def extract_paper_structure(self, pdf_text: str) -> Dict:
        """Extract structured information from paper text"""
        
        prompt = f"""
        Extract structured information from this ML research paper.
        
        Paper text:
        {pdf_text[:6000]}  # Truncate for context
        
        Return JSON with:
        - title: Paper title
        - abstract: Abstract text
        - sections: List of main sections with content
        - methods: Extracted methodology descriptions
        - equations: Mathematical equations found
        - figures: Figure captions
        - pseudocode: Any algorithmic pseudocode
        """
        
        response = await self._invoke_bedrock(
            model_id=self.planning_model,
            prompt=prompt,
            max_tokens=3000
        )
        
        return self._parse_json_response(response)
    
    async def _invoke_bedrock(self, 
                            model_id: str, 
                            prompt: str, 
                            max_tokens: int = 2000) -> str:
        """Invoke Bedrock model with proper formatting"""
        
        # Format for Claude models
        if "claude" in model_id:
            body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": max_tokens,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }
        else:
            # Format for other models (Titan, etc.)
            body = {
                "inputText": prompt,
                "textGenerationConfig": {
                    "maxTokenCount": max_tokens,
                    "temperature": 0.1,
                    "topP": 0.9
                }
            }
        
        try:
            response = self.bedrock.invoke_model(
                modelId=model_id,
                body=json.dumps(body),
                contentType="application/json"
            )
            
            response_body = json.loads(response['body'].read())
            
            # Extract text based on model type
            if "claude" in model_id:
                return response_body['content'][0]['text']
            else:
                return response_body['results'][0]['outputText']
                
        except Exception as e:
            print(f"Bedrock invocation error: {e}")
            raise
    
    def _parse_json_response(self, response_text: str) -> Dict:
        """Parse JSON from model response, handling markdown formatting"""
        try:
            # Remove markdown code blocks if present
            if "```json" in response_text:
                start = response_text.find("```json") + 7
                end = response_text.find("```", start)
                response_text = response_text[start:end].strip()
            elif "```" in response_text:
                start = response_text.find("```") + 3
                end = response_text.find("```", start)
                response_text = response_text[start:end].strip()
            
            return json.loads(response_text)
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            print(f"Response text: {response_text}")
            # Return a basic structure if parsing fails
            return {"error": "Failed to parse response", "raw_response": response_text}

# Amazon Q Developer Integration (for code assistance)
class QDeveloperService:
    """Integration with Amazon Q Developer for code assistance"""
    
    def __init__(self):
        # Q Developer typically integrates through IDE extensions
        # For API access, you'd use the Q Business API
        self.q_client = boto3.client(
            'qbusiness',
            region_name=settings.AWS_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )
    
    async def get_code_suggestions(self, 
                                 code_context: str, 
                                 paper_context: str) -> List[str]:
        """Get code suggestions from Q Developer"""
        
        # This would integrate with Q Developer's API when available
        # For now, we can use Bedrock with Q-style prompting
        
        prompt = f"""
        As an expert ML engineer, provide code suggestions for implementing this paper.
        
        Current code context:
        {code_context}
        
        Paper context:
        {paper_context}
        
        Provide 3-5 specific, actionable code suggestions with explanations.
        """
        
        # Use Bedrock for now, but this could be Q Developer API
        aws_ai = AWSAIService()
        response = await aws_ai._invoke_bedrock(
            model_id=aws_ai.code_model,
            prompt=prompt,
            max_tokens=1500
        )
        
        return response.split('\n')

# Updated configuration
# backend/app/core/config.py (additions)
class Settings(BaseSettings):
    # ... existing settings ...
    
    # AWS AI Configuration
    AWS_REGION: str = "us-east-1"
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    
    # Bedrock Models
    BEDROCK_CODE_MODEL: str = "anthropic.claude-3-sonnet-20240229-v1:0"
    BEDROCK_PLANNING_MODEL: str = "anthropic.claude-3-haiku-20240307-v1:0"
    
    # Remove OpenAI/Anthropic keys if using only AWS
    # OPENAI_API_KEY: Optional[str] = None
    # ANTHROPIC_API_KEY: Optional[str] = None

# Updated requirements.txt additions
AWS_REQUIREMENTS = """
# AWS AI Services
boto3==1.34.0
botocore==1.34.0
"""

# Usage example in code generation service
# backend/app/services/generation/code_generator.py
from app.services.ai.aws_ai_service import AWSAIService, QDeveloperService

class CodeGenerationService:
    def __init__(self):
        self.ai_service = AWSAIService()
        self.q_service = QDeveloperService()
    
    async def generate_module(self, module_plan: Dict, paper_content: str) -> Dict:
        """Generate code module using AWS AI services"""
        
        # Use Bedrock for code generation
        result = await self.ai_service.generate_module_code(
            module_name=module_plan['name'],
            paper_sections=module_plan['relevant_sections'],
            context=paper_content
        )
        
        # Get additional suggestions from Q Developer
        suggestions = await self.q_service.get_code_suggestions(
            code_context=result.get('code', ''),
            paper_context=paper_content
        )
        
        result['suggestions'] = suggestions
        return result

# Docker Compose update for AWS credentials
DOCKER_COMPOSE_AWS = """
  # Backend API with AWS credentials
  api:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@postgres/paper2repo
      - REDIS_URL=redis://redis:6379
      - AWS_REGION=us-east-1
      - AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
      - AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
    depends_on:
      - postgres
      - redis
"""
