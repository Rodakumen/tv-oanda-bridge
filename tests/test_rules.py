# tests/test_rules.py
from risk.rules import is_symbol_allowed, is_size_allowed, is_trading_enabled


def test_allowed_symbol_passes():
    assert is_symbol_allowed("EUR_USD", {"EUR_USD", "GBP_USD"}) is True


def test_unlisted_symbol_is_blocked():
    assert is_symbol_allowed("USD_JPY", {"EUR_USD"}) is False


def test_empty_allowlist_blocks_everything():
    assert is_symbol_allowed("EUR_USD", set()) is False


def test_size_below_max_is_allowed():
    assert is_size_allowed(500, 1000) is True


def test_size_exactly_at_max_is_allowed():
    assert is_size_allowed(1000, 1000) is True


def test_size_above_max_is_blocked():
    assert is_size_allowed(1001, 1000) is False


def test_trading_enabled():
    assert is_trading_enabled(True) is True


def test_kill_switch_blocks_trading():
    assert is_trading_enabled(False) is False