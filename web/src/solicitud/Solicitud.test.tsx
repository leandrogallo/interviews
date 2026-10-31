import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { Solicitud } from "./Solicitud";

beforeEach(() => localStorage.clear());

test("avanza por los 3 pasos y muestra el resumen", async () => {
  render(<Solicitud clienteId={1} />);
  await userEvent.type(screen.getByLabelText(/monto/i), "15000");
  await userEvent.click(screen.getByText("Siguiente"));
  await userEvent.type(screen.getByLabelText(/teléfono/i), "099123456");
  await userEvent.click(screen.getByText("Siguiente"));
  expect(screen.getByText(/pedís \$15000 a 6 meses/i)).toBeInTheDocument();
});

test("retoma el borrador al volver a entrar", async () => {
  const { unmount } = render(<Solicitud clienteId={1} />);
  await userEvent.type(screen.getByLabelText(/monto/i), "8000");
  unmount();
  render(<Solicitud clienteId={1} />);
  expect(screen.getByLabelText(/monto/i)).toHaveValue("8000");
});
