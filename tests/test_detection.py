import unittest
import os
import sys
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.engine_ai import AIEngine

class TestHeuristics(unittest.TestCase):
    def setUp(self):
        self.ai = AIEngine()
        self.test_file = "temp_virus.exe"

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_high_entropy_detection(self):
        # Crear archivo con datos totalmente aleatorios (Alta entropía)
        with open(self.test_file, 'wb') as f:
            f.write(os.urandom(1024 * 10)) # 10KB de ruido puro

        is_threat, reason, score = self.ai.scan_file(self.test_file)
        
        print(f"\n[TEST] Score de amenaza: {score} - Razón: {reason}")
        self.assertTrue(score > 50, "Debería detectar alta entropía como sospechoso")

if __name__ == '__main__':
    unittest.main()