"use client";

import { useEffect, useState } from "react";
import BikeDataHistory from "./BikeDataHistory";
import BikeDataHourlyForecast from "./BikeDataHourlyForecast";
import BikeDataDailyAverage from "./BikeDataDailyAverage";

interface Station {
  id: number;
  name: string;
}

interface StationStatus {
  bikes: number;
  stands: number;
}

export default function BikePanel() {
  const [station, setStation] = useState<Station | null>(null);
  const [status, setStatus] = useState<StationStatus | null>(null);

  // 接收地图事件
  useEffect(() => {
    const selected = (e: any) => {
      setStation(e.detail.station);
      setStatus(e.detail.status);
    };
    const cleared = () => {
      setStation(null);
      setStatus(null);
    };
    window.addEventListener("bike-station-selected", selected);
    window.addEventListener("bike-station-cleared", cleared);
    return () => {
      window.removeEventListener("bike-station-selected", selected);
      window.removeEventListener("bike-station-cleared", cleared);
    };
  }, []);

  if (!station || !status) return null;

  return (
    <div
      className="
        fixed                /* 固定在屏幕上 */
        right-4              /* 离右边 1rem */
        top-1/2              /* 垂直居中 */
        -translate-y-1/2     /* 调整为真正垂直居中 */
        z-[6000]             /* 保持在最上层 */
        flex
        flex-col
        gap-4
        w-[420px]
      "
    >
      <BikeDataHistory station={station} status={status} />
      <BikeDataHourlyForecast station={station} />
      <BikeDataDailyAverage station={station} />
    </div>
  );
}