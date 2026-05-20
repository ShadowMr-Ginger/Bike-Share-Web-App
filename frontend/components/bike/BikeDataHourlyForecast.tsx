"use client";

import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
} from "recharts";

interface HourlyData {
  time: string; // "14:00"
  bikes: number;
  stands: number;
}

interface BikeDataHourlyForecastProps {
  station: { id: number; name: string };
}

export default function BikeDataHourlyForecast({ station }: BikeDataHourlyForecastProps) {
  const [data, setData] = useState<HourlyData[]>([]);

  useEffect(() => {
    if (!station?.id) return;

    apiFetch(`/api/station/${station.id}/hourly-forecast`)
      .then(res => res.json())
      .then(data => setData(data))
      .catch(err => console.error(err));
  }, [station]);

  {/* 
  // 模拟后端返回预测数据
  useEffect(() => {
    const mockData: HourlyData[] = [];
    const now = new Date();
    for (let i = 1; i <= 10; i++) { // 接下来的 10 小时
      const d = new Date(now.getTime() + i * 60 * 60 * 1000);
      const hourStr = d.getHours().toString().padStart(2, "0") + ":00";
      mockData.push({
        time: hourStr,
        bikes: Math.floor(Math.random() * 20) + 5,  // 5~25 随机
        stands: Math.floor(Math.random() * 15) + 5, // 5~20 随机
      });
    }
    setData(mockData);
  }, []);
  */}

  return (
    <div className="bg-white/90 backdrop-blur rounded-2xl shadow-xl p-4">
      <h2 className="font-bold text-lg mb-2">Hourly Forecast (Next 10h)</h2>
      <div className="w-full h-36">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart
            data={data}
            margin={{ top: 20, right: 20, bottom: 0, left: -30 }}
          >
            <CartesianGrid stroke="#eee" strokeDasharray="3 3" />
            <XAxis
              dataKey="time"
              tick={{ fontSize: 12 }}
              tickLine={false}
              axisLine={{ stroke: "#ccc" }}
            />
            <YAxis
              tick={{ fontSize: 12 }}
              tickLine={false}
              axisLine={{ stroke: "#ccc" }}
              allowDecimals={false}
            />
            <Tooltip />
            <Line
              type="monotone"
              dataKey="bikes"
              stroke="#ff4d4f"  // 红色
              strokeWidth={2}
              dot={{ r: 3 }}
              activeDot={{ r: 5 }}
            />
            <Line
              type="monotone"
              dataKey="stands"
              stroke="#1890ff"  // 蓝色
              strokeWidth={2}
              dot={{ r: 3 }}
              activeDot={{ r: 5 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}