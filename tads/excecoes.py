"""Exceções próprias usadas para verificar pré-condições dos TADs."""


class PreCondicaoError(Exception):
    """Base: uma pré-condição de operação não foi respeitada."""


class EstruturaVaziaError(PreCondicaoError):
    """Operação exige estrutura não vazia."""


class EstruturaCheiaError(PreCondicaoError):
    """Operação exige estrutura com espaço livre."""


class PosicaoInvalidaError(PreCondicaoError):
    """Posição fora do intervalo permitido."""


class ElementoInexistenteError(PreCondicaoError):
    """Elemento, chave ou vértice não existe na estrutura."""


class ChaveDuplicadaError(PreCondicaoError):
    """A chave já existe e a estrutura não aceita repetidos."""
