import { ref, shallowRef } from 'vue'
import { FalloApi } from '@/lib/api'

/** Estado de carga uniforme: datos, cargando, error y reintento. */
export function useCarga<T>(fn: () => Promise<T>) {
  const datos = shallowRef<T | null>(null)
  const cargando = ref(false)
  const error = ref<string | null>(null)
  let turno = 0
  async function ejecutar() {
    const mio = ++turno
    cargando.value = true
    error.value = null
    try {
      const r = await fn()
      if (mio === turno) datos.value = r
    } catch (e) {
      if (mio === turno) error.value = e instanceof FalloApi ? e.cuerpo.mensaje : String(e)
    } finally {
      if (mio === turno) cargando.value = false
    }
  }
  return { datos, cargando, error, ejecutar }
}
