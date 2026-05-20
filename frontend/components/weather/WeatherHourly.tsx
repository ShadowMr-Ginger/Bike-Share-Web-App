"use client";

import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";
import { mapWeatherCode, weatherIcon } from "@/lib/weatherUtils";

export default function WeatherHourly() {

  const [data, setData] = useState<any[]>([]);

  useEffect(() => {
    apiFetch("/api/weather/hourly")
      .then(res => res.json())
      .then(res => {

        const formatted = res.hourly.map((h: any) => {
          const date = new Date(h.time);
          return {
            t: date.getHours().toString().padStart(2, "0"),
            temp: Math.round(h.temperature),
            icon: weatherIcon(mapWeatherCode(h.weathercode))
          };
        });

        setData(formatted);
      })
      .catch(err => console.error(err));
  }, []);

  if (!data.length) {
    return (
      <div className="bg-white/90 rounded-2xl shadow-lg p-4">
        Loading hourly weather...
      </div>
    );
  }

  const temps = data.map(d => d.temp);
  const rawMax = Math.max(...temps);
  const rawMin = Math.min(...temps);

  // 上下缓冲区（避免贴边）
  const displayMax = rawMax + 2;
  const displayMin = rawMin - 2;
  const range = displayMax - displayMin;

  const height = 120;
  const widthPerItem = 60;
  const totalWidth = data.length * widthPerItem;

  const paddingTop = 15;
  const paddingBottom = 15;

  // 生成平滑曲线（Bezier）
  const points = data.map((d, i) => {
    const x = i * widthPerItem + widthPerItem / 2;
    const ratio = (d.temp - displayMin) / range;
    const y =
      paddingTop +
      (height - paddingTop - paddingBottom) * (1 - ratio);
    return { x, y };
  });

  const smoothPath = points.reduce((acc, point, i, arr) => {
    if (i === 0) {
      return `M ${point.x} ${point.y}`;
    }
    const prev = arr[i - 1];
    const cx = (prev.x + point.x) / 2;
    return acc + ` Q ${prev.x} ${prev.y}, ${cx} ${(prev.y + point.y) / 2}`;
  }, "");

  return (
    <div className="bg-white/90 backdrop-blur-md rounded-2xl shadow-lg p-4">

      <div className="mb-3">
        <h3 className="font-semibold">Next 24 Hours</h3>
      </div>

      <div className="overflow-x-auto pb-2">
        <div style={{ width: totalWidth }}>

          {/* 图表区域 */}
          <svg width={totalWidth} height={height} className="mb-3">

            {/* 黑色背景 */}
            <rect
              x="0"
              y="0"
              width={totalWidth}
              height={height}
              rx="16"
              fill="#0f172a"
            />

            {/* 网格线 + 温度刻度 */}
            {[0, 0.25, 0.5, 0.75, 1].map((ratio, i) => {
              const y =
                paddingTop +
                (height - paddingTop - paddingBottom) * ratio;

              const tempValue =
                Math.round(displayMax - ratio * range);

              return (
                <g key={i}>
                  {/* 网格线 */}
                  <line
                    x1="40"
                    x2={totalWidth}
                    y1={y}
                    y2={y}
                    stroke="#334155"
                    strokeWidth="1"
                  />

                  {/* 左侧温度文字 */}
                  <text
                    x="35"
                    y={y + 4}
                    textAnchor="end"
                    fill="#94a3b8"
                    fontSize="10"
                  >
                    {tempValue}°
                  </text>
                </g>
              );
            })}

            {/* 平滑曲线 */}
            <path
              d={smoothPath}
              fill="none"
              stroke="#38bdf8"
              strokeWidth="3"
              strokeLinecap="round"
            />

          </svg>


          {/* 小时数据 */}
          <div className="flex">
            {data.map((d, i) => (
              <div
                key={i}
                className="flex flex-col items-center text-xs"
                style={{ width: widthPerItem }}
              >
                <div>{d.temp}°</div>
                <div className="text-lg">{d.icon}</div>
                <div className="text-gray-500">{d.t}</div>
              </div>
            ))}
          </div>

        </div>
      </div>
    </div>
  );
}
