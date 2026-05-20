"use client";
import { useState } from "react";
import { useAuth } from "@/auth/AuthContext";
import { apiFetch } from "@/lib/api";

interface Props {
  onClose: () => void;
  openSignup: () => void;
}

export default function LoginModal({ onClose, openSignup }: Props) {
  const { login } = useAuth();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [remember, setRemember] = useState(true);

  async function handleLogin() {
    const res = await apiFetch("/api/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });

    if (!res.ok) {
      alert("Login failed");
      return;
    }

    const data = await res.json();
    login(data, remember);
    onClose();
  }

  return (
    <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-[7000]">
      <div className="bg-white rounded-2xl p-6 w-80 shadow-xl">
        <h2 className="text-xl font-semibold mb-4">Login</h2>

        <input
          className="w-full border rounded-lg p-2 mb-3"
          placeholder="Username"
          value={username}
          onChange={e => setUsername(e.target.value)}
        />

        <input
          type="password"
          className="w-full border rounded-lg p-2 mb-3"
          placeholder="Password"
          value={password}
          onChange={e => setPassword(e.target.value)}
        />

        <label className="flex items-center gap-2 mb-3 text-sm">
          <input
            type="checkbox"
            checked={remember}
            onChange={e => setRemember(e.target.checked)}
          />
          Remember me
        </label>

        <button
          onClick={handleLogin}
          className="w-full bg-green-500 text-white rounded-lg py-2 mb-2"
        >
          Login
        </button>

        {/* 切换到注册 */}
        <button
          className="text-sm text-blue-600 w-full hover:underline"
          onClick={() => {
            onClose();
            openSignup();
          }}
        >
          Don't have an account? Sign Up
        </button>

        <button onClick={onClose} className="mt-2 text-sm w-full">
          Cancel
        </button>
      </div>
    </div>
  );
}
