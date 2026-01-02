import React from "react";
import { useLocation } from "react-router-dom";
import "./Input.css"; // ← CSSファイルをインポート

export default function Input() {
  const location = useLocation();
  const hotel = location.state || {};

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

  return (
    <div className="input-container">
      <h1 className="form-title">Reservation Form</h1>

      <form className="form">
        {/* Hotel Name */}
        <div className="form-group">
          <label className="form-label">Hotel Name</label>
          <input
            type="text"
            value={hotel.name || ""}
            readOnly
            className="form-input readonly"
          />
        </div>

        {/* Address */}
        <div className="form-group">
          <label className="form-label">Address</label>
          <input
            type="text"
            value={hotel.address || ""}
            readOnly
            className="form-input readonly"
          />
        </div>

        {/* Nationality */}
        <div className="form-group">
          <label className="form-label">Nationality</label>
          <select className="form-input">
            <option value="">Please select</option>
            {g7Countries.map((country, idx) => (
              <option key={idx} value={country}>
                {country}
              </option>
            ))}
          </select>
        </div>

        <button type="submit" className="submit-button">
          Confirm Reservation
        </button>
      </form>
    </div>
  );
}
