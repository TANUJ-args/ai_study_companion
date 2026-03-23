import React, { useState } from "react";
import { motion } from "framer-motion";
import {
  BookOpenCheck,
  BrainCircuit,
  GraduationCap,
  IdCard,
  Save,
  Sparkles,
  Target,
  TrendingUp,
} from "lucide-react";

const Profile = () => {
  const [goals, setGoals] = useState({
    dailyHours: "2.5",
    dsaProblems: "3",
    revisionMinutes: "45",
  });

  const handleSave = (event) => {
    event.preventDefault();
  };

  return (
    <div className="bg-slate-50 min-h-full space-y-6">
      <section className="bg-white border border-slate-200 shadow-sm rounded-2xl p-6 md:p-8">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-5">
          <div className="flex items-center gap-4">
            <div className="w-16 h-16 rounded-2xl bg-emerald-50 border border-emerald-200 text-emerald-700 flex items-center justify-center">
              <BrainCircuit className="w-8 h-8" />
            </div>
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-500">
                Profile Overview
              </p>
              <h1 className="text-2xl md:text-3xl font-bold text-slate-800 mt-1">
                Tannuj Margana
              </h1>
              <p className="text-slate-500 text-sm mt-1">3rd-Year CSE BTech</p>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div className="rounded-xl border border-slate-200 bg-slate-50 px-4 py-3">
              <p className="text-xs text-slate-500">Weekly Streak</p>
              <p className="text-lg font-semibold text-slate-800">11 days</p>
            </div>
            <div className="rounded-xl border border-slate-200 bg-slate-50 px-4 py-3">
              <p className="text-xs text-slate-500">Quizzes Completed</p>
              <p className="text-lg font-semibold text-slate-800">37</p>
            </div>
          </div>
        </div>
      </section>

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
        <section className="xl:col-span-2 bg-white border border-slate-200 shadow-sm rounded-2xl p-6">
          <div className="flex items-center justify-between gap-3">
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.16em] text-slate-500">
                Learning Path
              </p>
              <h2 className="text-xl font-bold text-slate-800 mt-1">
                Java Full-Stack Mastery & LeetCode Prep
              </h2>
            </div>
            <span className="inline-flex items-center gap-1.5 text-xs font-medium px-3 py-1.5 rounded-full bg-emerald-50 text-emerald-700">
              <Sparkles className="w-3.5 h-3.5" />
              Active Track
            </span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mt-5">
            <article className="rounded-xl border border-slate-200 bg-slate-50 p-4">
              <div className="flex items-center gap-2 text-slate-700">
                <BookOpenCheck className="w-4 h-4 text-emerald-600" />
                <p className="text-sm font-semibold">Syllabus Coverage</p>
              </div>
              <p className="text-2xl font-bold text-slate-800 mt-2">68%</p>
              <p className="text-xs text-slate-500 mt-1">
                React + Spring Boot modules completed
              </p>
            </article>

            <article className="rounded-xl border border-slate-200 bg-slate-50 p-4">
              <div className="flex items-center gap-2 text-slate-700">
                <Target className="w-4 h-4 text-emerald-600" />
                <p className="text-sm font-semibold">DSA Goal Pace</p>
              </div>
              <p className="text-2xl font-bold text-slate-800 mt-2">82%</p>
              <p className="text-xs text-slate-500 mt-1">
                On track for interview prep milestone
              </p>
            </article>

            <article className="rounded-xl border border-slate-200 bg-slate-50 p-4">
              <div className="flex items-center gap-2 text-slate-700">
                <TrendingUp className="w-4 h-4 text-emerald-600" />
                <p className="text-sm font-semibold">Accuracy Trend</p>
              </div>
              <p className="text-2xl font-bold text-slate-800 mt-2">+14%</p>
              <p className="text-xs text-slate-500 mt-1">
                Across last 10 adaptive quizzes
              </p>
            </article>

            <article className="rounded-xl border border-slate-200 bg-slate-50 p-4">
              <div className="flex items-center gap-2 text-slate-700">
                <GraduationCap className="w-4 h-4 text-emerald-600" />
                <p className="text-sm font-semibold">Interview Readiness</p>
              </div>
              <p className="text-2xl font-bold text-slate-800 mt-2">Level 2</p>
              <p className="text-xs text-slate-500 mt-1">
                Focus next: graphs, system design basics
              </p>
            </article>
          </div>
        </section>

        <motion.section
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.25, ease: "easeOut" }}
          className="bg-white border border-slate-200 shadow-sm rounded-2xl p-6"
        >
          <p className="text-xs font-semibold uppercase tracking-[0.16em] text-slate-500">
            Settings
          </p>
          <h2 className="text-xl font-bold text-slate-800 mt-1">
            Daily Study Goals
          </h2>

          <form className="mt-5 space-y-4" onSubmit={handleSave}>
            <label className="block">
              <span className="text-sm text-slate-500">Daily Study Hours</span>
              <input
                type="number"
                min="0.5"
                step="0.5"
                value={goals.dailyHours}
                onChange={(event) =>
                  setGoals((prev) => ({
                    ...prev,
                    dailyHours: event.target.value,
                  }))
                }
                className="mt-1.5 w-full rounded-xl border border-slate-300 bg-white px-3.5 py-2.5 text-sm text-slate-800 outline-none focus:ring-2 focus:ring-emerald-500/35 focus:border-emerald-500"
              />
            </label>

            <label className="block">
              <span className="text-sm text-slate-500">DSA Problems / Day</span>
              <input
                type="number"
                min="1"
                value={goals.dsaProblems}
                onChange={(event) =>
                  setGoals((prev) => ({
                    ...prev,
                    dsaProblems: event.target.value,
                  }))
                }
                className="mt-1.5 w-full rounded-xl border border-slate-300 bg-white px-3.5 py-2.5 text-sm text-slate-800 outline-none focus:ring-2 focus:ring-emerald-500/35 focus:border-emerald-500"
              />
            </label>

            <label className="block">
              <span className="text-sm text-slate-500">
                Revision Minutes / Day
              </span>
              <input
                type="number"
                min="10"
                step="5"
                value={goals.revisionMinutes}
                onChange={(event) =>
                  setGoals((prev) => ({
                    ...prev,
                    revisionMinutes: event.target.value,
                  }))
                }
                className="mt-1.5 w-full rounded-xl border border-slate-300 bg-white px-3.5 py-2.5 text-sm text-slate-800 outline-none focus:ring-2 focus:ring-emerald-500/35 focus:border-emerald-500"
              />
            </label>

            <button
              type="submit"
              className="w-full rounded-xl bg-emerald-500 hover:bg-emerald-600 text-white py-2.5 font-semibold inline-flex items-center justify-center gap-2 transition-colors shadow-[0_0_15px_rgba(16,185,129,0.4)]"
            >
              <Save className="w-4 h-4" />
              Save Changes
            </button>
          </form>

          <div className="mt-4 rounded-xl border border-slate-200 bg-slate-50 px-3.5 py-3">
            <p className="text-xs text-slate-500">Student ID</p>
            <p className="text-sm font-semibold text-slate-800 mt-1 inline-flex items-center gap-1.5">
              <IdCard className="w-3.5 h-3.5 text-emerald-600" />
              CSE-23-1187
            </p>
          </div>
        </motion.section>
      </div>
    </div>
  );
};

export default Profile;
