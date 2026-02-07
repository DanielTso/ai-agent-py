import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      colors: {
        primary: { DEFAULT: "#1e40af", light: "#3b82f6", dark: "#1e3a8a" },
        danger: { DEFAULT: "#dc2626", light: "#f87171" },
        warning: { DEFAULT: "#f59e0b", light: "#fbbf24" },
        success: { DEFAULT: "#16a34a", light: "#4ade80" },
      },
    },
  },
  plugins: [],
};
export default config;
