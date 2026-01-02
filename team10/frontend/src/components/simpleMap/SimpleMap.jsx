import React, { useState, useEffect } from "react";
import { GoogleMap, useJsApiLoader, MarkerF } from "@react-google-maps/api";

const containerStyle = {
  width: "100%",
  height: "80vh",
};

// ★ステップ1: 基準となるホテルの情報を定義
const baseHotel = {
  name: "仮のホテル（例：九大学研都市駅）",
  lat: 33.5855, // 例：九大学研都市駅の緯度
  lng: 130.2215, // 例：九大学研都市駅の経度
};

function ShelterMapAroundHotel() {
  const { isLoaded } = useJsApiLoader({
    id: "google-map-script",
    googleMapsApiKey: process.env.REACT_APP_GOOGLE_MAPS_API_KEY,
  });

  const [shelters, setShelters] = useState([]);
  const [mapCenter, setMapCenter] = useState({
    lat: baseHotel.lat,
    lng: baseHotel.lng,
  }); // 地図の中心をホテルに設定

  useEffect(() => {
    const fetchNearbyShelters = async () => {
      try {
        // ★ステップ2: APIリクエストにホテルの緯度経度をクエリパラメータとして追加
        const response = await fetch(
          `http://localhost:8000/api/shelters/nearby?lat=${baseHotel.lat}&lng=${baseHotel.lng}`
        );
        if (!response.ok) {
          throw new Error("データの取得に失敗しました。");
        }
        const data = await response.json();
        setShelters(data.shelters || []);
      } catch (error) {
        console.error("周辺避難所データの取得に失敗しました:", error);
      }
    };

    fetchNearbyShelters();
  }, []); // 初回レンダリング時に一度だけ実行

  if (!isLoaded) return <div>地図を読み込んでいます...</div>;

  return (
    <GoogleMap mapContainerStyle={containerStyle} center={mapCenter} zoom={15}>
      {/* ★ステップ3: 基準のホテル自体もマーカーとして表示 */}
      <MarkerF
        position={{ lat: baseHotel.lat, lng: baseHotel.lng }}
        title={baseHotel.name}
        // ホテルと避難所を区別するためにアイコンを変える（青いピン）
        icon={"http://maps.google.com/mapfiles/ms/icons/blue-dot.png"}
      />

      {/* 取得した周辺の避難所をマッピングして表示 */}
      {shelters.map((shelter) => (
        <MarkerF
          key={shelter.id}
          position={{ lat: shelter.latitude, lng: shelter.longitude }}
          title={shelter.name}
        />
      ))}
    </GoogleMap>
  );
}

export default ShelterMapAroundHotel;
