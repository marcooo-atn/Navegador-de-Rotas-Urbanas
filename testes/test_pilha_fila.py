import unittest

from tads.excecoes import EstruturaVaziaError
from tads.fila import Fila
from tads.pilha import Pilha


class TestPilha(unittest.TestCase):
    def test_lifo(self):
        p = Pilha()
        for x in (1, 2, 3):
            p.empilhar(x)
        self.assertEqual(p.topo(), 3)
        self.assertEqual([p.desempilhar() for _ in range(3)], [3, 2, 1])
        self.assertTrue(p.vazia())

    def test_vazia(self):
        with self.assertRaises(EstruturaVaziaError):
            Pilha().desempilhar()
        with self.assertRaises(EstruturaVaziaError):
            Pilha().topo()


class TestFila(unittest.TestCase):
    def test_fifo(self):
        f = Fila()
        for x in (1, 2, 3):
            f.enfileirar(x)
        self.assertEqual(f.primeiro(), 1)
        self.assertEqual([f.desenfileirar() for _ in range(3)], [1, 2, 3])
        self.assertTrue(f.vazia())

    def test_reuso_apos_esvaziar(self):
        f = Fila()
        f.enfileirar(1); f.desenfileirar(); f.enfileirar(2)
        self.assertEqual(f.desenfileirar(), 2)

    def test_vazia(self):
        with self.assertRaises(EstruturaVaziaError):
            Fila().desenfileirar()
        with self.assertRaises(EstruturaVaziaError):
            Fila().primeiro()


if __name__ == "__main__":
    unittest.main()
