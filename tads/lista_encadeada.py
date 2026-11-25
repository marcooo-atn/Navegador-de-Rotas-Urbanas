"""TAD Lista Encadeada Simples e Dinâmica (itens 2.1 e 2.2)."""
from tads.excecoes import (ElementoInexistenteError, EstruturaVaziaError,
                           PosicaoInvalidaError)


class No:
    """Nó com valor e referência para o próximo nó."""
    __slots__ = ("valor", "proximo")

    def __init__(self, valor, proximo=None):
        self.valor = valor
        self.proximo = proximo


class ListaEncadeada:
    """Lista simplesmente encadeada com referências ao início e ao fim.

    Invariante: `_fim` é o último nó alcançável a partir de `_inicio`
    (ambos None quando vazia); `_tamanho` conta os nós.
    """

    def __init__(self):
        """Pós: lista vazia."""
        self._inicio = None
        self._fim = None
        self._tamanho = 0

    def __len__(self) -> int:
        return self._tamanho

    def vazia(self) -> bool:
        return self._tamanho == 0

    def inserir_inicio(self, valor) -> None:
        """Pós: valor é o primeiro elemento; tamanho + 1. Custo O(1).

        A ordem das atribuições importa: o novo nó deve apontar para o
        antigo início ANTES de `_inicio` ser trocado, senão a lista se perde.
        """
        novo = No(valor)
        novo.proximo = self._inicio
        self._inicio = novo
        if self._fim is None:
            self._fim = novo
        self._tamanho += 1

    def inserir_fim(self, valor) -> None:
        """Pós: valor é o último elemento; tamanho + 1. Custo O(1)."""
        novo = No(valor)
        if self._fim is None:
            self._inicio = novo
        else:
            self._fim.proximo = novo
        self._fim = novo
        self._tamanho += 1

    def inserir_posicao(self, pos: int, valor) -> None:
        """Insere `valor` de modo que fique no índice `pos`.

        Pré: 0 <= pos <= tamanho. Pós: tamanho + 1; demais mantêm a ordem.
        """
        if not 0 <= pos <= self._tamanho:
            raise PosicaoInvalidaError(f"posição {pos} inválida")
        if pos == 0:
            self.inserir_inicio(valor)
        elif pos == self._tamanho:
            self.inserir_fim(valor)
        else:
            anterior = self._no_em(pos - 1)
            novo = No(valor)
            novo.proximo = anterior.proximo
            anterior.proximo = novo
            self._tamanho += 1

    def remover(self, valor) -> None:
        """Remove a primeira ocorrência de `valor`.

        Pré: valor existe na lista. Pós: tamanho - 1.
        """
        anterior = None
        atual = self._inicio
        while atual is not None and atual.valor != valor:
            anterior = atual
            atual = atual.proximo
        if atual is None:
            raise ElementoInexistenteError(f"{valor!r} não está na lista")
        if anterior is None:
            self._inicio = atual.proximo
        else:
            anterior.proximo = atual.proximo
        if atual is self._fim:
            self._fim = anterior
        self._tamanho -= 1

    def remover_posicao(self, pos: int):
        """Remove e devolve o elemento do índice `pos`.

        Pré: lista não vazia e 0 <= pos < tamanho. Pós: tamanho - 1.
        """
        if self.vazia():
            raise EstruturaVaziaError("lista vazia")
        if not 0 <= pos < self._tamanho:
            raise PosicaoInvalidaError(f"posição {pos} inválida")
        if pos == 0:
            alvo = self._inicio
            self._inicio = alvo.proximo
            if self._inicio is None:
                self._fim = None
        else:
            anterior = self._no_em(pos - 1)
            alvo = anterior.proximo
            anterior.proximo = alvo.proximo
            if alvo is self._fim:
                self._fim = anterior
        self._tamanho -= 1
        return alvo.valor

    def buscar(self, valor):
        """Devolve o primeiro `No` com `valor`, ou None. Custo O(n)."""
        atual = self._inicio
        while atual is not None:
            if atual.valor == valor:
                return atual
            atual = atual.proximo
        return None

    def obter(self, pos: int):
        """Pré: 0 <= pos < tamanho. Devolve o valor do índice `pos`."""
        if not 0 <= pos < self._tamanho:
            raise PosicaoInvalidaError(f"posição {pos} inválida")
        return self._no_em(pos).valor

    def percorrer(self):
        """Gera os valores do início ao fim."""
        atual = self._inicio
        while atual is not None:
            yield atual.valor
            atual = atual.proximo

    def __iter__(self):
        return self.percorrer()

    def _no_em(self, pos: int) -> No:
        atual = self._inicio
        for _ in range(pos):
            atual = atual.proximo
        return atual
