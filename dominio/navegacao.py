"""Pilha de telas (botão voltar) e fila de solicitações de rota (item 2.4)."""
from tads.excecoes import EstruturaVaziaError
from tads.fila import Fila
from tads.pilha import Pilha


class Navegacao:
    def __init__(self):
        self._telas = Pilha()
        self._pendentes = Fila()

    # --- botão voltar (Pilha) ---
    def entrar(self, tela: str) -> None:
        self._telas.empilhar(tela)

    def pode_voltar(self) -> bool:
        return len(self._telas) > 1

    def voltar(self) -> str:
        """Pré: pode_voltar(). Descarta a tela atual e devolve a anterior."""
        if not self.pode_voltar():
            raise EstruturaVaziaError("não há tela anterior")
        self._telas.desempilhar()
        return self._telas.topo()

    def tela_atual(self) -> str:
        return self._telas.topo()

    # --- solicitações pendentes (Fila) ---
    def solicitar_rota(self, id_origem: int, id_destino: int) -> None:
        self._pendentes.enfileirar((id_origem, id_destino))

    def proxima_solicitacao(self):
        """Pré: há solicitação pendente. Devolve (origem, destino) mais antiga."""
        return self._pendentes.desenfileirar()

    def pendentes(self) -> int:
        return len(self._pendentes)
