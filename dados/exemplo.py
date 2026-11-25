"""Dados FICTÍCIOS da cidade de Nova Aurora (nenhum dado real)."""
from dominio.mapa import MapaUrbano

LOCAIS = (
    ("Praça Central", "Centro", "Praça", 4.5),
    ("Mercado Municipal", "Centro", "Comércio", 4.2),
    ("Biblioteca Aurora", "Centro", "Cultura", 4.8),
    ("Hospital Sul", "Jardim", "Saúde", 4.0),
    ("Parque das Águas", "Jardim", "Lazer", 4.7),
    ("Terminal Norte", "Norte", "Transporte", 3.9),
    ("Universidade Nova", "Norte", "Educação", 4.6),
    ("Estádio Municipal", "Leste", "Esporte", 4.1),
    ("Café do Porto", "Leste", "Alimentação", 4.4),
    ("Farol Distante", "Ilha", "Turismo", 4.9),   # isolado de propósito
)

CONEXOES = (
    ("Praça Central", "Mercado Municipal", 0.8),
    ("Praça Central", "Biblioteca Aurora", 0.5),
    ("Mercado Municipal", "Hospital Sul", 2.0),
    ("Biblioteca Aurora", "Terminal Norte", 3.1),
    ("Hospital Sul", "Parque das Águas", 1.2),
    ("Terminal Norte", "Universidade Nova", 1.5),
    ("Praça Central", "Estádio Municipal", 2.4),
    ("Estádio Municipal", "Café do Porto", 0.9),
    ("Parque das Águas", "Café do Porto", 3.5),
)


def criar_mapa_exemplo(capacidade: int = 100) -> MapaUrbano:
    mapa = MapaUrbano(capacidade)
    for nome, bairro, categoria, avaliacao in LOCAIS:
        mapa.adicionar_local(nome, bairro, categoria, avaliacao)
    for a, b, km in CONEXOES:
        mapa.conectar(mapa.buscar_por_nome(a).id, mapa.buscar_por_nome(b).id, km)
    return mapa
