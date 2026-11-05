"""Resolvedor simbólico passo a passo, feito com SymPy."""
import re

from sympy import Poly, diff, factor, integrate, latex, solve, symbols
from sympy.parsing.sympy_parser import (
    convert_xor,
    implicit_multiplication_application,
    parse_expr,
    standard_transformations,
)

X = symbols("x")
_TRANSF = standard_transformations + (implicit_multiplication_application, convert_xor)
_PERMITIDO = re.compile(r"^[0-9xX+\-*/^().=\s]{1,100}$")


class EntradaInvalida(ValueError):
    pass


def _ler(txt):
    # Lista branca de caracteres: o texto nunca chega ao parser com letras ou nomes livres.
    if not _PERMITIDO.match(txt):
        raise EntradaInvalida("Use apenas números, x, + - * / ^ ( ) e =.")
    if re.search(r"\d{4,}", txt) or re.search(r"\d\s*\^", txt):
        raise EntradaInvalida("Use números de até 3 dígitos e ^ só depois de x ou de parênteses.")
    try:
        return parse_expr(txt.lower(), local_dict={"x": X}, transformations=_TRANSF)
    except Exception:
        raise EntradaInvalida("Não consegui entender a expressão.")


def _equacao(txt):
    if txt.count("=") != 1:
        raise EntradaInvalida("Escreva uma equação com um único sinal de =.")
    esq, dire = (_ler(p) for p in txt.split("="))
    expr = (esq - dire).expand()
    try:
        poly = Poly(expr, X)
    except Exception:
        raise EntradaInvalida("Use apenas polinômios em x.")
    grau = poly.degree()
    if grau < 1 or grau > 4:
        raise EntradaInvalida("A equação precisa ter x e grau de 1 a 4.")

    passos = [f"{latex(esq)} = {latex(dire)}", f"{latex(expr)} = 0"]
    if grau == 1:
        a, b = poly.all_coeffs()
        passos.append(f"{latex(a)}x = {latex(-b)}")
        return {"passos": passos, "resposta": f"x = {latex(-b / a)}"}

    if grau == 2:
        a, b, c = poly.all_coeffs()
        delta = b**2 - 4 * a * c
        passos += [
            f"a = {latex(a)},\\; b = {latex(b)},\\; c = {latex(c)}",
            f"\\Delta = b^2 - 4ac = {latex(delta)}",
        ]
        if delta < 0:
            return {"passos": passos, "resposta": r"\text{Sem raízes reais}"}
        passos.append(r"x = \frac{-b \pm \sqrt{\Delta}}{2a}")

    raizes = sorted(solve(expr, X), key=lambda r: complex(r).real)
    resposta = ",\\; ".join(f"x = {latex(r)}" for r in raizes) or r"\text{Sem solução}"
    return {"passos": passos, "resposta": resposta}


def resolver(modo, entrada):
    t = entrada.strip()
    if modo == "equacao":
        return _equacao(t)
    f = _ler(t)
    if modo == "derivada":
        return {
            "passos": [f"f(x) = {latex(f)}", r"\text{Aplique a regra da potência em cada termo}"],
            "resposta": f"f'(x) = {latex(diff(f, X))}",
        }
    if modo == "integral":
        return {
            "passos": [f"f(x) = {latex(f)}", r"\text{Integre cada termo e some a constante } C"],
            "resposta": f"\\int f(x)\\,dx = {latex(integrate(f, X))} + C",
        }
    if modo == "fatorar":
        return {"passos": [f"{latex(f)}"], "resposta": latex(factor(f))}
    raise EntradaInvalida("Modo desconhecido.")
