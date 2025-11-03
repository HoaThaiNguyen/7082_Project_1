/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./kairos/templates/**/*.html",
    "./events/templates/**/*.html",
    "./kairos/**/*.py",
    "./events/**/*.py",
    "./**/*.html",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          100: '#5A6AB7',
          200: '#3567CC',
        },
        secondary: '#38369A',
        dark: '#15151A',
        light: '#F3F0FF',
        notify: '#B31157',
      },
    },
  },
  plugins: [],
};
