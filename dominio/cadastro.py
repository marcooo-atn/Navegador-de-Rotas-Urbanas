"""Cadastro de locais: vetor de registros com CRUD (item 1.4)."""
from dominio.local import Local
from tads.excecoes import ChaveDuplicadaError, ElementoInexistenteError
from tads.lista_estatica import ListaEstatica


class Cadastro:
    """Vetor (capacidade fixa) de registros `Local`."""

    def __init__(self, capacidade: int):
        self._locais = ListaEstatica(capacidade)

    def __len__(self) -> int:
        return len(self._locais)

    def incluir(self, local: Local) -> None:
        """Pré: id inédito e cadastro não cheio (a lista estática verifica)."""
        if self.buscar_por_id(local.id) is not None:
            raise ChaveDuplicadaError(f"id {local.id} já cadastrado")
        self._locais.inserir_fim(local)

    def listar(self):
        """Gera os locais na ordem de cadastro."""
        return iter(self._locais)

    def buscar_por_id(self, id_local: int):
        """Busca sequencial; devolve o Local ou None."""
        for local in self._locais:
            if local.id == id_local:
                return local
        return None

    def alterar(self, id_local: int, nome=None, bairro=None,
                categoria=None, avaliacao=None) -> None:
        """Pré: id existe. Só os campos informados são alterados."""
        local = self.buscar_por_id(id_local)
        if local is None:
            raise ElementoInexistenteError(f"local {id_local} não existe")
        if nome is not None:
            local.nome = nome
        if bairro is not None:
            local.bairro = bairro
        if categoria is not None:
            local.categoria = categoria
        if avaliacao is not None:
            local.avaliacao = avaliacao

    def excluir(self, id_local: int) -> None:
        """Pré: id existe. Pós: registro removido do vetor."""
        for pos in range(len(self._locais)):
            if self._locais[pos].id == id_local:
                self._locais.remover(pos)
                return
        raise ElementoInexistenteError(f"local {id_local} não existe")
