"use client";

import { useAuth } from "@/auth/AuthContext";
import { getMediaUrl, assetUrl } from "@/lib/api";
import { useEffect, useRef, useState } from "react";

interface Props {
  openProfile: () => void; // 父组件传入函数用于打开 ProfileModal
}

export default function UserMenu({ openProfile }: Props) {
  const { user, logout } = useAuth();
  const [menuOpen, setMenuOpen] = useState(false);
  const ref = useRef<HTMLDivElement | null>(null);

  // 点击外部关闭菜单
  useEffect(() => {
    function handleClickOutside(e: MouseEvent) {
      if (!ref.current) return;
      if (!ref.current.contains(e.target as Node)) {
        setMenuOpen(false);
      }
    }

    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  if (!user) return null;

  return (
    <div className="relative" ref={ref}>
      {/* 头像按钮 */}
      <button
        onClick={() => setMenuOpen(v => !v)}
        className="w-10 h-10 rounded-full overflow-hidden shadow-md border bg-white"
      >
        <img
          src={user.avatar ? getMediaUrl(user.avatar) : assetUrl("/file.svg")}
          alt="avatar"
          className="w-full h-full object-cover"
        />
      </button>

      {/* 下拉菜单 */}
      {menuOpen && (
        <div className="absolute right-0 mt-2 w-40 bg-white rounded-xl shadow-xl border overflow-hidden z-[2000]">
          <button
            onClick={() => {
              setMenuOpen(false);
              openProfile();
            }}
            className="w-full text-left px-4 py-2 hover:bg-gray-100"
          >
            Profile
          </button>

          <button
            onClick={() => {
              logout();
              setMenuOpen(false);
            }}
            className="w-full text-left px-4 py-2 hover:bg-gray-100 text-red-500"
          >
            Log out
          </button>
        </div>
      )}
    </div>
  );
}
