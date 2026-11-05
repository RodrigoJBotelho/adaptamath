"""Dificuldade adaptativa com pontuação no estilo Elo."""
DIFICULDADE = {1: 900, 2: 1100, 3: 1300}
K = 32


def nivel_para(rating):
    return 1 if rating < 1050 else 2 if rating < 1200 else 3


def atualizar(rating, nivel, acertou):
    esperado = 1 / (1 + 10 ** ((DIFICULDADE[nivel] - rating) / 400))
    return round(rating + K * ((1 if acertou else 0) - esperado))
