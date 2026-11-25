"""TAD Pilha (item 2.4), implementada com nós encadeados."""
from tads.excecoes import EstruturaVaziaError
from tads.lista_encadeada import No


class Pilha:
    """Estrutura LIFO. Todas as operações são O(1)."""

    def __init__(self):
        """Pós: pilha vazia."""
        self._topo = None
        self._tamanho = 0

    def __len__(self) -> int:
        return self._tamanho

    def vazia(self) -> bool:
        return self._topo is None

    def empilhar(self, valor) -> None:
        """Pós: valor no topo; tamanho + 1."""
        self._topo = No(valor, self._topo)
        self._tamanho += 1

    def desempilhar(self):
        """Remove e devolve o topo.

        Pré: pilha não vazia. Pós: tamanho - 1.
        """
        if self._topo is None:
            raise EstruturaVaziaError("pilha vazia")
        valor = self._topo.valor
        self._topo = self._topo.proximo
        self._tamanho -= 1
        return valor

    def topo(self):
        """Pré: pilha não vazia. Devolve o topo sem remover."""
        if self._topo is None:
            raise EstruturaVaziaError("pilha vazia")
        return self._topo.valor
