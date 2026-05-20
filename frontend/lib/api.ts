/* ================================================================
   API Base URL & Fetch Helper
   ---------------------------------------------------------------
   - NEXT_PUBLIC_API_BASE 会在 build 时被内联到代码中。
   - 开发时可在 .env.local 里设为 http://127.0.0.1:5000
   - 生产 build 前设为实际后端域名，例如：
     NEXT_PUBLIC_API_BASE=https://bike-api.yourdomain.com
   ================================================================ */

export const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "";

export function apiUrl(path: string): string {
  if (path.startsWith("http")) return path;
  const cleanPath = path.startsWith("/") ? path : `/${path}`;
  return API_BASE ? `${API_BASE}${cleanPath}` : cleanPath;
}

export function apiFetch(path: string, init?: RequestInit) {
  return fetch(apiUrl(path), init);
}

/* 头像 / 静态资源拼接后端域名 */
export function getMediaUrl(path: string): string {
  if (!path) return "";
  if (path.startsWith("http")) return path;
  const cleanPath = path.startsWith("/") ? path : `/${path}`;
  return API_BASE ? `${API_BASE}${cleanPath}` : cleanPath;
}

/* 前端本地静态资源（public 文件夹）拼接 basePath */
const BASE_PATH = process.env.NEXT_PUBLIC_BASE_PATH || "";

export function assetUrl(path: string): string {
  if (path.startsWith("http")) return path;
  const cleanPath = path.startsWith("/") ? path : `/${path}`;
  return BASE_PATH ? `${BASE_PATH}${cleanPath}` : cleanPath;
}

/* 兼容旧代码的 stations fetch */
export async function fetchStations() {
  const res = await apiFetch("/api/stations");
  if (!res.ok) throw new Error("failed to load stations");
  return res.json();
}
