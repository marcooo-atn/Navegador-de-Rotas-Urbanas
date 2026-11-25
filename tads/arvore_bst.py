"""TAD Árvore Binária de Busca (item 2.5).

Todas as operações são iterativas (sem recursão), para que uma árvore
degenerada com dezenas de milhares de nós não estoure o limite de recursão.
"""
from tads.excecoes import ChaveDuplicadaError, ElementoInexistenteError
from tads.fila import Fila
from tads.lista_encadeada import ListaEncadeada
from tads.pilha import Pilha


class NoBST:
    """Nó com chave, valor associado e filhos esquerdo/direito."""
    __slots__ = ("chave", "valor", "esq", "dir")

    def __init__(self, chave, valor=None):
        self.chave = chave
        self.valor = valor
        self.esq = None
        self.dir = None


class ArvoreBST:
    """Árvore de busca sem balanceamento e sem chaves repetidas.

    Invariante: para todo nó, chaves da esquerda < chave < chaves da direita.
    Custo médio de inserir/buscar/remover: O(log n); pior caso (chaves
    inseridas em ordem): O(n).
    """

    def __init__(self):
        """Pós: árvore vazia."""
        self._raiz = None
        self._tamanho = 0

    def __len__(self) -> int:
        return self._tamanho

    def vazia(self) -> bool:
        return self._raiz is None

    def inserir(self, chave, valor=None) -> None:
        """Pré: chave comparável e ainda inexistente. Pós: tamanho + 1."""
        novo = NoBST(chave, valor)
        if self._raiz is None:
            self._raiz = novo
        else:
            atual = self._raiz
            while True:
                if chave == atual.chave:
                    raise ChaveDuplicadaError(f"chave {chave!r} já existe")
                if chave < atual.chave:
                    if atual.esq is None:
                        atual.esq = novo
                        break
                    atual = atual.esq
                else:
                    if atual.dir is None:
                        atual.dir = novo
                        break
                    atual = atual.dir
        self._tamanho += 1

    def buscar(self, chave):
        """Devolve o `NoBST` da chave, ou None. Pós: árvore inalterada."""
        atual = self._raiz
        while atual is not None and atual.chave != chave:
            atual = atual.esq if chave < atual.chave else atual.dir
        return atual

    def remover(self, chave) -> None:
        """Remove o nó da chave (3 casos: folha, 1 filho, 2 filhos).

        Pré: chave existe. Pós: tamanho - 1; invariante da BST mantida.
        """
        pai = None
        atual = self._raiz
        while atual is not None and atual.chave != chave:
            pai = atual
            atual = atual.esq if chave < atual.chave else atual.dir
        if atual is None:
            raise ElementoInexistenteError(f"chave {chave!r} não existe")
        if atual.esq is not None and atual.dir is not None:
            pai_suc = atual
            suc = atual.dir
            while suc.esq is not None:
                pai_suc = suc
                suc = suc.esq
            atual.chave = suc.chave
            atual.valor = suc.valor
            pai = pai_suc
            atual = suc
        filho = atual.esq if atual.esq is not None else atual.dir
        if pai is None:
            self._raiz = filho
        elif pai.esq is atual:
            pai.esq = filho
        else:
            pai.dir = filho
        self._tamanho -= 1

    def altura(self) -> int:
        """Número de níveis (0 se vazia), por percurso em largura."""
        if self._raiz is None:
            return 0
        fila = Fila()
        fila.enfileirar(self._raiz)
        niveis = 0
        while not fila.vazia():
            for _ in range(len(fila)):
                no = fila.desenfileirar()
                if no.esq is not None:
                    fila.enfileirar(no.esq)
                if no.dir is not None:
                    fila.enfileirar(no.dir)
            niveis += 1
        return niveis

    # --- percursos: devolvem ListaEncadeada de chaves ---------------------
    def em_ordem(self) -> ListaEncadeada:
        """Esquerda, raiz, direita (chaves em ordem crescente)."""
        res = ListaEncadeada()
        pilha = Pilha()
        atual = self._raiz
        while atual is not None or not pilha.vazia():
            while atual is not None:
                pilha.empilhar(atual)
                atual = atual.esq
            atual = pilha.desempilhar()
            res.inserir_fim(atual.chave)
            atual = atual.dir
        return res

    def pre_ordem(self) -> ListaEncadeada:
        """Raiz, esquerda, direita."""
        res = ListaEncadeada()
        pilha = Pilha()
        if self._raiz is not None:
            pilha.empilhar(self._raiz)
        while not pilha.vazia():
            no = pilha.desempilhar()
            res.inserir_fim(no.chave)
            if no.dir is not None:
                pilha.empilhar(no.dir)
            if no.esq is not None:
                pilha.empilhar(no.esq)
        return res

    def pos_ordem(self) -> ListaEncadeada:
        """Esquerda, direita, raiz (duas pilhas)."""
        res = ListaEncadeada()
        entrada = Pilha()
        saida = Pilha()
        if self._raiz is not None:
            entrada.empilhar(self._raiz)
        while not entrada.vazia():
            no = entrada.desempilhar()
            saida.empilhar(no)
            if no.esq is not None:
                entrada.empilhar(no.esq)
            if no.dir is not None:
                entrada.empilhar(no.dir)
        while not saida.vazia():
            res.inserir_fim(saida.desempilhar().chave)
        return res

    def autocompletar(self, prefixo: str) -> ListaEncadeada:
        """Chaves (str) que começam com `prefixo`, em ordem crescente.

        Pré: chaves da árvore são str. Percurso em-ordem com poda: ignora
        subárvores menores que o prefixo e para na primeira chave maior que
        todas as que têm o prefixo.
        """
        res = ListaEncadeada()
        pilha = Pilha()
        atual = self._raiz
        while atual is not None or not pilha.vazia():
            while atual is not None:
                if atual.chave >= prefixo:
                    pilha.empilhar(atual)
                    atual = atual.esq
                else:
                    atual = atual.dir
            if pilha.vazia():
                break
            atual = pilha.desempilhar()
            if not atual.chave.startswith(prefixo):
                break
            res.inserir_fim(atual.chave)
            atual = atual.dir
        return res
