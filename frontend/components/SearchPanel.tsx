"use client";

import { useState } from "react";
import { apiFetch } from "@/lib/api";

interface SearchPanelProps {
  drawRoute: (
    geojson: any | null,
    color?: string,
    type?: "walk" | "bike",
    markers?: { start?: [number, number]; bike?: [number, number]; end?: [number, number] }
  ) => void;
}

export default function SearchPanel({ drawRoute }: SearchPanelProps) {

  const [from, setFrom] = useState("D02 X285");
  const [to, setTo] = useState("The Spire of Dublin");
  const [loading, setLoading] = useState(false);

  const ready =
    from.trim().length > 0 &&
    to.trim().length > 0;

  // ✅ GeoJSON 安全检查
  const validGeoJSON = (geo: any) => {
    return (
      geo &&
      geo.features &&
      geo.features.length > 0 &&
      geo.features[0].geometry &&
      geo.features[0].geometry.coordinates &&
      geo.features[0].geometry.coordinates.length > 0
    );
  };

  const handleDirect = async () => {

    if (!ready || loading) return;

    try {

      setLoading(true);

      const res = await apiFetch(
        "/api/route",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            from,
            to,
          }),
        }
      );

      const data = await res.json();

      if (!res.ok) {
        throw new Error(
          data.message || "Routing failed"
        );
      }

      console.log("Route API:", data);

      // ✅ 清除旧路线
      drawRoute(null);

      // ----------------------------
      // Segment 1 Bike Station → 终点
      // ----------------------------

      if (validGeoJSON(data?.segments?.[1])) {

        drawRoute(data.segments[1], "#0000ff", "bike", {
          bike: [data.segments[0].bbox[1], data.segments[0].bbox[0]],
          end: [data.segments[0].bbox[0], data.segments[0].bbox[1]],
        });
      } else {
        console.warn(
          "Segment 1 invalid GeoJSON"
        );
      }
      // ----------------------------
      // Segment 0 起点 → Bike Station
      // ----------------------------

      if (validGeoJSON(data?.segments?.[0])) {

        drawRoute(data.segments[0], "#ff0000", "walk", {
          start: [data.segments[0].bbox[0], data.segments[0].bbox[1]],
          bike: [data.segments[0].bbox[0], data.segments[0].bbox[1]],
        });
      } else {
        console.warn(
          "Segment 0 invalid GeoJSON"
        );
      }


    } catch (err: any) {

      console.error(err);

      alert(
        err.message ||
        "Route request failed"
      );

    } finally {

      setLoading(false);
    }
  };

  return (

    <div className="absolute top-8 left-1/2 -translate-x-1/2 w-[90%] max-w-xl z-[1000]">

      <div className="bg-white/95 backdrop-blur-lg shadow-xl rounded-3xl p-5 space-y-4">

        {/* FROM */}

        <div className="flex gap-3">

          <input
            type="text"
            placeholder="From (Eircode or address)"
            value={from}
            onChange={(e) =>
              setFrom(e.target.value)
            }
            className="
            flex-1 px-4 py-3
            rounded-xl border border-gray-300
            focus:outline-none
            focus:ring-2 focus:ring-blue-400
            "
          />

        </div>

        {/* TO */}

        <div className="flex gap-3">

          <input
            type="text"
            placeholder="To (Eircode or address)"
            value={to}
            onChange={(e) =>
              setTo(e.target.value)
            }
            className="
            flex-1 px-4 py-3
            rounded-xl border border-gray-300
            focus:outline-none
            focus:ring-2 focus:ring-green-400
            "
          />

          <button

            onClick={handleDirect}

            disabled={!ready || loading}

            className={`
              px-5 rounded-xl font-medium transition

              ${ready && !loading
                ? "bg-green-500 text-white hover:bg-green-600 active:scale-95"
                : "bg-gray-300 text-gray-500 cursor-not-allowed"
              }
            `}

          >

            {loading
              ? "Loading..."
              : "Direct"}

          </button>

        </div>

      </div>

    </div>
  );
}