/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",  // Make sure this points to your HTML file or any file that contains Tailwind classes
    "./renderer.js", // Add any JS files where you may use Tailwind classes
    "./styles.css",  // Include your styles file
  ],
  theme: {
    extend: {
      backgroundImage: {
        'catchmeifyoucan': "url('/panam.png')", // Ensure the path matches the root of the project
      }
    },
  },
  plugins: [],
}