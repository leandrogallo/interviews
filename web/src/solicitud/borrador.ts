export type Borrador = {
  paso: 1 | 2 | 3;
  monto: string;
  plazoMeses: string;
  telefono: string;
  direccion: string;
};

export const BORRADOR_VACIO: Borrador = {
  paso: 1,
  monto: "",
  plazoMeses: "6",
  telefono: "",
  direccion: "",
};

const CLAVE = "borrador-solicitud";

export function leerBorrador(): Borrador {
  try {
    const crudo = localStorage.getItem(CLAVE);
    return crudo ? { ...BORRADOR_VACIO, ...JSON.parse(crudo) } : BORRADOR_VACIO;
  } catch {
    return BORRADOR_VACIO;
  }
}

export function guardarBorrador(borrador: Borrador): void {
  localStorage.setItem(CLAVE, JSON.stringify(borrador));
}
