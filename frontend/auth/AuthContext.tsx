"use client";
import { createContext, useContext, useState, useEffect } from "react";

export interface User {
  id: string;
  email: string;
  avatar?: string;
  token: string;
}

interface AuthContextType {
  user: User | null;
  login: (user: User, remember: boolean) => void;
  logout: () => void;
  updateUser: (updates: Partial<User>) => void; // 新增
}

const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);

  // 页面刷新恢复登录
  useEffect(() => {
    const saved = localStorage.getItem("session");
    if (saved) setUser(JSON.parse(saved));
  }, []);

  const login = (userData: User, remember: boolean) => {
    setUser(userData);
    if (remember) localStorage.setItem("session", JSON.stringify(userData));
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem("session");
  };

  // 新增 updateUser：用于更新头像、用户名等
  const updateUser = (updates: Partial<User>) => {
    setUser((prev) => {
      if (!prev) return null;
      const updated = { ...prev, ...updates };
      localStorage.setItem("session", JSON.stringify(updated));
      return updated;
    });
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, updateUser }}>
      {children}
    </AuthContext.Provider>
  );
}

// 自定义 Hook
export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("AuthProvider missing");
  return ctx;
}
