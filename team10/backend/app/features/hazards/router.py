from fastapi import APIRouter, Query

router = APIRouter()

def _hazard_payload(lat: float, lng: float, zoom: int):
    layers = [
        {"id":"flood_max","title":"洪水（想定最大規模）","template":"https://disaportaldata.gsi.go.jp/raster/01_flood_l2_shinsuishin_data/{z}/{x}/{y}.png","visible": True,"opacity":0.6,"minZoom":2,"maxZoom":17},
        {"id":"flood_duration","title":"浸水継続時間（最大）","template":"https://disaportaldata.gsi.go.jp/raster/01_flood_l2_keizoku_data/{z}/{x}/{y}.png","opacity":0.6},
        {"id":"tsunami","title":"津波浸水想定","template":"https://disaportaldata.gsi.go.jp/raster/04_tsunami_newlegend_data/{z}/{x}/{y}.png","opacity":0.6},
        {"id":"hightide","title":"高潮浸水想定","template":"https://disaportaldata.gsi.go.jp/raster/03_hightide_l2_shinsuishin_data/{z}/{x}/{y}.png","opacity":0.6},
        {"id":"dosha_dosekiryuu","title":"土砂（⽯流）","template":"https://disaportaldata.gsi.go.jp/raster/05_dosekiryukeikaikuiki/{z}/{x}/{y}.png","opacity":0.7},
        {"id":"dosha_kyukeisha","title":"土砂（急傾斜）","template":"https://disaportaldata.gsi.go.jp/raster/05_kyukeishakeikaikuiki/{z}/{x}/{y}.png","opacity":0.7},
        {"id":"dosha_jisuberi","title":"土砂（地すべり）","template":"https://disaportaldata.gsi.go.jp/raster/05_jisuberikeikaikuiki/{z}/{x}/{y}.png","opacity":0.7}
    ]
    return {"center":{"lat": lat,"lng": lng,"zoom": zoom},"layers": layers}

@router.get("/around", summary="周辺ハザード地図レイヤー")
def hazards_around(lat: float = Query(...), lng: float = Query(...), zoom: int = Query(15)):
    return _hazard_payload(lat, lng, zoom)

@router.get("/around-by-address", summary="住所から周辺ハザード地図レイヤー")
def hazards_around_by_address(address: str = Query(...), zoom: int = Query(15)):
    # 呼び出し時に import（依存が無い場合でも API を落とさない）
    try:
        from app.features.area.jp_geocode import geocode_address_jp
        pt = geocode_address_jp(address)
    except Exception:
        pt = None

    if pt:
        lat, lng = pt
        payload = _hazard_payload(lat, lng, zoom)
    else:
        # 明示的なフォールバック（東京駅）
        lat, lng = 35.681236, 139.767125
        payload = _hazard_payload(lat, lng, zoom)
        payload["note"] = "fallback_to_tokyo"
        payload["resolved_from"] = address

    return payload
