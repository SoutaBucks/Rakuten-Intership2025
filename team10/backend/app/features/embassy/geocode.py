# backend/app/features/embassy/geocode.py
from __future__ import annotations
import requests

class GeocodeError(Exception):
    pass

def geocode(address: str) -> tuple[float, float]:
    """
    住所 -> (lat, lng)
    Nominatim(OpenStreetMap) を使用。レート制限: 1req/sec 目安
    """
    if not address or not address.strip():
        raise GeocodeError("address is empty")

    url = "https://nominatim.openstreetmap.org/search"
    headers = {"User-Agent": "safetravel-hackathon/1.0"}
    params = {"q": address, "format": "jsonv2", "limit": 1}

    try:
        r = requests.get(url, headers=headers, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        if not data:
            raise GeocodeError(f"No results for: {address}")
        lat = float(data[0]["lat"])
        lon = float(data[0]["lon"])
        return lat, lon
    except requests.RequestException as e:
        raise GeocodeError(f"HTTP error: {e}") from e
    except (KeyError, ValueError, IndexError) as e:
        raise GeocodeError(f"Parse error: {e}") from e