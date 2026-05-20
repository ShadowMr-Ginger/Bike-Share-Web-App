"use client";

import { useRef, useState, useEffect } from "react";
import WeatherNow from "./WeatherNow";
import WeatherHourly from "./WeatherHourly";
import WeatherWeekly from "./WeatherWeekly";

export default function WeatherPanel() {

  const panelRef = useRef<HTMLDivElement | null>(null);

  const [position, setPosition] = useState({ x: 100, y: 100 });
  const dragging = useRef(false);
  const offset = useRef({ x: 0, y: 0 });

  useEffect(() => {
    const panel = panelRef.current;
    if (!panel) return;
    const handlePointerDown = (e: PointerEvent) => {
      dragging.current = true;

      offset.current = {
        x: e.clientX - position.x,
        y: e.clientY - position.y,
      };

      panel.setPointerCapture(e.pointerId);
    };

    const handlePointerMove = (e: PointerEvent) => {
      if (!dragging.current) return;

      setPosition({
        x: e.clientX - offset.current.x,
        y: e.clientY - offset.current.y,
      });
    };

    const handlePointerUp = () => {
      dragging.current = false;
    };

    panel.addEventListener("pointerdown", handlePointerDown);
    panel.addEventListener("pointermove", handlePointerMove);
    panel.addEventListener("pointerup", handlePointerUp);

    return () => {
      panel.removeEventListener("pointerdown", handlePointerDown);
      panel.removeEventListener("pointermove", handlePointerMove);
      panel.removeEventListener("pointerup", handlePointerUp);
    };
  }, [position]);

  return (
    <div
      ref={panelRef}
      style={{
        transform: `translate(${position.x}px, ${position.y}px)`,
      }}
      className="
        absolute
        z-[999]
        flex flex-col gap-3
        w-[320px]
        max-w-[85vw]
        cursor-grab
        active:cursor-grabbing
      "
    >
      <WeatherNow />
      <WeatherHourly />
      <WeatherWeekly />
    </div>
  );
}
