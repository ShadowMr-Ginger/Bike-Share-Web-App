"use client";

import { useState, useEffect } from "react";
import { apiFetch } from "@/lib/api";
import {
  weatherIcon,
  weatherText,
  windScaleText,
  mapWeatherCode
} from "@/lib/weatherUtils";

export default function WeatherNow() {

  const [data, setData] = useState<any>(null);

  useEffect(() => {
    apiFetch(`/api/weather/current`)
      .then(res => res.json())
      .then(res => {

        const condition = mapWeatherCode(res.weathercode);

        // 风力等级（简单换算）
        const wind_scale = Math.round(res.windspeed / 2);

        const timeObj = new Date(res.time);
        const updated_at = timeObj.toLocaleTimeString([], {
          hour: "2-digit",
          minute: "2-digit"
        });

        setData({
          temp: Math.round(res.temperature),
          appearent_temp: Math.round(res.appearent_temperature),
          wind_speed: res.windspeed,
          wind_scale: wind_scale,
          condition: condition,
          updated_at: updated_at
        });
      });
  }, []);

  if (!data) return null;

  return (
    <div className="bg-white/90 backdrop-blur-md rounded-2xl shadow-lg p-4">

      {/* Title */}
      <div className="flex justify-between items-center mb-2">
        <h3 className="font-semibold">Current Weather</h3>
      </div>

      {/* Temperature + Icon */}
      <div className="flex items-center justify-between">
        <div>
          <div className="text-3xl font-bold">
            {data.temp}°C
          </div>
          <div className="text-sm text-gray-500">
            Feels like {data.appearent_temp}°C
          </div>
        </div>

        <div className="text-3xl">
          {weatherIcon(data.condition)}
        </div>
      </div>

      {/* Condition */}
      <div className="text-sm mt-1">
        {weatherText(data.condition)}
      </div>

      {/* Wind */}
      <div className="text-sm text-gray-600 mt-2">
        Wind {data.wind_speed} m/s · {windScaleText(data.wind_scale)}
      </div>

      {/* Updated */}
      <div className="text-xs text-gray-400 mt-1">
        Updated at {data.updated_at}
      </div>
    </div>
  );
}
