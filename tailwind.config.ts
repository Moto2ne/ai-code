import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}",
    "./lib/**/*.{js,ts,jsx,tsx}"
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: "#ecf8ff",
          100: "#d5ecff",
          200: "#aad8ff",
          300: "#7dc2ff",
          400: "#4aa9ff",
          500: "#1b8fff",
          600: "#0f74e0",
          700: "#0a5cb5",
          800: "#08488b",
          900: "#073b71"
        }
      }
    }
  },
  plugins: []
};

export default config;
