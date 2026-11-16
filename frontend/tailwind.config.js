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
        'acento-hondo': 'rgb(var(--acento-hondo) / <alpha-value>)',
        'acento-texto': 'rgb(var(--acento-texto) / <alpha-value>)',
        velo: 'rgb(var(--velo) / <alpha-value>)',
        mejor: 'rgb(var(--mejor) / <alpha-value>)',
        ambar: 'rgb(var(--ambar) / <alpha-value>)',
        roja: 'rgb(var(--roja) / <alpha-value>)',
      },
      // «nav»: ancho a partir del cual cabe la navegación horizontal completa sin apretarse.
      screens: { nav: '993px' },
      spacing: { seccion: '96px', barra: '72px' },
      maxWidth: { contenido: '1440px', landing: '1170px' },
      boxShadow: {
        tarjeta: '0 12px 40px -16px rgb(0 0 0 / 0.28)',
        menu: '0 14px 34px -10px rgb(0 0 0 / 0.4)',
      },
      keyframes: {
        pulso: {
          '0%': { boxShadow: '0 0 0 0 rgb(var(--acento) / 0.55)' },
          '70%': { boxShadow: '0 0 0 14px rgb(var(--acento) / 0)' },
          '100%': { boxShadow: '0 0 0 0 rgb(var(--acento) / 0)' },
        },
      },
      animation: { pulso: 'pulso 2.2s ease-out infinite' },
      transitionDuration: { DEFAULT: '240ms' },
    },
  },
  plugins: [],
}
