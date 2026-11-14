/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,ts}'],
  darkMode: 'class',
  theme: {
    extend: {
      fontFamily: {
        titulo: ['"Fraunces Variable"', 'Georgia', 'serif'],
        sans: ['"Inter Variable"', 'system-ui', 'sans-serif'],
      },
      colors: {
        tinta: 'rgb(var(--tinta) / <alpha-value>)',
        papel: 'rgb(var(--papel) / <alpha-value>)',
        superficie: 'rgb(var(--superficie) / <alpha-value>)',
        linea: 'rgb(var(--linea) / <alpha-value>)',
        tenue: 'rgb(var(--tenue) / <alpha-value>)',
        acento: 'rgb(var(--acento) / <alpha-value>)',
        mejor: 'rgb(var(--mejor) / <alpha-value>)',
        ambar: 'rgb(var(--ambar) / <alpha-value>)',
        roja: 'rgb(var(--roja) / <alpha-value>)',
      },
      transitionDuration: { DEFAULT: '240ms' },
    },
  },
  plugins: [],
}
