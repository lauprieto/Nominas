import pytest # type: ignore
from nomina import calcular_nomina

def test_tiempo_completo_sin_recargos():
    """Cálculo básico para tiempo completo sin horas extras"""
    resultado = calcular_nomina("tiempo_completo", 160, 0, 0, 50000)
    assert resultado["salario_bruto"] == 8000000
    assert resultado["salario_neto"] == pytest.approx(8000000 * (1 - 0.04 - 0.04 - 0.0833), rel=1e-3)
    assert resultado["detalle_descuentos"]["salud"] == pytest.approx(8000000 * 0.04)
    assert resultado["tipo_contrato"] == "tiempo_completo"

def test_medio_tiempo_sin_recargos():
    """Cálculo básico para medio tiempo sin horas extras"""
    resultado = calcular_nomina("medio_tiempo", 80, 0, 0, 50000)
    assert resultado["salario_bruto"] == 4000000
    assert resultado["salario_neto"] == pytest.approx(4000000 * (1 - 0.04 - 0.04 - 0.0417), rel=1e-3)
    assert resultado["detalle_descuentos"]["cesantias"] == pytest.approx(4000000 * 0.0417)

def test_recargo_nocturno_tiempo_completo():
    """Cálculo con horas nocturnas (35% recargo)"""
    resultado = calcular_nomina("tiempo_completo", 0, 10, 0, 50000)
    assert resultado["salario_bruto"] == pytest.approx(10 * 50000 * 1.35)
    assert resultado["salario_neto"] == pytest.approx(675000 * (1 - 0.04 - 0.04 - 0.0833))
    assert resultado["detalle_descuentos"]["pension"] == pytest.approx(675000 * 0.04)

def test_recargo_dominical_tiempo_completo():
    """Cálculo con horas dominicales (75% recargo)"""
    resultado = calcular_nomina("tiempo_completo", 0, 0, 10, 50000)
    assert resultado["salario_bruto"] == pytest.approx(10 * 50000 * 1.75)
    assert resultado["salario_neto"] == pytest.approx(875000 * (1 - 0.04 - 0.04 - 0.0833))
    assert resultado["detalle_descuentos"]["salud"] == pytest.approx(875000 * 0.04)

def test_combinacion_horas_extras():
    """Cálculo combinando diferentes tipos de horas"""
    resultado = calcular_nomina("tiempo_completo", 100, 20, 10, 50000)
    bruto_esperado = (100*50000) + (20*50000*1.35) + (10*50000*1.75)
    assert resultado["salario_bruto"] == pytest.approx(bruto_esperado)
    assert sum(resultado["detalle_descuentos"].values()) == pytest.approx(resultado["descuentos"])

def test_horas_negativas_error():
    """Validación de horas negativas"""
    with pytest.raises(ValueError, match="Horas diurnas inválidas"):
        calcular_nomina("tiempo_completo", -10, 0, 0, 50000)

def test_valor_hora_cero_error():
    """Validación de valor hora cero"""
    with pytest.raises(ValueError, match="Valor hora inválido"):
        calcular_nomina("tiempo_completo", 10, 0, 0, 0)

def test_maximo_horas_mensuales():
    """Validación de máximo 220 horas mensuales"""
    with pytest.raises(ValueError, match="Máximo 220 horas mensuales"):
        calcular_nomina("tiempo_completo", 221, 0, 0, 50000)

def test_tipo_contrato_invalido():
    """Validación de tipo de contrato inválido"""
    with pytest.raises(ValueError, match="Tipo de contrato inválido"):
        calcular_nomina("contrato_invalido", 160, 0, 0, 50000)

def test_formato_resultado():
    """Validación del formato del resultado"""
    resultado = calcular_nomina("tiempo_completo", 1, 0, 0, 50000)
    assert isinstance(resultado, dict)
    required_keys = ['salario_bruto', 'descuentos', 'salario_neto', 'tipo_contrato', 'detalle_descuentos']
    assert all(key in resultado for key in required_keys)
    assert isinstance(resultado["detalle_descuentos"], dict)
    assert set(resultado["detalle_descuentos"].keys()) == {'salud', 'pension', 'cesantias'}

def test_salario_neto_no_negativo():
    """Validación que el salario neto no sea negativo"""
    resultado = calcular_nomina("tiempo_completo", 1, 0, 0, 1000)
    assert resultado["salario_neto"] >= 0
    assert resultado["detalle_descuentos"]["salud"] >= 0

def test_ejemplo_4_horas_20000():
    """Prueba específica de 4 horas a $20,000"""
    resultado = calcular_nomina("tiempo_completo", 4, 0, 0, 20000)
    assert resultado["salario_bruto"] == 80000
    assert resultado["salario_neto"] == pytest.approx(80000 * (1 - 0.04 - 0.04 - 0.0833))
    assert resultado["detalle_descuentos"]["cesantias"] == pytest.approx(80000 * 0.0833)

def test_comparacion_60mil():
    """Comparación con valor hora de 60,000"""
    resultado = calcular_nomina("tiempo_completo", 4, 0, 0, 60000)
    assert resultado["salario_bruto"] == 240000
    assert 4 * 60000 == 240000
    assert resultado["detalle_descuentos"]["pension"] == pytest.approx(240000 * 0.04)

def test_horas_no_numericas_error():
    """Validación de horas no numéricas"""
    with pytest.raises(ValueError):
        calcular_nomina("tiempo_completo", "a", 0, 0, 50000)

def test_cero_horas_error():
    """Validación de cero horas trabajadas"""
    with pytest.raises(ValueError, match="Debe trabajar al menos 1 hora"):
        calcular_nomina("tiempo_completo", 0, 0, 0, 50000)

def test_precision_calculos():
    """Validación de precisión en cálculos con decimales"""
    resultado = calcular_nomina("tiempo_completo", 1, 0, 0, 33333.33)
    assert resultado["salario_bruto"] == pytest.approx(33333.33, rel=1e-3)
    assert resultado["detalle_descuentos"]["salud"] == pytest.approx(33333.33 * 0.04, rel=1e-3)

def test_redondeo_a_dos_decimales():
    """Validación de redondeo a dos decimales"""
    resultado = calcular_nomina("tiempo_completo", 3, 0, 0, 33333.333)
    assert isinstance(resultado["salario_bruto"], float)
    assert len(str(resultado["salario_bruto"]).split('.')[1]) <= 2
    assert len(str(resultado["detalle_descuentos"]["cesantias"]).split('.')[1]) <= 2

def test_diferencias_tipos_contrato():
    """Comparación de descuentos entre tipos de contrato"""
    full_time = calcular_nomina("tiempo_completo", 100, 0, 0, 50000)
    half_time = calcular_nomina("medio_tiempo", 100, 0, 0, 50000)
    assert full_time["descuentos"] > half_time["descuentos"]
    assert full_time["detalle_descuentos"]["cesantias"] > half_time["detalle_descuentos"]["cesantias"]

def test_completo_vs_medio_tiempo():
    """Comparación directa tiempo completo vs medio tiempo"""
    full_time = calcular_nomina("tiempo_completo", 160, 0, 0, 50000)
    half_time = calcular_nomina("medio_tiempo", 80, 0, 0, 50000)
    assert full_time["salario_bruto"] == 2 * half_time["salario_bruto"]
    assert full_time["descuentos"] > 2 * half_time["descuentos"]
    assert full_time["detalle_descuentos"]["cesantias"] == pytest.approx(2 * half_time["detalle_descuentos"]["cesantias"] * 2, rel=0.1)

def test_estructura_detalle_descuentos():
    """Validación de estructura de detalle de descuentos"""
    resultado = calcular_nomina("tiempo_completo", 10, 0, 0, 50000)
    detalle = resultado["detalle_descuentos"]
    assert isinstance(detalle, dict)
    assert set(detalle.keys()) == {'salud', 'pension', 'cesantias'}
    assert sum(detalle.values()) == pytest.approx(resultado["descuentos"], rel=1e-3)
    assert all(valor >= 0 for valor in detalle.values())