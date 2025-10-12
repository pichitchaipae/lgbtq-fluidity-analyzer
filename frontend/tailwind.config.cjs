/* eslint-env node */
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        pride: {
          50: "#f8f6ff",
          100: "#f1edff",
          200: "#e2dbff",
          300: "#c8b3ff",
          400: "#9d71ff",
          500: "#825bff",
          600: "#6136d6",
          700: "#4c29ab",
          800: "#3e2388",
          900: "#321b6b",
        },
      },
    },
  },
  plugins: [],
};
