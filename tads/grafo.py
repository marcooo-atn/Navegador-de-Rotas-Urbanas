"""TAD Grafo não direcionado e ponderado, por matriz de adjacência.

Itens 1.2 (matriz) e 2.5 (grafo, BFS, DFS). O identificador de um vértice é
o seu índice na matriz e nunca é reutilizado após a remoção.
"""
from tads.excecoes import (ElementoInexistenteError, EstruturaCheiaError,
                           PreCondicaoError)
from tads.fila import Fila
from tads.lista_encadeada import ListaEncadeada
from tads.lista_estatica import ListaEstatica
from tads.pilha import Pilha


class Grafo:
    """Grafo com no máximo `capacidade` vértices.

    Invariantes: matriz simétrica; peso 0 = sem aresta; pesos > 0; sem laços;
    linha/coluna de vértice inativo só contêm zeros.
    Memória O(V²); percurso BFS/DFS O(V²).
    """

    def __init__(self, capacidade: int):
        """Pré: capacidade > 0. Pós: grafo sem vértices."""
        if capacidade <= 0:
            raise PreCondicaoError("capacidade deve ser positiva")
        self._capacidade = capacidade
        self._matriz = [[0] * capacidade for _ in range(capacidade)]
        self._ativo = ListaEstatica.preenchida(capacidade, False)
        self._proximo_id = 0
        self._n = 0

    @property
    def capacidade(self) -> int:
        return self._capacidade

    def __len__(self) -> int:
        """Quantidade de vértices ativos."""
        return self._n

    def adicionar_vertice(self) -> int:
        """Cria um vértice e devolve seu id.

        Pré: ainda há id livre. Pós: len(grafo) + 1; novo vértice sem arestas.
        """
        if self._proximo_id >= self._capacidade:
            raise EstruturaCheiaError("grafo sem capacidade para novos vértices")
        v = self._proximo_id
        self._proximo_id += 1
        self._ativo[v] = True
        self._n += 1
        return v

    def remover_vertice(self, v: int) -> None:
        """Pré: v ativo. Pós: v inativo e todas as suas arestas removidas."""
        self._validar(v)
        for u in range(self._capacidade):
            self._matriz[v][u] = 0
            self._matriz[u][v] = 0
        self._ativo[v] = False
        self._n -= 1

    def existe_vertice(self, v: int) -> bool:
        return isinstance(v, int) and 0 <= v < self._capacidade and self._ativo[v]

    def adicionar_aresta(self, u: int, v: int, peso: float) -> None:
        """Cria (ou atualiza) a aresta u-v.

        Pré: u e v ativos, u != v, peso > 0. Pós: peso(u,v) == peso(v,u) == peso.
        """
        self._validar(u)
        self._validar(v)
        if u == v:
            raise PreCondicaoError("laços não são permitidos")
        if peso <= 0:
            raise PreCondicaoError("peso deve ser positivo")
        self._matriz[u][v] = peso
        self._matriz[v][u] = peso

    def remover_aresta(self, u: int, v: int) -> None:
        """Pré: aresta u-v existe. Pós: aresta removida nos dois sentidos."""
        if not self.existe_aresta(u, v):
            raise ElementoInexistenteError(f"aresta {u}-{v} não existe")
        self._matriz[u][v] = 0
        self._matriz[v][u] = 0

    def existe_aresta(self, u: int, v: int) -> bool:
        return (self.existe_vertice(u) and self.existe_vertice(v)
                and self._matriz[u][v] > 0)

    def peso(self, u: int, v: int) -> float:
        """Pré: aresta u-v existe."""
        if not self.existe_aresta(u, v):
            raise ElementoInexistenteError(f"aresta {u}-{v} não existe")
        return self._matriz[u][v]

    def vizinhos(self, v: int) -> ListaEncadeada:
        """Pré: v ativo. Ids dos vizinhos, em ordem crescente."""
        self._validar(v)
        res = ListaEncadeada()
        for u in range(self._capacidade):
            if self._matriz[v][u] > 0:
                res.inserir_fim(u)
        return res

    def grau(self, v: int) -> int:
        """Pré: v ativo."""
        return len(self.vizinhos(v))

    def vertices(self) -> ListaEncadeada:
        """Ids dos vértices ativos, em ordem crescente."""
        res = ListaEncadeada()
        for v in range(self._capacidade):
            if self._ativo[v]:
                res.inserir_fim(v)
        return res

    def isolados(self) -> ListaEncadeada:
        """Vértices ativos sem nenhuma aresta."""
        res = ListaEncadeada()
        for v in self.vertices():
            if self.grau(v) == 0:
                res.inserir_fim(v)
        return res

    def menor_caminho_paradas(self, origem: int, destino: int, bloqueado=None):
        """BFS: caminho com menos arestas, como ListaEncadeada de ids.

        Pré: origem e destino ativos. `bloqueado` é uma função opcional
        v -> bool; vértices bloqueados (exceto a origem) não são visitados.
        Pós: devolve None se não há caminho; o grafo não é alterado.
        """
        self._validar(origem)
        self._validar(destino)
        visitado = ListaEstatica.preenchida(self._capacidade, False)
        pred = ListaEstatica.preenchida(self._capacidade, -1)
        fila = Fila()
        fila.enfileirar(origem)
        visitado[origem] = True
        while not fila.vazia():
            u = fila.desenfileirar()
            if u == destino:
                break
            for v in range(self._capacidade):
                if (self._matriz[u][v] > 0 and not visitado[v]
                        and not (bloqueado is not None and bloqueado(v))):
                    visitado[v] = True
                    pred[v] = u
                    fila.enfileirar(v)
        if not visitado[destino]:
            return None
        caminho = ListaEncadeada()
        v = destino
        while v != -1:
            caminho.inserir_inicio(v)
            v = pred[v]
        return caminho

    def alcancaveis(self, origem: int) -> ListaEncadeada:
        """DFS com pilha explícita: vértices alcançáveis (inclui a origem).

        Pré: origem ativa. Pós: ordem de visita da DFS; grafo inalterado.
        """
        self._validar(origem)
        visitado = ListaEstatica.preenchida(self._capacidade, False)
        res = ListaEncadeada()
        pilha = Pilha()
        pilha.empilhar(origem)
        while not pilha.vazia():
            u = pilha.desempilhar()
            if visitado[u]:
                continue
            visitado[u] = True
            res.inserir_fim(u)
            for v in range(self._capacidade - 1, -1, -1):
                if self._matriz[u][v] > 0 and not visitado[v]:
                    pilha.empilhar(v)
        return res

    def custo_caminho(self, caminho: ListaEncadeada) -> float:
        """Soma dos pesos ao longo de `caminho`.

        Pré: vértices consecutivos do caminho são adjacentes.
        """
        total = 0
        anterior = None
        for v in caminho:
            if anterior is not None:
                total += self.peso(anterior, v)
            anterior = v
        return total

    def _validar(self, v: int) -> None:
        if not self.existe_vertice(v):
            raise ElementoInexistenteError(f"vértice {v!r} não existe")
