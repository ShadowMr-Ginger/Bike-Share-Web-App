export function weatherText(code: string) {
  switch (code) {
    case "clear": return "Clear";
    case "cloud": return "Cloudy";
    case "partly_cloudy": return "Partly Cloudy";
    case "light_rain": return "Light Rain";
    case "rain": return "Moderate Rain";
    case "heavy_rain": return "Heavy Rain";
    case "snow": return "Snow";
    case "fog": return "Fog";
    default: return "Unknown";
  }
}

export function weatherIcon(code: string) {
  switch (code) {
    case "clear": return "☀️";
    case "cloud": return "☁️";
    case "partly_cloudy": return "⛅";
    case "light_rain": return "🌦️";
    case "rain": return "🌧️";
    case "heavy_rain": return "⛈️";
    case "snow": return "❄️";
    case "fog": return "🌫️";
    default: return "❓";
  }
}

export function mapWeatherCode(code: number): string {
  if (code === 0) return "clear";

  if (code >= 1 && code <= 3) return "partly_cloudy";

  if (code >= 45 && code <= 48) return "fog";

  if (code >= 51 && code <= 57) return "light_rain";

  if (code >= 61 && code <= 65) return "rain";

  if (code >= 66 && code <= 67) return "heavy_rain";

  if (code >= 71 && code <= 77) return "snow";

  if (code >= 80 && code <= 82) return "rain";

  if (code >= 95) return "heavy_rain";

  return "cloud";
}

/* Beaufort scale description */
export function windScaleText(scale: number) {
  const desc = [
    "Calm",
    "Light air",
    "Light breeze",
    "Gentle breeze",
    "Moderate breeze",
    "Fresh breeze",
    "Strong breeze",
    "Near gale",
    "Gale",
    "Severe gale",
    "Storm",
    "Violent storm",
    "Hurricane"
  ];

  return `Bft ${scale} · ${desc[scale] ?? ""}`;
}