import React, { useMemo, useState } from "react";
import { Link } from "react-router-dom";
import {
  ArrowLeft,
  ArrowRight,
  Brain,
  ChartNoAxesCombined,
  CheckCircle2,
  GraduationCap,
  MessageSquareText,
  Sparkles,
  Trophy,
} from "lucide-react";
import heroImage from "../assets/image (6).png";
import dashboardImage from "../assets/progressgraph.png";
import quickActionsImage from "../assets/quickactions.png";
import quizImage from "../assets/quiz.png";
import chatImage from "../assets/aichat.png";
import flashcardImage from "../assets/flashcard.png";
import flashcardAnswerImage from "../assets/flashcardanswer.png";
import reportImage from "../assets/weeknessheatmap.png";
import examImage from "../assets/interactiveexammode1.png";
import examOverlayImage from "../assets/interractiveexammode2.png";
import "./LandingPage.css";

const toolkits = [
  {
    id: "dashboard",
    name: "Dashboard",
    cta: "Open dashboard",
    to: "/dashboard",
    points: [
      "Track daily and weekly study streaks",
      "See topic-wise performance in one place",
      "Get instant progress insights",
    ],
    image: quickActionsImage,
    overlayImage: dashboardImage,
  },
  {
    id: "quiz",
    name: "Quiz Engine",
    cta: "Practice now",
    to: "/quiz",
    points: [
      "Adaptive questions based on your accuracy",
      "Timed quizzes to simulate exam pressure",
      "Auto feedback for each answer",
    ],
    image: quizImage,
    overlayImage: null,
  },
  {
    id: "chat",
    name: "AI Tutor Chat",
    cta: "Start chat",
    to: "/chat",
    points: [
      "Ask doubts in plain language",
      "Get concept explanations with examples",
      "Receive quick follow-up hints",
    ],
    image: chatImage,
    overlayImage: null,
  },
  {
    id: "flashcards",
    name: "Flashcards",
    cta: "Revise fast",
    to: "/flashcards",
    points: [
      "Auto-generate cards from weak topics",
      "Spaced repetition for long-term memory",
      "Mark mastered cards and move forward",
    ],
    image: flashcardImage,
    overlayImage: flashcardAnswerImage,
  },
  {
    id: "reports",
    name: "Report Insights",
    cta: "View reports",
    to: "/report",
    points: [
      "Find weak concepts instantly",
      "Compare attempts over time",
      "Study smarter with action steps",
    ],
    image: reportImage,
    overlayImage: null,
  },
  {
    id: "exam",
    name: "Exam Mode",
    cta: "Start exam mode",
    to: "/exam",
    points: [
      "Full-screen distraction-free sessions",
      "Strict timer and section control",
      "Post-exam analytics summary",
    ],
    image: examImage,
    overlayImage: examOverlayImage,
  },
];

const highlights = [
  {
    icon: Brain,
    title: "Adaptive Intelligence",
    desc: "The app adjusts question difficulty and guidance in real time based on your progress.",
  },
  {
    icon: MessageSquareText,
    title: "Doubt-to-Clarity Chat",
    desc: "Convert confusion into understanding with short, clear AI tutor explanations.",
  },
  {
    icon: ChartNoAxesCombined,
    title: "Actionable Reports",
    desc: "Every quiz ends with practical next steps so you know exactly what to revise.",
  },
  {
    icon: GraduationCap,
    title: "Structured Learning Path",
    desc: "Move from basics to mastery with milestone-based topic progression.",
  },
  {
    icon: Trophy,
    title: "Streaks and Motivation",
    desc: "Build momentum through streak tracking, goals, and weekly achievements.",
  },
  {
    icon: Sparkles,
    title: "Smart Revision",
    desc: "Flashcards and quick recap sessions make last-minute revision efficient.",
  },
];

const reviews = [
  {
    name: "Aarav Singh",
    role: "B.Tech Student",
    quote:
      "StudIQ made my study routine focused and measurable. I stopped guessing and started improving with data.",
    review:
      "I used to jump between random videos. With StudIQ, my preparation became structured and my mock test score improved by 21%.",
  },
  {
    name: "Nisha Verma",
    role: "NEET Aspirant",
    quote:
      "The weakness report gave me exactly what to revise each week, and my confidence improved with every attempt.",
    review:
      "The weakness report is the best part. I can see exactly where I am losing marks and fix it quickly.",
  },
  {
    name: "Rohan Gupta",
    role: "Competitive Exam Learner",
    quote:
      "Exam mode feels realistic and the AI explanations are clear. It feels like studying with a personal mentor.",
    review:
      "Exam mode feels realistic and the AI explanations are very clear. It feels like studying with a personal mentor.",
  },
  {
    name: "Priya Nair",
    role: "Full-Stack Learner",
    quote:
      "The chat plus flashcards combo helped me retain concepts faster than any random playlist approach.",
    review:
      "Practice, revision and chat are tightly connected. I always know the next best action.",
  },
];

const footerColumns = [
  {
    heading: "STUDIQ",
    links: [
      "Features",
      "Pricing",
      "Free Trial",
      "Success Stories",
      "Insights",
      "News",
    ],
  },
  {
    heading: "HELP",
    links: ["Knowledge Base", "Academy", "API", "Community", "Webinars"],
  },
  {
    heading: "MORE TOOLS",
    links: [
      "Exam Mode",
      "AI Tutor Chat",
      "Progress Reports",
      "Flashcards",
      "Adaptive Quiz",
    ],
  },
  {
    heading: "COMPANY",
    links: [
      "About Us",
      "Careers",
      "Partners",
      "Legal Info",
      "Privacy Policy",
      "Contact",
    ],
  },
  {
    heading: "FOLLOW US",
    links: ["X (Twitter)", "LinkedIn", "Instagram", "YouTube"],
  },
];

const LandingPage = () => {
  const [activeIndex, setActiveIndex] = useState(0);
  const [activeReviewIndex, setActiveReviewIndex] = useState(0);

  const goNext = () => {
    setActiveIndex((prev) => (prev + 1) % toolkits.length);
  };

  const goPrev = () => {
    setActiveIndex((prev) => (prev - 1 + toolkits.length) % toolkits.length);
  };

  const goNextReview = () => {
    setActiveReviewIndex((prev) => (prev + 1) % reviews.length);
  };

  const goPrevReview = () => {
    setActiveReviewIndex(
      (prev) => (prev - 1 + reviews.length) % reviews.length,
    );
  };

  const activeToolkit = toolkits[activeIndex];
  const previousToolkit =
    toolkits[(activeIndex - 1 + toolkits.length) % toolkits.length];
  const nextToolkit = toolkits[(activeIndex + 1) % toolkits.length];

  const activeReview = reviews[activeReviewIndex];
  const initials = useMemo(() => {
    const parts = activeReview.name.split(" ").filter(Boolean);
    return parts
      .slice(0, 2)
      .map((part) => part[0])
      .join("");
  }, [activeReview.name]);

  return (
    <main className="landing-root">
      <header className="landing-navbar-wrap">
        <nav className="landing-navbar container-wide" aria-label="Primary">
          <div className="landing-brand">
            <span className="landing-brand-dot" aria-hidden="true" />
            <span className="landing-brand-text">STUDIQ</span>
          </div>

          <div
            className="landing-nav-links"
            role="navigation"
            aria-label="Main menu"
          >
            <a href="#main_toolkits">Products</a>
            <a href="#features">Features</a>
            <a href="#reviews">Testimonials</a>
            <a href="#main_toolkits">App Center</a>
          </div>

          <div className="landing-nav-actions">
            <Link to="/login" className="landing-login-btn">
              Log In
            </Link>
            <Link to="/register" className="landing-signup-btn">
              Sign Up
            </Link>
          </div>
        </nav>
      </header>

      <section className="landing-hero container-wide">
        <div className="landing-hero-copy">
          <p className="landing-chip">AI Study Companion</p>
          <h1>Study with clarity, consistency, and confidence.</h1>
          <p className="landing-subtext">
            StudIQ helps you prepare faster with adaptive quizzes, AI doubt
            solving, targeted revision, and measurable progress tracking.
          </p>
          <div className="landing-hero-actions">
            <Link to="/register" className="cta-primary">
              Start free trial
            </Link>
            <Link to="/login" className="cta-secondary">
              Login
            </Link>
          </div>
          <ul className="landing-trust-points">
            <li>
              <CheckCircle2 size={16} /> Personalized daily plan
            </li>
            <li>
              <CheckCircle2 size={16} /> Real-time AI support
            </li>
            <li>
              <CheckCircle2 size={16} /> Topic-level insights
            </li>
          </ul>
        </div>

        <div
          className="landing-hero-image-wrap"
          aria-label="AI learning visualization"
        >
          <img
            src={heroImage}
            alt="AI-powered learning interface"
            className="landing-hero-image"
          />
          <div className="hero-stat hero-stat-top">12k+ learners</div>
          <div className="hero-stat hero-stat-bottom">
            Average score boost: 28%
          </div>
        </div>
      </section>

      <section
        id="main_toolkits"
        className="toolkits-section"
        aria-labelledby="toolkits-header"
        data-path="main_toolkits"
      >
        <h2 id="toolkits-header" className="toolkits-title">
          Toolkits to make your preparation accurate, fast, and unstoppable
        </h2>

        <div
          className="toolkit-tabs"
          role="tablist"
          aria-label="Toolkit categories"
        >
          {toolkits.map((toolkit, idx) => (
            <button
              key={toolkit.id}
              className={`toolkit-tab ${idx === activeIndex ? "active" : ""}`}
              onClick={() => setActiveIndex(idx)}
              role="tab"
              aria-selected={idx === activeIndex}
            >
              {toolkit.name}
            </button>
          ))}
        </div>

        <div className="toolkit-showcase container-wide">
          <button
            className="toolkit-nav"
            aria-label="Previous toolkit"
            onClick={goPrev}
          >
            <ArrowLeft size={22} />
          </button>

          <div className="toolkit-flex-row" aria-live="polite">
            <article className="toolkit-side-card" aria-hidden="true">
              <h3>{previousToolkit.name}</h3>
              <img
                src={previousToolkit.image}
                alt={`${previousToolkit.name} preview`}
              />
            </article>

            <article
              key={activeToolkit.id}
              className="toolkit-main-card"
              role="group"
              aria-label={`${activeIndex + 1} / ${toolkits.length}`}
            >
              <h3 className="toolkit-card-title">{activeToolkit.name}</h3>
              <ul className="toolkit-list">
                {activeToolkit.points.map((point) => (
                  <li key={point}>{point}</li>
                ))}
              </ul>

              <div
                className="toolkit-image-stage"
                aria-label={`${activeToolkit.name} screenshots`}
              >
                <img
                  src={activeToolkit.image}
                  alt={`${activeToolkit.name} screenshot`}
                  className="toolkit-main-image"
                />
                {activeToolkit.overlayImage ? (
                  <img
                    src={activeToolkit.overlayImage}
                    alt={`${activeToolkit.name} secondary screenshot`}
                    className="toolkit-overlay-image"
                  />
                ) : null}
              </div>

              <Link to={activeToolkit.to} className="toolkit-cta">
                {activeToolkit.cta}
              </Link>
            </article>

            <article className="toolkit-side-card" aria-hidden="true">
              <h3>{nextToolkit.name}</h3>
              <img
                src={nextToolkit.image}
                alt={`${nextToolkit.name} preview`}
              />
            </article>
          </div>

          <button
            className="toolkit-nav"
            aria-label="Next toolkit"
            onClick={goNext}
          >
            <ArrowRight size={22} />
          </button>
        </div>

        <div className="toolkit-pagination" aria-label="Slide pagination">
          {toolkits.map((toolkit, idx) => (
            <button
              key={toolkit.id}
              className={`toolkit-dot ${idx === activeIndex ? "active" : ""}`}
              aria-label={`Go to slide ${idx + 1}`}
              aria-current={idx === activeIndex}
              onClick={() => setActiveIndex(idx)}
            />
          ))}
        </div>
      </section>

      <section
        id="features"
        className="highlights-section container-wide"
        aria-labelledby="features-header"
      >
        <h2 id="features-header">Feature Showcase</h2>
        <p>
          Designed for students who want sharp understanding, better retention,
          and consistent score growth.
        </p>

        <div className="highlights-grid">
          {highlights.map((item) => {
            const Icon = item.icon;
            return (
              <article key={item.title} className="highlight-card">
                <div className="highlight-icon">
                  <Icon size={18} />
                </div>
                <h3>{item.title}</h3>
                <p>{item.desc}</p>
              </article>
            );
          })}
        </div>
      </section>

      <section
        id="reviews"
        className="reviews-section container-wide"
        aria-labelledby="reviews-header"
      >
        <h2 id="reviews-header">What learners say</h2>

        <div className="testimonial-controls" aria-label="Testimonial controls">
          <button onClick={goPrevReview} aria-label="Previous testimonial">
            <ArrowLeft size={20} />
          </button>
          <span>
            {activeReviewIndex + 1} / {reviews.length}
          </span>
          <button onClick={goNextReview} aria-label="Next testimonial">
            <ArrowRight size={20} />
          </button>
        </div>

        <article key={activeReview.name} className="featured-quote-card">
          <p className="featured-quote">"{activeReview.quote}"</p>
          <div className="featured-author">
            <div className="featured-avatar" aria-hidden="true">
              {initials}
            </div>
            <strong>{activeReview.name}</strong>
            <span>{activeReview.role}</span>
          </div>
        </article>

        <div className="reviews-grid">
          {reviews.map((item) => (
            <article key={item.name} className="review-card">
              <p>{item.review}</p>
              <div>
                <strong>{item.name}</strong>
                <span>{item.role}</span>
              </div>
            </article>
          ))}
        </div>
      </section>

      <footer className="landing-footer">
        <div className="container-wide footer-top-row">
          <button className="footer-contact-btn" type="button">
            Contact us
          </button>
          <p>USA, 800 Boylston Street, Suite 2475, Boston, MA 02199</p>
          <button className="footer-cta-btn" type="button">
            Get started with StudIQ!
          </button>
        </div>

        <div className="container-wide footer-links-grid">
          {footerColumns.map((column) => (
            <section key={column.heading}>
              <h3>{column.heading}</h3>
              <ul>
                {column.links.map((link) => (
                  <li key={link}>
                    <a href="#" onClick={(event) => event.preventDefault()}>
                      {link}
                    </a>
                  </li>
                ))}
              </ul>
            </section>
          ))}
        </div>
      </footer>
    </main>
  );
};

export default LandingPage;
