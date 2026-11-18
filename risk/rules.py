# risk/rules.py
def is_symbol_allowed(symbol: str, allowed: set[str]) -> bool:
    return symbol in allowed

def is_size_allowed(size: int, max_size: int) -> bool:
    return size <= max_size

def is_trading_enabled(enabled: bool) -> bool:
    return enabled