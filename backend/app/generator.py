"""Gerador de exercícios por nível e conferência de respostas."""
import math
import random
import re


def _sinal(n):
    return f"+ {n}" if n >= 0 else f"- {abs(n)}"


def gerar(nivel):
    if nivel <= 1:
        a, x, b = random.randint(2, 9), random.randint(-9, 9), random.randint(-15, 15)
        return {
            "nivel": 1,
            "instrucao": "Resolva a equação:",
            "expressao": f"{a}x {_sinal(b)} = {a * x + b}",
            "respostas": [x],
        }
    if nivel == 2:
        while True:
            r1, r2 = random.randint(-6, 6), random.randint(-6, 6)
            if r1 and r2 and r1 != r2 and r1 + r2:
                break
        return {
            "nivel": 2,
            "instrucao": "Encontre as duas raízes (separe por vírgula):",
            "expressao": f"x^2 {_sinal(-(r1 + r2))}x {_sinal(r1 * r2)} = 0",
            "respostas": [r1, r2],
        }
    a, b, c = random.randint(1, 5), random.randint(-9, 9), random.randint(-4, 4)
    return {
        "nivel": 3,
        "instrucao": "Calcule a derivada de f no ponto indicado:",
        "expressao": f"f(x) = {a}x^2 {_sinal(b)}x,\\quad f'({c}) = ?",
        "respostas": [2 * a * c + b],
    }


def conferir(exercicio, texto):
    dados = sorted(float(n.replace(",", ".")) for n in re.findall(r"-?\d+(?:[.,]\d+)?", texto))
    certos = sorted(float(r) for r in exercicio["respostas"])
    return len(dados) == len(certos) and all(math.isclose(d, c) for d, c in zip(dados, certos))
