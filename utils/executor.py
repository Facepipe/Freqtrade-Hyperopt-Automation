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
Hyperopt Automation Executor v1.6.6
Changes:
- Fixed ExecutionResult reference error
- Single summary CSV after all strategies complete
- Per-run text files for each strategy
- Maintained all previous fixes
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
        if 'Best Result:' in line:
            metrics['epoch'] = line.split()[2].strip()
        elif 'Total profit' in line:
            metrics['total_profit'] = line.split(':')[1].strip()
        elif 'Trades' in line and 'Avg' not in line:
            metrics['trade_count'] = line.split(':')[1].strip()
        elif 'Win Ratio' in line:
            metrics['win_ratio'] = line.split(':')[1].strip()
        elif 'Profit factor' in line:
            metrics['profit_factor'] = line.split(':')[1].strip()
        elif 'Max Drawdown' in line:
            metrics['max_drawdown'] = line.split(':')[1].strip()
    
    return metrics

def generate_result_files(freqtrade_path: str, output_dir: Path, config: 'HyperoptConfig', run_num: int, logger: logging.Logger) -> Dict[str, str]:
    """Generate output files for a single run"""
    summary_data = {}
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
                'run_number': run_num
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
                "-c", config.config_file
            ]
            
            try:
                result = subprocess.run(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=60
                )
                
                with open(output_file, 'w') as f:
                    f.write(result.stdout)
                
                if cmd_type == '--best':
                    summary_data = parse_hyperopt_results(result.stdout)
                    summary_data.update({
                        'strategy': config.strategy,
                        'run_number': str(run_num),
                        'config_name': config.name
                    })
                    
            except Exception as e:
                logger.error(f"Failed to generate {name} results for run {run_num}: {str(e)}")
        
        return summary_data
        
    except Exception as e:
        logger.error(f"Failed to generate result files: {str(e)}")
        return {}

def create_summary_csv(all_results: List[List[ExecutionResult]], output_dir: Path):
    """Create single CSV summary of all runs"""
    if not any(all_results):
        return
        
    csv_file = output_dir / "hyperopt_summary.csv"
    fieldnames = [
        'config_name',
        'strategy',
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
    
    with open(csv_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for strategy_results in all_results:
            for result in strategy_results:
                if result.summary_data:  # Only include successful runs
                    row = result.summary_data.copy()
                    row.update({
                        'elapsed_time': str(timedelta(seconds=result.elapsed_time)),
                        'output_dir': str(result.metrics_dir)
                    })
                    writer.writerow(row)

def run_hyperopt_series(config, output_dir, logger, dry_run=False):
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

    config_dir = output_dir / config.name
    config_dir.mkdir(parents=True, exist_ok=True)
    
    results = []
    for run_num in range(1, config.num_runs + 1):
        try:
            start_time = time.time()
            
            # Create run-specific directory
            run_dir = config_dir / f"run_{run_num}"
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