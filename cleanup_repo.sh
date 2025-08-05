#!/bin/bash

# Freqtrade Hyperopt Automation - Repository Cleanup Script
# This script tidies up the repository structure and prepares for the new README

echo "🧹 Starting repository cleanup..."

# Create proper directory structure
echo "📁 Creating directory structure..."
mkdir -p {docs,examples,configs,output,logs,scripts}
mkdir -p docs/{images,tutorials}
mkdir -p examples/{strategies,configs}

# Move files to appropriate directories
echo "📦 Organizing files..."

# Move configuration files
if [ -f "hyperopt_configs.csv" ]; then
    mv hyperopt_configs.csv configs/
    echo "✅ Moved hyperopt_configs.csv to configs/"
fi

# Create example configuration if it doesn't exist
if [ ! -f "configs/hyperopt_configs.csv" ]; then
    cat > configs/hyperopt_configs.csv << 'EOF'
strategy,timeframe,hyperopt_loss,epochs,config_file,timerange
SampleStrategy,5m,SharpeHyperOptLoss,100,user_data/config.json,20240101-20240201
AnotherStrategy,1h,OnlyProfitHyperOptLoss,200,user_data/config_alt.json,20240101-20240301
EOF
    echo "✅ Created example hyperopt_configs.csv"
fi

# Create logs directory structure
mkdir -p logs/{hyperopt,errors,debug}

# Create output directory structure with clear naming
mkdir -p output/{results,summaries,reports}

# Clean up any temporary files
echo "🗑️  Cleaning temporary files..."
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null
find . -name "*.log" -path "./logs/*" -prune -o -name "*.log" -delete
find . -name ".DS_Store" -delete

# Create useful scripts directory
echo "📝 Creating utility scripts..."

# Create a quick setup script
cat > scripts/setup_environment.sh << 'EOF'
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
EOF

chmod +x scripts/setup_environment.sh

# Create a backup script
cat > scripts/backup_results.sh << 'EOF'
#!/bin/bash
# Backup hyperopt results with timestamp

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="backups/hyperopt_backup_$TIMESTAMP"

echo "💾 Creating backup: $BACKUP_DIR"
mkdir -p "$BACKUP_DIR"

# Backup output directory
if [ -d "output" ]; then
    cp -r output "$BACKUP_DIR/"
    echo "✅ Backed up output directory"
fi

# Backup logs
if [ -d "logs" ]; then
    cp -r logs "$BACKUP_DIR/"
    echo "✅ Backed up logs directory"
fi

# Backup configs
if [ -d "configs" ]; then
    cp -r configs "$BACKUP_DIR/"
    echo "✅ Backed up configs directory"
fi

echo "🎉 Backup completed: $BACKUP_DIR"
EOF

chmod +x scripts/backup_results.sh

# Create performance analysis script
cat > scripts/analyze_performance.py << 'EOF'
#!/usr/bin/env python3
"""
Quick performance analysis of hyperopt results
"""
import pandas as pd
import os
from pathlib import Path

def analyze_results():
    """Analyze hyperopt summary results"""
    summary_files = list(Path('output').glob('**/hyperopt_summary.csv'))
    
    if not summary_files:
        print("❌ No summary files found in output directory")
        return
    
    print(f"📊 Found {len(summary_files)} summary file(s)")
    
    for summary_file in summary_files:
        print(f"\n📈 Analyzing: {summary_file}")
        
        try:
            df = pd.read_csv(summary_file)
            
            if len(df) == 0:
                print("   ⚠️  Empty summary file")
                continue
                
            print(f"   📋 Total runs: {len(df)}")
            print(f"   🏆 Best strategy: {df.loc[df['total_profit'].idxmax(), 'strategy']}")
            print(f"   💰 Best profit: {df['total_profit'].max():.4f}")
            print(f"   📊 Average profit: {df['total_profit'].mean():.4f}")
            print(f"   🎯 Win rate range: {df['win_ratio'].min():.2%} - {df['win_ratio'].max():.2%}")
            
        except Exception as e:
            print(f"   ❌ Error reading file: {e}")

if __name__ == "__main__":
    analyze_results()
EOF

chmod +x scripts/analyze_performance.py

# Create gitignore if it doesn't exist
if [ ! -f ".gitignore" ]; then
    cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/*
!logs/.gitkeep

# Output files
output/*
!output/.gitkeep
backups/

# Temporary files
*.tmp
*.bak
*~

# Freqtrade specific
user_data/backtest_results/
user_data/hyperopt_results/
user_data/logs/
EOF
    echo "✅ Created .gitignore"
fi

# Create placeholder files to maintain directory structure
touch logs/.gitkeep
touch output/.gitkeep

# Set executable permissions
chmod +x *.py 2>/dev/null

echo ""
echo "🎉 Repository cleanup completed!"
echo ""
echo "📋 Summary of changes:"
echo "   ✅ Created organized directory structure"
echo "   ✅ Moved configuration files to configs/"
echo "   ✅ Created utility scripts in scripts/"
echo "   ✅ Added .gitignore for Python projects"
echo "   ✅ Cleaned temporary files"
echo ""
echo "🚀 Next steps:"
echo "   1. Review and update configs/hyperopt_configs.csv"
echo "   2. Update FREQTRADE_PATHS in executor.py"
echo "   3. Run: ./scripts/setup_environment.sh"
echo "   4. Test with: python3 run_hyperopt.py"
echo ""
echo "📚 Don't forget to commit these changes to git!"