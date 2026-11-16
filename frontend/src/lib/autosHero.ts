import bmwM2 from '@/assets/images/hero/bmw-m2.png'
import fordMustang from '@/assets/images/hero/ford-mustang.png'
import hyundaiIoniq6 from '@/assets/images/hero/hyundai-ioniq-6.png'
import subaruWrx from '@/assets/images/hero/subaru-wrx.png'
import hondaCivic from '@/assets/images/hero/honda-civic.png'
import toyotaCorollaCross from '@/assets/images/hero/toyota-corolla-cross.png'
import mazdaCx30 from '@/assets/images/hero/mazda-cx-30.png'

/** Dato del tercer punto: cambia por auto para que cada uno cuente algo distinto. */
export type DatoExtra = 'aceleracion' | 'consumo' | 'autonomia' | 'traccion' | 'fiabilidad' | 'baul'

/** Posición de un punto en % de la imagen (x desde la izquierda, y desde arriba). */
type Punto = [number, number]

export interface AutoHero {
  slug: string
  nombre: string
  imagen: string
  alto: number
  alt: string
  credito: { autor: string; licencia: string; url: string }
  /** Puntos sobre el motor (capó), la puerta (costo) y un tercer lugar con el dato extra. */
  puntos: { motor: Punto; costo: Punto; extra: Punto }
  extra: DatoExtra
  /** Pregunta del titular mientras se muestra este auto: [parte en acento, resto]. La responde el tercer punto. */
  pregunta: [string, string]
}

/** Autos del hero: fotos reales con fondo eliminado (ancho 1400 px), todos mirando a la izquierda. Rotan cada minuto. */
export const AUTOS_HERO: AutoHero[] = [
  {
    slug: 'bmw-m2-2025-m2-coupe-at', nombre: 'BMW M2 2025', imagen: bmwM2, alto: 632,
    alt: 'BMW M2 blanco visto de tres cuartos frontal',
    credito: { autor: 'Alexander-93', licencia: 'CC BY-SA 4.0', url: 'https://commons.wikimedia.org/wiki/File:BMW_G87_M2_1X7A1838.jpg' },
    puntos: { motor: [30, 36], costo: [78, 50], extra: [56, 76] }, extra: 'aceleracion',
    pregunta: ['¿Es', 'rápido?'],
  },
  {
    slug: 'ford-mustang-2026-dark-horse-5-0-v8-at', nombre: 'Ford Mustang 2026', imagen: fordMustang, alto: 673,
    alt: 'Ford Mustang azul visto de tres cuartos frontal',
    credito: { autor: 'Alexander Migl', licencia: 'CC BY-SA 4.0', url: 'https://commons.wikimedia.org/wiki/File:Ford_Mustang_VII_GT_Rutesheimer_Autoschau_2025_DSC_9234.jpg' },
    puntos: { motor: [28, 36], costo: [82, 48], extra: [56, 78] }, extra: 'aceleracion',
    pregunta: ['¿Es', 'rápido?'],
  },
  {
    slug: 'hyundai-ioniq-6-2025-long-range-rwd', nombre: 'Hyundai Ioniq 6 2025', imagen: hyundaiIoniq6, alto: 621,
    alt: 'Hyundai Ioniq 6 gris visto de tres cuartos frontal',
    credito: { autor: 'Kevauto', licencia: 'CC BY-SA 4.0', url: 'https://commons.wikimedia.org/wiki/File:2023_Hyundai_Ioniq_6_Limited,_front_4.27.23.jpg' },
    puntos: { motor: [28, 38], costo: [72, 48], extra: [50, 76] }, extra: 'autonomia',
    pregunta: ['¿Llega', 'lejos?'],
  },
  {
    slug: 'subaru-wrx-2026-gt-2-4t-spt-awd', nombre: 'Subaru WRX 2026', imagen: subaruWrx, alto: 675,
    alt: 'Subaru WRX azul visto de tres cuartos frontal',
    credito: { autor: 'Elise240SX', licencia: 'CC BY-SA 4.0', url: 'https://commons.wikimedia.org/wiki/File:2022_Subaru_WRX_Sport-Tech_in_World_Rally_Blue_Pearl,_Front_Left,_06-03-2022.jpg' },
    puntos: { motor: [24, 36], costo: [76, 52], extra: [55, 80] }, extra: 'traccion',
    pregunta: ['¿Se agarra', 'bien?'],
  },
  {
    slug: 'honda-civic-2026-e-hev-touring', nombre: 'Honda Civic e:HEV 2026', imagen: hondaCivic, alto: 657,
    alt: 'Honda Civic blanco visto de tres cuartos frontal',
    credito: { autor: 'M 93', licencia: 'CC BY-SA 3.0 DE', url: 'https://commons.wikimedia.org/wiki/File:Honda_Civic_e-HEV_Sport_(XI)_%E2%80%93_f_30062024.jpg' },
    puntos: { motor: [24, 40], costo: [70, 50], extra: [90, 30] }, extra: 'fiabilidad',
    pregunta: ['¿Es', 'confiable?'],
  },
  {
    slug: 'toyota-corolla-cross-2026-gr-sport-hev', nombre: 'Toyota Corolla Cross 2026', imagen: toyotaCorollaCross, alto: 672,
    alt: 'Toyota Corolla Cross blanca vista de tres cuartos frontal',
    credito: { autor: 'Mr.choppers', licencia: 'CC BY-SA 3.0', url: 'https://commons.wikimedia.org/wiki/File:2023_Toyota_Corolla_Cross_XLE_4WD_in_Wind_Chill_Pearl,_front_left.jpg' },
    puntos: { motor: [30, 34], costo: [72, 48], extra: [46, 80] }, extra: 'consumo',
    pregunta: ['¿Es', 'rendidor?'],
  },
  {
    slug: 'mazda-cx-30-2026-carbon-turbo-awd', nombre: 'Mazda CX-30 2026', imagen: mazdaCx30, alto: 683,
    alt: 'Mazda CX-30 blanca vista de tres cuartos frontal',
    credito: { autor: 'EurovisionNim', licencia: 'CC BY-SA 4.0', url: 'https://commons.wikimedia.org/wiki/File:Mazda_CX-30_Touring,_2020_front.jpg' },
    puntos: { motor: [24, 40], costo: [78, 44], extra: [92, 26] }, extra: 'baul',
    pregunta: ['¿Le cabe', 'todo?'],
  },
]

/** Cada cuánto cambia el auto del hero. */
export const ROTACION_MS = 60_000
