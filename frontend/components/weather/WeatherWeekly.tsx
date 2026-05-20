"use client";

import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";
import { mapWeatherCode, weatherIcon } from "@/lib/weatherUtils";

export default function WeatherWeekly() {

  const [days, setDays] = useState<any[]>([]);

  useEffect(() => {
    apiFetch("/api/weather/daily")
      .then(res => res.json())
      .then(res => {

        const formatted = res.daily.map((d: any) => {
          const date = new Date(d.date);

          const weekday = date.toLocaleDateString("en-US", {
            weekday: "short"
          });

          return {
            d: weekday,
            min: Math.round(d.temp_min),
            max: Math.round(d.temp_max),
            icon: weatherIcon(mapWeatherCode(d.weathercode))
          };
        });

        setDays(formatted);
      })
      .catch(err => console.error(err));
  }, []);

  if (!days.length) {
    return (
      <div className="bg-white/90 backdrop-blur-md rounded-2xl shadow-lg p-4">
        <h3 className="font-semibold mb-2">7-day forecast</h3>
        <div className="text-sm text-gray-500">Loading...</div>
      </div>
    );
  }

  return (
    <div className="bg-white/90 backdrop-blur-md rounded-2xl shadow-lg p-4">
      <h3 className="font-semibold mb-2">7-day forecast</h3>

      <div className="space-y-1 text-sm">
        {days.map((d, i) => (
          <div key={i} className="flex justify-between">
            <span className="w-10">{d.d}</span>
            <span>{d.icon}</span>
            <span>{d.min}° ~ {d.max}°</span>
          </div>
        ))}
      </div>
    </div>
  );
}

