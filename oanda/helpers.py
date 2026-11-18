# oanda/helpers.py (or inside oanda_client.py)
def side_to_close(position: dict) -> str | None:
    """Return "longUnits", "shortUnits", or None if nothing is open."""
    long_units = float(position["long"]["units"])
    short_units = float(position["short"]["units"])

    if long_units > 0 and short_units < 0:
        raise ValueError("Both sides open: hedging accounts are not supported")

    if long_units > 0:
        return "longUnits"
    if short_units < 0:
        return "shortUnits"

    return None
