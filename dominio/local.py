"""Registros do domínio (item 1.4)."""
from dataclasses import dataclass

from tads.lista_encadeada import ListaEncadeada


@dataclass
class Local:
    """Registro do cadastro de locais. `id` é também o vértice no grafo."""
    id: int
    nome: str
    bairro: str
    categoria: str
    avaliacao: float


@dataclass
class Rota:
    """Resultado de uma rota calculada (guardado no histórico)."""
    origem: str
    destino: str
    paradas: ListaEncadeada   # nomes dos locais, na ordem do trajeto
    distancia: float
