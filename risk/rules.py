# risk/rules.py

CLOSE = "close"

def is_symbol_allowed(symbol: str, allowed: set[str]) -> bool:
    return symbol in allowed

def is_size_allowed(size: int, max_size: int) -> bool:
    return size <= max_size

def is_trading_enabled(enabled: bool) -> bool:
    return enabled

def check_rules(
    action: str,
    symbol: str,
    size: int,
    allowed_symbols: set[str],
    max_size: int,
    trading_enabled: bool,
) -> str | None:
    """Return a reason code if the alert must be rejected, or None if it may go ahead."""

    if action != CLOSE and not is_trading_enabled(trading_enabled):
        return "kill_switch"

    if not is_symbol_allowed(symbol, allowed_symbols):
        return "symbol_not_allowed"

    if action != CLOSE and not is_size_allowed(size, max_size):
        return "size_exceeds_max"

    return None