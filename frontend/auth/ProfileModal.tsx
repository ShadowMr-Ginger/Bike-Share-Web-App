"use client";

import { useState, useEffect, useRef } from "react";
import { useAuth } from "./AuthContext";
import { apiFetch, getMediaUrl, assetUrl } from "@/lib/api";
import type { Station } from "../src/types/station";

interface Props {
  onClose: () => void;
  refocusStation?: (stationId: number) => void; // ⭐ 改为可选
}

export default function ProfileModal({ onClose, refocusStation }: Props) {
  const { user, updateUser } = useAuth();

  if (!user) return null;

  const [avatar, setAvatar] = useState(user.avatar || "");
  const [favorites, setFavorites] = useState<Station[]>([]);
  const [loading, setLoading] = useState(true);
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  // 获取收藏站点
  useEffect(() => {
    if (!user) return;

    const fetchFavorites = async () => {
      setLoading(true);
      try {
        const res = await apiFetch(
          `/api/user/${user.email}/favorites`
        );
        const data = await res.json();
        setFavorites(data.favorites || []);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchFavorites();
  }, [user]);

  // 上传头像
  const handleAvatarChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!user) return;
    const file = e.target.files?.[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("avatar", file);

    try {
      const res = await apiFetch(
        `/api/user/${user.id}/avatar`,
        {
          method: "POST",
          headers: { Authorization: `Bearer ${user.token}` },
          body: formData,
        }
      );
      const data = await res.json();
      if (res.ok) {
        const avatarPath = data.avatar as string;
        const fullUrl = `${getMediaUrl(avatarPath)}?t=${Date.now()}`;
        setAvatar(fullUrl);
        updateUser({ ...user, avatar: avatarPath });
      } else {
        alert(data.message || "Failed to upload avatar");
      }
    } catch (err) {
      console.error(err);
    }
  };

  const handleUploadClick = () => {
    fileInputRef.current?.click();
  };

  // 收藏/取消收藏
  const toggleFavorite = async (station: Station) => {
    if (!user) return;

    const exists = favorites.some(f => f.number === station.number);
    const url = `/api/user/${user.email}/favorites/${station.number}`;

    try {
      const res = await apiFetch(url, {
        method: exists ? "DELETE" : "POST",
      });

      if (!res.ok) throw new Error("Failed to update favorite");

      setFavorites(prev =>
        exists
          ? prev.filter(f => f.number !== station.number)
          : [...prev, station]
      );
    } catch (err) {
      console.error(err);
    }
  };

  // 点击车站名
  const handleJumpToStation = (station: Station) => {
    console.log("1");
    if (!refocusStation) return; // ⭐ 没提供就什么都不做
    console.log("2");
    refocusStation(station.number);
  };

  return (
    <div
      className="fixed inset-0 z-[8000] flex items-center justify-center bg-black/40"
      onClick={onClose}
    >
      <div
        className="w-[400px] max-h-[90vh] overflow-y-auto rounded-2xl bg-white p-6 shadow-xl relative"
        onClick={(e) => e.stopPropagation()}
      >
        <button
          onClick={onClose}
          className="absolute right-4 top-3 text-gray-400 hover:text-black text-xl"
        >
          ✕
        </button>

        <h2 className="text-2xl font-semibold mb-4 text-center">Profile</h2>

        {/* Avatar */}
        <div className="flex flex-col items-center mb-6">
          <img
            src={avatar ? getMediaUrl(avatar) : assetUrl("/file.svg")}
            alt="avatar"
            className="w-24 h-24 rounded-full object-cover mb-2"
          />
          <button
            onClick={handleUploadClick}
            className="mt-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
          >
            Upload Avatar
          </button>
          <input
            ref={fileInputRef}
            type="file"
            className="hidden"
            onChange={handleAvatarChange}
          />
        </div>

        {/* Favorites */}
        <h3 className="text-lg font-semibold mb-2">Favorite Stations</h3>
        {loading ? (
          <p>Loading...</p>
        ) : favorites.length === 0 ? (
          <p className="text-sm text-gray-500">No favorite stations yet.</p>
        ) : (
          <ul className="space-y-2 max-h-64 overflow-y-auto">
            {favorites.map(station => (
              <li
                key={station.number}
                className="flex justify-between items-center p-2 border rounded-lg"
              >
                <span
                  onClick={() => handleJumpToStation(station)}
                  className={`cursor-pointer ${refocusStation
                      ? "text-blue-600 hover:underline"
                      : "text-gray-400 cursor-default"
                    }`}
                >
                  {station.name}
                </span>
                <button
                  onClick={() => toggleFavorite(station)}
                  className="text-sm text-red-500 hover:underline"
                >
                  Remove
                </button>
              </li>
            ))}
          </ul>
        )}

        <p className="mt-4 text-sm text-gray-400 text-center">
          Click a station name to jump to the map marker.
        </p>
      </div>
    </div>
  );
}
