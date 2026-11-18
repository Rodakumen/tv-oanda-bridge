# oanda/oanda_client.py
import httpx

from oanda.helpers import side_to_close


PRACTICE_URL = "https://api-fxpractice.oanda.com"


class OandaClient:
    def __init__(self, token: str, account_id: str, base_url: str = PRACTICE_URL):
        self.account_id = account_id
        self.client = httpx.Client(
            base_url=base_url,
            headers={"Authorization": f"Bearer {token}"},
            timeout=10.0,
        )

    def place_order(self, symbol: str, units: int) -> dict:
        """Market order. Positive units = buy, negative = sell."""
        body = {
            "order": {
                "type": "MARKET",
                "instrument": symbol,
                "units": str(units),
                "timeInForce": "FOK",
                "positionFill": "DEFAULT",
            }
        }
        r = self.client.post(f"/v3/accounts/{self.account_id}/orders", json=body)
        r.raise_for_status()
        return r.json()

    def close_position(self, symbol: str) -> dict:
        response = self.get_position(symbol)
        side = side_to_close(response["position"])

        if side is None:
            return {"status": "no_position"}

        r = self.client.put(
            f"/v3/accounts/{self.account_id}/positions/{symbol}/close",
            json={side: "ALL"},
        )
        r.raise_for_status()
        return r.json()

    def get_position(self,symbol: str) -> dict:
        r = self.client.get(f"/v3/accounts/{self.account_id}/positions/{symbol}")
        r.raise_for_status()
        return r.json()