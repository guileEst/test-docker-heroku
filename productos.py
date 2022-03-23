class Producto:
    def __init__(self, titulo: str, valor: float, moneda: str):
        self.titulo = titulo
        self.valor = valor
        self.moneda = moneda

    def to_dict(self) -> dict:
        return{
            "title": self.titulo,
            "value": self.valor,
            "currency": self.moneda
        }