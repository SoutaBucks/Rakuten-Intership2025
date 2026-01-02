// import React, { useState, useEffect, useCallback } from 'react';
// import { Link } from 'react-router-dom';
// import { Map, Source, Layer, Marker } from 'react-map-gl/maplibre';
// import maplibregl from 'maplibre-gl';
// import 'maplibre-gl/dist/maplibre-gl.css';
// import './Flooding.css';
//
// const API_BASE_URL = 'http://127.0.0.1:8000/api/hazards';
//
// // ホテルの固定座標
// const DEFAULT_HOTEL_LOCATION = {
//   latitude: 35.4561,
//   longitude: 139.6338,
//   name: '横浜ベイホテル東急'
// };
//
// const legendMapping = {
//   "flood_max": "https://disaportal.gsi.go.jp/img/raster/01_flood_l2_shinsuishin_legend.png",
//   "flood_duration": "https://disaportal.gsi.go.jp/img/raster/01_flood_l2_keizoku_legend.png",
//   "tsunami": "https://disaportal.gsi.go.jp/img/raster/04_tsunami_newlegend_legend.png",
//   "hightide": "https://disaportal.gsi.go.jp/img/raster/03_hightide_l2_shinsuishin_legend.png",
//   "dosha_dosekiryuu": "https://disaportal.gsi.go.jp/img/raster/05_dosekiryukeikaikuiki_legend.png",
//   "dosha_kyukeisha": "https://disaportal.gsi.go.jp/img/raster/05_kyukeishakeikaikuiki_legend.png",
//   "dosha_jisuberi": "https://disaportal.gsi.go.jp/img/raster/05_jisuberikeikaikuiki_legend.png"
// };
//
// export default function FloodingMap() {
//   const [mapData, setMapData] = useState(null);
//   const [activeLayerIds, setActiveLayerIds] = useState(new Set());
//   const [loading, setLoading] = useState(true);
//   const [error, setError] = useState(null);
//   const [viewState, setViewState] = useState({ ...DEFAULT_HOTEL_LOCATION, zoom: 13 });
//   const [userLocation, setUserLocation] = useState(null);
//
//   // ★ 修正点2: ホテルの位置情報をstateとして管理する
//   const [hotelLocation, setHotelLocation] = useState(DEFAULT_HOTEL_LOCATION);
//
//
//   // ハザードデータを取得する関数（初回のみ使用）
//   const fetchHazardDataForLocation = useCallback(async (location) => {
//     setLoading(true);
//     setError(null);
//     try {
//       const url = `${API_BASE_URL}/around?lat=${location.latitude}&lng=${location.longitude}&zoom=14`;
//       const response = await fetch(url);
//       if (!response.ok) throw new Error('地図データの取得に失敗しました');
//       const data = await response.json();
//       setMapData(data);
//       if (activeLayerIds.size === 0) {
//         const initialLayer = data.layers.find(layer => layer.visible);
//         if (initialLayer) setActiveLayerIds(new Set([initialLayer.id]));
//       }
//     } catch (err) {
//       setError(err.message);
//     } finally {
//       setLoading(false);
//     }
//   }, [activeLayerIds]);
//
//   // 初回レンダリング時に現在地を取得し、ホテル周辺のハザードマップを読み込む
//   useEffect(() => {
//     let targetLocation = DEFAULT_HOTEL_LOCATION; // まずデフォルト値を設定
//
//     const cachedData = localStorage.getItem("reservationResult");
//     if (cachedData) {
//       try {
//         const reservationResult = JSON.parse(cachedData);
//         // キャッシュに hotel と lat, lng があれば更新
//         if (reservationResult.hotel?.lat && reservationResult.hotel?.lng) {
//           console.log("✅ キャッシュからホテルの位置情報を読み込みます。");
//           targetLocation = {
//             latitude: reservationResult.hotel.lat,
//             longitude: reservationResult.hotel.lng,
//             name: reservationResult.hotel.address || '予約したホテル'
//           };
//         }
//       } catch (e) {
//         console.error("キャッシュデータの解析に失敗しました:", e);
//       }
//     } else {
//       console.log("⚠️ キャッシュがありません。デフォルトのホテル位置を使用します。");
//     }
//     // 確定した位置情報をstateにセット
//     setHotelLocation(targetLocation);
//
//     // 確定した位置情報でハザードマップを読み込む
//     fetchHazardDataForLocation(targetLocation);
//
//     // 同時にユーザーの現在地を取得する
//     navigator.geolocation.getCurrentPosition(
//       (position) => {
//         const { latitude, longitude } = position.coords;
//         setUserLocation({ latitude, longitude });
//       },
//       () => {
//         // 取得に失敗しても何もしない（ピンが表示されないだけ）
//         console.error("現在地の取得に失敗しました。");
//         setUserLocation(null);
//       }
//     );
//   }, [fetchHazardDataForLocation]);
//
//   // 【変更】指定された位置に地図を移動させる関数
//   const panToLocation = (location) => {
//     if (!location) return;
//     setViewState({
//       ...location,
//       zoom: 15, // ズームインする
//     });
//   };
//
//   const handleLayerChange = (layerId, isChecked) => {
//     setActiveLayerIds(prevIds => {
//       const newIds = new Set(prevIds);
//       if (isChecked) newIds.add(layerId);
//       else newIds.delete(layerId);
//       return newIds;
//     });
//   };
//
//   const activeLayers = mapData?.layers.filter(layer => activeLayerIds.has(layer.id)) || [];
//
//   if (!mapData) return <div className="container"><p>地図データを読み込み中...</p></div>;
//   if (error) return <div className="container"><p>エラー: {error}</p></div>;
//
//   return (
//     <div className="container full-height">
//       <header className="header">
//
//         <h1>浸水・土砂災害ハザードマップ</h1>
//         {/* hotelLocation.name を使用して動的に表示 */}
//
//
//
//         <div className="location-switcher">
//           <button onClick={() => panToLocation(userLocation)} disabled={!userLocation}>
//             現在地に移動
//           </button>
//           {/* hotelLocation を使用 */}
//           <button onClick={() => panToLocation(hotelLocation)}>
//             ホテルに移動
//           </button>
//         </div>
//         {loading && <p className="info-area">読み込み中...</p>}
//       </header>
//
//       <div className="mainContent map-wrapper">
//         <div className="sidebar">
//           <h2>表示レイヤー</h2>
//           {mapData.layers.map(layer => (
//             <div key={layer.id} className="layer-control">
//               <input type="checkbox" id={layer.id} value={layer.id} checked={activeLayerIds.has(layer.id)} onChange={(e) => handleLayerChange(layer.id, e.target.checked)} />
//               <label htmlFor={layer.id}>{layer.title}</label>
//             </div>
//           ))}
//         </div>
//
//         <div className="map-container">
//           <Map
//             mapLib={maplibregl}
//             {...viewState}
//             onMove={evt => setViewState(evt.viewState)}
//             style={{ width: '100%', height: '100%' }}
//             mapStyle="https://gsi-cyberjapan.github.io/gsivectortile-mapbox-gl-js/std.json"
//           >
//             {activeLayers.map(layer => (
//               <Source key={layer.id} id={layer.id} type="raster" tiles={[layer.template]} tileSize={256}>
//                 <Layer id={`${layer.id}-layer`} type="raster" source={layer.id} paint={{ 'raster-opacity': layer.opacity || 0.7 }} />
//               </Source>
//             ))}
//
//             {/* hotelLocation を使用 */}
//           <Marker longitude={hotelLocation.longitude} latitude={hotelLocation.latitude} anchor="bottom">
//             <div className="location-pin hotel-pin" />
//           </Marker>
//
//             {/* 【追加】現在地のピンを常に表示（座標が取得できている場合） */}
//             {userLocation && (
//               <Marker longitude={userLocation.longitude} latitude={userLocation.latitude} anchor="bottom">
//                 <div className="location-pin user-pin" />
//               </Marker>
//             )}
//           </Map>
//
//           <div className="legend-container">
//             {activeLayers.map(layer => legendMapping[layer.id] && (
//               <div key={layer.id} className="legend-item">
//                 <p>{layer.title}</p>
//                 <img src={legendMapping[layer.id]} alt={`${layer.title}の凡例`} />
//               </div>
//             ))}
//           </div>
//         </div>
//       </div>
//
//       <footer className="footer">
//         <Link to="/info" className="backLink">緊急情報システムに戻る</Link>
//       </footer>
//     </div>
//   );
// }

import React, { useState, useEffect, useCallback } from 'react';
import { Link } from 'react-router-dom';
import { Map, Source, Layer, Marker } from 'react-map-gl/maplibre';
import maplibregl from 'maplibre-gl';
import 'maplibre-gl/dist/maplibre-gl.css';
import './Flooding.css';

const API_BASE_URL = 'http://127.0.0.1:8000/api/hazards';

// Fixed coordinates for the hotel
const DEFAULT_HOTEL_LOCATION = {
  latitude: 35.4561,
  longitude: 139.6338,
  name: 'Yokohama Bay Hotel Tokyu'
};

// ★ 変更点 1: 初期位置を決定する関数をコンポーネントの外に定義
// これにより、コンポーネントがレンダリングされる前に一度だけ実行される
const getInitialLocation = () => {
  const cachedData = localStorage.getItem("reservationResult");
  if (cachedData) {
    try {
      const reservationResult = JSON.parse(cachedData);
      if (reservationResult.hotel?.lat && reservationResult.hotel?.lng) {
        console.log("✅ Initializing from cached hotel location.");
        return {
          latitude: reservationResult.hotel.lat,
          longitude: reservationResult.hotel.lng,
          name: reservationResult.hotel.address || 'Your Booked Hotel'
        };
      }
    } catch (e) {
      console.error("Failed to parse cached data:", e);
    }
  }
  console.log("⚠️ No valid cache. Initializing with default hotel location.");
  return DEFAULT_HOTEL_LOCATION;
};

// ★ 変更点 2: ページ読み込み時に初期位置を一度だけ取得
const initialLocation = getInitialLocation();

export default function FloodingMap() {
  const [mapData, setMapData] = useState(null);
  const [activeLayerIds, setActiveLayerIds] = useState(new Set());
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [userLocation, setUserLocation] = useState(null);

  // ★ 変更点 3: 地図の中心(viewState)とホテルの位置(hotelLocation)を
  // キャッシュから取得した `initialLocation` で初期化する
  const [hotelLocation] = useState(initialLocation);
  const [viewState, setViewState] = useState({ ...initialLocation, zoom: 13 });

  // Function to fetch hazard data (used only on initial load)
  const fetchHazardDataForLocation = useCallback(async (location) => {
    setLoading(true);
    setError(null);
    try {
      const url = `${API_BASE_URL}/around?lat=${location.latitude}&lng=${location.longitude}&zoom=14`;
      const response = await fetch(url);
      if (!response.ok) throw new Error('Failed to fetch map data');
      const data = await response.json();
      setMapData(data);
      if (activeLayerIds.size === 0) {
        const initialLayer = data.layers.find(layer => layer.visible);
        if (initialLayer) setActiveLayerIds(new Set([initialLayer.id]));
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [activeLayerIds]);

  // On initial render, get current location and load the hazard map
  useEffect(() => {
    // ★ 変更点 4: 初期位置は既に設定済みのため、ここではデータ取得と現在地取得のみ行う
    // Load the hazard map with the determined location
    fetchHazardDataForLocation(hotelLocation);

    // Concurrently, get the user's current location
    navigator.geolocation.getCurrentPosition(
      (position) => {
        const { latitude, longitude } = position.coords;
        setUserLocation({ latitude, longitude });
      },
      () => {
        // Do nothing on failure (the pin just won't be displayed)
        console.error("Failed to get current location.");
        setUserLocation(null);
      }
    );
    // hotelLocationが変更された場合にも再実行するように依存配列に追加
  }, [fetchHazardDataForLocation, hotelLocation]);

  // Function to pan the map to a specified location
  const panToLocation = (location) => {
    if (!location) return;
    setViewState({
      ...location,
      zoom: 15, // Zoom in
    });
  };

  const handleLayerChange = (layerId, isChecked) => {
    setActiveLayerIds(prevIds => {
      const newIds = new Set(prevIds);
      if (isChecked) newIds.add(layerId);
      else newIds.delete(layerId);
      return newIds;
    });
  };

  const activeLayers = mapData?.layers.filter(layer => activeLayerIds.has(layer.id)) || [];

  if (!mapData) return <div className="container"><p>Loading map data...</p></div>;
  if (error) return <div className="container"><p>Error: {error}</p></div>;

  return (
    <div className="container full-height">
      <header className="header">
        <h1>Flood Zone Map</h1>
        <span>Button to switch viewing position</span>
        <div className="location-switcher">
          <button
            className="btn-hotel"
            onClick={() => panToLocation(hotelLocation)}
          >
            Hotel
          </button>
          <button
            className="btn-location"
            onClick={() => panToLocation(userLocation)}
            disabled={!userLocation}
          >
            Current Location
          </button>
        </div>
        {loading && <p className="info-area">Loading...</p>}
      </header>

      <div className="mainContent map-wrapper">
        <div className="sidebar">
          <h2>Display Layers</h2>
          {mapData.layers.map(layer => (
            <div key={layer.id} className="layer-control">
              <input type="checkbox" id={layer.id} value={layer.id} checked={activeLayerIds.has(layer.id)} onChange={(e) => handleLayerChange(layer.id, e.target.checked)} />
              <label htmlFor={layer.id}>{layer.title}</label>
            </div>
          ))}
        </div>

        <div className="map-container">
          <Map
            mapLib={maplibregl}
            {...viewState}
            onMove={evt => setViewState(evt.viewState)}
            style={{ width: '100%', height: '100%' }}
            mapStyle="https://gsi-cyberjapan.github.io/gsivectortile-mapbox-gl-js/std.json"
          >
            {activeLayers.map(layer => (
              <Source key={layer.id} id={layer.id} type="raster" tiles={[layer.template]} tileSize={256}>
                <Layer id={`${layer.id}-layer`} type="raster" source={layer.id} paint={{ 'raster-opacity': layer.opacity || 0.7 }} />
              </Source>
            ))}

            <Marker longitude={hotelLocation.longitude} latitude={hotelLocation.latitude} anchor="bottom">
              <div className="location-pin hotel-pin" />
            </Marker>

            {/* Always display the current location pin if coordinates are available */}
            {userLocation && (
              <Marker longitude={userLocation.longitude} latitude={userLocation.latitude} anchor="bottom">
                <div className="location-pin user-pin" />
              </Marker>
            )}
          </Map>

          {/* <div className="legend-container">
            {activeLayers.map(layer => legendMapping[layer.id] && (
              <div key={layer.id} className="legend-item">
                <p>{layer.title}</p>
                <img src={legendMapping[layer.id]} alt={`Legend for ${layer.title}`} />
              </div>
            ))}
          </div> */}
        </div>
      </div>

      <footer className="footer">
        <Link to="/info" className="backLink">Back to Emergency Information System</Link>
      </footer>
    </div>
  );
}