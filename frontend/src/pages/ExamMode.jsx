import React, { useMemo, useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
import {
  Brain,
  CheckCircle2,
  Code2,
  Layers,
  Server,
  Sparkles,
} from "lucide-react";

const mockQuestions = [
  {
    id: "dsa-1",
    category: "DSA",
    icon: Code2,
    prompt:
      "You need the fastest average lookup for key-value pairs in an in-memory cache. Which data structure is best?",
    options: ["Binary Search Tree", "Hash Map", "Singly Linked List", "Stack"],
    correctIndex: 1,
    explanation:
      "A hash map gives average O(1) lookup and insert, making it ideal for in-memory cache access. A BST is often O(log n), while linked list and stack are O(n) for lookup.",
  },
  {
    id: "react-1",
    category: "React",
    icon: Layers,
    prompt:
      "In a React app, a large filtered list recomputes on every keystroke and causes lag. Which approach is most appropriate first?",
    options: [
      "Wrap the derived filtered list with useMemo",
      "Convert all components to class components",
      "Store the filtered output in localStorage",
      "Use useRef instead of state for everything",
    ],
    correctIndex: 0,
    explanation:
      "useMemo memoizes expensive derived values and recalculates only when dependencies change. This is a targeted performance fix before deeper architectural changes.",
  },
  {
    id: "spring-1",
    category: "Spring Boot",
    icon: Server,
    prompt:
      "Your React frontend on localhost:5173 is blocked calling a Spring Boot API on localhost:8080. What is the clean backend-side fix?",
    options: [
      "Enable CORS for the frontend origin in Spring Boot",
      "Disable browser security",
      "Switch API responses to plain text only",
      "Use GET for all endpoints",
    ],
    correctIndex: 0,
    explanation:
      "This is a cross-origin policy issue. Configure CORS in Spring Boot (global config or @CrossOrigin) to allow the trusted frontend origin and methods.",
  },
];

const slideVariants = {
  initial: (direction) => ({
    x: direction > 0 ? 40 : -40,
    opacity: 0,
  }),
  animate: {
    x: 0,
    opacity: 1,
    transition: { duration: 0.25, ease: "easeOut" },
  },
  exit: (direction) => ({
    x: direction > 0 ? -40 : 40,
    opacity: 0,
    transition: { duration: 0.2, ease: "easeIn" },
  }),
};

const ExamMode = () => {
  const [index, setIndex] = useState(0);
  const [selectedMap, setSelectedMap] = useState({});
  const [direction, setDirection] = useState(1);

  const total = mockQuestions.length;
  const question = mockQuestions[index];
  const selectedIndex = selectedMap[question.id];
  const hasAnswered = selectedIndex !== undefined;
  const isCorrect = hasAnswered && selectedIndex === question.correctIndex;

  const progress = useMemo(() => ((index + 1) / total) * 100, [index, total]);

  const selectOption = (optionIndex) => {
    if (selectedMap[question.id] !== undefined) return;
    setSelectedMap((prev) => ({ ...prev, [question.id]: optionIndex }));
  };

  const goNext = () => {
    if (index >= total - 1) return;
    setDirection(1);
    setIndex((prev) => prev + 1);
  };

  const goPrevious = () => {
    if (index <= 0) return;
    setDirection(-1);
    setIndex((prev) => prev - 1);
  };

  const answeredCount = Object.keys(selectedMap).length;
  const score = Object.entries(selectedMap).reduce((acc, [id, answerIndex]) => {
    const current = mockQuestions.find((item) => item.id === id);
    if (!current) return acc;
    return acc + (current.correctIndex === answerIndex ? 1 : 0);
  }, 0);

  const CategoryIcon = question.icon;

  return (
    <div className="bg-slate-50 min-h-full">
      <section className="max-w-4xl mx-auto bg-white border border-slate-200 shadow-sm rounded-2xl p-6 md:p-8">
        <div className="flex items-center justify-between gap-3 mb-4">
          <div>
            <h2 className="text-2xl md:text-3xl font-bold text-slate-800">
              Adaptive Concept Check
            </h2>
          </div>
          <div className="text-right">
            <p className="text-xs text-slate-500">Progress</p>
            <p className="text-sm font-semibold text-slate-800">
              {index + 1}/{total}
            </p>
          </div>
        </div>

        <div className="h-2 w-full rounded-full bg-slate-100 overflow-hidden mb-6">
          <motion.div
            className="h-full bg-emerald-500"
            initial={false}
            animate={{ width: `${progress}%` }}
            transition={{ duration: 0.25, ease: "easeOut" }}
          />
        </div>

        <div className="relative min-h-90">
          <AnimatePresence mode="wait" custom={direction}>
            <motion.article
              key={question.id}
              custom={direction}
              variants={slideVariants}
              initial="initial"
              animate="animate"
              exit="exit"
              className="space-y-5"
            >
              <div className="flex flex-wrap items-center gap-2">
                <span className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-emerald-50 text-emerald-700 text-xs font-medium">
                  <CategoryIcon className="w-3.5 h-3.5" />
                  {question.category}
                </span>
                <span className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-slate-100 text-slate-600 text-xs font-medium">
                  <Brain className="w-3.5 h-3.5" />
                  AI-evaluated explanation
                </span>
              </div>

              <h3 className="text-xl md:text-2xl font-semibold text-slate-800 leading-snug">
                {question.prompt}
              </h3>

              <div className="grid grid-cols-1 gap-3">
                {question.options.map((option, optionIndex) => {
                  const isSelected = selectedIndex === optionIndex;
                  const isAnswer = question.correctIndex === optionIndex;

                  let optionClass =
                    "border-slate-200 bg-white text-slate-700 hover:bg-slate-50";

                  if (hasAnswered && isAnswer) {
                    optionClass =
                      "border-emerald-300 bg-emerald-50 text-emerald-800";
                  } else if (hasAnswered && isSelected && !isAnswer) {
                    optionClass = "border-rose-300 bg-rose-50 text-rose-700";
                  }

                  return (
                    <button
                      key={option}
                      onClick={() => selectOption(optionIndex)}
                      className={`w-full text-left rounded-xl border px-4 py-3.5 transition-colors ${optionClass}`}
                    >
                      <span className="text-sm md:text-base font-medium">
                        {option}
                      </span>
                    </button>
                  );
                })}
              </div>

              <AnimatePresence>
                {hasAnswered ? (
                  <motion.div
                    key="explanation"
                    initial={{ opacity: 0, y: 8, height: 0 }}
                    animate={{ opacity: 1, y: 0, height: "auto" }}
                    exit={{ opacity: 0, y: -4, height: 0 }}
                    transition={{ duration: 0.22, ease: "easeOut" }}
                    className="rounded-2xl border border-emerald-200 bg-emerald-50/70 p-4"
                  >
                    <div className="flex items-start gap-2">
                      <Sparkles className="w-4 h-4 mt-0.5 text-emerald-700" />
                      <div>
                        <p className="text-sm font-semibold text-emerald-800">
                          {isCorrect ? "Great pick" : "AI Explanation"}
                        </p>
                        <p className="text-sm text-slate-700 mt-1 leading-relaxed">
                          {question.explanation}
                        </p>
                      </div>
                    </div>
                  </motion.div>
                ) : null}
              </AnimatePresence>
            </motion.article>
          </AnimatePresence>
        </div>

        <div className="mt-6 flex flex-wrap items-center justify-between gap-3">
          <div className="text-sm text-slate-500">
            Answered {answeredCount}/{total} · Score {score}/{total}
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={goPrevious}
              disabled={index === 0}
              className="rounded-xl border border-slate-200 hover:bg-slate-50 text-slate-700 px-4 py-2.5 text-sm font-semibold transition-colors disabled:opacity-40"
            >
              Previous
            </button>
            <button
              onClick={goNext}
              disabled={index === total - 1}
              className="rounded-xl bg-emerald-500 hover:bg-emerald-600 text-white px-4 py-2.5 text-sm font-semibold transition-colors disabled:opacity-40"
            >
              Next Question
            </button>
          </div>
        </div>

        {index === total - 1 ? (
          <div className="mt-5 rounded-2xl border border-slate-200 bg-slate-50 p-4 flex flex-wrap items-center justify-between gap-3">
            <p className="text-sm text-slate-700">
              Final score preview:{" "}
              <span className="font-semibold">
                {score}/{total}
              </span>
            </p>
            <span className="inline-flex items-center gap-2 text-xs px-3 py-1.5 rounded-full bg-emerald-50 text-emerald-700 font-medium">
              <CheckCircle2 className="w-3.5 h-3.5" />
              Review complete
            </span>
          </div>
        ) : null}
      </section>
    </div>
  );
};

export default ExamMode;
