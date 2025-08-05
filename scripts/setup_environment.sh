#!/bin/bash
# Quick environment setup for Freqtrade Hyperopt Automation

echo "🚀 Setting up Freqtrade Hyperopt Automation environment..."

# Check if freqtrade is installed
if ! command -v freqtrade &> /dev/null; then
    echo "❌ freqtrade is not installed or not in PATH"
    echo "Please install freqtrade first: https://www.freqtrade.io/en/stable/installation/"
    exit 1
fi

# Check freqtrade version
FREQTRADE_VERSION=$(freqtrade --version 2>/dev/null | head -n1 | grep -o '[0-9]\+\.[0-9]\+\.[0-9]\+')
echo "📦 Found freqtrade version: $FREQTRADE_VERSION"

# Create necessary directories
mkdir -p {configs,output,logs}
mkdir -p logs/{hyperopt,errors,debug}
mkdir -p output/{results,summaries,reports}

echo "✅ Environment setup complete!"
echo "📋 Next steps:"
echo "   1. Edit configs/hyperopt_configs.csv with your strategies"
echo "   2. Update FREQTRADE_PATHS in executor.py"
echo "   3. Run: python3 run_hyperopt.py"
