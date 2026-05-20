"use client";
import { useAuth } from "@/auth/AuthContext";
import LoginModal from "@/auth/LoginModal";
import SignUpModal from "@/auth/SignUpModal";
import UserMenu from "@/auth/UserMenu";
import ProfileModal from "@/auth/ProfileModal";
import { useState, useEffect } from "react";

export default function Header() {
  const { user } = useAuth();

  // 弹窗状态
  const [loginOpen, setLoginOpen] = useState(false);

  useEffect(() => {
    const handler = () => setLoginOpen(true);
    window.addEventListener("open-login-modal", handler);
    return () => window.removeEventListener("open-login-modal", handler);
  }, []);
  const [signupOpen, setSignupOpen] = useState(false);
  const [profileOpen, setProfileOpen] = useState(false);

  return (
    <>
      <div className="absolute top-5 right-6 z-[6000]">
        {!user ? (
          <button
            onClick={() => setLoginOpen(true)}
            className="bg-white shadow-lg rounded-xl px-4 py-2 font-medium hover:bg-gray-100"
          >
            Login
          </button>
        ) : (
          <UserMenu openProfile={() => setProfileOpen(true)} />
        )}
      </div>

      {/* Login Modal */}
      {loginOpen && (
        <LoginModal
          onClose={() => setLoginOpen(false)}
          openSignup={() => {
            setLoginOpen(false);
            setSignupOpen(true);
          }}
        />
      )}

      {/* Sign Up Modal */}
      {signupOpen && (
        <SignUpModal
          onClose={() => setSignupOpen(false)}
          openLogin={() => {
            setSignupOpen(false);
            setLoginOpen(true);
          }}
        />
      )}

      {/* Profile Modal */}
      {profileOpen && (
        <ProfileModal
          onClose={() => setProfileOpen(false)}
        />
      )}
    </>
  );
}
