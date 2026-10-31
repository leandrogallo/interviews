import { useEffect, useState } from "react";
import { api, type Cliente } from "./api";
import { Solicitud } from "./solicitud/Solicitud";

const CLAVE_SESION = "cliente-actual";

/** Simula el login: elegís con qué cliente estás «logueado». */
export function App() {
  const [clientes, setClientes] = useState<Cliente[]>([]);
  const [clienteId, setClienteId] = useState<number | null>(() => {
    const guardado = localStorage.getItem(CLAVE_SESION);
    return guardado ? Number(guardado) : null;
  });

  useEffect(() => {
    api.clientes().then(setClientes).catch(() => setClientes([]));
  }, []);

  function entrar(id: number) {
    localStorage.setItem(CLAVE_SESION, String(id));
    setClienteId(id);
  }

  function salir() {
    localStorage.removeItem(CLAVE_SESION);
    setClienteId(null);
  }

  if (clienteId === null) {
    return (
      <main>
        <h1>Mini-crédito</h1>
        <p>¿Con qué cliente entrás?</p>
        {clientes.map((c) => (
          <button key={c.id} onClick={() => entrar(c.id)}>
            {c.nombre}
          </button>
        ))}
      </main>
    );
  }

  const nombre = clientes.find((c) => c.id === clienteId)?.nombre ?? "";
  return (
    <main>
      <header>
        Hola, {nombre} · <button onClick={salir}>Salir</button>
      </header>
      <Solicitud clienteId={clienteId} />
    </main>
  );
}
