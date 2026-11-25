import unittest

from tads.excecoes import (ElementoInexistenteError, EstruturaVaziaError,
                           PosicaoInvalidaError)
from tads.lista_encadeada import ListaEncadeada


class TestListaEncadeada(unittest.TestCase):
    def test_insercoes(self):
        l = ListaEncadeada()
        l.inserir_fim(2); l.inserir_inicio(1); l.inserir_fim(4)
        l.inserir_posicao(2, 3)
        self.assertEqual(list(l), [1, 2, 3, 4])
        self.assertEqual(len(l), 4)

    def test_inserir_posicao_extremos_e_invalida(self):
        l = ListaEncadeada()
        l.inserir_posicao(0, "a"); l.inserir_posicao(1, "c"); l.inserir_posicao(1, "b")
        self.assertEqual(list(l), ["a", "b", "c"])
        with self.assertRaises(PosicaoInvalidaError):
            l.inserir_posicao(9, "x")

    def test_remover_valor(self):
        l = ListaEncadeada()
        for x in (1, 2, 3):
            l.inserir_fim(x)
        l.remover(3)            # remove o fim
        l.inserir_fim(9)        # o fim deve continuar consistente
        l.remover(1)            # remove o início
        self.assertEqual(list(l), [2, 9])

    def test_remover_inexistente(self):
        l = ListaEncadeada()
        l.inserir_fim(1)
        with self.assertRaises(ElementoInexistenteError):
            l.remover(7)

    def test_remover_unico_zera_fim(self):
        l = ListaEncadeada()
        l.inserir_fim(1); l.remover(1)
        self.assertTrue(l.vazia())
        l.inserir_fim(2)
        self.assertEqual(list(l), [2])

    def test_remover_posicao(self):
        l = ListaEncadeada()
        for x in "abc":
            l.inserir_fim(x)
        self.assertEqual(l.remover_posicao(2), "c")
        l.inserir_fim("d")
        self.assertEqual(list(l), ["a", "b", "d"])
        with self.assertRaises(PosicaoInvalidaError):
            l.remover_posicao(3)
        with self.assertRaises(EstruturaVaziaError):
            ListaEncadeada().remover_posicao(0)

    def test_buscar_e_obter(self):
        l = ListaEncadeada()
        l.inserir_fim(5); l.inserir_fim(6)
        self.assertEqual(l.buscar(6).valor, 6)
        self.assertIsNone(l.buscar(7))
        self.assertEqual(l.obter(1), 6)


if __name__ == "__main__":
    unittest.main()
