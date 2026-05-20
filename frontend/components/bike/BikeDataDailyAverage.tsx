"use client";

import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
} from "recharts";

interface DailyData {
  weekday: string; // "Mon" ~ "Sun"
  bikes: number;
  stands: number;
}

interface BikeDataDailyAverageProps {
  station: { id: number; name: string };
}

export default function BikeDataDailyAverage({ station }: BikeDataDailyAverageProps) {
  const [data, setData] = useState<DailyData[]>([]);
  const [today, setToday] = useState<string>("");

  useEffect(() => {
    if (!station?.id) return;

    // 根据 station.id 动态请求
    apiFetch(`/api/station/${station.id}/daily-average`)
      .then(res => res.json())
      .then(data => setData(data))
      .catch(err => console.error(err));

    const weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
    const todayIndex = new Date().getDay(); // 0=Sunday, 1=Monday
    const todayStr = weekdays[(todayIndex + 6) % 7]; // 转成 Mon=0 ... Sun=6
    setToday(todayStr);
  }, [station]);

  {/* 
  // 模拟后端返回数据
  useEffect(() => {
    const weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
    const todayIndex = new Date().getDay(); // 0=Sunday, 1=Monday
    const todayStr = weekdays[(todayIndex + 6) % 7]; // 转换成 Mon=0 ~ Sun=6
    setToday(todayStr);

    const mockData: DailyData[] = weekdays.map((d) => ({
      weekday: d,
      bikes: Math.floor(Math.random() * 20) + 5,
      stands: Math.floor(Math.random() * 15) + 5,
    }));

    setData(mockData);
  }, []);
  */}
  return (
    <div className="bg-white/90 backdrop-blur rounded-2xl shadow-xl p-4">
      <h2 className="font-bold text-lg mb-2">Daily Average</h2>
      <div className="w-full h-40">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={data}
            margin={{ top: 20, right: 20, bottom: 0, left: -30 }}
          >
            <CartesianGrid stroke="#eee" strokeDasharray="3 3" />
            <XAxis
              dataKey="weekday"
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

            <Bar
              dataKey="bikes"
              fill="#ffcccc" // 淡红色
              radius={[4, 4, 0, 0]}
              // 高亮今天
              shape={(props) => {
                const { x, y, width, height, payload } = props;
                const isToday = payload.weekday === today;
                return (
                  <rect
                    x={x}
                    y={y}
                    width={width}
                    height={height}
                    fill={isToday ? "#ff4d4f" : "#ffcccc"}
                    rx={4}
                    ry={4}
                  />
                );
              }}
            />
            <Bar
              dataKey="stands"
              fill="#cce5ff" // 淡蓝色
              radius={[4, 4, 0, 0]}
              shape={(props) => {
                const { x, y, width, height, payload } = props;
                const isToday = payload.weekday === today;
                return (
                  <rect
                    x={x}
                    y={y}
                    width={width}
                    height={height}
                    fill={isToday ? "#1890ff" : "#cce5ff"}
                    rx={4}
                    ry={4}
                  />
                );
              }}
            />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}