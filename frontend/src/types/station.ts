export interface Station {
  number: number;
  name: string;
  address: string;

  position: {
    lat: number;
    lng: number;
  };
}

export interface StationStatus {
  number: number;
  available_bikes: number;
  available_bike_stands: number;
  last_update: number;
}
