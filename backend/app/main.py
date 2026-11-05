from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .adaptive import atualizar, nivel_para
from .generator import conferir, gerar
from .solver import EntradaInvalida, resolver

app = FastAPI(title="AdaptaMath")
_EXERCICIOS = {}  # em memória; troque por banco de dados quando evoluir o projeto


class Pedido(BaseModel):
    modo: str
    entrada: str


class Resposta(BaseModel):
    id: str
    resposta: str
    rating: int = 1000


@app.post("/api/resolver")
def api_resolver(p: Pedido):
    try:
        return resolver(p.modo, p.entrada)
    except EntradaInvalida as e:
        raise HTTPException(422, str(e))


@app.get("/api/exercicio")
def api_exercicio(rating: int = 1000):
    ex = gerar(nivel_para(rating))
    ex_id = uuid4().hex
    _EXERCICIOS[ex_id] = ex
    if len(_EXERCICIOS) > 500:
        _EXERCICIOS.pop(next(iter(_EXERCICIOS)))
    return {"id": ex_id, "nivel": ex["nivel"], "instrucao": ex["instrucao"], "expressao": ex["expressao"]}


@app.post("/api/responder")
def api_responder(r: Resposta):
    ex = _EXERCICIOS.pop(r.id, None)
    if ex is None:
        raise HTTPException(404, "Exercício não encontrado. Peça um novo.")
    ok = conferir(ex, r.resposta)
    certa = ", ".join(str(n) for n in sorted(ex["respostas"]))
    return {"correto": ok, "resposta_certa": certa, "rating": atualizar(r.rating, ex["nivel"], ok)}


app.mount("/", StaticFiles(directory=Path(__file__).resolve().parents[2] / "frontend", html=True))
