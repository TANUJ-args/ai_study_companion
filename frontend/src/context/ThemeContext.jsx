/* eslint-disable react-refresh/only-export-components */
import React, { createContext, useContext, useState, useEffect } from "react";

const ThemeContext = createContext();

export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error("useTheme must be used within a ThemeProvider");
  }
  return context;
};

export const ThemeProvider = ({ children }) => {
  const [theme, setTheme] = useState("theme-cyber-dark");

  useEffect(() => {
    document.documentElement.classList.remove(
      "theme-cyber-dark",
      "theme-cyber-light",
      "theme-stream-dark",
      "theme-stream-light",
    );
    document.documentElement.classList.add(theme);
    window.localStorage.setItem("ai-tutor-theme", theme);
  }, [theme]);

  const themes = [
    {
      id: "theme-cyber-dark",
      name: "Cyber Dark",
      colors: {
        bg: "#26104F",
        card: "#35176D",
        primary: "#8F63F9",
        secondary: "#FF7A3D",
      },
    },
    {
      id: "theme-cyber-light",
      name: "Cyber Light",
      colors: {
        bg: "#FFFAFF",
        card: "#FFFFFF",
        primary: "#7A4AE2",
        secondary: "#FF7A3D",
      },
    },
    {
      id: "theme-stream-dark",
      name: "Stream Dark",
      colors: {
        bg: "#200A43",
        card: "#311261",
        primary: "#A37EFF",
        secondary: "#FF8E4D",
      },
    },
    {
      id: "theme-stream-light",
      name: "Stream Light",
      colors: {
        bg: "#FFF8FE",
        card: "#FFFFFF",
        primary: "#7444D8",
        secondary: "#FF7B33",
      },
    },
  ];

  return (
    <ThemeContext.Provider value={{ theme, setTheme, themes }}>
      {children}
    </ThemeContext.Provider>
  );
};
