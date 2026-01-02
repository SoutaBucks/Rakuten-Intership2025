// import React, {useState, useEffect} from "react";
// import {GoogleMap, useJsApiLoader, MarkerF} from "@react-google-maps/api";
//
// const containerStyle = {
//   width: "100%",
//   height: "80vh",
// };
//
// // ★ステップ1: 基準となるホテルの情報を定義
// const baseHotel = {
//   name: "仮のホテル（例：九大学研都市駅）",
//   lat: 35.6762, // Tokyo center
//   lng: 139.6503,
// };
//
// function ShelterMapAroundHotel() {
//   const {isLoaded} = useJsApiLoader({
//     id: "google-map-script",
//     googleMapsApiKey: process.env.REACT_APP_GOOGLE_MAPS_API_KEY,
//   });
//
//   const [shelters, setShelters] = useState([]); // All Shelters in Tokyo
//   const [nearbyShelters, setNearbyShelters] = useState([]); // Get Shelters near by Hotel
//   const [mapCenter, setMapCenter] = useState({
//     lat: baseHotel.lat,
//     lng: baseHotel.lng,
//   }); // 地図の中心をホテルに設定
//
//   // Get all Shelters
//   const fetchAllShelters = async () => {
//     try {
//       const response = await fetch("http://localhost:8000/api/shelters");
//       if (!response.ok) {
//         throw new Error("Fail to Get Information.");
//       }
//       const data = await response.json();
//       setShelters(data.shelters || []);
//     } catch (error) {
//       console.error("Fail to get Shelters:", error);
//     }
//   };
//
//   // Find Shelters based on Hotel's location
//   const fetchNearbyShelters = async () => {
//     try {
//       const response = await fetch(`http://localhost:8000/api/shelters/search/location?latitude=${baseHotel.lat}&longitude=${baseHotel.lng}&radius_km=10`);
//       if (!response.ok) {
//         throw new Error("Fail to get Data");
//       }
//       const data = await response.json();
//       setNearbyShelters(data.shelters || []);
//     } catch (error) {
//       console.error("Fail to get Shelters based on Hotel's location", error);
//       setNearbyShelters(shelters);
//     }
//   }
//
//   useEffect(() => {
//     fetchAllShelters();
//     fetchNearbyShelters();
//   }, []); // 初回レンダリング時に一度だけ実行
//
//   // Let's calculate distance!
//   const calculateDistance = (lat1, lng1, lat2, lng2) => {
//     const R = 6371;
//     const dLat = (lat2 - lat1) * Math.PI / 180;
//     const dLng = (lng2 - lng1) * Math.PI / 180;
//     const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
//       Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
//       Math.sin(dLng / 2) * Math.sin(dLng / 2);
//     const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
//     return Math.round(R * c * 100) / 100;
//   };
//
//   // Sort by distance between hotel and shelters
//   const sortedNearbyShelters = [...nearbyShelters].map(shelter => ({
//     ...shelter,
//     distance: calculateDistance(
//       baseHotel.lat,
//       baseHotel.lng,
//       parseFloat(shelter.latitude),
//       parseFloat(shelter.longitude)
//     )
//   })).sort((a, b) => a.distance - b.distance);
//
//   if (!isLoaded) return <div>地図を読み込んでいます...</div>;
//
//   return (
//     <div style={{display: "flex", height: "80vh"}}>
//       {/* MAP AREA*/}
//       <div style={{flex: "2", position: "relative"}}>
//         <GoogleMap
//           mapContainerStyle={containerStyle}
//           center={mapCenter}
//           zoom={12}
//         >
//           {/* MARKER OF HOTEL LOCATION*/}
//           <MarkerF
//             position={{lat: baseHotel.lat, lng: baseHotel.lng}}
//             title={baseHotel.name}
//             icon={"http://maps.google.com/mapfiles/ms/icons/blue-dot.png"}
//           />
//
//           {/* MARKERS OF ALL SHELTERS*/}
//           {shelters.map((shelter) => (
//             <MarkerF
//               key={shelter.id}
//               position={{
//                 lat: parseFloat(shelter.latitude),
//                 lng: parseFloat(shelter.longitude)
//               }}
//               title={shelter.name}
//               icon={"http://maps.google.com/mapfiles/ms/icons/red-dot.png"}
//             />
//           ))}
//         </GoogleMap>
//       </div>
//       {/* Nearby shelters sidebar */}
//       <div style={{
//         flex: "1",
//         backgroundColor: "#f8f9fa",
//         padding: "20px",
//         overflowY: "auto",
//         borderLeft: "1px solid #dee2e6"
//       }}>
//         <h2 style={{
//           marginBottom: "20px",
//           color: "#2c3e50",
//           fontSize: "1.5rem"
//         }}>
//           🏨 Nearby Shelters
//         </h2>
//
//         <div style={{
//           background: "#e3f2fd",
//           padding: "10px",
//           borderRadius: "8px",
//           marginBottom: "15px",
//           fontSize: "14px"
//         }}>
//           📍 Hotel Location: {baseHotel.name}
//           <br/>
//           Coordinates: {baseHotel.lat.toFixed(6)}, {baseHotel.lng.toFixed(6)}
//           <br/>
//           <span style={{color: "#e74c3c", fontWeight: "bold"}}>
//             Total {sortedNearbyShelters.length} shelters (within 10km radius)
//           </span>
//         </div>
//
//         <div style={{marginBottom: "15px"}}>
//           <button
//             onClick={fetchNearbyShelters}
//             style={{
//               background: "#3498db",
//               color: "white",
//               border: "none",
//               padding: "8px 16px",
//               borderRadius: "5px",
//               cursor: "pointer",
//               fontSize: "14px"
//             }}
//           >
//             🔄 Refresh
//           </button>
//         </div>
//
//         {sortedNearbyShelters.length === 0 ? (
//           <div style={{textAlign: "center", color: "#666"}}>
//             No shelters found near the hotel.
//           </div>
//         ) : (
//           <div>
//             {sortedNearbyShelters.map((shelter, index) => (
//               <div
//                 key={shelter.id}
//                 style={{
//                   background: "white",
//                   padding: "15px",
//                   marginBottom: "10px",
//                   borderRadius: "8px",
//                   borderLeft: index === 0 ? "4px solid #e74c3c" : "4px solid #3498db",
//                   boxShadow: "0 2px 4px rgba(0,0,0,0.1)",
//                   cursor: "pointer",
//                   transition: "all 0.3s ease"
//                 }}
//                 onMouseEnter={(e) => {
//                   e.target.style.transform = "translateX(5px)";
//                   e.target.style.boxShadow = "0 4px 8px rgba(0,0,0,0.15)";
//                 }}
//                 onMouseLeave={(e) => {
//                   e.target.style.transform = "translateX(0)";
//                   e.target.style.boxShadow = "0 2px 4px rgba(0,0,0,0.1)";
//                 }}
//                 onClick={() => {
//                   setMapCenter({
//                     lat: parseFloat(shelter.latitude),
//                     lng: parseFloat(shelter.longitude)
//                   });
//                 }}
//               >
//                 <div style={{
//                   fontWeight: "bold",
//                   color: "#2c3e50",
//                   marginBottom: "5px",
//                   fontSize: "16px"
//                 }}>
//                   {index + 1}. {shelter.name}
//                 </div>
//                 <div style={{
//                   color: "#666",
//                   fontSize: "14px",
//                   marginBottom: "5px"
//                 }}>
//                   📍 {shelter.address}
//                 </div>
//                 <div style={{
//                   color: "#e74c3c",
//                   fontWeight: "bold",
//                   fontSize: "14px"
//                 }}>
//                   📏 {shelter.distance}km
//                 </div>
//                 <div style={{
//                   color: "#999",
//                   fontSize: "12px",
//                   marginTop: "5px"
//                 }}>
//                   ID: {shelter.id}
//                 </div>
//               </div>
//             ))}
//           </div>
//         )}
//       </div>
//     </div>
//   );
// }
//
// export default ShelterMapAroundHotel;


import React, {useState, useEffect} from "react";
import {GoogleMap, useJsApiLoader, MarkerF} from "@react-google-maps/api";
import "./Shelter.css";

const containerStyle = {
  width: "100%",
  height: "100%",
};


// Hotel information
const defaultHotel = {
  name: "Tokyo Hotel",
  lat: 35.6762, // Tokyo center
  lng: 139.6503,
};


function ShelterMapAroundHotel() {
  const {isLoaded} = useJsApiLoader({
    id: "google-map-script",
    googleMapsApiKey: process.env.REACT_APP_GOOGLE_MAPS_API_KEY,
  });

  /* ----- V1 ----
  const [baseHotel, setBaseHotel] = useState({
    name: "Tokyo Hotel",
    lat: 35.6762,
    lng: 139.6503,
  });
  //------------*/

  const [baseHotel, setBaseHotel] = useState(defaultHotel);
  const [shelters, setShelters] = useState([]); // All Shelters in Tokyo
  const [nearbyShelters, setNearbyShelters] = useState([]); // Get Shelters near by Hotel
  const [mapCenter, setMapCenter] = useState({
    lat: 35.6762,
    lng: 139.6503,
  });
  const [hoveredShelterId, setHoveredShelterId] = useState(null); // 호버된 shelter ID 추가

  useEffect(() => {
      const cachedData = localStorage.getItem("reservationResult");

      if (cachedData) {
        console.log("✅ Loading hotel information from cache.");
        try {
          const reservationResult = JSON.parse(cachedData);

          if (reservationResult.hotel) {
            const hotelData = {
              name: `Hotel at ${reservationResult.hotel.address}`,
              lat: reservationResult.hotel.lat,
              lng: reservationResult.hotel.lng,
            };

            setBaseHotel(hotelData);
            setMapCenter({
              lat: hotelData.lat,
              lng: hotelData.lng,
            });

            console.log("✅ Using cached hotel information:", hotelData);
          } else {
            console.log("⚠️ No hotel information in cache. Using default values.");
          }
        } catch (e) {
          console.error("Failed to parse cache data:", e);
          console.log("⚠️ Using default hotel information.");
        }
      } else {
        console.log("⚠️ No cache found. Using default hotel information.");
      }
    }, []);

// Get all Shelters
  const fetchAllShelters = async () => {
    try {
      const response = await fetch("http://localhost:8000/api/shelters");
      if (!response.ok) {
        throw new Error("Fail to Get Information.");
      }
      const data = await response.json();
      setShelters(data.shelters || []);
    } catch (error) {
      console.error("Fail to get Shelters:", error);
    }
  };

// Find Shelters based on Hotel's location
  const fetchNearbyShelters = async () => {
    try {
      const response = await fetch(`http://localhost:8000/api/shelters/search/location?latitude=${baseHotel.lat}&longitude=${baseHotel.lng}&radius_km=10`);
      if (!response.ok) {
        throw new Error("Fail to get Data");
      }
      const data = await response.json();
      setNearbyShelters(data.shelters || []);
    } catch (error) {
      console.error("Fail to get Shelters based on Hotel's location", error);
      setNearbyShelters(shelters);
    }
  }

  useEffect(() => {
    fetchAllShelters();
    fetchNearbyShelters();
  }, [baseHotel.lat, baseHotel.lng]);

// Calculate distance
  const calculateDistance = (lat1, lng1, lat2, lng2) => {
    const R = 6371;
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLng = (lng2 - lng1) * Math.PI / 180;
    const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
      Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
      Math.sin(dLng / 2) * Math.sin(dLng / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return Math.round(R * c * 100) / 100;
  };

// Sort by distance between hotel and shelters
  const sortedNearbyShelters = [...nearbyShelters].map(shelter => ({
    ...shelter,
    distance: calculateDistance(
      baseHotel.lat,
      baseHotel.lng,
      parseFloat(shelter.latitude),
      parseFloat(shelter.longitude)
    )
  })).sort((a, b) => a.distance - b.distance);

  if (!isLoaded) return <div className="loading">Loading map...</div>;

  return (
    <div className="container">
      {/* Map Area */}
      <div className="map-container">
        <GoogleMap
          mapContainerStyle={containerStyle}
          center={mapCenter}
          zoom={15}
        >
          {/* Hotel location marker */}
          <MarkerF
            position={{lat: baseHotel.lat, lng: baseHotel.lng}}
            title={baseHotel.name}
            icon={"http://maps.google.com/mapfiles/ms/icons/blue-dot.png"}
          />

          {/* All shelter markers */}
          {shelters.map((shelter) => {
            // if you hovered shelter, then show that or show every shelter
            const shouldShow = !hoveredShelterId || shelter.id === hoveredShelterId

            if (!shouldShow) return null;

            return (
              <MarkerF
                key={shelter.id}
                position={{
                  lat: parseFloat(shelter.latitude),
                  lng: parseFloat(shelter.longitude)
                }}
                title={shelter.name}
                icon={hoveredShelterId === shelter.id
                  ? "http://maps.google.com/mapfiles/ms/icons/yellow-dot.png" // 노란색 핀
                  : "http://maps.google.com/mapfiles/ms/icons/red-dot.png" // 빨간색 핀
                }
              />
            );
          })}
        </GoogleMap>
      </div>

      {/* Nearby shelters sidebar */}
      <div className="sidebar">
        <h2 className="sidebar-title">
          🏨 Nearby Shelters
        </h2>

        <div className="hotel-info">
          📍 Hotel Location: {baseHotel.name}
          <br/>
          Coordinates: {baseHotel.lat.toFixed(6)}, {baseHotel.lng.toFixed(6)}
          <br/>
          <span>
            Total {sortedNearbyShelters.length} shelters (within 10km radius)
          </span>
        </div>

        <button
          onClick={() => {
            setMapCenter({
              lat: baseHotel.lat,
              lng: baseHotel.lng
            });
          }}
          className="refresh-button"
        >
          🏨 Focus on Hotel
        </button>

        {sortedNearbyShelters.length === 0 ? (
          <div className="no-shelters">
            No shelters found near the hotel.
          </div>
        ) : (
          <div>
            {sortedNearbyShelters.map((shelter, index) => (
              <div
                key={shelter.id}
                className={`shelter-item ${index === 0 ? 'closest' : ''}`}
                onMouseEnter={() => setHoveredShelterId(shelter.id)}
                onMouseLeave={() => setHoveredShelterId(null)}
                onClick={() => {
                  setMapCenter({
                    lat: parseFloat(shelter.latitude),
                    lng: parseFloat(shelter.longitude)
                  });
                }}
              >
                <div className="shelter-name">
                  {index + 1}. {shelter.name}
                </div>
                <div className="shelter-address">
                  📍 {shelter.address}
                </div>
                <div className="shelter-distance">
                  📏 {shelter.distance}km
                </div>
                <div className="shelter-id">
                  ID: {shelter.id}
                </div>
                {/* find the route Shelter*/}
                <button
                  className="directions-btn"
                  onClick={(e) => {
                    e.stopPropagation(); // 부모 클릭 이벤트 방지
                    const directionsUrl = `https://www.google.com/maps/dir/?api=1&origin=${baseHotel.lat},${baseHotel.lng}&destination=${shelter.latitude},${shelter.longitude}&travelmode=walking`;
                    window.open(directionsUrl, '_blank');
                  }}
                >
                  Find route
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
    ;
}

export default ShelterMapAroundHotel;