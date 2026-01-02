import "./App.css";
import { Routes, Route } from "react-router-dom";
import HotelReserve from "./pages/reserve/HotelReserve";
import Info from "./pages/info/Info";
import Flooding from "./pages/flooding/Flooding";
import Shelter from "./pages/shelter/Shelter";

function App() {
  return (
    <Routes>
      <Route path="/" element={<HotelReserve />} />
      <Route path="/info" element={<Info />} />
      <Route path="/flooding" element={<Flooding />} />
      <Route path="/shelter" element={<Shelter />} />
    </Routes>
  );
}

export default App;
