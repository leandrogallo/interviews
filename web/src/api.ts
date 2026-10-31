const URL_API = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

export type Cliente = { id: number; nombre: string };
export type Oferta = {
  id: number;
  monto: number;
  plazo_meses: number;
  tea: number;
  comision: number;
  estado: string;
};

async function pedir<T>(ruta: string, clienteId: number | null, init?: RequestInit): Promise<T> {
  const r = await fetch(`${URL_API}${ruta}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(clienteId ? { "X-Cliente-Id": String(clienteId) } : {}),
      ...init?.headers,
    },
  });
  if (!r.ok) {
    const cuerpo = await r.json().catch(() => ({}));
    throw new Error(cuerpo.detail ?? `error_${r.status}`);
  }
  return r.json();
}

export const api = {
  clientes: () => pedir<Cliente[]>("/clientes", null),
  crearOferta: (clienteId: number, monto: number, plazoMeses: number) =>
    pedir<Oferta>("/ofertas", clienteId, {
      method: "POST",
      body: JSON.stringify({ monto, plazo_meses: plazoMeses }),
    }),
};
