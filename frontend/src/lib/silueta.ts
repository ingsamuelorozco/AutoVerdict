/**
 * Geometría de siluetas esquemáticas a escala real (milímetros).
 * Las formas son plantillas propias por carrocería, estiradas a las medidas reales:
 * no reproducen el diseño de ninguna marca.
 * Coordenadas: x = 0 en el extremo delantero; y = 0 en el suelo, creciendo hacia arriba.
 */
import type { Medidas } from './tipos'

type Punto = [number, number]

/** Línea superior del perfil: [fracción del largo, fracción de altura entre la base de la carrocería y el techo]. */
const PLANTILLAS: Record<string, Punto[]> = {
  Sedán: [[0, 0.18], [0.01, 0.42], [0.05, 0.5], [0.27, 0.58], [0.38, 0.94], [0.47, 1], [0.64, 0.98], [0.77, 0.64], [0.95, 0.6], [1, 0.48], [1, 0.16]],
  Hatchback: [[0, 0.18], [0.01, 0.42], [0.05, 0.52], [0.3, 0.6], [0.42, 0.95], [0.5, 1], [0.84, 0.98], [0.97, 0.78], [1, 0.55], [1, 0.16]],
  SUV: [[0, 0.18], [0.01, 0.5], [0.05, 0.6], [0.26, 0.66], [0.35, 0.96], [0.42, 1], [0.9, 0.99], [0.98, 0.9], [1, 0.62], [1, 0.16]],
  Pickup: [[0, 0.16], [0.01, 0.5], [0.04, 0.62], [0.2, 0.67], [0.28, 0.97], [0.33, 1], [0.52, 1], [0.56, 0.66], [1, 0.64], [1, 0.16]],
  Coupé: [[0, 0.16], [0.01, 0.38], [0.05, 0.46], [0.33, 0.55], [0.45, 0.95], [0.53, 1], [0.66, 0.96], [0.86, 0.62], [0.98, 0.56], [1, 0.4], [1, 0.14]],
  Convertible: [[0, 0.16], [0.01, 0.4], [0.05, 0.5], [0.36, 0.6], [0.44, 0.98], [0.47, 1], [0.6, 0.68], [0.95, 0.62], [1, 0.46], [1, 0.14]],
}

/** Ventanas (polígono en la misma escala de la plantilla). */
const VENTANAS: Record<string, Punto[]> = {
  Sedán: [[0.29, 0.62], [0.39, 0.9], [0.47, 0.94], [0.63, 0.92], [0.74, 0.64]],
  Hatchback: [[0.32, 0.64], [0.43, 0.9], [0.5, 0.94], [0.83, 0.92], [0.94, 0.7]],
  SUV: [[0.28, 0.7], [0.36, 0.92], [0.42, 0.95], [0.88, 0.94], [0.95, 0.72]],
  Pickup: [[0.21, 0.7], [0.29, 0.92], [0.33, 0.95], [0.51, 0.95], [0.53, 0.7]],
  Coupé: [[0.35, 0.6], [0.46, 0.9], [0.53, 0.94], [0.65, 0.9], [0.8, 0.64]],
  Convertible: [[0.38, 0.64], [0.45, 0.94], [0.47, 0.96], [0.55, 0.7]],
}

export function plantilla(carroceria: string): string {
  return PLANTILLAS[carroceria] ? carroceria : 'Sedán'
}

function geometriaBase(m: Medidas) {
  const r = (m.diametro_rueda_mm || 650) / 2
  const base = m.distancia_libre_suelo_mm // borde inferior de la carrocería
  const altoCuerpo = m.alto_mm - base
  const ejeDel = m.voladizo_delantero_mm
  const ejeTras = m.voladizo_delantero_mm + m.distancia_entre_ejes_mm
  return { r, base, altoCuerpo, ejeDel, ejeTras }
}

function punto(m: Medidas, [fx, fy]: Punto): Punto {
  const { base, altoCuerpo } = geometriaBase(m)
  return [fx * m.largo_mm, base + fy * altoCuerpo]
}

/** Arco de rueda: semicírculo un poco mayor que la rueda, cortado en la base de la carrocería. */
function arco(cx: number, r: number, base: number): string {
  const ra = r * 1.08
  const y0 = base
  const dy = Math.max(0, r - y0)
  const dx = Math.sqrt(Math.max(ra * ra - dy * dy, 0))
  return `L ${cx + dx} ${y0} A ${ra} ${ra} 0 0 0 ${cx - dx} ${y0}`
}

export interface PerfilLateral {
  cuerpo: string
  ventanas: string
  ruedas: { cx: number; cy: number; r: number }[]
  largo: number
  alto: number
}

/** Perfil lateral en coordenadas de mundo (mm, y hacia arriba). */
export function perfilLateral(m: Medidas): PerfilLateral {
  const tipo = plantilla(m.carroceria)
  const { r, base, ejeDel, ejeTras } = geometriaBase(m)
  const sup = PLANTILLAS[tipo].map((p) => punto(m, p))
  // Recorrido: borde inferior delantero → línea superior → borde inferior trasero → base con arcos (de atrás hacia adelante).
  let d = `M ${sup[0][0]} ${base} ` + sup.map(([x, y]) => `L ${x} ${y}`).join(' ')
  d += ` L ${m.largo_mm} ${base} `
  d += arco(ejeTras, r, base) + ' ' + arco(ejeDel, r, base) + ` L 0 ${base} Z`
  const v = VENTANAS[tipo].map((p) => punto(m, p))
  const ventanas = `M ${v.map(([x, y]) => `${x} ${y}`).join(' L ')} Z`
  return { cuerpo: d, ventanas, ruedas: [{ cx: ejeDel, cy: r, r }, { cx: ejeTras, cy: r, r }], largo: m.largo_mm, alto: m.alto_mm }
}

export interface Planta {
  cuerpo: { x: number; y: number; w: number; h: number; rx: number }
  espejos: { x: number; y: number; w: number; h: number }[]
  ruedas: { x: number; y: number; w: number; h: number }[]
  anchoTotal: number
}

/** Vista de planta: x a lo largo, y a lo ancho (centrado en 0). */
export function planta(m: Medidas): Planta {
  const ancho = m.ancho_sin_espejos_mm || 1800
  const anchoEsp = m.ancho_con_espejos_mm || ancho + 190
  const { r, ejeDel, ejeTras } = geometriaBase(m)
  const salienteEsp = (anchoEsp - ancho) / 2
  const xEsp = m.voladizo_delantero_mm + m.distancia_entre_ejes_mm * 0.28
  const anchoLlanta = 220
  return {
    cuerpo: { x: 0, y: -ancho / 2, w: m.largo_mm, h: ancho, rx: Math.min(260, ancho * 0.16) },
    espejos: [
      { x: xEsp, y: -anchoEsp / 2, w: 140, h: salienteEsp },
      { x: xEsp, y: ancho / 2, w: 140, h: salienteEsp },
    ],
    ruedas: [ejeDel, ejeTras].flatMap((cx) => [
      { x: cx - r, y: -ancho / 2 + 40, w: 2 * r, h: anchoLlanta },
      { x: cx - r, y: ancho / 2 - 40 - anchoLlanta, w: 2 * r, h: anchoLlanta },
    ]),
    anchoTotal: anchoEsp,
  }
}

/** Vista frontal: contorno simplificado (x centrado en 0, y hacia arriba). */
export function frontal(m: Medidas): { cuerpo: string; vidrio: string; ruedas: { x: number; y: number; w: number; h: number }[]; espejos: string } {
  const ancho = m.ancho_sin_espejos_mm || 1800
  const anchoEsp = m.ancho_con_espejos_mm || ancho + 190
  const base = m.distancia_libre_suelo_mm
  const alto = m.alto_mm
  const tipo = plantilla(m.carroceria)
  const hombro = base + (alto - base) * (tipo === 'SUV' || tipo === 'Pickup' ? 0.6 : 0.52)
  const techo = ancho * (tipo === 'SUV' || tipo === 'Pickup' ? 0.4 : 0.34)
  const a = ancho / 2
  const cuerpo = `M ${-a} ${base + 60} L ${-a} ${hombro} L ${-techo} ${alto} L ${techo} ${alto} L ${a} ${hombro} L ${a} ${base + 60} Q ${a} ${base} ${a - 60} ${base} L ${-a + 60} ${base} Q ${-a} ${base} ${-a} ${base + 60} Z`
  const vidrio = `M ${-a * 0.82} ${hombro + 40} L ${-techo + 40} ${alto - 50} L ${techo - 40} ${alto - 50} L ${a * 0.82} ${hombro + 40} Z`
  const r = (m.diametro_rueda_mm || 650) / 2
  const wl = 230
  const ruedas = [{ x: -a + 30, y: 0, w: wl, h: Math.min(2 * r, base + 200) }, { x: a - 30 - wl, y: 0, w: wl, h: Math.min(2 * r, base + 200) }]
  const ye = hombro + 30
  const espejos = `M ${-anchoEsp / 2} ${ye} h ${(anchoEsp - ancho) / 2} v 110 h ${-(anchoEsp - ancho) / 2} Z M ${anchoEsp / 2} ${ye} h ${-(anchoEsp - ancho) / 2} v 110 h ${(anchoEsp - ancho) / 2} Z`
  return { cuerpo, vidrio, ruedas, espejos }
}

/** Desplazamiento horizontal para alinear varias siluetas. */
export function desplazamiento(m: Medidas, alinear: 'rueda' | 'frente' | 'centro', referencia: number): number {
  if (alinear === 'frente') return 0
  if (alinear === 'centro') return (referencia - m.largo_mm) / 2
  return referencia - (m.voladizo_delantero_mm + m.distancia_entre_ejes_mm)
}

/** Silueta humana de 1,75 m (por defecto) como referencia de escala. */
export function persona(altura = 1750): string {
  const c = altura * 0.065
  const hombro = altura * 0.82
  const cadera = altura * 0.5
  return [
    `M 0 ${altura - c} m ${-c} 0 a ${c} ${c} 0 1 0 ${2 * c} 0 a ${c} ${c} 0 1 0 ${-2 * c} 0`,
    `M ${-altura * 0.12} ${hombro} L ${altura * 0.12} ${hombro} L ${altura * 0.09} ${cadera} L ${altura * 0.06} 0 L ${altura * 0.015} 0 L 0 ${cadera * 0.9} L ${-altura * 0.015} 0 L ${-altura * 0.06} 0 L ${-altura * 0.09} ${cadera} Z`,
  ].join(' ')
}

/** Trazos distintos para distinguir autos sin depender del color. */
export const TRAZOS = ['', '14 8', '4 6', '18 6 4 6', '2 4', '24 10', '10 4 2 4', '6 6', '30 6 6 6', '8 3']
/** Paleta apta para daltonismo (Okabe–Ito ampliada). */
export const COLORES = ['#0072B2', '#D55E00', '#009E73', '#CC79A7', '#E69F00', '#56B4E9', '#7F3C8D', '#3D3D3D', '#B8860B', '#1B7F5B']
