/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html", // Project-level templates
    "./events/templates/**/*.html", // App-specific templates
    "./static/**/*.css", // Static CSS files
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};
