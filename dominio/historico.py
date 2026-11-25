"""Histórico de rotas navegável nos dois sentidos (item 2.3)."""
from tads.lista_dupla import ListaDupla


class Historico:
    def __init__(self):
        self._rotas = ListaDupla()

    def __len__(self) -> int:
        return len(self._rotas)

    def registrar(self, rota) -> None:
        """Pós: rota é a mais recente e o cursor aponta para ela."""
        self._rotas.inserir_fim(rota)
        self._rotas.ir_para_fim()

    def atual(self):
        """Pré: histórico não vazio."""
        return self._rotas.cursor_atual()

    def anterior(self):
        """Pré: há rota anterior. Move o cursor e devolve a rota."""
        return self._rotas.voltar()

    def proxima(self):
        """Pré: há rota seguinte. Move o cursor e devolve a rota."""
        return self._rotas.avancar()

    def tem_anterior(self) -> bool:
        return self._rotas.tem_anterior()

    def tem_proxima(self) -> bool:
        return self._rotas.tem_proximo()
