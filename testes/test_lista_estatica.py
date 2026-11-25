import unittest

from tads.excecoes import (EstruturaCheiaError, EstruturaVaziaError,
                           PosicaoInvalidaError, PreCondicaoError)
from tads.lista_estatica import ListaEstatica


class TestListaEstatica(unittest.TestCase):
    def test_capacidade_invalida(self):
        with self.assertRaises(PreCondicaoError):
            ListaEstatica(0)

    def test_inserir_meio_desloca(self):
        l = ListaEstatica(5)
        l.inserir_fim(1); l.inserir_fim(3); l.inserir(1, 2)
        self.assertEqual(list(l), [1, 2, 3])
        self.assertEqual(len(l), 3)

    def test_cheia(self):
        l = ListaEstatica(2)
        l.inserir_fim("a"); l.inserir_fim("b")
        self.assertTrue(l.cheia())
        with self.assertRaises(EstruturaCheiaError):
            l.inserir_fim("c")

    def test_vazia(self):
        with self.assertRaises(EstruturaVaziaError):
            ListaEstatica(3).remover(0)

    def test_posicao_invalida(self):
        l = ListaEstatica(3)
        l.inserir_fim(1)
        for pos in (-1, 1, 5):
            with self.assertRaises(PosicaoInvalidaError):
                l.consultar(pos)
        with self.assertRaises(PosicaoInvalidaError):
            l.inserir(3, 9)

    def test_remover_atualizar_buscar(self):
        l = ListaEstatica(4)
        for x in (10, 20, 30):
            l.inserir_fim(x)
        self.assertEqual(l.remover(1), 20)
        self.assertEqual(list(l), [10, 30])
        l.atualizar(0, 11)
        self.assertEqual(l.consultar(0), 11)
        self.assertEqual(l.buscar(30), 1)
        self.assertEqual(l.buscar(99), -1)

    def test_preenchida(self):
        l = ListaEstatica.preenchida(3, False)
        self.assertTrue(l.cheia())
        self.assertEqual(list(l), [False] * 3)


if __name__ == "__main__":
    unittest.main()
