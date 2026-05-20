import L from "leaflet";
import { User } from "@/auth/AuthContext";
import { apiFetch } from "@/lib/api";

/* ========= 类型 ========= */

export interface Station {
  id: number;
  name: string;
  lat: number;
  lng: number;
}

export interface StationStatus {
  id: number;
  bikes: number;
  stands: number;
  updated: number;
}

/* ========= 内部缓存 ========= */
const markers = new Map<number, L.Marker>();
const stations = new Map<number, Station>();
const lastStatusMap = new Map<number, StationStatus>();
let initialized = false;
let favoriteSet = new Set<number>();
let currentUser: User | null = null;

export async function setCurrentUser(user: User | null) {
  currentUser = user;
  if (user) {
    await loadFavorites(user);
  } else {
    favoriteSet = new Set<number>();
  }
  // Refresh all marker icons to reflect new login state
  for (const [id, marker] of markers) {
    const status = lastStatusMap.get(id);
    const station = stations.get(id);
    if (!status || !station) continue;
    const isFav = favoriteSet.has(id);
    marker.setIcon(getIcon(status.bikes, status.stands, isFav));
    marker.setPopupContent(buildPopup(station, status, isFav));
  }
}

/* ========= 图标 ========= */
function getIcon(bikes: number, stands: number, favorited: boolean) {
  let color = "gray";
  if (bikes === 0) color = "red";
  else if (stands === 0) color = "orange";
  else color = "green";

  let color_margin = "white";
  if (favorited) color_margin = "yellow";

  return L.divIcon({
    className: "bike-marker",
    html: `<div style="
      width:18px;
      height:18px;
      border-radius:50%;
      background:${color};
      border:2px solid ${color_margin};
      box-shadow:0 0 4px rgba(0,0,0,0.5);
    "></div>`,
    iconSize: [18, 18],
    iconAnchor: [9, 9],
  });
}

/* ========= Popup HTML ========= */
function buildPopup(
  station: Station,
  status: StationStatus,
  favorited: boolean,
) {
  const time = new Date(status.updated).toLocaleTimeString();
  const btnText = favorited ? "★ Remove Favorite" : "☆ Add Favorite";

  return `
    <div class="popup-root" data-station="${station.id}" style="font-size:14px">
      <b>${station.name}</b><br/>
      🚲 Bikes: <b>${status.bikes}</b><br/>
      🅿️ Stands: <b>${status.stands}</b><br/>
      <span style="color:gray;font-size:12px">Updated: ${time}</span><br/>
      <button 
        class="fav-btn" 
        data-id="${station.id}"
        style="
          margin-top:6px;
          padding:4px 8px;
          font-size:12px;
          border-radius:6px;
          border:1px solid #ccc;
          background:white;
          cursor:pointer
        ">
        ${btnText}
      </button>
    </div>
  `;
}

/* ========= API ========= */
async function loadFavorites(user: User) {
  const res = await apiFetch(
    `/api/user/${user.email}/favorites`,
  );
  const data = await res.json();
  favoriteSet = new Set<number>(
    (data.favorites || []).map((f: any) => f.number),
  );
}

async function toggleFavorite(
  user: User,
  stationId: number,
  currentlyFav: boolean,
) {
  const url = `/api/user/${user.email}/favorites/${stationId}`;
  const method = currentlyFav ? "DELETE" : "POST";

  const res = await apiFetch(url, { method });

  if (!res.ok) return currentlyFav;

  if (currentlyFav) favoriteSet.delete(stationId);
  else favoriteSet.add(stationId);

  return !currentlyFav;
}

/* ========= 加载站点 ========= */
async function loadStations(map: L.Map, user: User | null) {
  const res = await apiFetch("/api/stations");
  const data: Station[] = await res.json();

  if (user) await loadFavorites(user);

  data.forEach((station) => {
    stations.set(station.id, station);
    const marker = L.marker([station.lat, station.lng], {
      icon: getIcon(0, 0, false),
    }).addTo(map);
    marker.bindPopup("Loading...");

    marker.on("popupopen", async (e) => {
      const status = lastStatusMap.get(station.id);
      if (!status) return;

      const isFav = favoriteSet.has(station.id);
      marker.setPopupContent(buildPopup(station, status, isFav));

      const popupEl = e.popup.getElement();
      if (!popupEl) return;

      L.DomEvent.disableClickPropagation(popupEl);

      // ⭐⭐ 通知 React UI 有站点被点击
      window.dispatchEvent(
        new CustomEvent("bike-station-selected", {
          detail: {
            station,
            status,
          },
        }),
      );
      marker.on("popupclose", () => {
        window.dispatchEvent(new CustomEvent("bike-station-cleared"));
      });

      // ⭐ 事件委托：popup内的按钮点击
      popupEl.onclick = async (ev) => {
        const target = ev.target as HTMLElement;
        if (!target.classList.contains("fav-btn")) return;
        if (!currentUser) {
          window.dispatchEvent(new CustomEvent("open-login-modal"));
          return;
        }

        ev.preventDefault();
        ev.stopPropagation();

        const id = Number(target.dataset.id);
        const current = favoriteSet.has(id);

        const newFav = await toggleFavorite(currentUser, id, current);

        const s = lastStatusMap.get(id);
        const st = stations.get(id);
        if (!s || !st) return;

        marker.setPopupContent(buildPopup(st, s, newFav));
      };
    });

    markers.set(station.id, marker);
  });
}

/* ========= 更新状态 ========= */
async function updateStatus(user: User | null) {
  const res = await apiFetch("/api/stations");
  const statusList: StationStatus[] = await res.json();

  statusList.forEach((status) => lastStatusMap.set(status.id, status));

  for (const status of statusList) {
    const marker = markers.get(status.id);
    const station = stations.get(status.id);
    if (!marker || !station) continue;

    const isFav = favoriteSet.has(status.id);
    marker.setIcon(getIcon(status.bikes, status.stands, isFav));
    marker.setPopupContent(buildPopup(station, status, isFav));
  }
}

/* ========= 对外入口 ========= */
export async function initStationLayer(map: L.Map, user: User | null) {
  if (initialized) return;
  initialized = true;

  await loadStations(map, user);
  await updateStatus(user);
  setInterval(() => updateStatus(user), 30000);
}
