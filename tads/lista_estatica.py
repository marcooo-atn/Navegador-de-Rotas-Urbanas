"""TAD Lista Sequencial Estática (item 1.5).

Vetor de capacidade fixa + variável `tamanho`. A `list` do Python é usada
apenas como vetor (nunca cresce).
"""
from tads.excecoes import (EstruturaCheiaError, EstruturaVaziaError,
                           PosicaoInvalidaError, PreCondicaoError)


class ListaEstatica:
    """Lista com capacidade fixa definida na criação.

    Invariante: 0 <= tamanho <= capacidade; posições >= tamanho valem None.
    """

    def __init__(self, capacidade: int):
        """Pré: capacidade > 0. Pós: lista vazia (tamanho 0)."""
        if capacidade <= 0:
            raise PreCondicaoError("capacidade deve ser positiva")
        self._vetor = [None] * capacidade
        self._capacidade = capacidade
        self._tamanho = 0

    @classmethod
    def preenchida(cls, capacidade: int, valor):
        """Pré: capacidade > 0. Pós: lista cheia, todas as posições = valor."""
        lista = cls(capacidade)
        for i in range(capacidade):
            lista._vetor[i] = valor
        lista._tamanho = capacidade
        return lista

    @property
    def capacidade(self) -> int:
        return self._capacidade

    def __len__(self) -> int:
        return self._tamanho

    def vazia(self) -> bool:
        return self._tamanho == 0

    def cheia(self) -> bool:
        return self._tamanho == self._capacidade

    def inserir(self, pos: int, valor) -> None:
        """Insere `valor` em `pos`, deslocando os seguintes à direita.

        Pré: lista não cheia e 0 <= pos <= tamanho.
        Pós: tamanho aumenta em 1; valor está em `pos`; ordem relativa mantida.
        """
        if self.cheia():
            raise EstruturaCheiaError("lista cheia")
        if not 0 <= pos <= self._tamanho:
            raise PosicaoInvalidaError(f"posição {pos} inválida")
        i = self._tamanho
        while i > pos:
            self._vetor[i] = self._vetor[i - 1]
            i -= 1
        self._vetor[pos] = valor
        self._tamanho += 1

    def inserir_fim(self, valor) -> None:
        """Pré: lista não cheia. Pós: valor na última posição."""
        self.inserir(self._tamanho, valor)

    def remover(self, pos: int):
        """Remove e devolve o elemento de `pos`, deslocando à esquerda.

        Pré: lista não vazia e 0 <= pos < tamanho.
        Pós: tamanho diminui em 1; ordem relativa dos demais mantida.
        """
        if self.vazia():
            raise EstruturaVaziaError("lista vazia")
        self._validar_pos(pos)
        removido = self._vetor[pos]
        for i in range(pos, self._tamanho - 1):
            self._vetor[i] = self._vetor[i + 1]
        self._vetor[self._tamanho - 1] = None
        self._tamanho -= 1
        return removido

    def atualizar(self, pos: int, valor) -> None:
        """Pré: 0 <= pos < tamanho. Pós: posição `pos` passa a valer `valor`."""
        self._validar_pos(pos)
        self._vetor[pos] = valor

    def consultar(self, pos: int):
        """Pré: 0 <= pos < tamanho. Pós: lista inalterada."""
        self._validar_pos(pos)
        return self._vetor[pos]

    def buscar(self, valor) -> int:
        """Índice da primeira ocorrência de `valor`, ou -1. Pós: inalterada."""
        for i in range(self._tamanho):
            if self._vetor[i] == valor:
                return i
        return -1

    def copiar(self) -> "ListaEstatica":
        """Cópia rasa (mesma capacidade e mesmas referências aos elementos).

        Pós: a original não é alterada; ordenar a cópia não muda a original.
        """
        nova = ListaEstatica(self._capacidade)
        for i in range(self._tamanho):
            nova._vetor[i] = self._vetor[i]
        nova._tamanho = self._tamanho
        return nova

    def como_vetor(self):
        """Devolve o vetor interno (sem cópia), para algoritmos in-place.

        Uso restrito aos algoritmos de ordenação, que precisam de acesso
        direto por índice sem o custo de validar cada leitura. Só as
        posições 0 .. len(lista)-1 são válidas e o vetor nunca deve crescer.
        """
        return self._vetor

    def _validar_pos(self, pos: int) -> None:
        if not 0 <= pos < self._tamanho:
            raise PosicaoInvalidaError(f"posição {pos} inválida")

    def __getitem__(self, pos: int):
        return self.consultar(pos)

    def __setitem__(self, pos: int, valor) -> None:
        self.atualizar(pos, valor)

    def __iter__(self):
        for i in range(self._tamanho):
            yield self._vetor[i]
