import React, { useState } from "react";

const mockHeatmapData = [
  { subject: "Math", topic: "Integration", strength: 25 },
  { subject: "Math", topic: "Derivatives", strength: 75 },
  { subject: "Math", topic: "Trigonometry", strength: 50 },
  { subject: "Physics", topic: "Kinematics", strength: 90 },
  { subject: "Physics", topic: "Optics", strength: 15 },
  { subject: "Physics", topic: "Thermodynamics", strength: 60 },
  { subject: "Chemistry", topic: "Organic", strength: 40 },
  { subject: "Chemistry", topic: "Inorganic", strength: 80 },
  { subject: "Chemistry", topic: "Physical", strength: 20 },
  { subject: "Biology", topic: "Genetics", strength: 70 },
  { subject: "CS", topic: "Algorithms", strength: 85 },
  { subject: "CS", topic: "Data Structures", strength: 55 },
  { subject: "CS", topic: "Databases", strength: 30 },
  { subject: "Math", topic: "Limits", strength: 10 },
  { subject: "Physics", topic: "Waves", strength: 65 },
];

const getTier = (strength) => {
  if (strength <= 39) return "weak";
  if (strength <= 69) return "average";
  return "strong";
};

const tierStyles = {
  weak: "bg-red-500 text-white",
  average: "bg-yellow-500 text-slate-900",
  strong: "bg-emerald-500 text-white",
};

const tierLabels = {
  weak: "Weak (0-39%)",
  average: "Average (40-69%)",
  strong: "Strong (70-100%)",
};

const WeaknessHeatmap = ({ items = mockHeatmapData }) => {
  const data = items;
  const [hoveredIndex, setHoveredIndex] = useState(null);

  return (
    <div className="w-full">
      <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
        {data.map((item, index) => {
          const tier = getTier(item.strength);
          return (
            <div
              key={`${item.topic}-${index}`}
              onMouseEnter={() => setHoveredIndex(index)}
              onMouseLeave={() => setHoveredIndex(null)}
              className={`relative h-16 rounded-xl flex items-center justify-center cursor-default transition-all duration-300 shadow-sm ${tierStyles[tier]} ${index === hoveredIndex ? "scale-[1.03] shadow-md z-40" : "hover:scale-[1.03] z-10 hover:z-40"}`}
            >
              <span className="text-xs font-bold px-2 text-center truncate w-full tracking-wide pointer-events-none">
                {item.topic}
              </span>

              <div
                className={`absolute z-50 bottom-full mb-3 left-1/2 -translate-x-1/2 transition-all duration-300 ease-out pointer-events-none w-52 p-3.5 bg-white/95 backdrop-blur-md border border-slate-200 rounded-2xl shadow-[0_10px_40px_-10px_rgba(0,0,0,0.5)] flex flex-col gap-1 ${index === hoveredIndex ? "opacity-100 translate-y-0 visible" : "opacity-0 translate-y-2 invisible"}`}
              >
                <div className="font-bold text-sm mb-1 text-slate-900">
                  <span className="text-emerald-600">{item.subject}:</span>{" "}
                  {item.topic}
                </div>

                <div className="flex items-center justify-between text-xs font-medium text-slate-600">
                  <span>Proficiency:</span>
                  <span className="text-slate-900 font-bold text-sm">
                    {item.strength}%
                  </span>
                </div>

                <div className="mt-1 text-xs font-bold flex items-center gap-1.5 text-slate-800">
                  {tier === "weak" && (
                    <span className="text-red-600">⚠️ Needs focus</span>
                  )}
                  {tier === "average" && (
                    <span className="text-yellow-700">⚡ On track</span>
                  )}
                  {tier === "strong" && (
                    <span className="text-emerald-600">✨ Mastered</span>
                  )}
                </div>

                <div className="absolute top-[98%] left-1/2 -translate-x-1/2 border-8 border-transparent border-t-slate-200/60 drop-shadow-sm"></div>
                <div className="absolute top-[96%] left-1/2 -translate-x-1/2 border-[7px] border-transparent border-t-white/95"></div>
              </div>
            </div>
          );
        })}
      </div>

      <div className="mt-6 flex flex-wrap gap-4 text-xs font-semibold text-slate-600 justify-end">
        {["weak", "average", "strong"].map((tier) => (
          <div key={tier} className="flex items-center gap-1.5">
            <div
              className={`w-3 h-3 rounded-sm shadow-sm ${tierStyles[tier]}`}
            ></div>
            {tierLabels[tier]}
          </div>
        ))}
      </div>
    </div>
  );
};

export default WeaknessHeatmap;
