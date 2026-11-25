import unittest

from tads.excecoes import (ElementoInexistenteError, EstruturaVaziaError,
                           PosicaoInvalidaError)
from tads.lista_dupla import ListaDupla


class TestListaDupla(unittest.TestCase):
    def setUp(self):
        self.l = ListaDupla()
        for x in (1, 2, 3):
            self.l.inserir_fim(x)

    def test_dois_sentidos(self):
        self.assertEqual(list(self.l.percorrer_frente()), [1, 2, 3])
        self.assertEqual(list(self.l.percorrer_tras()), [3, 2, 1])

    def test_inserir_inicio(self):
        self.l.inserir_inicio(0)
        self.assertEqual(list(self.l.percorrer_frente()), [0, 1, 2, 3])
        self.assertEqual(list(self.l.percorrer_tras()), [3, 2, 1, 0])

    def test_cursor(self):
        self.assertEqual(self.l.cursor_atual(), 1)
        self.assertEqual(self.l.avancar(), 2)
        self.l.ir_para_fim()
        self.assertFalse(self.l.tem_proximo())
        self.assertEqual(self.l.voltar(), 2)
        with self.assertRaises(PosicaoInvalidaError):
            self.l.ir_para_inicio(); self.l.voltar()

    def test_cursor_vazio(self):
        with self.assertRaises(EstruturaVaziaError):
            ListaDupla().cursor_atual()

    def test_remover_ligacoes(self):
        self.l.remover(2)
        self.assertEqual(list(self.l.percorrer_frente()), [1, 3])
        self.assertEqual(list(self.l.percorrer_tras()), [3, 1])
        self.l.remover(1); self.l.remover(3)
        self.assertTrue(self.l.vazia())
        self.assertEqual(list(self.l.percorrer_tras()), [])

    def test_remover_move_cursor(self):
        self.l.ir_para_fim()
        self.l.remover(3)
        self.assertEqual(self.l.cursor_atual(), 2)

    def test_remover_inexistente(self):
        with self.assertRaises(ElementoInexistenteError):
            self.l.remover(99)


if __name__ == "__main__":
    unittest.main()
