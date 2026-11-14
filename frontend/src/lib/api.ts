export interface ErrorApi {
  codigo: string
  mensaje: string
  detalle?: unknown
}

export class FalloApi extends Error {
  constructor(public estado: number, public cuerpo: ErrorApi) {
    super(cuerpo.mensaje)
  }
}

type Params = Record<string, string | number | boolean | (string | number)[] | null | undefined>

export function query(params: Params = {}): string {
  const sp = new URLSearchParams()
  for (const [k, v] of Object.entries(params)) {
    if (v === undefined || v === null || v === '') continue
    if (Array.isArray(v)) v.forEach((x) => sp.append(k, String(x)))
    else sp.set(k, String(v))
  }
  const s = sp.toString()
  return s ? `?${s}` : ''
}

async function pedir<T>(url: string, init?: RequestInit): Promise<T> {
  let r: Response
  try {
    r = await fetch(url, { headers: { 'Content-Type': 'application/json' }, ...init })
  } catch {
    throw new FalloApi(0, { codigo: 'sin_conexion', mensaje: 'Sin conexión con el servidor' })
  }
  if (!r.ok) {
    const cuerpo = await r.json().catch(() => ({ codigo: 'error', mensaje: r.statusText }))
    throw new FalloApi(r.status, cuerpo)
  }
  return r.json() as Promise<T>
}

export const api = {
  get: <T>(ruta: string, params?: Params) => pedir<T>(`/api${ruta}${query(params)}`),
  post: <T>(ruta: string, cuerpo: unknown) => pedir<T>(`/api${ruta}`, { method: 'POST', body: JSON.stringify(cuerpo) }),
}
