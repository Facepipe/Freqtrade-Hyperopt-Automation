#!/usr/bin/env python3
"""
Hyperopt Automation System v1.7.0
Changes:
- New output folder structure: output/<yyMMddhhmm>/<timeframe>/<hyperopt_loss>/<strategy>
- Summary CSV builds incrementally as each run completes
- Single session timestamp for all strategies
- Maintained all previous functionality and path handling
"""

import sys
from pathlib import Path
from datetime import datetime
from utils.config_loader import load_configurations
from utils.executor import (
    run_hyperopt_series, 
    create_summary_csv,
    verify_freqtrade_installation
)
from utils.logger import setup_logging
import logging

def main():
    BASE_DIR = Path("/home/facepipe/freqtrade/hyperopt-automation")
    CONFIG_CSV = BASE_DIR / "configs" / "hyperopt_configs.csv"
    OUTPUT_DIR = BASE_DIR / "outputs"
    OUTPUT_DIR.mkdir(exist_ok=True)

    # Create single session timestamp for all strategies
    session_timestamp = datetime.now().strftime('%y%m%d%H%M')
    
    # Create session-specific log file
    session_log_file = OUTPUT_DIR / session_timestamp / "hyperopt_automation.log"
    session_log_file.parent.mkdir(parents=True, exist_ok=True)
    
    logger = setup_logging(session_log_file)
    logger.info(f"Hyperopt Automation v1.7.0 starting from: {BASE_DIR}")
    logger.info(f"Session timestamp: {session_timestamp}")
    logger.info(f"Output structure: outputs/{session_timestamp}/<timeframe>/<hyperopt_loss>/<strategy>/")

    all_results = []
    try:
        freqtrade_path = verify_freqtrade_installation(logger)
        logger.info(f"Using Freqtrade at: {freqtrade_path}")
        
        if not CONFIG_CSV.exists():
            raise FileNotFoundError(f"Config CSV missing at: {CONFIG_CSV}")
            
        configs = load_configurations(CONFIG_CSV)
        logger.info(f"Loaded {len(configs)} configurations")

        for i, config in enumerate(configs, 1):
            logger.info(f"Processing strategy {i}/{len(configs)}: {config.name}")
            
            config_path = Path(config.config_file)
            if not config_path.exists():
                logger.error(f"Config file missing: {config.config_file}")
                continue
                
            results = run_hyperopt_series(
                config=config, 
                output_dir=OUTPUT_DIR, 
                logger=logger,
                session_timestamp=session_timestamp
            )
            all_results.append(results)
            logger.info(f"Completed {len(results)} runs for {config.name}")

        # Summary CSV is now built incrementally during execution
        summary_csv_path = OUTPUT_DIR / session_timestamp / "hyperopt_summary.csv"
        if summary_csv_path.exists():
            logger.info(f"Session summary CSV available at: {summary_csv_path}")
        else:
            logger.warning("No summary CSV was created (no successful runs)")

    except Exception as e:
        logger.critical(f"Fatal error: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()