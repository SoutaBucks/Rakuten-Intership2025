# backend/app/common/country_codes.py
from typing import Optional

# 基本の ISO2 マップ（主要国 + よく使う地域）
_CANONICAL_TO_ISO2 = {
    "japan": "JP",
    "united states": "US",
    "usa": "US",
    "u.s.": "US",
    "u.s.a.": "US",
    "america": "US",  # 便宜上 US に寄せる
    "united kingdom": "GB",
    "uk": "GB",
    "u.k.": "GB",
    "great britain": "GB",
    "england": "GB",
    "france": "FR",
    "germany": "DE",
    "italy": "IT",
    "spain": "ES",
    "portugal": "PT",
    "netherlands": "NL",
    "belgium": "BE",
    "switzerland": "CH",
    "austria": "AT",
    "canada": "CA",
    "australia": "AU",
    "new zealand": "NZ",
    "china": "CN",
    "people's republic of china": "CN",
    "prc": "CN",
    "taiwan": "TW",
    "hong kong": "HK",
    "macau": "MO",
    "south korea": "KR",
    "korea": "KR",  # 曖昧だが観光文脈では KR 寄せ
    "republic of korea": "KR",
    "north korea": "KP",
    "republic of korea (south korea)": "KR",
    "korea, republic of": "KR",
    "singapore": "SG",
    "malaysia": "MY",
    "thailand": "TH",
    "vietnam": "VN",
    "philippines": "PH",
    "indonesia": "ID",
    "india": "IN",
    "mexico": "MX",
    "brazil": "BR",
    "argentina": "AR",
    "chile": "CL",
    "turkey": "TR",
    "united arab emirates": "AE",
    "uae": "AE",
    "saudi arabia": "SA",
    "qatar": "QA",
    "egypt": "EG",
    "south africa": "ZA",
    "ireland": "IE",
    "denmark": "DK",
    "sweden": "SE",
    "norway": "NO",
    "finland": "FI",
    "poland": "PL",
    "czech": "CZ",
    "czech republic": "CZ",
    "hungary": "HU",
    "greece": "GR",
}

# ISO2 → ISO2 の正規化（既に2文字のとき用）
_ISO2_SET = {v for v in _CANONICAL_TO_ISO2.values()}

def _normalize_text(s: str) -> str:
    s = s.strip().lower()
    # 句読点やドットのバリエーションをざっくり除去
    for ch in [",", ".", "’", "'", "(", ")", "  "]:
        s = s.replace(ch, " ")
    s = " ".join(s.split())
    return s

def to_iso2(country_or_code: str) -> Optional[str]:
    """
    入力が「Japan」「United States」「US」「jp」など何でも来ても
    ISO2（例: JP, US）に正規化して返す。該当なしは None。
    """
    if not country_or_code:
        return None
    s = country_or_code.strip()
    if len(s) == 2:  # 既に ISO2 っぽい
        code = s.upper()
        return code if code in _ISO2_SET else None
    key = _normalize_text(s)
    return _CANONICAL_TO_ISO2.get(key)

def supported_names() -> list[str]:
    """受け付ける国名の例リスト（UI 表示やエラーメッセージ用）"""
    # 表示は代表的な名称だけに絞って返す
    reps = [
        "Japan", "United States", "United Kingdom", "France", "Germany", "Italy", "Spain",
        "Canada", "Australia", "New Zealand", "China", "Taiwan", "Hong Kong",
        "South Korea", "Singapore", "Malaysia", "Thailand", "Vietnam", "Philippines",
        "Indonesia", "India",
        "Mexico", "Brazil", "Turkey", "United Arab Emirates", "Saudi Arabia", "Qatar",
        "Egypt", "South Africa",
    ]
    return reps