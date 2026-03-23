import React from "react";
import { NavLink, useNavigate } from "react-router-dom";
import {
  LayoutDashboard,
  CircleHelp,
  MessageSquareText,
  BadgeCheck,
  FileBarChart2,
  Layers,
  LogOut,
  Sparkles,
  User,
} from "lucide-react";
import { useAppState } from "../context/AppStateContext";

const navItems = [
  { to: "/dashboard", label: "Dashboard", icon: <LayoutDashboard size={20} /> },
  { to: "/quiz", label: "Quiz", icon: <CircleHelp size={20} /> },
  { to: "/exam", label: "Exam Mode", icon: <BadgeCheck size={20} /> },
  { to: "/chat", label: "AI Chat", icon: <MessageSquareText size={20} /> },
  { to: "/report", label: "Report", icon: <FileBarChart2 size={20} /> },
  { to: "/flashcards", label: "Flashcards", icon: <Layers size={20} /> },
  { to: "/profile", label: "Profile", icon: <User size={20} /> },
];

const Sidebar = () => {
  const { logout, userName } = useAppState();
  const navigate = useNavigate();
  const userEmail = `${(userName || "learner").replace(/\s+/g, "").toLowerCase()}@aitutor.app`;

  const handleLogout = () => {
    logout();
    navigate("/");
  };

  return (
    <aside className="group fixed left-0 top-0 h-screen w-16 hover:w-56 bg-white border-r border-slate-200 z-50 transition-all duration-300 ease-in-out shadow-sm flex flex-col overflow-hidden">
      <div className="h-20 flex items-center px-4 border-b border-slate-200 shrink-0">
        <div className="w-9 h-9 rounded-xl bg-emerald-50 border border-emerald-100 text-emerald-700 flex items-center justify-center shrink-0">
          <Sparkles size={18} />
        </div>
        <div className="ml-3 min-w-0">
          <span className="overflow-hidden whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity duration-300 text-xl font-bold tracking-tight text-slate-800 block">
            AI Tutor
          </span>
        </div>
      </div>

      <nav className="flex-1 py-6 px-2 space-y-2 overflow-y-auto overflow-x-hidden">
        {navItems.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            className={({ isActive }) =>
              `w-full flex items-center justify-center group-hover:justify-start h-11 px-2 rounded-xl transition-colors duration-200 outline-none ${
                isActive
                  ? "bg-emerald-50 text-emerald-700 border border-emerald-100"
                  : "text-slate-600 hover:bg-slate-50 hover:text-slate-900"
              }`
            }
          >
            <div className="shrink-0 flex items-center justify-center w-7">
              {item.icon}
            </div>
            <div className="ml-3 min-w-0">
              <span className="overflow-hidden whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity duration-300 font-semibold text-sm text-left block">
                {item.label}
              </span>
            </div>
          </NavLink>
        ))}
      </nav>

      <div className="mt-auto p-2 border-t border-slate-200 shrink-0 space-y-2">
        <div className="flex items-center h-12 p-1.5 rounded-xl bg-slate-50 border border-slate-200">
          <div className="w-9 h-9 rounded-full bg-emerald-50 border border-emerald-100 flex items-center justify-center text-emerald-700 shrink-0">
            <User size={18} />
          </div>
          <div className="ml-3 min-w-0 overflow-hidden whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity duration-300">
            <p className="font-semibold text-slate-800 text-sm truncate">
              {userName || "Learner"}
            </p>
            <p className="text-[11px] text-slate-500 truncate">{userEmail}</p>
          </div>
        </div>

        <div className="max-h-0 overflow-hidden opacity-0 group-hover:max-h-14 group-hover:opacity-100 transition-all duration-300">
          <button
            onClick={handleLogout}
            className="w-full flex items-center h-11 px-2 rounded-xl text-slate-600 hover:bg-slate-50 hover:text-slate-900 transition-colors duration-200"
          >
            <div className="shrink-0 flex items-center justify-center w-7">
              <LogOut size={18} />
            </div>
            <div className="ml-3 min-w-0">
              <span className="overflow-hidden whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity duration-300 font-semibold text-sm block">
                Logout
              </span>
            </div>
          </button>
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;
