import { useEffect, useState } from "react";
import { api, type Oferta } from "../api";
import { guardarBorrador, leerBorrador, type Borrador } from "./borrador";

/** Formulario de solicitud en 3 pasos. El borrador se guarda para retomarlo. */
export function Solicitud({ clienteId }: { clienteId: number }) {
  const [b, setB] = useState<Borrador>(() => leerBorrador());
  const [oferta, setOferta] = useState<Oferta | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => guardarBorrador(b), [b]);

  const cambiar = (campo: keyof Borrador) => (e: { target: { value: string } }) =>
    setB({ ...b, [campo]: e.target.value });

  async function enviar() {
    setError(null);
    try {
      setOferta(await api.crearOferta(clienteId, Number(b.monto), Number(b.plazoMeses)));
    } catch (e) {
      setError((e as Error).message);
    }
  }

  if (oferta) {
    return (
      <section>
        <h2>¡Solicitud enviada!</h2>
        <p>
          Oferta #{oferta.id}: ${oferta.monto} a {oferta.plazo_meses} meses.
        </p>
      </section>
    );
  }

  return (
    <section>
      <h2>Pedí tu préstamo · paso {b.paso} de 3</h2>

      {b.paso === 1 && (
        <>
          <label>
            Monto <input value={b.monto} onChange={cambiar("monto")} inputMode="decimal" />
          </label>
          <label>
            Plazo
            <select value={b.plazoMeses} onChange={cambiar("plazoMeses")}>
              <option value="3">3 meses</option>
              <option value="6">6 meses</option>
              <option value="12">12 meses</option>
            </select>
          </label>
          <button onClick={() => setB({ ...b, paso: 2 })}>Siguiente</button>
        </>
      )}

      {b.paso === 2 && (
        <>
          <label>
            Teléfono <input value={b.telefono} onChange={cambiar("telefono")} />
          </label>
          <label>
            Dirección <input value={b.direccion} onChange={cambiar("direccion")} />
          </label>
          <button onClick={() => setB({ ...b, paso: 1 })}>Atrás</button>
          <button onClick={() => setB({ ...b, paso: 3 })}>Siguiente</button>
        </>
      )}

      {b.paso === 3 && (
        <>
          <p>
            Pedís ${b.monto} a {b.plazoMeses} meses. Te contactamos al {b.telefono}.
          </p>
          <button onClick={() => setB({ ...b, paso: 2 })}>Atrás</button>
          <button onClick={enviar}>Confirmar</button>
        </>
      )}

      {error && <p role="alert">No pudimos enviar la solicitud ({error}).</p>}
    </section>
  );
}
