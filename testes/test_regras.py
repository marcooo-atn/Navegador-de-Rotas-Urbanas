"""Verifica automaticamente as proibições da Seção 3 do enunciado
nos módulos de estruturas e algoritmos (tads/ e algoritmos/)."""
import ast
import os
import unittest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
METODOS_PROIBIDOS = {"append", "pop", "insert", "sort", "popleft", "appendleft"}
FUNCOES_PROIBIDAS = {"set", "dict", "sorted", "frozenset"}
MODULOS_PROIBIDOS = {"collections", "queue", "heapq", "bisect", "networkx"}


def arquivos():
    for pasta in ("tads", "algoritmos"):
        for nome in sorted(os.listdir(os.path.join(RAIZ, pasta))):
            if nome.endswith(".py"):
                yield os.path.join(RAIZ, pasta, nome)


class TestRegras(unittest.TestCase):
    def test_sem_recursos_proibidos(self):
        problemas = []
        for caminho in arquivos():
            with open(caminho, encoding="utf-8") as f:
                arvore = ast.parse(f.read())
            for no in ast.walk(arvore):
                if isinstance(no, ast.Call):
                    if isinstance(no.func, ast.Attribute) and no.func.attr in METODOS_PROIBIDOS:
                        problemas.append(f"{caminho}:{no.lineno} .{no.func.attr}()")
                    if isinstance(no.func, ast.Name) and no.func.id in FUNCOES_PROIBIDAS:
                        problemas.append(f"{caminho}:{no.lineno} {no.func.id}()")
                if isinstance(no, ast.Import):
                    for alias in no.names:
                        if alias.name.split(".")[0] in MODULOS_PROIBIDOS:
                            problemas.append(f"{caminho}:{no.lineno} import {alias.name}")
                if isinstance(no, ast.ImportFrom) and (no.module or "").split(".")[0] in MODULOS_PROIBIDOS:
                    problemas.append(f"{caminho}:{no.lineno} from {no.module}")
        self.assertEqual(problemas, [], "\n".join(problemas))


if __name__ == "__main__":
    unittest.main()
