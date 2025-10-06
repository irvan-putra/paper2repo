# backend/app/models/database.py
from sqlalchemy import Column, String, Text, Integer, Float, Boolean, DateTime, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

Base = declarative_base()

class Paper(Base):
    __tablename__ = "papers"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(500), nullable=False)
    arxiv_id = Column(String(50), nullable=True)
    doi = Column(String(100), nullable=True)
    pdf_path = Column(String(500), nullable=False)
    pdf_hash = Column(String(64), nullable=False)  # For deduplication
    
    # Extracted content
    abstract = Column(Text, nullable=True)
    sections = Column(JSON, nullable=True)  # Structured sections
    methods = Column(JSON, nullable=True)   # Extracted methods
    equations = Column(JSON, nullable=True) # Mathematical equations
    figures = Column(JSON, nullable=True)   # Figure captions
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    processing_runs = relationship("ProcessingRun", back_populates="paper")

class ProcessingRun(Base):
    __tablename__ = "processing_runs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    paper_id = Column(UUID(as_uuid=True), ForeignKey("papers.id"), nullable=False)
    
    # Status tracking
    status = Column(String(50), nullable=False, default="queued")
    # Status values: queued, parsing, planning, generating, verifying, complete, failed
    
    # Timing
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    processing_time = Column(Integer, nullable=True)  # seconds
    
    # Results
    success_rate = Column(Float, nullable=True)  # 0.0 to 1.0
    compile_success = Column(Boolean, nullable=True)
    test_pass_rate = Column(Float, nullable=True)
    
    # Generated structure
    repo_structure = Column(JSON, nullable=True)  # Planned modules
    error_log = Column(Text, nullable=True)
    
    # Cost tracking
    tokens_used = Column(Integer, nullable=True)
    cost_estimate = Column(Float, nullable=True)
    
    # Relationships
    paper = relationship("Paper", back_populates="processing_runs")
    modules = relationship("GeneratedModule", back_populates="run")
    interactions = relationship("UserInteraction", back_populates="run")

class GeneratedModule(Base):
    __tablename__ = "generated_modules"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    run_id = Column(UUID(as_uuid=True), ForeignKey("processing_runs.id"), nullable=False)
    
    # Module info
    module_name = Column(String(100), nullable=False)  # e.g., "model.py"
    module_type = Column(String(50), nullable=False)   # e.g., "model", "train", "data"
    
    # Generated content
    code = Column(Text, nullable=False)
    docstring = Column(Text, nullable=True)
    imports = Column(JSON, nullable=True)  # List of imports
    
    # Test results
    compile_success = Column(Boolean, nullable=True)
    test_results = Column(JSON, nullable=True)  # Test outcomes
    error_message = Column(Text, nullable=True)
    
    # Generation metadata
    generation_time = Column(Integer, nullable=True)  # seconds
    tokens_used = Column(Integer, nullable=True)
    model_used = Column(String(50), nullable=True)
    
    # Versioning (for regeneration)
    version = Column(Integer, default=1)
    parent_module_id = Column(UUID(as_uuid=True), ForeignKey("generated_modules.id"), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    run = relationship("ProcessingRun", back_populates="modules")
    provenance_links = relationship("ProvenanceLink", back_populates="module")
    parent_module = relationship("GeneratedModule", remote_side=[id])

class ProvenanceLink(Base):
    __tablename__ = "provenance_links"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    module_id = Column(UUID(as_uuid=True), ForeignKey("generated_modules.id"), nullable=False)
    
    # Paper source
    paper_section = Column(String(100), nullable=False)  # e.g., "Methods", "3.2"
    paper_text = Column(Text, nullable=False)  # Original text snippet
    paper_start_char = Column(Integer, nullable=True)  # Character position
    paper_end_char = Column(Integer, nullable=True)
    
    # Code target
    code_line_start = Column(Integer, nullable=False)
    code_line_end = Column(Integer, nullable=False)
    code_snippet = Column(Text, nullable=False)
    
    # Link metadata
    confidence = Column(Float, nullable=False, default=1.0)  # 0.0 to 1.0
    link_type = Column(String(50), nullable=False)  # "method", "equation", "parameter", etc.
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    module = relationship("GeneratedModule", back_populates="provenance_links")

class UserInteraction(Base):
    __tablename__ = "user_interactions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    run_id = Column(UUID(as_uuid=True), ForeignKey("processing_runs.id"), nullable=False)
    
    # Interaction details
    action = Column(String(100), nullable=False)
    # Actions: click_provenance, regenerate_module, fix_with_context, download_repo, etc.
    
    target = Column(String(100), nullable=True)  # Module name, line number, etc.
    context = Column(JSON, nullable=True)  # Additional context data
    
    # Timing
    timestamp = Column(DateTime, default=datetime.utcnow)
    session_id = Column(String(100), nullable=True)
    
    # Relationships
    run = relationship("ProcessingRun", back_populates="interactions")

class PaperEmbedding(Base):
    __tablename__ = "paper_embeddings"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    paper_id = Column(UUID(as_uuid=True), ForeignKey("papers.id"), nullable=False)
    
    # Chunk info
    section = Column(String(100), nullable=False)
    chunk_index = Column(Integer, nullable=False)
    text = Column(Text, nullable=False)
    
    # Embedding
    embedding = Column(JSON, nullable=False)  # Vector as JSON array
    embedding_model = Column(String(50), nullable=False)
    
    # Metadata
    token_count = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class SystemMetrics(Base):
    __tablename__ = "system_metrics"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Metric info
    metric_name = Column(String(100), nullable=False)
    metric_value = Column(Float, nullable=False)
    metric_type = Column(String(50), nullable=False)  # "counter", "gauge", "histogram"
    
    # Context
    run_id = Column(UUID(as_uuid=True), ForeignKey("processing_runs.id"), nullable=True)
    tags = Column(JSON, nullable=True)  # Additional tags
    
    # Timing
    timestamp = Column(DateTime, default=datetime.utcnow)

# Database initialization
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    """Create all tables"""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Database dependency for FastAPI"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Alembic migration script template
ALEMBIC_MIGRATION = '''"""Initial Paper2Repo schema

Revision ID: 001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create papers table
    op.create_table('papers',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('title', sa.String(length=500), nullable=False),
        sa.Column('arxiv_id', sa.String(length=50), nullable=True),
        sa.Column('doi', sa.String(length=100), nullable=True),
        sa.Column('pdf_path', sa.String(length=500), nullable=False),
        sa.Column('pdf_hash', sa.String(length=64), nullable=False),
        sa.Column('abstract', sa.Text(), nullable=True),
        sa.Column('sections', sa.JSON(), nullable=True),
        sa.Column('methods', sa.JSON(), nullable=True),
        sa.Column('equations', sa.JSON(), nullable=True),
        sa.Column('figures', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create processing_runs table
    op.create_table('processing_runs',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('paper_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('started_at', sa.DateTime(), nullable=True),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('processing_time', sa.Integer(), nullable=True),
        sa.Column('success_rate', sa.Float(), nullable=True),
        sa.Column('compile_success', sa.Boolean(), nullable=True),
        sa.Column('test_pass_rate', sa.Float(), nullable=True),
        sa.Column('repo_structure', sa.JSON(), nullable=True),
        sa.Column('error_log', sa.Text(), nullable=True),
        sa.Column('tokens_used', sa.Integer(), nullable=True),
        sa.Column('cost_estimate', sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(['paper_id'], ['papers.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create other tables...
    # (Additional table creation code would go here)
    
    # Create indexes
    op.create_index('idx_papers_arxiv_id', 'papers', ['arxiv_id'])
    op.create_index('idx_papers_pdf_hash', 'papers', ['pdf_hash'])
    op.create_index('idx_processing_runs_status', 'processing_runs', ['status'])
    op.create_index('idx_processing_runs_created', 'processing_runs', ['started_at'])

def downgrade():
    op.drop_table('processing_runs')
    op.drop_table('papers')
'''
