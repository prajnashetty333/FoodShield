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
          A: '#22c55e', // green-500
          B: '#3b82f6', // blue-500
          C: '#f97316', // orange-500
          D: '#ef4444', // red-500
        }
      }
    },
  },
  plugins: [],
}
