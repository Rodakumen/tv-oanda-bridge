# tests/test_rules.py
import pytest
from risk.rules import is_symbol_allowed, is_size_allowed, is_trading_enabled, check_rules

@pytest.mark.parametrize("kwargs, expected", [
    ({"enabled": False, "action": "close"}, None),                 # close passes with kill switch on
    ({"symbol": "USD_JPY"}, "symbol_not_allowed"),
    ({"symbol": "USD_JPY", "action": "close"}, "symbol_not_allowed"),
    ({"allowed": set()}, "symbol_not_allowed"),                    # empty allowlist
    ({"size": 1001}, "size_exceeds_max"),
    ({"size": 1001, "action": "close"}, None),                     # size ignored for close
    ({"size": 1000}, None),                                        # boundary
    ({"enabled": False, "symbol": "USD_JPY"}, "kill_switch"),      # pins the order of checks
    ({"action": "sell", "size": 1001}, "size_exceeds_max"),
    ({"action": "sell", "enabled": False}, "kill_switch"),
])
def test_check_rules(kwargs, expected):
    assert run(**kwargs) == expected

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

def run(action="buy", symbol="EUR_USD", size=500, allowed=None, max_size=1000, enabled=True):
    allowed = {"EUR_USD"} if allowed is None else allowed
    return check_rules(action, symbol, size, allowed, max_size, enabled)

def test_normal_buy_passes():
    assert run() is None

def test_kill_switch_rejects_buy():
    assert run(enabled=False) == "kill_switch"