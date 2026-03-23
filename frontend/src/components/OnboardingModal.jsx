import React, { useRef, useState } from "react";
import {
  Bot,
  FileText,
  Sparkles,
  UploadCloud,
  UserCircle2,
  X,
} from "lucide-react";

const avatarOptions = [
  {
    id: "robot",
    label: "Robot Guide",
    accent: "bg-emerald-50 border-emerald-200 text-emerald-700",
  },
  {
    id: "ninja",
    label: "Ninja Mentor",
    accent: "bg-slate-50 border-slate-200 text-slate-700",
  },
  {
    id: "scholar",
    label: "Scholar Sage",
    accent: "bg-emerald-50 border-emerald-200 text-emerald-700",
  },
  {
    id: "guardian",
    label: "Guardian",
    accent: "bg-slate-50 border-slate-200 text-slate-700",
  },
  {
    id: "navigator",
    label: "Navigator",
    accent: "bg-emerald-50 border-emerald-200 text-emerald-700",
  },
];

const goalOptions = [
  { id: "quick", title: "Quick Review", value: "15m" },
  { id: "steady", title: "Steady Pace", value: "1 hr" },
  { id: "deep", title: "Deep Work", value: "2+ hrs" },
];

const TOTAL_STEPS = 3;

const OnboardingModal = ({ isOpen, onComplete }) => {
  const [step, setStep] = useState(1);
  const [selectedAvatar, setSelectedAvatar] = useState("robot");
  const [selectedGoal, setSelectedGoal] = useState("steady");
  const [isHovering, setIsHovering] = useState(false);
  const [learningGoals, setLearningGoals] = useState("");
  const [uploadedFile, setUploadedFile] = useState(null);
  const resumeInputRef = useRef(null);

  if (!isOpen) return null;

  const handleNext = () => {
    setStep((prev) => Math.min(prev + 1, TOTAL_STEPS));
  };

  const handleBack = () => setStep((prev) => Math.max(prev - 1, 1));

  const handleComplete = () => {
    onComplete({
      avatar: selectedAvatar,
      dailyCommitment: selectedGoal,
      learningGoals,
      resumeName: uploadedFile?.name || "",
    });
  };

  const handleDragOver = (event) => {
    event.preventDefault();
    setIsHovering(true);
  };

  const handleDragLeave = () => setIsHovering(false);

  const handleDrop = (event) => {
    event.preventDefault();
    setIsHovering(false);
    if (event.dataTransfer.files && event.dataTransfer.files[0]) {
      setUploadedFile(event.dataTransfer.files[0]);
    }
  };

  const handleFileChange = (event) => {
    if (event.target.files && event.target.files[0]) {
      setUploadedFile(event.target.files[0]);
    }
  };

  const handleTextareaKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      if (learningGoals.trim() || uploadedFile) {
        handleComplete();
      }
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-slate-900/45 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="bg-white border border-slate-200 shadow-sm rounded-2xl p-6 md:p-8 max-w-2xl w-full max-h-[92vh] overflow-y-auto">
        <div className="flex items-center justify-center gap-2 mb-6">
          {Array.from({ length: TOTAL_STEPS }).map((_, idx) => {
            const dot = idx + 1;
            return (
              <span
                key={dot}
                className={`h-2.5 rounded-full transition-all duration-300 ${
                  step === dot ? "w-8 bg-emerald-500" : "w-2.5 bg-slate-300"
                }`}
              />
            );
          })}
        </div>

        <div className="min-h-97.5 transition-all duration-300">
          {step === 1 ? (
            <div className="space-y-5">
              <div>
                <p className="text-xs font-semibold uppercase tracking-[0.16em] text-slate-500">
                  Step 1
                </p>
                <h2 className="text-2xl font-bold mt-1 text-slate-800">
                  Choose Your AI Avatar
                </h2>
                <p className="text-sm text-slate-500 mt-1">
                  Select the AI persona that resonates with your learning style.
                </p>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                {avatarOptions.map((avatar) => {
                  const isActive = selectedAvatar === avatar.id;
                  return (
                    <button
                      key={avatar.id}
                      onClick={() => setSelectedAvatar(avatar.id)}
                      className={`rounded-2xl border p-4 text-left transition-all duration-200 ${
                        isActive
                          ? "border-emerald-300 bg-emerald-50"
                          : `border-slate-200 ${avatar.accent}`
                      }`}
                    >
                      <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-full bg-white border border-slate-200 flex items-center justify-center text-emerald-700">
                          <UserCircle2 className="w-5 h-5" />
                        </div>
                        <div>
                          <p className="text-sm font-semibold text-slate-800">
                            {avatar.label}
                          </p>
                          <p className="text-xs text-slate-500">
                            AI persona style
                          </p>
                        </div>
                      </div>
                    </button>
                  );
                })}
              </div>
            </div>
          ) : null}

          {step === 2 ? (
            <div className="space-y-5">
              <div>
                <p className="text-xs font-semibold uppercase tracking-[0.16em] text-slate-500">
                  Step 2
                </p>
                <h2 className="text-2xl font-bold mt-1 text-slate-800">
                  Set Your Daily Goal
                </h2>
                <p className="text-sm text-slate-500 mt-1">
                  Pick a realistic rhythm to build a consistent learning streak.
                </p>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                {goalOptions.map((goal) => {
                  const isActive = selectedGoal === goal.id;
                  return (
                    <button
                      key={goal.id}
                      onClick={() => setSelectedGoal(goal.id)}
                      className={`rounded-2xl border p-4 text-left transition-all duration-200 ${
                        isActive
                          ? "border-emerald-300 bg-emerald-50"
                          : "border-slate-200 bg-slate-50 hover:bg-white"
                      }`}
                    >
                      <p className="text-sm font-semibold text-slate-800">
                        {goal.title}
                      </p>
                      <p className="text-2xl font-bold mt-1 text-emerald-600">
                        {goal.value}
                      </p>
                      <p className="text-xs text-slate-500 mt-2">
                        Sustainable daily commitment
                      </p>
                    </button>
                  );
                })}
              </div>
            </div>
          ) : null}

          {step === 3 ? (
            <div className="space-y-5">
              <div>
                <p className="text-xs font-semibold uppercase tracking-[0.16em] text-slate-500">
                  Step 3
                </p>
                <h2 className="text-2xl font-bold mt-1 text-slate-800">
                  Kickstart Your AI Tutor
                </h2>
                <p className="text-sm text-slate-500 mt-1">
                  Upload your syllabus or describe your goals.
                </p>
              </div>

              <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4 flex items-start gap-3">
                <div className="p-2 bg-emerald-50 rounded-full border border-emerald-200 shrink-0 mt-0.5">
                  <Bot className="w-4 h-4 text-emerald-600" />
                </div>
                <p className="text-sm font-medium leading-relaxed text-slate-700">
                  We map your syllabus and goals to personalized quizzes,
                  flashcards, and recommendations.
                </p>
              </div>

              <div
                className={`w-full border-2 border-dashed rounded-2xl p-5 flex flex-col items-center justify-center cursor-pointer transition-all duration-300 ${
                  isHovering
                    ? "border-emerald-400 bg-emerald-50"
                    : "border-slate-300 bg-white hover:border-emerald-400 hover:bg-emerald-50/40"
                }`}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
                onClick={() => resumeInputRef.current?.click()}
              >
                <input
                  ref={resumeInputRef}
                  type="file"
                  className="hidden"
                  accept=".pdf,.doc,.docx"
                  onChange={handleFileChange}
                />

                {uploadedFile ? (
                  <div className="flex flex-col items-center gap-1.5">
                    <FileText className="w-8 h-8 text-emerald-600" />
                    <span className="font-medium text-sm text-slate-800">
                      {uploadedFile.name}
                    </span>
                    <span className="text-[11px] text-slate-500">
                      Click to replace
                    </span>
                  </div>
                ) : (
                  <>
                    <UploadCloud className="w-8 h-8 mb-2 text-slate-500" />
                    <span className="font-medium text-sm mb-0.5 text-slate-800">
                      Drag and drop your syllabus
                    </span>
                    <span className="text-[11px] text-slate-500">
                      PDF or DOCX (max 5MB)
                    </span>
                  </>
                )}
              </div>

              <div className="flex items-center gap-4 py-1.5">
                <div className="h-px bg-slate-200 flex-1"></div>
                <span className="text-[10px] font-semibold text-slate-500 tracking-[0.14em] uppercase">
                  or type goals
                </span>
                <div className="h-px bg-slate-200 flex-1"></div>
              </div>

              <textarea
                className="w-full min-h-27.5 text-sm bg-white border border-slate-300 rounded-2xl p-3.5 text-slate-800 placeholder:text-slate-500/80 resize-none transition-all outline-none focus:ring-2 focus:ring-emerald-500/35 focus:border-emerald-500"
                placeholder="E.g., I am preparing for OS + DBMS exams and need weekly practice sets and revision reminders."
                value={learningGoals}
                onChange={(event) => setLearningGoals(event.target.value)}
                onKeyDown={handleTextareaKeyDown}
              />
            </div>
          ) : null}
        </div>

        <div className="mt-6 flex items-center justify-between gap-3">
          <button
            onClick={handleBack}
            disabled={step === 1}
            className="px-4 py-2 rounded-xl border border-slate-300 bg-white text-sm font-semibold text-slate-700 disabled:opacity-40 disabled:cursor-not-allowed"
          >
            Back
          </button>

          {step < TOTAL_STEPS ? (
            <button
              onClick={handleNext}
              className="px-5 py-2.5 rounded-xl bg-emerald-500 hover:bg-emerald-600 text-white text-sm font-semibold transition-colors"
            >
              Next
            </button>
          ) : (
            <button
              onClick={handleComplete}
              className="px-5 py-2.5 rounded-xl bg-emerald-500 hover:bg-emerald-600 disabled:opacity-50 disabled:cursor-not-allowed text-white text-sm font-semibold transition-colors inline-flex items-center gap-2"
              disabled={!learningGoals.trim() && !uploadedFile}
            >
              <Sparkles className="w-4 h-4" />
              Generate My AI Tutor
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default OnboardingModal;
