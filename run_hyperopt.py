#!/usr/bin/env python3
"""
Hyperopt Automation System v1.6.7
Changes:
- Fixed missing verify_freqtrade_installation import
- Maintained all previous functionality
"""

import sys
from pathlib import Path
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

    logger = setup_logging(OUTPUT_DIR / "hyperopt_automation.log")
    logger.info(f"Hyperopt Automation v1.6.7 starting from: {BASE_DIR}")

    all_results = []
    try:
        freqtrade_path = verify_freqtrade_installation(logger)
        
        if not CONFIG_CSV.exists():
            raise FileNotFoundError(f"Config CSV missing at: {CONFIG_CSV}")
            
        configs = load_configurations(CONFIG_CSV)
        logger.info(f"Loaded {len(configs)} configurations")

        for config in configs:
            config_path = Path(config.config_file)
            if not config_path.exists():
                logger.error(f"Config file missing: {config.config_file}")
                continue
                
            results = run_hyperopt_series(config, OUTPUT_DIR, logger)
            all_results.append(results)
            logger.info(f"Completed {len(results)} runs for {config.name}")

        # Create single summary CSV after all strategies complete
        create_summary_csv(all_results, OUTPUT_DIR)
        logger.info("Generated summary CSV for all runs")

    except Exception as e:
        logger.critical(f"Fatal error: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()