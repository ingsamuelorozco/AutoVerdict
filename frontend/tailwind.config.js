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
        cuerpo: 'rgb(var(--cuerpo) / <alpha-value>)',
        papel: 'rgb(var(--papel) / <alpha-value>)',
        suave: 'rgb(var(--suave) / <alpha-value>)',
        superficie: 'rgb(var(--superficie) / <alpha-value>)',
        elevada: 'rgb(var(--elevada) / <alpha-value>)',
        apagado: 'rgb(var(--apagado) / <alpha-value>)',
        'm-azul-claro': 'rgb(var(--m-azul-claro) / <alpha-value>)',
        'm-azul': 'rgb(var(--m-azul) / <alpha-value>)',
        'm-rojo': 'rgb(var(--m-rojo) / <alpha-value>)',
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
