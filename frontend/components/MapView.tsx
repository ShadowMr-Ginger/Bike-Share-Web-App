"use client";

import { useEffect, useRef, useState } from "react";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { initStationLayer, setCurrentUser } from "@/lib/stations/useBikeStation";
import { useAuth } from "@/auth/AuthContext";
import SearchPanel from "./SearchPanel";

const walkIcon = L.icon({
  iconUrl: "/icons/walk.svg",
  iconSize: [36, 36],
  iconAnchor: [18, 36],
});

const bikeIcon = L.icon({
  iconUrl: "/icons/bike.svg",
  iconSize: [32, 32],
  iconAnchor: [16, 32],
});

const endflagIcon = L.icon({
  iconUrl: "/icons/endflag.svg",
  iconSize: [36, 36],
  iconAnchor: [18, 36],
});

export default function MapView() {
  const { user } = useAuth();
  const mapRef = useRef<L.Map | null>(null);
  const divRef = useRef<HTMLDivElement | null>(null);

  const [walkLayer, setWalkLayer] = useState<L.GeoJSON<any> | null>(null);
  const [bikeLayer, setBikeLayer] = useState<L.GeoJSON<any> | null>(null);

  // marker 图层，永远存在
  const markerLayerRef = useRef<L.LayerGroup | null>(null);

  useEffect(() => {
    if (!divRef.current || mapRef.current) return;

    mapRef.current = L.map(divRef.current).setView([53.3498, -6.2603], 13);

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: "© OpenStreetMap",
    }).addTo(mapRef.current);

    initStationLayer(mapRef.current, user);

    // 初始化 marker 图层
    markerLayerRef.current = L.layerGroup().addTo(mapRef.current);
  }, []);

  useEffect(() => {
    setCurrentUser(user);
  }, [user]);

  const drawRoute = (
    geojson: any | null,
    color = "#ff0000",
    type: "walk" | "bike" = "walk",
    markers?: { start?: [number, number]; bike?: [number, number]; end?: [number, number] }
  ) => {
    const map = mapRef.current;
    if (!map) return;

    // -------------------- 删除旧路线 --------------------
    if (type === "walk" && walkLayer) {
      map.removeLayer(walkLayer);
      setWalkLayer(null);
    }
    if (type === "bike" && bikeLayer) {
      map.removeLayer(bikeLayer);
      setBikeLayer(null);
    }

    if (!geojson) return;

    if (!geojson.features || geojson.features.length === 0) {
      console.warn("Invalid GeoJSON");
      return;
    }

    // -------------------- 绘制路线 --------------------
    const style =
      type === "walk"
        ? { color, weight: 4, dashArray: "8,10", opacity: 0.9, zIndex: 999 }
        : { color, weight: 5, opacity: 0.8, zIndex: 1 };

    const layer = L.geoJSON(geojson, { style }).addTo(map);
    if (type === "walk") setWalkLayer(layer);
    else setBikeLayer(layer);
    
    // -------------------- 绘制 marker --------------------
    /* 
    console.log(markers);
    console.log(markerLayerRef.current);
    if (markers && markerLayerRef.current) {
      console.log("3");
      const markerLayer = markerLayerRef.current;

      // 清空旧 marker（可选）
      markerLayer.clearLayers();
      console.log("Start:", markers.start);
      console.log("Bike:", markers.bike);
      console.log("End:", markers.end);

      if (markers.start) L.marker(markers.start, { icon: walkIcon }).addTo(markerLayer);
      if (markers.bike) L.marker(markers.bike, { icon: bikeIcon }).addTo(markerLayer);
      if (markers.end) L.marker(markers.end, { icon: endflagIcon }).addTo(markerLayer);
    }
    */

    // -------------------- fitBounds --------------------
    const bounds = layer.getBounds();
    if (bounds.isValid()) map.fitBounds(bounds, { padding: [50, 50] });
  };

  return (
    <>
      <SearchPanel drawRoute={drawRoute} />
      <div ref={divRef} className="w-full h-full" />
    </>
  );
}