import { MapPin, Star, BadgeDollarSign } from "lucide-react";
import Header from "../../components/header/Header";
import Footer from "../../components/footer/Footer";
import "./HotelReserve.css";

import { useState } from "react";

export default function HotelReserve() {
  const [nationality, setNationality] = useState({});

  const hotels = [
    {
      id: 1,
      name: "東京グランドホテル",
      address: "東京都港区芝２丁目５−２",
      price: "¥12,800~",
      img: "/assets/hotel11.jpg",
      rating: "4.2 (1,234件)",
    },
    {
      id: 2,
      name: "アパホテル〈六本木SIX〉",
      address: "東京都港区六本木2-3-11",
      price: "¥9,000~",
      img: "/assets/hotel2.jpg",
      rating: "4.5 (800件)",
    },
    {
      id: 3,
      name: "品川プリンスホテル",
      address: "東京都港区高輪4-10-30",
      price: "¥6,200~",
      img: "/assets/hotel3.jpg",
      rating: "3.85 (23.086件)",
    },
    {
      id: 4,
      name: "東京ドームホテル",
      address: "東京都文京区後楽1-3-61",
      price: "¥7,500~",
      img: "/assets/hotel4.jpg",
      rating: "4.48 (13,212件)",
    },
    {
      id: 5,
      name: "アワーズイン阪急",
      address: "東京都品川区大井1-50-5",
      price: "¥3,500~",
      img: "/assets/hotel5.jpg",
      rating: "4.28 (5610件)",
    },
    // 必要に応じて追加
  ];

  const g7Countries = [
    "Japan",
    "United States",
    "United Kingdom",
    "France",
    "Germany",
    "Italy",
    "Canada",
    "China",
    "South Korea",
    "Vietnam",
  ];

  const handleReserve = async (hotel) => {
    const selectedNationality = nationality[hotel.id] || "";

    if (!selectedNationality) {
      alert("Please select nationality");
      return;
    }

    const payload = {
      to: "kimsoungyoon01@gmail.com",
      address: hotel.address,
      nationality: selectedNationality,
    };

    try {
      const res = await fetch("http://127.0.0.1:8000/api/reservation/submit", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      const data = await res.json(); // 先にレスポンスをパース

      if (res.ok) {
        // 👉 レスポンスをキャッシュ
        localStorage.setItem("reservationResult", JSON.stringify(data));
        alert("Reservation request sent!");

        // 👉 キャッシュ確認用ログ
        console.log("✅ Cached reservation result:", data);
        console.log(
          "✅ LocalStorage content:",
          JSON.parse(localStorage.getItem("reservationResult"))
        );
      } else {
        alert(
          "Failed to send reservation: " + (data?.detail || "Unknown error")
        );
      }
    } catch (err) {
      console.error("❌ Error sending reservation:", err);
      alert("Error sending reservation");
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <div className="hotelCards">
        {hotels.map((hotel) => (
          <div key={hotel.id} className="hotelCard">
            <div className="md:w-1/3">
              <img src={hotel.img} alt="" className="hotelImg" />
            </div>
            <div className="hotelComponent">
              <h3 className="text-xl font-bold mb-1">{hotel.name}</h3>
              <div className="flex items-center text-sm text-gray-600 mb-2">
                <MapPin className="h-4 w-4 mr-1" />
                {hotel.address}
              </div>
              <div className="flex items-center">
                <Star className="text-yellow-400 fill-yellow-400" />
                <span className="ml-2 text-sm text-gray-600">
                  {hotel.rating}
                </span>
              </div>
              <div className="flex items-baseline">
                <BadgeDollarSign />
                <span className="text-2xl font-bold text-red-600">
                  {hotel.price}
                </span>
              </div>
              <div className="form-group">
                <label className="form-label">Nationality</label>
                <select
                  className="form-input"
                  value={nationality[hotel.id] || ""}
                  onChange={(e) =>
                    setNationality({
                      ...nationality,
                      [hotel.id]: e.target.value,
                    })
                  }
                >
                  <option value="">Please select</option>
                  {g7Countries.map((country, idx) => (
                    <option key={idx} value={country}>
                      {country}
                    </option>
                  ))}
                </select>
              </div>
            </div>
            <button
              className="reserveButton"
              onClick={() => handleReserve(hotel)}
            >
              Book Now
            </button>
          </div>
        ))}
      </div>
      <Footer />
    </div>
  );
}
