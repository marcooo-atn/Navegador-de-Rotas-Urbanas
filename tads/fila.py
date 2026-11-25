"""TAD Fila (item 2.4), implementada com nós encadeados."""
from tads.excecoes import EstruturaVaziaError
from tads.lista_encadeada import No


class Fila:
    """Estrutura FIFO. Todas as operações são O(1)."""

    def __init__(self):
        """Pós: fila vazia."""
        self._inicio = None
        self._fim = None
        self._tamanho = 0

    def __len__(self) -> int:
        return self._tamanho

    def vazia(self) -> bool:
        return self._inicio is None

    def enfileirar(self, valor) -> None:
        """Pós: valor é o último da fila; tamanho + 1."""
        novo = No(valor)
        if self._fim is None:
            self._inicio = novo
        else:
            self._fim.proximo = novo
        self._fim = novo
        self._tamanho += 1

    def desenfileirar(self):
        """Remove e devolve o primeiro da fila.

        Pré: fila não vazia. Pós: tamanho - 1.
        """
        if self._inicio is None:
            raise EstruturaVaziaError("fila vazia")
        valor = self._inicio.valor
        self._inicio = self._inicio.proximo
        if self._inicio is None:
            self._fim = None
        self._tamanho -= 1
        return valor

    def primeiro(self):
        """Pré: fila não vazia. Devolve o primeiro sem remover."""
        if self._inicio is None:
            raise EstruturaVaziaError("fila vazia")
        return self._inicio.valor
