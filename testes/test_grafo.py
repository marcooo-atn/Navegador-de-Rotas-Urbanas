import unittest

from tads.excecoes import (ElementoInexistenteError, EstruturaCheiaError,
                           PreCondicaoError)
from tads.grafo import Grafo


def montar():
    """0-1-2-3 em linha, 0-4 e 4-3 (atalho), 5 isolado."""
    g = Grafo(10)
    for _ in range(6):
        g.adicionar_vertice()
    for u, v, p in ((0, 1, 1), (1, 2, 1), (2, 3, 1), (0, 4, 5), (4, 3, 5)):
        g.adicionar_aresta(u, v, p)
    return g


class TestGrafo(unittest.TestCase):
    def test_vertices_e_arestas(self):
        g = montar()
        self.assertEqual(len(g), 6)
        self.assertTrue(g.existe_aresta(1, 0))
        self.assertEqual(g.peso(0, 4), 5)
        self.assertEqual(list(g.vizinhos(0)), [1, 4])

    def test_pre_condicoes(self):
        g = montar()
        with self.assertRaises(PreCondicaoError):
            g.adicionar_aresta(0, 0, 1)
        with self.assertRaises(PreCondicaoError):
            g.adicionar_aresta(0, 2, 0)
        with self.assertRaises(PreCondicaoError):
            g.adicionar_aresta(0, 2, -3)
        with self.assertRaises(ElementoInexistenteError):
            g.adicionar_aresta(0, 99, 1)
        with self.assertRaises(ElementoInexistenteError):
            g.remover_aresta(0, 3)

    def test_capacidade(self):
        g = Grafo(1)
        g.adicionar_vertice()
        with self.assertRaises(EstruturaCheiaError):
            g.adicionar_vertice()

    def test_bfs_menos_paradas(self):
        g = montar()
        self.assertEqual(list(g.menor_caminho_paradas(0, 3)), [0, 4, 3])

    def test_bfs_bloqueado(self):
        g = montar()
        caminho = g.menor_caminho_paradas(0, 3, bloqueado=lambda v: v == 4)
        self.assertEqual(list(caminho), [0, 1, 2, 3])

    def test_bfs_casos_limite(self):
        g = montar()
        self.assertIsNone(g.menor_caminho_paradas(0, 5))            # sem conexão
        self.assertEqual(list(g.menor_caminho_paradas(2, 2)), [2])  # origem = destino
        with self.assertRaises(ElementoInexistenteError):
            g.menor_caminho_paradas(0, 42)

    def test_dfs_alcancaveis_e_isolados(self):
        g = montar()
        self.assertEqual(sorted_ids(g.alcancaveis(0)), [0, 1, 2, 3, 4])
        self.assertEqual(list(g.alcancaveis(5)), [5])
        self.assertEqual(list(g.isolados()), [5])

    def test_remover_vertice(self):
        g = montar()
        g.remover_vertice(4)
        self.assertFalse(g.existe_vertice(4))
        self.assertEqual(list(g.vizinhos(0)), [1])
        with self.assertRaises(ElementoInexistenteError):
            g.vizinhos(4)

    def test_custo(self):
        g = montar()
        self.assertEqual(g.custo_caminho(g.menor_caminho_paradas(0, 3)), 10)

    def test_grafo_vazio_e_unico_vertice(self):
        g = Grafo(3)
        self.assertEqual(len(g.vertices()), 0)
        v = g.adicionar_vertice()
        self.assertEqual(list(g.isolados()), [v])


def sorted_ids(lista):
    """Ordena ids só para comparar nos testes (fora das estruturas centrais)."""
    return sorted(lista)


if __name__ == "__main__":
    unittest.main()
