# AdaptaMath

Plataforma de matemática com cálculo em **Python** (FastAPI + SymPy) e interface em **JavaScript** (KaTeX para as fórmulas).

## O que faz

- **Resolver:** equações de 1º ao 4º grau (com passos), derivadas, integrais e fatoração.
- **Praticar:** exercícios gerados por nível. A dificuldade sobe ou desce conforme os acertos, usando uma pontuação no estilo Elo.

## Como rodar

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Abra `http://localhost:8000`. No GitHub Codespaces, abra a porta 8000 na aba **Ports**.

## Testes

```bash
cd backend
pytest
```

## Estrutura

```
backend/app/solver.py      resolução simbólica passo a passo
backend/app/generator.py   gerador de exercícios e conferência
backend/app/adaptive.py    dificuldade adaptativa (Elo)
backend/app/main.py        API e entrega do frontend
frontend/                  interface (HTML, CSS, JS)
```

## Próximos passos

- Mais tipos de exercício (sistemas, funções, geometria) e respostas em fração.
- Banco de dados e contas de usuário para guardar o histórico.
- Gráficos de funções e relatório de evolução.

## Aviso

É um MVP. Antes de publicar na internet, adicione limite de tempo e de requisições à rota de resolução.

## Licença

MIT
