import csv
from pathlib import Path
from dataclasses import dataclass
from typing import List

@dataclass
class HyperoptConfig:
    name: str
    strategy: str
    config_file: str
    hyperopt_loss: str
    epochs: int
    max_open_trades: int
    timeframe: str
    days_back: int
    space_buy: bool
    space_sell: bool
    space_roi: bool
    space_stoploss: bool
    space_trailing: bool
    enable_protections: bool
    num_runs: int
    sleep_between_runs: int

    def __post_init__(self):
        self.config_file = self._resolve_path()

    def _resolve_path(self) -> str:
        path = Path(self.config_file)
        if path.is_absolute():
            return str(path)
        return str(Path("/home/facepipe/freqtrade/user_data") / path.name)

    @property
    def spaces(self) -> List[str]:
        return [space for space, enabled in [
            ('buy', self.space_buy),
            ('sell', self.space_sell),
            ('roi', self.space_roi),
            ('stoploss', self.space_stoploss),
            ('trailing', self.space_trailing)
        ] if enabled]

def load_configurations(csv_path: Path) -> List[HyperoptConfig]:
    if not csv_path.exists():
        raise FileNotFoundError(f"Config CSV missing at: {csv_path}")
    
    configs = []
    with open(csv_path) as f:
        for row in csv.DictReader(f):
            try:
                configs.append(HyperoptConfig(
                    name=row['name'],
                    strategy=row['strategy'],
                    config_file=row['config_file'],
                    hyperopt_loss=row['hyperopt_loss'],
                    epochs=int(row['epochs']),
                    max_open_trades=int(row['max_open_trades']),
                    timeframe=row['timeframe'],
                    days_back=int(row['days_back']),
                    space_buy=row['space_buy'].lower() == 'true',
                    space_sell=row['space_sell'].lower() == 'true',
                    space_roi=row['space_roi'].lower() == 'true',
                    space_stoploss=row['space_stoploss'].lower() == 'true',
                    space_trailing=row['space_trailing'].lower() == 'true',
                    enable_protections=row['enable_protections'].lower() == 'true',
                    num_runs=int(row['num_runs']),
                    sleep_between_runs=int(row['sleep_between_runs'])
                ))
            except (KeyError, ValueError) as e:
                raise ValueError(f"Invalid CSV row: {e}")

    return configs