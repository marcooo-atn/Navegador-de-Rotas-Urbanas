import os
import tempfile
import unittest

from algoritmos.ordenacao import esta_ordenada
from benchmark import benchmark as bm


class TestBenchmark(unittest.TestCase):
    def test_cenarios_de_dados(self):
        ordenada = bm.gerar_dados(50, "ordenada")
        inversa = bm.gerar_dados(50, "inversa")
        aleatoria = bm.gerar_dados(50, "aleatoria")
        self.assertTrue(esta_ordenada(ordenada, bm.CHAVE))
        self.assertEqual([l.id for l in inversa], list(range(49, -1, -1)))
        self.assertFalse(esta_ordenada(aleatoria, bm.CHAVE))
        self.assertEqual(sorted(l.id for l in aleatoria), list(range(50)))

    def test_dados_reproduziveis(self):
        a = [l.id for l in bm.gerar_dados(100, "aleatoria")]
        b = [l.id for l in bm.gerar_dados(100, "aleatoria")]
        self.assertEqual(a, b)

    def test_cenario_invalido(self):
        with self.assertRaises(ValueError):
            bm.gerar_dados(5, "xyz")

    def test_execucao_pequena_gera_csv_e_retoma(self):
        with tempfile.TemporaryDirectory() as pasta:
            caminho = os.path.join(pasta, "r", "o.csv")
            bm.executar(caminho, (30,), 30)
            linhas = bm.ler_csv(caminho)
            self.assertEqual(len(linhas), 5 * 3)          # 5 algoritmos x 3 cenários
            bm.executar(caminho, (30,), 30)               # retomada: nada novo
            self.assertEqual(len(bm.ler_csv(caminho)), 15)
            self.assertIn("bubble", bm.tabela_markdown(linhas, (30,)))


if __name__ == "__main__":
    unittest.main()
