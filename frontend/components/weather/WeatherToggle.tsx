"use client";
import { useState } from "react";
import WeatherPanel from "./WeatherPanel";

export default function WeatherToggle() {
  const [open, setOpen] = useState(false);

  return (
    <>
      {/* 按钮 */}
      <div className="absolute top-4 left-[25vw] -translate-x-1/2 z-[1000]">
        <button
          onClick={() => setOpen(!open)}
          className="bg-white/90 backdrop-blur-md shadow-lg rounded-xl px-4 py-2 text-sm font-medium hover:bg-white transition"
        >
          ☁ Weather
        </button>
      </div>

      {/* 面板 */}
      {open && <WeatherPanel />}
    </>
  );
}
