class Bitcoin:
    def __init__(self, simbolo: str, base: str, precioSinConvertir: float, precio: float, cambio24H: float, spread: float, creado: str, actualizado: str):
        self.simbolo = simbolo
        self.base = base
        self.precioSinConvertir = precioSinConvertir
        self.precio = precio
        self.cambio24H = cambio24H
        self.spread = spread
        self.creado = creado
        self.actualizado = actualizado

    def to_dict(self) -> dict:
        return{
            "symbol": self.simbolo,
            "base_asset": self.base,
            "price_unconverted": self.precioSinConvertir,
            "price": self.precio,
            "change_24h": self.cambio24H,
            "spread": self.spread,
            "created_at": self.creado,
            "updated_at": self.actualizado
        }