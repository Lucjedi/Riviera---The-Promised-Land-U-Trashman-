"""
venda_imovel.py - Módulo para venda de imóvel para até 3 compradores.
"""

MAX_COMPRADORES = 3


class Comprador:
    def __init__(self, nome, cpf):
        self.nome = nome
        self.cpf = cpf

    def __repr__(self):
        return f"Comprador(nome={self.nome!r}, cpf={self.cpf!r})"


class Imovel:
    def __init__(self, endereco, valor):
        self.endereco = endereco
        self.valor = valor
        self.compradores = []
        self.vendido = False

    def adicionar_comprador(self, comprador):
        if self.vendido:
            raise ValueError("Imóvel já foi vendido.")
        if len(self.compradores) >= MAX_COMPRADORES:
            raise ValueError(
                f"Não é possível adicionar mais de {MAX_COMPRADORES} compradores."
            )
        self.compradores.append(comprador)

    def finalizar_venda(self):
        if not self.compradores:
            raise ValueError("É necessário ao menos um comprador para finalizar a venda.")
        self.vendido = True
        nomes = ", ".join(c.nome for c in self.compradores)
        return (
            f"Imóvel '{self.endereco}' vendido por R$ {self.valor:.2f} "
            f"para: {nomes}."
        )

    def __repr__(self):
        return (
            f"Imovel(endereco={self.endereco!r}, valor={self.valor!r}, "
            f"compradores={self.compradores!r}, vendido={self.vendido!r})"
        )
