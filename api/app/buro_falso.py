"""Simula el buró de crédito externo. No lo modifiques: es «el proveedor».

Cada llamada a `consultar` tarda y **cuesta plata**. El contador
`consultas_cobradas` es lo que nos facturaría el proveedor.
"""

import hashlib
import time

SCORES_CONOCIDOS = {
    "41234567": 820,  # Ana
    "38765432": 310,  # Bruno
    "52223334": 640,  # Carla
}


class BuroFalso:
    def __init__(self, demora_segundos: float = 0.3):
        self.demora_segundos = demora_segundos
        self.consultas_cobradas = 0

    def consultar(self, cedula: str) -> int:
        time.sleep(self.demora_segundos)
        self.consultas_cobradas += 1
        if cedula in SCORES_CONOCIDOS:
            return SCORES_CONOCIDOS[cedula]
        return int(hashlib.sha256(cedula.encode()).hexdigest(), 16) % 1000


buro = BuroFalso()
