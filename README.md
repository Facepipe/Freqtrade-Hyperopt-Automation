# Hyperopt Automation System v1.3.1

## Path Resolution
The system now checks for freqtrade in this order:
1. Hardcoded venv path: `/home/facepipe/freqtrade/.venv/bin/freqtrade`
2. System PATH (if above not found)

## Changelog
### v1.3.1
- Fixed freqtrade path resolution
- Added fallback to system PATH
- Improved error messages for missing freqtrade
- Maintained all v1.3.0 features

### v1.3.0
- Added timeout protection
- Enhanced logging
- Dry-run capability
- Comprehensive reporting

# Hyperopt Automation System v1.4.2

## Changes in v1.4.2
- Fixed missing subprocess import
- Added comprehensive path verification
- Improved version checking
- Enhanced error messages

## Configuration Guide
1. Set your primary freqtrade path in `executor.py`:
   ```python
   FREQTRADE_PATHS = [
       "/home/facepipe/freqtrade/.venv/bin/freqtrade",  # ← Update this
       "~/.local/bin/freqtrade",
       "/usr/local/bin/freqtrade",
       shutil.which("freqtrade")
   ]
   
   # Hyperopt Automation System v1.4.3

## Key Features
- **Reliable Path Resolution**: Multiple fallback locations for freqtrade
- **Version Verification**: Ensures compatible freqtrade version
- **Comprehensive Logging**: Detailed execution logs
- **Error Recovery**: Continues after individual run failures
- **Dry Run Mode**: Test configurations without execution

## Installation
1. Set your freqtrade path in `executor.py`:
   ```python
   FREQTRADE_PATHS = [
       "/home/facepipe/freqtrade/.venv/bin/freqtrade",  # Primary path
       "~/.local/bin/freqtrade",                       # User install
       "/usr/local/bin/freqtrade",                     # System install
       shutil.which("freqtrade")                       # PATH lookup
   ]
   
# Hyperopt Automation System v1.4.4

## Key Features
- **Reliable Path Resolution**: Multiple fallback locations for freqtrade
- **Version Verification**: Ensures compatible freqtrade version (2025.6+)
- **Comprehensive Logging**: Detailed execution logs
- **Error Recovery**: Continues after individual run failures
- **Dry Run Mode**: Test configurations without execution

## Installation
1. Set your freqtrade path in `executor.py`:
   ```python
   FREQTRADE_PATHS = [
       "/home/facepipe/freqtrade/.venv/bin/freqtrade",  # Primary path
       "~/.local/bin/freqtrade",                       # User install
       "/usr/local/bin/freqtrade",                     # System install
       shutil.which("freqtrade")                       # PATH lookup
   ]
   
   
# Hyperopt Automation System v1.4.6

## Key Features
- **Fixed Working Directory Paths**: Ensures correct path resolution when run from `/home/facepipe/freqtrade/hyperopt-automation`
- **Reliable Path Resolution**: Multiple fallback locations for freqtrade
- **Version Verification**: Ensures compatible freqtrade version (2025.6+)
- **Comprehensive Logging**: Detailed execution logs
- **Error Recovery**: Continues after individual run failures
- **Dry Run Mode**: Test configurations without execution
- **Path Auto-resolution**: Handles relative paths in config files

## Changelog
### v1.4.6
- Fixed working directory path resolution issues
- Added absolute path handling for config files
- Improved error messages for path resolution
- Maintained all previous fixes and features

### v1.4.5
- Fixed import error for freqtrade path resolution
- Enhanced path verification for config files
- Maintained all previous fixes and features

### v1.4.4
- Added version requirement enforcement
- Improved error messages
- Maintained all v1.4.3 features

### v1.4.3
- Added multiple fallback paths for freqtrade
- Improved version checking
- Maintained all v1.4.2 features

### v1.4.2
- Fixed missing subprocess import
- Added comprehensive path verification
- Maintained all v1.4.1 features

### v1.4.1
- Added robust freqtrade path resolution
- Version compatibility checking
- Comprehensive error handling

### v1.3.1
- Fixed freqtrade path resolution
- Added fallback to system PATH
- Improved error messages for missing freqtrade

### v1.3.0
- Added timeout protection
- Enhanced logging
- Dry-run capability
- Comprehensive reporting

## Installation
1. Place the script in `/home/facepipe/freqtrade/hyperopt-automation`
2. Set your freqtrade path in `executor.py`:
   ```python
   FREQTRADE_PATHS = [
       "/home/facepipe/freqtrade/.venv/bin/freqtrade",  # Primary path
       "~/.local/bin/freqtrade",                       # User install
       "/usr/local/bin/freqtrade",                     # System install
       shutil.which("freqtrade")                       # PATH lookup
   ]
   
# Hyperopt Automation System v1.4.7

## Key Features
- **Fixed Import Error**: Corrected freqtrade verification import
- **Absolute Path Handling**: Ensures reliable execution from any directory
- **Version Verification**: Requires freqtrade 2025.6+
- **Comprehensive Logging**: Detailed execution history
- **Error Recovery**: Continues after individual failures
- **Path Resolution**: Multiple fallback locations for config files

## Changelog
### v1.4.7
- Fixed import error in run_hyperopt.py
- Enhanced absolute path handling
- Improved error messages for missing files
- Maintained all previous fixes

### v1.4.6
- Fixed working directory path issues
- Added explicit path resolution
- Maintained all v1.4.5 features

### v1.4.5
- Corrected freqtrade path verification
- Enhanced config file checking
- Maintained all v1.4.4 features

### v1.4.4
- Added version requirement enforcement
- Improved error messages
- Maintained all v1.4.3 features

### v1.4.3
- Multiple freqtrade path fallbacks
- Enhanced version checking
- Maintained all v1.4.2 features

### v1.4.2
- Fixed missing subprocess import
- Comprehensive path verification
- Maintained all v1.4.1 features

### v1.4.1
- Robust freqtrade resolution
- Version compatibility checks
- Maintained all v1.3.x features

## Installation
1. Clone to `/home/facepipe/freqtrade/hyperopt-automation`
2. Set freqtrade path in `executor.py`:
   ```python
   FREQTRADE_PATHS = [
       "/home/facepipe/freqtrade/.venv/bin/freqtrade",
       "~/.local/bin/freqtrade",
       "/usr/local/bin/freqtrade",
       shutil.which("freqtrade")
   ]
   

## Configuration
1. Place `hyperopt_configs.csv` in `configs/` directory
2. Config file paths can be:
- Absolute: `/home/facepipe/freqtrade/user_data/config.json`
- Relative to freqtrade: `user_data/config.json`
- Relative to script: `../freqtrade/user_data/config.json`

## Troubleshooting
- **Config CSV Not Found**:
- Ensure file exists at `hyperopt-automation/configs/hyperopt_configs.csv`
- **Config Files Not Found**:
- Check error message for resolved absolute path
- Verify file exists at that location
- **Version Errors**:
- Run `freqtrade --version` to check
- Update freqtrade if needed

# Hyperopt Automation System v1.4.8

## Key Features
- **Fixed Config Paths**: Correctly handles configs in `configs/` directory
- **Version Verification**: Requires freqtrade 2025.6+
- **Enhanced Diagnostics**: Detailed error messages for path issues
- **Error Recovery**: Continues after individual failures
- **Path Resolution**: Multiple fallback locations for all files

## Changelog
### v1.4.8
- Fixed config file path resolution
- Added specific error messages for missing CSV
- Maintained all previous fixes

### v1.4.7
- Fixed import error in run_hyperopt.py
- Enhanced absolute path handling
- Maintained all v1.4.6 features

### v1.4.6
- Fixed working directory path issues
- Added explicit path resolution
- Maintained all v1.4.5 features

## Installation
1. Clone to `/home/facepipe/freqtrade/hyperopt-automation`
2. Directory structure:

# Hyperopt Automation System v1.6.1

## Key Features
- **Fixed Timerange Format**: Now properly includes trailing dash in timerange parameter
- **Real-time Output**: Streams hyperopt progress to console
- **Working Directory Fix**: Runs from correct freqtrade directory
- **Path Resolution**: Multiple fallback locations for freqtrade
- **Version Verification**: Ensures compatible freqtrade version (2025.6+)

## Changelog
### v1.6.1
- Fixed timerange format to include required trailing dash
- Maintained real-time console output streaming
- Preserved all path resolution fixes
- Improved documentation

### v1.6.0
- Initial working version with command execution fix
- Added comprehensive path verification
- Enhanced error handling

## Configuration
1. Set your freqtrade paths in `executor.py`:
```python
FREQTRADE_PATHS = [
    "/home/facepipe/freqtrade/.venv/bin/freqtrade",
    "~/.local/bin/freqtrade",
    "/usr/local/bin/freqtrade",
    shutil.which("freqtrade")
]


# Hyperopt Automation System v1.6.2

## Key Features
- **Colored Console Output**: Preserves freqtrade's colored output
- **Fixed Timerange Format**: Proper --timerange format with trailing dash
- **Real-time Output**: Direct console streaming with colors
- **Working Directory Fix**: Correct execution context
- **Path Resolution**: Multiple fallback locations

## Changelog
### v1.6.2
- Preserved colored console output
- Fixed timerange format
- Improved output streaming
- Maintained all previous fixes

### v1.6.1
- Fixed timerange format
- Real-time output streaming
- Working directory fixes

## Configuration
```python
FREQTRADE_PATHS = [
    "/home/facepipe/freqtrade/.venv/bin/freqtrade",
    "~/.local/bin/freqtrade",
    "/usr/local/bin/freqtrade",
    shutil.which("freqtrade")
]

# Hyperopt Automation System v1.6.3

## New Features
- **Output Generation**:
  - `configuration.json`: Full run parameters
  - `results_best.txt`: Output of `hyperopt-show --best`
  - `results_profitable.txt`: Output of `hyperopt-list --profitable`

## File Structure

# Hyperopt Automation System v1.6.4

## New Features
- **Per-Run Output Files**:
  - `results_best_runX.txt`: Best results for each run
  - `results_profitable_runX.txt`: Profitable results for each run
  - `config_runX.json`: Configuration for each run

- **Summary CSV**:
  - Contains key metrics for all runs
  - Includes: strategy, run number, profit, win ratio, etc.
  - Saved as `hyperopt_summary.csv`

## File Structure


## Changelog
### v1.6.5
- Fixed base_dir reference error
- Single summary CSV after all strategies complete
- Improved directory structure
- Maintained all previous fixes

### v1.6.4
- Added per-run text files
- Enhanced error handling

# Hyperopt Automation System v1.6.5

## File Output Structure


## Changelog
### v1.6.6
- Fixed ExecutionResult reference error
- Single comprehensive summary CSV
- Per-run text files for each strategy
- Maintained all previous fixes:
  - Colored console output
  - Timerange formatting
  - Path resolution
  - Error handling

## Usage
```bash
python3 run_hyperopt.py

