import operator
import random
import unittest

from algoritmos.ordenacao import (ALGORITMOS, bubblesort, esta_ordenada,
                                  insertionsort, mergesort, obter_algoritmo,
                                  quicksort, selectionsort)
from dominio.local import Local
from tads.lista_estatica import ListaEstatica


def para_lista(valores, folga=3):
    lista = ListaEstatica(len(valores) + folga)
    for v in valores:
        lista.inserir_fim(v)
    return lista


def identidade(x):
    return x


class TestOrdenacaoNumeros(unittest.TestCase):
    def test_todos_os_cenarios(self):
        gerador = random.Random(7)
        for nome, ordenar in ALGORITMOS:
            for n in (0, 1, 2, 3, 10, 257):
                aleatorio = [gerador.random() for _ in range(n)]
                repetidos = [gerador.randrange(5) for _ in range(n)]
                casos = (aleatorio, sorted(aleatorio), sorted(aleatorio, reverse=True),
                         repetidos, [3] * n)
                for caso in casos:
                    lista = para_lista(caso)
                    ordenar(lista, identidade)
                    self.assertEqual(list(lista), sorted(caso), f"{nome} n={n}")

    def test_tamanho_e_capacidade_preservados(self):
        lista = para_lista([3, 1, 2], folga=4)
        mergesort(lista, identidade)
        self.assertEqual(len(lista), 3)
        self.assertEqual(lista.capacidade, 7)

    def test_quicksort_entrada_grande_ordenada_sem_recursao(self):
        lista = para_lista(list(range(20000)))
        quicksort(lista, identidade)
        self.assertTrue(esta_ordenada(lista, identidade))


class TestOrdenacaoRegistros(unittest.TestCase):
    def setUp(self):
        self.locais = (Local(0, "Zeta", "B", "x", 3.0), Local(1, "Alfa", "A", "x", 5.0),
                       Local(2, "Beta", "B", "x", 3.0), Local(3, "Delta", "A", "x", 4.5),
                       Local(4, "Gama", "C", "x", 5.0))

    def test_por_dois_campos_diferentes(self):
        for nome, ordenar in ALGORITMOS:
            por_nome = para_lista(self.locais)
            ordenar(por_nome, lambda l: l.nome)
            self.assertEqual([l.nome for l in por_nome],
                             ["Alfa", "Beta", "Delta", "Gama", "Zeta"], nome)
            por_nota = para_lista(self.locais)
            ordenar(por_nota, lambda l: (-l.avaliacao, l.nome))
            self.assertEqual([l.nome for l in por_nota],
                             ["Alfa", "Gama", "Delta", "Beta", "Zeta"], nome)

    def test_estabilidade_dos_estaveis(self):
        for ordenar in (bubblesort, insertionsort, mergesort):
            lista = para_lista(self.locais)
            ordenar(lista, operator.attrgetter("avaliacao"))
            # empates de nota mantêm a ordem original de cadastro
            self.assertEqual([l.id for l in lista], [0, 2, 3, 1, 4])

    def test_instaveis_ainda_ordenam(self):
        for ordenar in (selectionsort, quicksort):
            lista = para_lista(self.locais)
            ordenar(lista, operator.attrgetter("avaliacao"))
            self.assertTrue(esta_ordenada(lista, operator.attrgetter("avaliacao")))


class TestApoio(unittest.TestCase):
    def test_esta_ordenada(self):
        self.assertTrue(esta_ordenada(para_lista([]), identidade))
        self.assertTrue(esta_ordenada(para_lista([1, 1, 2]), identidade))
        self.assertFalse(esta_ordenada(para_lista([2, 1]), identidade))

    def test_obter_algoritmo(self):
        self.assertIs(obter_algoritmo("quick"), quicksort)
        with self.assertRaises(ValueError):
            obter_algoritmo("inexistente")

    def test_copiar_nao_altera_original(self):
        original = para_lista([3, 1, 2])
        copia = original.copiar()
        mergesort(copia, identidade)
        self.assertEqual(list(original), [3, 1, 2])
        self.assertEqual(list(copia), [1, 2, 3])


if __name__ == "__main__":
    unittest.main()
