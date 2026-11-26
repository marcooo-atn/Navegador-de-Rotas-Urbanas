"""Benchmark dos 5 algoritmos de ordenação (item 3.2).

Mede cada algoritmo com 1.000, 10.000 e 50.000 registros em 3 cenários
(aleatória, já ordenada, inversa), grava `resultados/ordenacao.csv`, mostra
a tabela, compara o crescimento medido com o teórico e gera o gráfico.

Uso (na raiz do projeto):
    python3 -m benchmark.benchmark                 # completo (demora!)
    python3 -m benchmark.benchmark --max-quadratico 10000   # pula O(n²) em 50.000
    python3 -m benchmark.benchmark --so-grafico    # refaz tabela/gráfico do CSV

O CSV é gravado a cada medição e as combinações já medidas são puladas, então
a execução pode ser interrompida e retomada. Apague o CSV para medir de novo.
"""
import argparse
import csv
import math
import operator
import os
import random
import sys
import time

if __package__ in (None, ""):
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from algoritmos.ordenacao import ALGORITMOS, esta_ordenada
from dominio.local import Local
from tads.lista_estatica import ListaEstatica

TAMANHOS = (1000, 10000, 50000)
CENARIOS = ("aleatoria", "ordenada", "inversa")
QUADRATICOS = ("bubble", "selection", "insertion")
PASTA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resultados")
CSV_PADRAO = os.path.join(PASTA, "ordenacao.csv")
SEMENTE = 42
CHAVE = operator.attrgetter("id")


def gerar_dados(n: int, cenario: str, semente: int = SEMENTE) -> ListaEstatica:
    """Vetor de n registros `Local` com ids únicos 0..n-1 na ordem do cenário.

    O embaralhamento (Fisher-Yates) usa semente fixa: todos os algoritmos
    recebem exatamente os mesmos dados.
    """
    ids = ListaEstatica.preenchida(n, 0)
    for i in range(n):
        ids[i] = i
    if cenario == "aleatoria":
        gerador = random.Random(semente + n)
        for i in range(n - 1, 0, -1):
            j = gerador.randrange(i + 1)
            ids[i], ids[j] = ids[j], ids[i]
    elif cenario == "inversa":
        for i in range(n):
            ids[i] = n - 1 - i
    elif cenario != "ordenada":
        raise ValueError(f"cenário desconhecido: {cenario!r}")
    dados = ListaEstatica(n)
    for i in range(n):
        dados.inserir_fim(Local(ids[i], f"Local {ids[i]}", "Bairro", "Categoria", 3.0))
    return dados


def medir(funcao, n: int, cenario: str, repeticoes: int) -> float:
    """Tempo médio (s) de `funcao` sobre dados novos a cada repetição."""
    total = 0.0
    for _ in range(repeticoes):
        dados = gerar_dados(n, cenario)
        inicio = time.perf_counter()
        funcao(dados, CHAVE)
        total += time.perf_counter() - inicio
        if not esta_ordenada(dados, CHAVE):
            raise AssertionError(f"{funcao.__name__} não ordenou ({n}, {cenario})")
    return total / repeticoes


def ler_csv(caminho: str):
    """Lista de linhas (dicts de registro de resultado) do CSV, ou lista vazia."""
    linhas = []
    if os.path.exists(caminho):
        with open(caminho, newline="", encoding="utf-8") as f:
            for linha in csv.DictReader(f):
                linhas.append({"algoritmo": linha["algoritmo"], "n": int(linha["n"]),
                               "cenario": linha["cenario"], "tempo_s": float(linha["tempo_s"])})
    return linhas


def procurar(linhas, algoritmo, n, cenario):
    for linha in linhas:
        if linha["algoritmo"] == algoritmo and linha["n"] == n and linha["cenario"] == cenario:
            return linha["tempo_s"]
    return None


def executar(caminho_csv: str, tamanhos, max_quadratico: int) -> None:
    os.makedirs(os.path.dirname(caminho_csv), exist_ok=True)
    existentes = ler_csv(caminho_csv)
    novo = not os.path.exists(caminho_csv)
    with open(caminho_csv, "a", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        if novo:
            escritor.writerow(["algoritmo", "n", "cenario", "tempo_s"])
        for n in tamanhos:
            repeticoes = 3 if n <= 1000 else 1
            for cenario in CENARIOS:
                for nome, funcao in ALGORITMOS:
                    if nome in QUADRATICOS and n > max_quadratico:
                        print(f"pulado: {nome} n={n} (acima de --max-quadratico)")
                        continue
                    if procurar(existentes, nome, n, cenario) is not None:
                        continue
                    t = medir(funcao, n, cenario, repeticoes)
                    escritor.writerow([nome, n, cenario, f"{t:.6f}"])
                    f.flush()
                    print(f"{nome:9s} n={n:6d} {cenario:9s} {t:10.4f} s", flush=True)


def _texto_tempo(t) -> str:
    return "—" if t is None else f"{t:.6f}"


def tabela_markdown(linhas, tamanhos) -> str:
    """Tabela algoritmo x (n, cenário) em Markdown; '—' = não medido."""
    colunas = [(n, c) for n in tamanhos for c in CENARIOS]
    cab = "| Algoritmo | " + " | ".join(f"{n} {c[:4]}." for n, c in colunas) + " |"
    sep = "|---|" + "---:|" * len(colunas)
    corpo = []
    for nome, _ in ALGORITMOS:
        celulas = [_texto_tempo(procurar(linhas, nome, n, c)) for n, c in colunas]
        corpo.append(f"| {nome} | " + " | ".join(celulas) + " |")
    return "Tempos em segundos.\n\n" + "\n".join([cab, sep] + corpo)


def _esperado(nome: str, n1: int, n2: int) -> float:
    """Razão teórica t(n2)/t(n1) para o caso médio/pior do algoritmo."""
    if nome in QUADRATICOS:
        return (n2 / n1) ** 2
    return (n2 * math.log2(n2)) / (n1 * math.log2(n1))


def analise_crescimento(linhas, tamanhos) -> str:
    """Compara a razão medida t(n2)/t(n1) com a razão teórica."""
    saida = ["| Algoritmo | Cenário | n1 → n2 | Medido | Teórico (médio/pior) |\n|---|---|---|---:|---:|"]
    for nome, _ in ALGORITMOS:
        for cenario in CENARIOS:
            for k in range(len(tamanhos) - 1):
                n1, n2 = tamanhos[k], tamanhos[k + 1]
                t1 = procurar(linhas, nome, n1, cenario)
                t2 = procurar(linhas, nome, n2, cenario)
                if t1 and t2:
                    saida.append(f"| {nome} | {cenario} | {n1} → {n2} | "
                                 f"{t2 / t1:.1f}x | {_esperado(nome, n1, n2):.1f}x |")
    return "\n".join(saida)


def gerar_grafico(linhas, tamanhos, caminho_png: str) -> bool:
    """Um gráfico por cenário (escala log-log). False se não há matplotlib."""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib não instalado: gráfico não gerado (pip install matplotlib).")
        return False
    fig, eixos = plt.subplots(1, 3, figsize=(15, 4.5), sharey=True)
    for eixo, cenario in zip(eixos, CENARIOS):
        for nome, _ in ALGORITMOS:
            xs, ys = [], []
            for n in tamanhos:
                t = procurar(linhas, nome, n, cenario)
                if t is not None and t > 0:
                    xs.append(n)
                    ys.append(t)
            if xs:
                eixo.plot(xs, ys, marker="o", label=nome)
        eixo.set_xscale("log")
        eixo.set_yscale("log")
        eixo.set_title(f"Entrada {cenario}")
        eixo.set_xlabel("n (registros)")
        eixo.grid(True, which="both", alpha=0.3)
    eixos[0].set_ylabel("tempo (s)")
    eixos[0].legend()
    fig.suptitle("Ordenação: tempo × tamanho")
    fig.tight_layout()
    fig.savefig(caminho_png, dpi=130)
    plt.close(fig)
    return True


def relatorio(caminho_csv: str, tamanhos) -> None:
    linhas = ler_csv(caminho_csv)
    tabela = tabela_markdown(linhas, tamanhos)
    analise = analise_crescimento(linhas, tamanhos)
    print("\n" + tabela + "\n\n" + analise)
    with open(os.path.join(os.path.dirname(caminho_csv), "tabela.md"), "w", encoding="utf-8") as f:
        f.write(tabela + "\n\nRazão de crescimento (medido × teórico)\n\n" + analise + "\n")
    png = os.path.join(os.path.dirname(caminho_csv), "ordenacao.png")
    if gerar_grafico(linhas, tamanhos, png):
        print(f"\nGráfico salvo em {png}")


def main() -> None:
    ap = argparse.ArgumentParser(description="Benchmark de ordenação")
    ap.add_argument("--csv", default=CSV_PADRAO)
    ap.add_argument("--tamanhos", type=int, nargs="+", default=list(TAMANHOS))
    ap.add_argument("--max-quadratico", type=int, default=max(TAMANHOS),
                    help="maior n para Bubble/Selection/Insertion")
    ap.add_argument("--so-grafico", action="store_true", help="não mede, só refaz tabela e gráfico")
    args = ap.parse_args()
    if not args.so_grafico:
        executar(args.csv, args.tamanhos, args.max_quadratico)
    relatorio(args.csv, args.tamanhos)


if __name__ == "__main__":
    main()
