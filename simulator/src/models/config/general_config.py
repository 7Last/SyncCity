from typing import Dict


class GeneralConfig:
    def __init__(self, config: Dict[str, any]) -> None:
        self.max_workers = config.get('max_workers', 1)
        self.log_level = config.get('log_level', 'INFO')
