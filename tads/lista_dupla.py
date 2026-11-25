"""TAD Lista Duplamente Encadeada com cursor (item 2.3).

Usada no histórico de rotas: percorre-se nos dois sentidos.
"""
from tads.excecoes import (ElementoInexistenteError, EstruturaVaziaError,
                           PosicaoInvalidaError)


class NoDuplo:
    """Nó com referências para o anterior e o próximo."""
    __slots__ = ("valor", "anterior", "proximo")

    def __init__(self, valor):
        self.valor = valor
        self.anterior = None
        self.proximo = None


class ListaDupla:
    """Lista duplamente encadeada com um cursor de navegação.

    Invariantes: para todo nó n, n.proximo.anterior is n (quando existem);
    o cursor é None somente se a lista estiver vazia.
    """

    def __init__(self):
        """Pós: lista vazia, sem cursor."""
        self._inicio = None
        self._fim = None
        self._cursor = None
        self._tamanho = 0

    def __len__(self) -> int:
        return self._tamanho

    def vazia(self) -> bool:
        return self._tamanho == 0

    def inserir_inicio(self, valor) -> None:
        """Pós: valor é o primeiro elemento; tamanho + 1."""
        novo = NoDuplo(valor)
        novo.proximo = self._inicio
        if self._inicio is None:
            self._fim = novo
        else:
            self._inicio.anterior = novo
        self._inicio = novo
        self._apos_inserir(novo)

    def inserir_fim(self, valor) -> None:
        """Pós: valor é o último elemento; tamanho + 1."""
        novo = NoDuplo(valor)
        novo.anterior = self._fim
        if self._fim is None:
            self._inicio = novo
        else:
            self._fim.proximo = novo
        self._fim = novo
        self._apos_inserir(novo)

    def remover(self, valor) -> None:
        """Remove a primeira ocorrência de `valor`.

        Pré: valor existe. Pós: tamanho - 1; se o cursor estava no nó
        removido, passa ao próximo (ou ao anterior, se era o último).
        """
        atual = self._inicio
        while atual is not None and atual.valor != valor:
            atual = atual.proximo
        if atual is None:
            raise ElementoInexistenteError(f"{valor!r} não está na lista")
        if atual.anterior is None:
            self._inicio = atual.proximo
        else:
            atual.anterior.proximo = atual.proximo
        if atual.proximo is None:
            self._fim = atual.anterior
        else:
            atual.proximo.anterior = atual.anterior
        if self._cursor is atual:
            self._cursor = atual.proximo if atual.proximo is not None else atual.anterior
        self._tamanho -= 1

    def percorrer_frente(self):
        """Gera os valores do início ao fim."""
        atual = self._inicio
        while atual is not None:
            yield atual.valor
            atual = atual.proximo

    def percorrer_tras(self):
        """Gera os valores do fim ao início."""
        atual = self._fim
        while atual is not None:
            yield atual.valor
            atual = atual.anterior

    # --- cursor -----------------------------------------------------------
    def cursor_atual(self):
        """Pré: lista não vazia. Devolve o valor sob o cursor."""
        if self._cursor is None:
            raise EstruturaVaziaError("lista vazia")
        return self._cursor.valor

    def tem_proximo(self) -> bool:
        return self._cursor is not None and self._cursor.proximo is not None

    def tem_anterior(self) -> bool:
        return self._cursor is not None and self._cursor.anterior is not None

    def avancar(self):
        """Pré: tem_proximo(). Move o cursor adiante e devolve o novo valor."""
        if not self.tem_proximo():
            raise PosicaoInvalidaError("não há próximo elemento")
        self._cursor = self._cursor.proximo
        return self._cursor.valor

    def voltar(self):
        """Pré: tem_anterior(). Move o cursor para trás e devolve o valor."""
        if not self.tem_anterior():
            raise PosicaoInvalidaError("não há elemento anterior")
        self._cursor = self._cursor.anterior
        return self._cursor.valor

    def ir_para_fim(self) -> None:
        """Pós: cursor no último elemento (se houver)."""
        self._cursor = self._fim

    def ir_para_inicio(self) -> None:
        """Pós: cursor no primeiro elemento (se houver)."""
        self._cursor = self._inicio

    def _apos_inserir(self, novo: NoDuplo) -> None:
        if self._cursor is None:
            self._cursor = novo
        self._tamanho += 1
