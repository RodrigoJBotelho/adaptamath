from app.adaptive import atualizar, nivel_para
from app.generator import conferir, gerar
from app.solver import resolver


def test_equacao_1_grau():
    assert resolver("equacao", "2x + 3 = 7")["resposta"] == "x = 2"


def test_equacao_2_grau():
    r = resolver("equacao", "x^2 - 5x + 6 = 0")["resposta"]
    assert "x = 2" in r and "x = 3" in r


def test_derivada():
    assert "2 x + 3" in resolver("derivada", "x^2 + 3x")["resposta"]


def test_adaptativo():
    assert atualizar(1000, 1, True) > 1000
    assert atualizar(1000, 3, False) < 1000
    assert nivel_para(1000) == 1 and nivel_para(1300) == 3


def test_gerador_confere():
    for nivel in (1, 2, 3):
        ex = gerar(nivel)
        assert conferir(ex, ", ".join(str(r) for r in ex["respostas"]))
