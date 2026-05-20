import ClientMap from "@/components/ClientMap";
import SearchPanel from "@/components/SearchPanel";
import WeatherToggle from "@/components/weather/WeatherToggle";
import Header from "@/components/layout/Header";
import BikePanel from "@/components/bike/BikePanel";

export default function Home() {
  return (
    <div className="relative w-full h-full">

      {/* 地图底层 */}
      <ClientMap />

      {/* UI层（关键） */}
      <div className="absolute inset-0 z-[5000] pointer-events-none">

        {/*
        <div className="pointer-events-auto">
          <SearchPanel />
        </div>
         */}

        <div className="pointer-events-auto">
          <WeatherToggle />
        </div>

        <div className="pointer-events-auto">
          <Header />
        </div>

        <div className="pointer-events-auto">
          <BikePanel/>  
        </div>

      </div>
    </div>
  );
}
