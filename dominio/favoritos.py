"""Locais favoritos: lista estática de capacidade fixa 10 (item 1.5)."""
from tads.excecoes import ChaveDuplicadaError, ElementoInexistenteError
from tads.lista_estatica import ListaEstatica

CAPACIDADE_FAVORITOS = 10


class Favoritos:
    def __init__(self):
        self._ids = ListaEstatica(CAPACIDADE_FAVORITOS)

    def __len__(self) -> int:
        return len(self._ids)

    def adicionar(self, id_local: int) -> None:
        """Pré: id não repetido e há vaga (EstruturaCheiaError se cheia)."""
        if self._ids.buscar(id_local) != -1:
            raise ChaveDuplicadaError("local já é favorito")
        self._ids.inserir_fim(id_local)

    def remover(self, id_local: int) -> None:
        """Pré: id é favorito."""
        pos = self._ids.buscar(id_local)
        if pos == -1:
            raise ElementoInexistenteError("local não é favorito")
        self._ids.remover(pos)

    def remover_se_existir(self, id_local: int) -> None:
        pos = self._ids.buscar(id_local)
        if pos != -1:
            self._ids.remover(pos)

    def listar(self):
        return iter(self._ids)
