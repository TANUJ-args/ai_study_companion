import React, { useMemo, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { RotateCcw, ChevronLeft, ChevronRight, Layers } from "lucide-react";
import { useAppState } from "../context/AppStateContext";

const notesByTopic = {
  Integration:
    "Integration is reverse differentiation; always remember + C for indefinite integrals.",
  Trigonometry:
    "Anchor identity: sin^2(x) + cos^2(x) = 1. Build all identities around this base.",
  Derivatives:
    "Practice chain rule and product rule with 5 mixed examples daily.",
  Kinematics: "Memorize v=u+at, s=ut+1/2at^2, v^2=u^2+2as with units.",
  Optics:
    "Lens sign convention and focal length unit (meter) are common trap points.",
  Organic: "Map functional groups visually to lock them into long-term memory.",
  Physical: "pH below 7 acidic, above 7 basic, 7 neutral.",
  Databases:
    "SQL = Structured Query Language. Focus on SELECT-WHERE-GROUP BY flow.",
  Algorithms: "Binary search works on sorted arrays with O(log n) complexity.",
  Waves: "Frequency means oscillations per second; measured in Hertz.",
};

const FlashcardsPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { topicPerformance, weakTopics } = useAppState();

  const [index, setIndex] = useState(0);
  const [flipped, setFlipped] = useState(false);

  const cards = useMemo(() => {
    const focusTopic = location.state?.presetTopic;

    let source = weakTopics.length ? weakTopics : topicPerformance;

    if (focusTopic) {
      const focused = source.find((item) => item.topic === focusTopic);
      const remaining = source.filter((item) => item.topic !== focusTopic);
      source = focused ? [focused, ...remaining] : source;
    }

    return source.slice(0, 8).map((item) => ({
      id: item.topic,
      front: `${item.subject}: ${item.topic}`,
      back:
        notesByTopic[item.topic] ||
        "Revise this topic with one concept and one solved example.",
      strength: item.strength,
    }));
  }, [location.state, topicPerformance, weakTopics]);

  const safeIndex = Math.min(index, Math.max(cards.length - 1, 0));
  const current = cards[safeIndex];

  if (!current) {
    return (
      <section className="max-w-4xl mx-auto bg-white border border-slate-200 shadow-sm rounded-2xl p-8 text-center">
        <h2 className="text-2xl font-bold text-slate-900">No flashcards yet</h2>
        <p className="text-slate-500 mt-2">
          Complete a quiz first to generate revision cards.
        </p>
        <button
          onClick={() => navigate("/quiz")}
          className="mt-6 inline-flex items-center justify-center rounded-xl px-5 py-3 bg-emerald-500 hover:bg-emerald-600 text-white font-semibold shadow-[0_0_15px_rgba(16,185,129,0.35)] transition-all"
        >
          Go to Quiz
        </button>
      </section>
    );
  }

  const cardShell =
    "bg-white border border-slate-200 shadow-sm rounded-2xl p-6 md:p-8";
  const subtleButton =
    "rounded-xl border border-slate-200 bg-slate-50 px-4 py-2.5 text-sm font-semibold text-slate-800 disabled:opacity-40 disabled:cursor-not-allowed flex items-center gap-2 hover:bg-white transition-colors";
  const primaryButton =
    "rounded-xl px-5 py-2.5 bg-emerald-500 hover:bg-emerald-600 text-white text-sm font-semibold shadow-[0_0_15px_rgba(16,185,129,0.35)] transition-all";

  return (
    <section className="max-w-5xl mx-auto space-y-6">
      <div className={cardShell}>
        <p className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-500">
          Revision Flow
        </p>
        <div className="mt-2 flex items-center gap-2">
          <div className="w-10 h-10 rounded-xl bg-emerald-50 text-emerald-700 flex items-center justify-center">
            <Layers className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-slate-900">
              Smart Flashcards
            </h2>
            <p className="text-sm text-slate-500">
              Flip through cards generated from your weak topics.
            </p>
          </div>
        </div>
      </div>

      <div className={cardShell}>
        <button
          onClick={() => setFlipped((prev) => !prev)}
          className="w-full text-left rounded-2xl border border-slate-200 bg-slate-50 hover:bg-white transition-all duration-200 p-5"
        >
          <div className="flex justify-between text-xs font-semibold uppercase tracking-[0.18em] text-slate-500">
            <span>{flipped ? "Answer" : "Question"}</span>
            <span>
              Card {safeIndex + 1}/{cards.length}
            </span>
          </div>

          <div className="mt-6">
            {!flipped ? (
              <>
                <p className="text-xl md:text-2xl font-bold text-slate-900">
                  {current.front}
                </p>
                <p className="mt-3 text-sm text-slate-500">
                  Current proficiency: {current.strength}%
                </p>
                <p className="mt-6 text-xs font-semibold uppercase tracking-[0.18em] text-emerald-600">
                  Tap to flip
                </p>
              </>
            ) : (
              <>
                <p className="text-lg md:text-xl font-semibold text-slate-900 leading-relaxed">
                  {current.back}
                </p>
                <p className="mt-6 text-xs font-semibold uppercase tracking-[0.18em] text-emerald-600">
                  Tap to flip back
                </p>
              </>
            )}
          </div>
        </button>

        <div className="mt-6 flex flex-wrap gap-3">
          <button
            onClick={() => {
              setIndex((prev) => Math.max(0, prev - 1));
              setFlipped(false);
            }}
            disabled={safeIndex === 0}
            className={subtleButton}
          >
            <ChevronLeft className="w-4 h-4" />
            Previous
          </button>

          <button
            onClick={() => {
              setIndex((prev) => Math.min(cards.length - 1, prev + 1));
              setFlipped(false);
            }}
            disabled={safeIndex === cards.length - 1}
            className={subtleButton}
          >
            Next
            <ChevronRight className="w-4 h-4" />
          </button>

          <button
            onClick={() => {
              setIndex(0);
              setFlipped(false);
            }}
            className={subtleButton}
          >
            <RotateCcw className="w-4 h-4" />
            Restart Deck
          </button>

          <button
            onClick={() => navigate("/dashboard")}
            className={primaryButton}
          >
            Back to Dashboard
          </button>
        </div>
      </div>
    </section>
  );
};

export default FlashcardsPage;
