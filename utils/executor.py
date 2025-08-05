import subprocess
import time
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, List, Dict
from dataclasses import dataclass
import logging
import os
import shutil
import json
import csv

"""
Hyperopt Automation Executor v1.7.0
Changes:
- New output folder structure: output/<yyMMddhhmm>/<timeframe>/<hyperopt_loss>/<strategy>
- Summary CSV builds incrementally as each run completes
- Maintained all previous functionality and path handling
"""

# Constants
FREQTRADE_PATHS = [
    "/home/facepipe/freqtrade/.venv/bin/freqtrade",
    os.path.expanduser("~/.local/bin/freqtrade"),
    "/usr/local/bin/freqtrade",
    shutil.which("freqtrade")
]
HYPEROPT_TIMEOUT = 86400  # 24 hours
MIN_FREQTRADE_VERSION = "2025.6"

@dataclass
class ExecutionResult:
    config_name: str
    run_number: int
    output_file: Path
    metrics_dir: Path
    config_file: Path
    elapsed_time: float
    summary_data: Dict[str, str]

def verify_freqtrade_installation(logger: logging.Logger) -> str:
    for path in [p for p in FREQTRADE_PATHS if p]:
        path_obj = Path(path)
        if not path_obj.exists():
            continue
            
        try:
            result = subprocess.run(
                [path, "--version"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=10
            )
            version_line = next(
                line for line in result.stdout.split('\n')
                if line.startswith("Freqtrade Version:")
            )
            version = version_line.split()[-1]
            
            if version >= MIN_FREQTRADE_VERSION:
                return path
                
        except Exception as e:
            logger.debug(f"Path check failed for {path}: {str(e)}")
            continue

    raise FileNotFoundError(
        "Freqtrade not found. Tried:\n" +
        "\n".join(f"• {p}" for p in FREQTRADE_PATHS if p)
    )

def parse_hyperopt_results(output: str) -> Dict[str, str]:
    """Extract key metrics from hyperopt-show output"""
    metrics = {
        'epoch': '',
        'total_profit': '',
        'trade_count': '',
        'win_ratio': '',
        'profit_factor': '',
        'max_drawdown': ''
    }
    
    lines = output.split('\n')
    for line in lines:
        line = line.strip()
        
        # Look for epoch details line (contains trades, wins/draws/losses, profits)
        if 'trades.' in line and 'Wins/Draws/Losses' in line:
            parts = line.split()
            # Extract epoch number (first part before '/')
            if '*' in parts[0]:
                epoch_part = parts[0].replace('*', '').strip()
                if '/' in epoch_part:
                    metrics['epoch'] = epoch_part.split('/')[0]
            
            # Extract trade count
            for i, part in enumerate(parts):
                if part.endswith(':') and i + 1 < len(parts) and parts[i + 1] == 'trades.':
                    metrics['trade_count'] = part.rstrip(':')
                    break
            
            # Extract total profit percentage
            for i, part in enumerate(parts):
                if 'profit' in part.lower() and i + 1 < len(parts):
                    profit_part = parts[i + 1]
                    if profit_part.startswith('(') and profit_part.endswith('%).'):
                        metrics['total_profit'] = profit_part.replace('(', '').replace('%).', '')
                        break
            
            # Extract win ratio from wins/draws/losses
            wins_losses_idx = -1
            for i, part in enumerate(parts):
                if 'Wins/Draws/Losses' in part:
                    wins_losses_idx = i
                    break
            
            if wins_losses_idx > 0:
                # Look for the pattern like "39/0/37" before "Wins/Draws/Losses"
                for i in range(wins_losses_idx - 1, max(0, wins_losses_idx - 3), -1):
                    if '/' in parts[i] and parts[i].count('/') == 2:
                        wins, draws, losses = parts[i].split('/')
                        total_trades = int(wins) + int(draws) + int(losses)
                        if total_trades > 0:
                            win_ratio = (int(wins) / total_trades) * 100
                            metrics['win_ratio'] = f"{win_ratio:.1f}%"
                        break
        
        # Look for profit factor in SUMMARY METRICS section
        elif 'Profit factor' in line and '│' in line:
            parts = line.split('│')
            if len(parts) >= 3:
                metrics['profit_factor'] = parts[2].strip()
        
        # Look for max drawdown in SUMMARY METRICS section
        elif ('Max % of account underwater' in line or 'Absolute Drawdown (Account)' in line) and '│' in line:
            parts = line.split('│')
            if len(parts) >= 3:
                metrics['max_drawdown'] = parts[2].strip()
    
    return metrics

def generate_result_files(freqtrade_path: str, output_dir: Path, config: 'HyperoptConfig', run_num: int, logger: logging.Logger) -> Dict[str, str]:
    """Generate output files for a single run"""
    summary_data = {
        'strategy': config.strategy,
        'run_number': str(run_num),
        'config_name': config.name,
        'timeframe': config.timeframe,
        'hyperopt_loss': config.hyperopt_loss,
        'config_file': config.config_file,
        'pairs_file': config.pairs_file,
        'epoch': 'N/A',
        'total_profit': 'N/A',
        'trade_count': 'N/A',
        'win_ratio': 'N/A',
        'profit_factor': 'N/A',
        'max_drawdown': 'N/A'
    }
    
    try:
        # Save configuration
        config_file = output_dir / f"config_run{run_num}.json"
        with open(config_file, 'w') as f:
            json.dump({
                'name': config.name,
                'strategy': config.strategy,
                'hyperopt_loss': config.hyperopt_loss,
                'epochs': config.epochs,
                'timerange': f"{(datetime.now() - timedelta(days=config.days_back)).strftime('%Y%m%d')}-",
                'spaces': config.spaces,
                'run_number': run_num,
                'config_file': config.config_file,
                'pairs_file': config.pairs_file
            }, f, indent=4)

        # Generate hyperopt results
        result_types = [
            ('--best', 'best'),
            ('--profitable', 'profitable')
        ]
        
        for cmd_type, name in result_types:
            output_file = output_dir / f"results_{name}_run{run_num}.txt"
            cmd = [
                freqtrade_path,
                "hyperopt-show",
                cmd_type,
                "-c", config.config_file,
                "-c", config.pairs_file
            ]
            
            try:
                logger.info(f"Running command: {' '.join(cmd)}")
                result = subprocess.run(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=60
                )
                
                with open(output_file, 'w') as f:
                    f.write(result.stdout)
                
                if result.stderr:
                    logger.warning(f"Command stderr for {name}: {result.stderr}")
                
                if cmd_type == '--best' and result.stdout:
                    logger.info(f"Parsing hyperopt results for run {run_num}")
                    parsed_metrics = parse_hyperopt_results(result.stdout)
                    
                    # Update summary_data with parsed results, keeping defaults for missing values
                    for key, value in parsed_metrics.items():
                        if value and value.strip():  # Only update if we got a non-empty value
                            summary_data[key] = value
                    
                    logger.info(f"Parsed metrics for run {run_num}: {parsed_metrics}")
                    
            except subprocess.TimeoutExpired:
                logger.error(f"Timeout generating {name} results for run {run_num}")
            except Exception as e:
                logger.error(f"Failed to generate {name} results for run {run_num}: {str(e)}")
        
        logger.info(f"Final summary data for run {run_num}: {summary_data}")
        return summary_data
        
    except Exception as e:
        logger.error(f"Failed to generate result files: {str(e)}")
        return summary_data  # Return the initialized summary_data even on error

def create_output_directory_structure(base_output_dir: Path, config: 'HyperoptConfig', session_timestamp: str) -> Path:
    """Create the new output directory structure: output/<yyMMddhhmm>/<timeframe>/<hyperopt_loss>/<strategy>"""
    output_path = (base_output_dir / 
                   session_timestamp / 
                   config.timeframe / 
                   config.hyperopt_loss / 
                   config.strategy)
    output_path.mkdir(parents=True, exist_ok=True)
    return output_path

def append_to_summary_csv(result: ExecutionResult, base_output_dir: Path, session_timestamp: str):
    """Append a single result to the summary CSV as each run completes"""
    csv_file = base_output_dir / session_timestamp / "hyperopt_summary.csv"
    
    fieldnames = [
        'config_name',
        'strategy',
        'timeframe',
        'hyperopt_loss',
        'config_file',
        'pairs_file',
        'run_number',
        'epoch',
        'total_profit',
        'trade_count',
        'win_ratio',
        'profit_factor',
        'max_drawdown',
        'elapsed_time',
        'output_dir'
    ]
    
    # Create CSV file with header if it doesn't exist
    if not csv_file.exists():
        csv_file.parent.mkdir(parents=True, exist_ok=True)
        with open(csv_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
    
    # Always append results, even if summary_data is incomplete
    try:
        with open(csv_file, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            # Ensure all required fields are present
            row = {}
            for field in fieldnames:
                if field == 'elapsed_time':
                    row[field] = str(timedelta(seconds=result.elapsed_time))
                elif field == 'output_dir':
                    row[field] = str(result.metrics_dir)
                else:
                    # Get value from summary_data or use 'N/A' as default
                    row[field] = result.summary_data.get(field, 'N/A')
            
            writer.writerow(row)
            
    except Exception as e:
        # Log the error but don't fail the entire process
        import logging
        logger = logging.getLogger("hyperopt_automation")
        logger.error(f"Failed to write to CSV: {str(e)}")
        logger.error(f"Result data: {result.summary_data}")
        logger.error(f"CSV file: {csv_file}")

def create_summary_csv(all_results: List[List[ExecutionResult]], output_dir: Path):
    """Legacy function - now handled by append_to_summary_csv"""
    # This function is kept for compatibility but functionality moved to append_to_summary_csv
    pass

def run_hyperopt_series(config, output_dir, logger, session_timestamp: str = None, dry_run=False):
    """Run a series of hyperopt runs for a configuration"""
    try:
        freqtrade_path = verify_freqtrade_installation(logger)
        
        # Verify config file exists before proceeding
        config_path = Path(config.config_file)
        if not config_path.exists():
            logger.error(f"Config file not found: {config.config_file}")
            return []
            
    except FileNotFoundError as e:
        logger.error(str(e))
        return []

    # Use provided session timestamp or create new one
    if session_timestamp is None:
        session_timestamp = datetime.now().strftime('%y%m%d%H%M')
    
    # Create new directory structure
    strategy_dir = create_output_directory_structure(output_dir, config, session_timestamp)
    
    results = []
    for run_num in range(1, config.num_runs + 1):
        try:
            start_time = time.time()
            
            # Create run-specific directory
            run_dir = strategy_dir / f"run_{run_num}"
            run_dir.mkdir(exist_ok=True)
            
            result = run_single_hyperopt(
                config=config,
                run_num=run_num,
                output_dir=run_dir,
                logger=logger,
                freqtrade_path=freqtrade_path,
                dry_run=dry_run
            )
            result.elapsed_time = time.time() - start_time
            
            # Generate result files and get summary data
            result.summary_data = generate_result_files(
                freqtrade_path=freqtrade_path,
                output_dir=run_dir,
                config=config,
                run_num=run_num,
                logger=logger
            )
            
            results.append(result)
            
            # Append to summary CSV immediately after each run completes
            append_to_summary_csv(result, output_dir, session_timestamp)
            logger.info(f"Added run {run_num} results to summary CSV")
            
            # Sleep between runs if configured
            if run_num < config.num_runs and config.sleep_between_runs > 0:
                logger.info(f"Sleeping {config.sleep_between_runs} seconds between runs")
                time.sleep(config.sleep_between_runs)
            
        except Exception as e:
            logger.error(f"Run {run_num} failed: {str(e)}")
            continue
            
    return results

def run_single_hyperopt(config, run_num, output_dir, logger, freqtrade_path: str, dry_run=False):
    """Execute a single hyperopt run"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = output_dir / f"hy_{timestamp}_run{run_num}.json"
    
    cmd = [
        freqtrade_path,
        "hyperopt",
        "-s", config.strategy,
        "--hyperopt-loss", config.hyperopt_loss,
        "-e", str(config.epochs),
        "--max-open-trades", str(config.max_open_trades),
        "-c", config.config_file,
        "-c", config.pairs_file,
        "--spaces"
    ]
    cmd.extend(config.spaces)
    
    timerange = f"{(datetime.now() - timedelta(days=config.days_back)).strftime('%Y%m%d')}-"
    cmd.extend(["--timerange", timerange])
    
    if config.enable_protections:
        cmd.append("--enable-protections")

    logger.info(f"Starting run {run_num} with command:\n{' '.join(cmd)}")
    
    if dry_run:
        return ExecutionResult(
            config_name=config.name,
            run_number=run_num,
            output_file=output_file,
            metrics_dir=output_dir,
            config_file=Path(config.config_file),
            elapsed_time=0,
            summary_data={}
        )
    
    try:
        process = subprocess.Popen(
            cmd,
            stdout=sys.stdout,
            stderr=sys.stderr,
            cwd="/home/facepipe/freqtrade",
            bufsize=1,
            universal_newlines=True
        )
        
        process.wait(timeout=HYPEROPT_TIMEOUT)
        
        if process.returncode != 0:
            raise subprocess.CalledProcessError(process.returncode, cmd)
            
        return ExecutionResult(
            config_name=config.name,
            run_number=run_num,
            output_file=output_file,
            metrics_dir=output_dir,
            config_file=Path(config.config_file),
            elapsed_time=0,
            summary_data={}
        )
        
    except subprocess.TimeoutExpired:
        process.kill()
        logger.error(f"Run timed out after {HYPEROPT_TIMEOUT} seconds")
        raise
    except subprocess.CalledProcessError as e:
        logger.error(f"Hyperopt failed (code {e.returncode})")
        raise