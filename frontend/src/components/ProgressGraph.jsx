import React from "react";
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

const fallbackData = [
  { label: "Mon", score: 62 },
  { label: "Tue", score: 68 },
  { label: "Wed", score: 71 },
  { label: "Thu", score: 74 },
  { label: "Fri", score: 76 },
  { label: "Sat", score: 80 },
  { label: "Sun", score: 82 },
];

const ProgressGraph = ({ data = [] }) => {
  const chartData = data.length ? data : fallbackData;

  return (
    <div className="w-full h-72">
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart
          data={chartData}
          margin={{ top: 10, right: 18, left: -6, bottom: 0 }}
        >
          <defs>
            <linearGradient id="progressFill" x1="0" y1="0" x2="0" y2="1">
              <stop
                offset="0%"
                stopColor="rgba(16,185,129,0.65)"
                stopOpacity={1}
              />
              <stop
                offset="100%"
                stopColor="rgba(16,185,129,0)"
                stopOpacity={0}
              />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
          <XAxis
            dataKey="label"
            tick={{ fill: "#475569" }}
            tickLine={false}
            axisLine={false}
          />
          <YAxis
            domain={[0, 100]}
            tick={{ fill: "#475569" }}
            tickLine={false}
            axisLine={false}
          />
          <Tooltip
            cursor={{ stroke: "rgba(16,185,129,0.35)", strokeWidth: 2 }}
            contentStyle={{
              background: "#0b1726",
              border: "1px solid rgba(226,232,240,0.25)",
              borderRadius: 12,
              color: "#e2e8f0",
            }}
          />
          <Area
            type="monotone"
            dataKey="score"
            stroke="rgba(16,185,129,0.9)"
            strokeWidth={3}
            fill="url(#progressFill)"
            isAnimationActive
            animationDuration={900}
            dot={{ stroke: "#10b981", strokeWidth: 2, r: 3, fill: "#fff" }}
            activeDot={{ r: 5, strokeWidth: 0, fill: "#10b981" }}
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
};

export default ProgressGraph;
