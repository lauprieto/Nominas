import unittest
from nomina import calcular_nomina

class TestNomina(unittest.TestCase):

    def test_nomina(self):
        """Cálculo básico para tiempo completo sin horas extras"""

        tipo_contrato = "tiempo_completo"
        horas_diurnas = 160
        horas_nocturnas = 0
        horas_dominicales = 0
        valor_hora = 50000
        salario_esperado = 8000000
        descuentos_esperados = salario_esperado * (0.04 + 0.04 + 0.0833)
        salario_neto_esperado = salario_esperado - descuentos_esperados

        resultado = calcular_nomina(tipo_contrato, horas_diurnas, horas_nocturnas, horas_dominicales, valor_hora)

        self.assertEqual(resultado["salario_bruto"], salario_esperado)
        self.assertAlmostEqual(resultado["salario_neto"], salario_neto_esperado, places=2)
        self.assertAlmostEqual(resultado["detalle_descuentos"]["salud"], salario_esperado * 0.04, places=2)
        self.assertEqual(resultado["tipo_contrato"], tipo_contrato)

if __name__ == "__main__":
    unittest.main()
