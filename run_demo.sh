#!/bin/bash
# Paper2Repo Web Demo Startup Script

echo "🚀 Starting Paper2Repo Web Demo..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
mkdir -p uploads outputs

# Start the web server
echo "🌐 Starting web server..."
echo "📝 Visit http://localhost:5000 in your browser"
echo "🛑 Press Ctrl+C to stop the server"
echo ""

python app.py
