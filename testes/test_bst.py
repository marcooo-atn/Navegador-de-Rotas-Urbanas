import unittest

from tads.arvore_bst import ArvoreBST
from tads.excecoes import ChaveDuplicadaError, ElementoInexistenteError


def montar(chaves):
    a = ArvoreBST()
    for c in chaves:
        a.inserir(c)
    return a


class TestBST(unittest.TestCase):
    def setUp(self):
        self.a = montar([50, 30, 70, 20, 40, 60, 80])

    def test_percursos(self):
        self.assertEqual(list(self.a.em_ordem()), [20, 30, 40, 50, 60, 70, 80])
        self.assertEqual(list(self.a.pre_ordem()), [50, 30, 20, 40, 70, 60, 80])
        self.assertEqual(list(self.a.pos_ordem()), [20, 40, 30, 60, 80, 70, 50])

    def test_buscar(self):
        self.assertEqual(self.a.buscar(60).chave, 60)
        self.assertIsNone(self.a.buscar(99))

    def test_duplicada(self):
        with self.assertRaises(ChaveDuplicadaError):
            self.a.inserir(40)

    def test_remover_tres_casos(self):
        self.a.remover(20)                       # folha
        self.a.remover(30)                       # um filho
        self.a.remover(50)                       # dois filhos (raiz)
        self.assertEqual(list(self.a.em_ordem()), [40, 60, 70, 80])
        self.assertEqual(len(self.a), 4)

    def test_remover_inexistente_e_vazia(self):
        with self.assertRaises(ElementoInexistenteError):
            self.a.remover(1)
        with self.assertRaises(ElementoInexistenteError):
            ArvoreBST().remover(1)

    def test_remover_ate_esvaziar(self):
        a = montar([2, 1, 3])
        for c in (2, 1, 3):
            a.remover(c)
        self.assertTrue(a.vazia())
        self.assertEqual(a.altura(), 0)

    def test_altura(self):
        self.assertEqual(self.a.altura(), 3)

    def test_desbalanceamento_sem_recursao(self):
        a = montar(range(5000))                  # dados ordenados
        self.assertEqual(a.altura(), 5000)       # vira uma lista
        self.assertEqual(len(a.em_ordem()), 5000)

    def test_autocompletar(self):
        a = montar(["praça central", "parque das águas", "padaria", "mercado", "pizzaria"])
        self.assertEqual(list(a.autocompletar("pa")), ["padaria", "parque das águas"])
        self.assertEqual(list(a.autocompletar("p")),
                         ["padaria", "parque das águas", "pizzaria", "praça central"])
        self.assertEqual(len(a.autocompletar("z")), 0)
        self.assertEqual(len(ArvoreBST().autocompletar("a")), 0)


if __name__ == "__main__":
    unittest.main()
