"""
Testes para o módulo venda_imovel.py
"""

import pytest
from venda_imovel import Comprador, Imovel, MAX_COMPRADORES


def make_imovel():
    return Imovel(endereco="Rua das Flores, 123", valor=500000.00)


def make_comprador(n=1):
    return Comprador(nome=f"Comprador {n}", cpf=f"000.000.000-0{n}")


# ── Testes básicos ──────────────────────────────────────────────────────────────

def test_adicionar_um_comprador():
    imovel = make_imovel()
    imovel.adicionar_comprador(make_comprador(1))
    assert len(imovel.compradores) == 1


def test_adicionar_tres_compradores():
    imovel = make_imovel()
    for i in range(1, 4):
        imovel.adicionar_comprador(make_comprador(i))
    assert len(imovel.compradores) == MAX_COMPRADORES


def test_nao_adicionar_mais_de_tres_compradores():
    imovel = make_imovel()
    for i in range(1, 4):
        imovel.adicionar_comprador(make_comprador(i))
    with pytest.raises(ValueError, match="3 compradores"):
        imovel.adicionar_comprador(make_comprador(4))


def test_finalizar_venda_com_tres_compradores():
    imovel = make_imovel()
    for i in range(1, 4):
        imovel.adicionar_comprador(make_comprador(i))
    resultado = imovel.finalizar_venda()
    assert imovel.vendido is True
    assert "Comprador 1" in resultado
    assert "Comprador 2" in resultado
    assert "Comprador 3" in resultado


def test_finalizar_venda_sem_compradores_falha():
    imovel = make_imovel()
    with pytest.raises(ValueError, match="ao menos um comprador"):
        imovel.finalizar_venda()


def test_adicionar_comprador_apos_venda_falha():
    imovel = make_imovel()
    imovel.adicionar_comprador(make_comprador(1))
    imovel.finalizar_venda()
    with pytest.raises(ValueError, match="já foi vendido"):
        imovel.adicionar_comprador(make_comprador(2))


def test_resultado_contem_valor_e_endereco():
    imovel = make_imovel()
    imovel.adicionar_comprador(make_comprador(1))
    resultado = imovel.finalizar_venda()
    assert "500000.00" in resultado
    assert "Rua das Flores, 123" in resultado
