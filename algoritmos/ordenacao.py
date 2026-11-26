"""Algoritmos de ordenação (itens 3.1 e 3.2), escritos pelo grupo.

Todos ordenam IN-PLACE uma `ListaEstatica` (vetor de registros) em ordem
crescente de `chave(elemento)`. `chave` é uma função elemento -> valor
comparável; para ordenar por mais de um campo, devolva uma tupla
(ex.: lambda l: (l.bairro, l.nome)); para ordem decrescente de um campo
numérico, devolva o valor negativo.

Pré (todos): `lista` é uma ListaEstatica e `chave` é aplicável a todos os
elementos. Pós (todos): chave(lista[i]) <= chave(lista[i+1]) para todo i;
os mesmos elementos continuam na lista (permutação).

Nenhum usa sorted(), .sort(), heapq nem recursão.
"""
from tads.pilha import Pilha
from tads.lista_estatica import ListaEstatica


def bubblesort(lista: ListaEstatica, chave) -> None:
    """Trocas de vizinhos até não haver troca. Estável.

    Tempo: O(n²) médio e pior; O(n) se já ordenada (parada antecipada).
    Espaço extra: O(1).
    """
    v = lista.como_vetor()
    limite = len(lista) - 1
    while limite > 0:
        ultima_troca = 0
        for j in range(limite):
            if chave(v[j + 1]) < chave(v[j]):
                v[j], v[j + 1] = v[j + 1], v[j]
                ultima_troca = j
        limite = ultima_troca


def selectionsort(lista: ListaEstatica, chave) -> None:
    """Seleciona o menor do trecho restante e o põe na posição. Instável.

    Tempo: Θ(n²) em qualquer entrada (sempre n(n-1)/2 comparações);
    no máximo n-1 trocas. Espaço extra: O(1).
    """
    v = lista.como_vetor()
    n = len(lista)
    for i in range(n - 1):
        menor = i
        for j in range(i + 1, n):
            if chave(v[j]) < chave(v[menor]):
                menor = j
        if menor != i:
            v[i], v[menor] = v[menor], v[i]


def insertionsort(lista: ListaEstatica, chave) -> None:
    """Insere cada elemento na parte já ordenada à esquerda. Estável.

    Tempo: O(n²) médio e pior (entrada inversa); O(n) se já ordenada.
    Espaço extra: O(1).
    """
    v = lista.como_vetor()
    for i in range(1, len(lista)):
        atual = v[i]
        k = chave(atual)
        j = i - 1
        while j >= 0 and k < chave(v[j]):
            v[j + 1] = v[j]
            j -= 1
        v[j + 1] = atual


def quicksort(lista: ListaEstatica, chave) -> None:
    """Quicksort iterativo, partição de Hoare, pivô = mediana de três.

    Instável. Tempo: O(n log n) médio; pior caso O(n²) (raro com mediana
    de três, e a entrada já ordenada/inversa deixa de ser o pior caso).
    Espaço extra: O(log n) de pilha explícita (sempre se continua pelo lado
    menor e se empilha o maior), sem risco de RecursionError.
    """
    v = lista.como_vetor()
    n = len(lista)
    pilha = Pilha()
    if n > 1:
        pilha.empilhar((0, n - 1))
    while not pilha.vazia():
        lo, hi = pilha.desempilhar()
        while lo < hi:
            meio = (lo + hi) // 2
            a, b, c = chave(v[lo]), chave(v[meio]), chave(v[hi])
            if a < b:
                pivo = b if b < c else (c if a < c else a)
            else:
                pivo = a if a < c else (c if b < c else b)
            i, j = lo, hi
            while i <= j:
                while chave(v[i]) < pivo:
                    i += 1
                while pivo < chave(v[j]):
                    j -= 1
                if i <= j:
                    v[i], v[j] = v[j], v[i]
                    i += 1
                    j -= 1
            # sub-trechos: [lo..j] e [i..hi]; empilha o maior, segue no menor
            if j - lo < hi - i:
                if i < hi:
                    pilha.empilhar((i, hi))
                hi = j
            else:
                if lo < j:
                    pilha.empilhar((lo, j))
                lo = i


def mergesort(lista: ListaEstatica, chave) -> None:
    """Mergesort iterativo (bottom-up) com vetor auxiliar. Estável.

    Tempo: Θ(n log n) em qualquer entrada. Espaço extra: O(n) (vetor
    auxiliar, criado com a ListaEstatica do grupo).
    """
    v = lista.como_vetor()
    n = len(lista)
    if n < 2:
        return
    aux = ListaEstatica.preenchida(n, None).como_vetor()
    origem, destino = v, aux
    largura = 1
    while largura < n:
        for ini in range(0, n, 2 * largura):
            meio = min(ini + largura, n)
            fim = min(ini + 2 * largura, n)
            i, j, k = ini, meio, ini
            while i < meio and j < fim:
                if chave(origem[j]) < chave(origem[i]):
                    destino[k] = origem[j]
                    j += 1
                else:
                    destino[k] = origem[i]
                    i += 1
                k += 1
            while i < meio:
                destino[k] = origem[i]
                i += 1
                k += 1
            while j < fim:
                destino[k] = origem[j]
                j += 1
                k += 1
        origem, destino = destino, origem
        largura *= 2
    if origem is not v:
        for i in range(n):
            v[i] = origem[i]


def esta_ordenada(lista: ListaEstatica, chave) -> bool:
    """True se a lista está em ordem crescente de `chave`. Não altera a lista."""
    for i in range(1, len(lista)):
        if chave(lista[i]) < chave(lista[i - 1]):
            return False
    return True


ALGORITMOS = (
    ("bubble", bubblesort),
    ("selection", selectionsort),
    ("insertion", insertionsort),
    ("quick", quicksort),
    ("merge", mergesort),
)


def obter_algoritmo(nome: str):
    """Devolve a função de ordenação pelo nome. Pré: nome em ALGORITMOS."""
    for chave_nome, funcao in ALGORITMOS:
        if chave_nome == nome:
            return funcao
    raise ValueError(f"algoritmo desconhecido: {nome!r}")
