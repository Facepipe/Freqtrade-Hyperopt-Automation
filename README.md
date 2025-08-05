# 🚀 Freqtrade Hyperopt Automation System

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Freqtrade 2025.6+](https://img.shields.io/badge/freqtrade-2025.6+-green.svg)](https://www.freqtrade.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Automate your Freqtrade hyperopt runs across multiple strategies, timeframes, and configurations with comprehensive result tracking and analysis.**

## 🌟 Key Features

- **🔄 Batch Processing**: Run hyperopt on multiple strategies automatically
- **📊 Multiple Configurations**: Support for different timeframes, hyperopt losses, and epochs
- **🎨 Colored Output**: Preserves Freqtrade's colored console output for better readability
- **📁 Organized Results**: Structured output with timestamped folders and comprehensive summaries
- **🛡️ Error Recovery**: Continues execution even if individual runs fail
- **🔍 Path Resolution**: Intelligent freqtrade binary detection with multiple fallback paths
- **📈 Real-time Monitoring**: Live progress streaming with detailed logging
- **🔧 Flexible Configuration**: Easy CSV-based configuration management

## 🏗️ Project Structure

```
freqtrade-hyperopt-automation/
├── 📁 configs/                  # Configuration files
│   └── hyperopt_configs.csv     # Main hyperopt configuration
├── 📁 output/                   # Generated results
│   └── YYMMDD_HHMM/            # Timestamped session folders
│       ├── hyperopt_summary.csv # Comprehensive results summary
│       └── [timeframe]/         # Results organized by timeframe
├── 📁 logs/                     # Execution logs
│   ├── hyperopt/               # Hyperopt execution logs
│   ├── errors/                 # Error logs
│   └── debug/                  # Debug information
├── 📁 scripts/                  # Utility scripts
│   ├── setup_environment.sh    # Environment setup
│   ├── backup_results.sh       # Results backup
│   └── analyze_performance.py  # Performance analysis
├── 📁 examples/                 # Example configurations
├── 📄 run_hyperopt.py          # Main execution script
├── 📄 executor.py              # Core hyperopt executor
└── 📄 README.md               # This file
```

## 🚀 Quick Start

### 1. Prerequisites

- **Python 3.8+** with pip
- **Freqtrade 2025.6+** installed and configured
- Git for cloning the repository

### 2. Installation

```bash
# Clone the repository
git clone https://github.com/Facepipe/Freqtrade-Hyperopt-Automation.git
cd Freqtrade-Hyperopt-Automation

# Run the setup script
./scripts/setup_environment.sh

# Make scripts executable (if needed)
chmod +x scripts/*.sh *.py
```

### 3. Configuration

#### Configure Freqtrade Paths

Edit `executor.py` and update the `FREQTRADE_PATHS` list with your freqtrade installation path:

```python
FREQTRADE_PATHS = [
    "/home/yourusername/freqtrade/.venv/bin/freqtrade",  # Update this path
    "~/.local/bin/freqtrade",                            # User installation
    "/usr/local/bin/freqtrade",                          # System installation
    shutil.which("freqtrade")                            # PATH lookup
]
```

#### Configure Hyperopt Runs

Edit `configs/hyperopt_configs.csv`:

```csv
strategy,timeframe,hyperopt_loss,epochs,config_file,timerange
SampleStrategy,5m,SharpeHyperOptLoss,100,user_data/config.json,20240101-20240201
MyStrategy,1h,OnlyProfitHyperOptLoss,200,user_data/config_alt.json,20240101-20240301
```

**Configuration Parameters:**
- **strategy**: Strategy class name
- **timeframe**: Candlestick timeframe (1m, 5m, 1h, etc.)
- **hyperopt_loss**: Loss function (SharpeHyperOptLoss, OnlyProfitHyperOptLoss, etc.)
- **epochs**: Number of hyperopt iterations
- **config_file**: Path to freqtrade configuration file
- **timerange**: Date range for backtesting (YYYYMMDD-YYYYMMDD)

### 4. Running Hyperopt

```bash
# Run all configured hyperopt sessions
python3 run_hyperopt.py

# Or with explicit path
/usr/bin/python3 run_hyperopt.py
```

## 📊 Output Structure

Each hyperopt session creates a timestamped folder with organized results:

```
output/
└── 250105_1430/                    # Session timestamp (YYMMDD_HHMM)
    ├── hyperopt_summary.csv         # Consolidated results
    ├── 5m/                         # Timeframe-specific results
    │   └── SharpeHyperOptLoss/     # Loss function results
    │       └── SampleStrategy/      # Strategy-specific outputs
    │           ├── config_run1.json
    │           ├── results_best_run1.txt
    │           └── results_profitable_run1.txt
    └── 1h/
        └── OnlyProfitHyperOptLoss/
            └── MyStrategy/
                ├── config_run2.json
                ├── results_best_run2.txt
                └── results_profitable_run2.txt
```

### Summary CSV Format

The `hyperopt_summary.csv` contains key metrics for all runs:

| Column | Description |
|--------|-------------|
| `session_id` | Unique session identifier |
| `run_number` | Sequential run number |
| `strategy` | Strategy name |
| `timeframe` | Used timeframe |
| `hyperopt_loss` | Loss function |
| `epochs` | Number of epochs |
| `total_profit` | Total profit percentage |
| `win_ratio` | Win ratio percentage |
| `avg_profit` | Average profit per trade |
| `total_trades` | Total number of trades |
| `start_time` | Run start timestamp |
| `end_time` | Run completion timestamp |
| `duration` | Execution duration |
| `status` | Success/failure status |

## 🔧 Advanced Usage

### Custom Loss Functions

The system supports all built-in Freqtrade loss functions:

- `SharpeHyperOptLoss` - Optimizes Sharpe ratio
- `OnlyProfitHyperOptLoss` - Focuses only on profit
- `SortinoHyperOptLoss` - Optimizes Sortino ratio
- `CalmarHyperOptLoss` - Optimizes Calmar ratio
- `MaxDrawDownHyperOptLoss` - Minimizes maximum drawdown

### Backup and Analysis

```bash
# Create backup of results
./scripts/backup_results.sh

# Analyze performance
python3 scripts/analyze_performance.py

# Quick performance overview
grep "Best result" output/*/logs/*.log
```

### Troubleshooting

#### Common Issues

**1. Freqtrade Not Found**
```bash
# Check if freqtrade is in PATH
which freqtrade

# Verify version
freqtrade --version

# Update path in executor.py
```

**2. Configuration File Not Found**
```bash
# Check file exists
ls -la configs/hyperopt_configs.csv

# Verify config file paths in CSV
cat configs/hyperopt_configs.csv
```

**3. Permission Errors**
```bash
# Make scripts executable
chmod +x scripts/*.sh *.py

# Check directory permissions
ls -la
```

## 📈 Performance Tips

### Optimization Strategies

1. **Start Small**: Begin with fewer epochs (50-100) to test configurations
2. **Progressive Refinement**: Use successful parameters as starting points
3. **Multiple Runs**: Run the same configuration multiple times with different random states
4. **Resource Management**: Monitor CPU and memory usage during long runs

### Best Practices

- **Data Quality**: Ensure you have sufficient historical data
- **Timerange Selection**: Use meaningful date ranges for backtesting
- **Strategy Validation**: Validate strategies in dry-run before live trading
- **Regular Backups**: Backup successful configurations and results

## 🔄 Version History

### v1.7.0 (Current - Output Improvements Branch)
- ✨ **New**: Organized output folder structure by session/timeframe/loss/strategy
- ✨ **New**: Incremental summary CSV building
- ✨ **New**: Single session timestamps for better organization
- 🐛 **Fixed**: Maintained all previous functionality and path handling

### v1.6.6
- 🐛 **Fixed**: ExecutionResult reference error
- ✨ **New**: Single comprehensive summary CSV
- ✨ **New**: Per-run text files for each strategy
- ✅ **Maintained**: Colored console output, timerange formatting, path resolution

### v1.6.5
- 🐛 **Fixed**: Base directory reference error
- ✨ **New**: Single summary CSV after all strategies complete
- ✨ **Improved**: Directory structure organization

### Earlier Versions
- Path resolution improvements
- Error handling enhancements
- Console output formatting
- Real-time progress streaming

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

### Development Setup

```bash
# Clone and setup development environment
git clone https://github.com/Facepipe/Freqtrade-Hyperopt-Automation.git
cd Freqtrade-Hyperopt-Automation

# Create feature branch
git checkout -b feature/your-feature-name

# Make changes and test
python3 run_hyperopt.py

# Commit and push
git commit -m "Add your feature"
git push origin feature/your-feature-name
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Freqtrade](https://www.freqtrade.io/) - The excellent cryptocurrency trading bot
- The Freqtrade community for strategies and guidance
- Contributors and users of this automation system

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/Facepipe/Freqtrade-Hyperopt-Automation/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Facepipe/Freqtrade-Hyperopt-Automation/discussions)
- **Freqtrade Documentation**: [Official Docs](https://www.freqtrade.io/en/stable/)

---

**⚠️ Disclaimer**: This tool is for educational and research purposes. Cryptocurrency trading involves substantial risk. Always test strategies thoroughly in dry-run mode before using real funds.

**🎯 Made with ❤️ for the Freqtrade community**