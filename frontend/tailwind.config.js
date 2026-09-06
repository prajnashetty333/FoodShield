/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        profile: {
          A: '#0e9f6a', // Current Network
          B: '#2bbf8a', // Historical Recovery
          C: '#2a7de1', // New Origin
          D: '#e23b2a', // Gap / Structural Constraint
        }
      },
      fontFamily: {
        serif: ['"Source Serif 4"', 'Georgia', 'serif'],
        sans: ['"Source Sans 3"', 'system-ui', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
