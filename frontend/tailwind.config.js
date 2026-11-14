/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,ts}'],
  darkMode: 'class',
  theme: {
    // Radio binario: todo es rectangular salvo los controles circulares (rounded-full).
    borderRadius: { none: '0', sm: '0', DEFAULT: '0', md: '0', lg: '0', xl: '0', '2xl': '0', '3xl': '0', full: '9999px' },
    extend: {
      fontFamily: {
        // Inter es el sustituto abierto de BMW Type Next Latin: 700 para titulares, 300 para cuerpo.
        titulo: ['"Inter Variable"', '-apple-system', 'BlinkMacSystemFont', '"Segoe UI"', 'Roboto', 'sans-serif'],
        sans: ['"Inter Variable"', '-apple-system', 'BlinkMacSystemFont', '"Segoe UI"', 'Roboto', 'sans-serif'],
      },
      // Par de pesos de la marca: titulares "estampados" (700) frente a cuerpo ligero (300).
      fontWeight: { medium: '400', semibold: '700' },
      letterSpacing: { maquinado: '1.5px' },
      fontSize: {
        'display-xl': ['80px', { lineHeight: '1', letterSpacing: '-0.5px', fontWeight: '700' }],
        'display-lg': ['56px', { lineHeight: '1.05', letterSpacing: '-0.5px', fontWeight: '700' }],
        'display-md': ['40px', { lineHeight: '1.1', letterSpacing: '-0.5px', fontWeight: '700' }],
        'display-sm': ['32px', { lineHeight: '1.15', letterSpacing: '0', fontWeight: '700' }],
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
      // «nav»: ancho a partir del cual cabe la navegación horizontal completa sin apretarse.
      screens: { nav: '1360px' },
      spacing: { seccion: '96px' },
      maxWidth: { contenido: '1440px' },
      transitionDuration: { DEFAULT: '240ms' },
    },
  },
  plugins: [],
}
