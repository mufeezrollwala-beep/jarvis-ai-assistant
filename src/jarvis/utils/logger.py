import logging
import re
import json
from pathlib import Path
from typing import List, Any


def mask_sensitive_data(data: Any, patterns: List[str]) -> Any:
    if isinstance(data, dict):
        return {k: mask_sensitive_data(v, patterns) for k, v in data.items()}
    elif isinstance(data, list):
        return [mask_sensitive_data(item, patterns) for item in data]
    elif isinstance(data, str):
        masked = data
        for pattern in patterns:
            regex = re.compile(pattern, re.IGNORECASE)
            if regex.search(masked):
                masked = regex.sub("***MASKED***", masked)
        return masked
    return data


class SensitiveDataFilter(logging.Filter):
    def __init__(self, patterns: List[str]):
        super().__init__()
        self.patterns = patterns
    
    def filter(self, record: logging.LogRecord) -> bool:
        record.msg = mask_sensitive_data(record.msg, self.patterns)
        if record.args:
            record.args = tuple(mask_sensitive_data(list(record.args), self.patterns))
        return True


def setup_logger(
    name: str,
    log_file: str,
    level: str = "INFO",
    mask_sensitive: bool = True,
    sensitive_patterns: List[str] = None,
) -> logging.Logger:
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    if logger.handlers:
        logger.handlers.clear()
    
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(getattr(logging, level.upper()))
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, level.upper()))
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    if mask_sensitive and sensitive_patterns:
        sensitive_filter = SensitiveDataFilter(sensitive_patterns)
        file_handler.addFilter(sensitive_filter)
        console_handler.addFilter(sensitive_filter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger
