def calcular_nomina(tipo_contrato, horas_diurnas, horas_nocturnas, horas_dominicales, valor_hora):
    """
    Calcula el pago a docentes con descuentos parafiscales según normativa colombiana
    
    Args:
        tipo_contrato: "tiempo_completo" o "medio_tiempo"
        horas_diurnas: Horas trabajadas en turno diurno (0-220)
        horas_nocturnas: Horas nocturnas trabajadas (recargo 35%)
        horas_dominicales: Horas dominicales/festivas trabajadas (recargo 75%)
        valor_hora: Valor de la hora ordinaria (debe ser positivo)
        
    Returns:
        dict: {
            'salario_bruto': float,
            'descuentos': float,
            'salario_neto': float,
            'tipo_contrato': str,
            'detalle_descuentos': {
                'salud': float,
                'pension': float,
                'cesantias': float
            }
        }
    """
    
    # Validaciones de entrada
    if not isinstance(horas_diurnas, (int, float)) or horas_diurnas < 0:
        raise ValueError("Horas diurnas inválidas")
    if not isinstance(horas_nocturnas, (int, float)) or horas_nocturnas < 0:
        raise ValueError("Horas nocturnas inválidas")
    if not isinstance(horas_dominicales, (int, float)) or horas_dominicales < 0:
        raise ValueError("Horas dominicales inválidas")
    if not isinstance(valor_hora, (int, float)) or valor_hora <= 0:
        raise ValueError("Valor hora inválido")
    
    total_horas = horas_diurnas + horas_nocturnas + horas_dominicales
    if total_horas > 220:
        raise ValueError("Máximo 220 horas mensuales")
    if total_horas == 0:
        raise ValueError("Debe trabajar al menos 1 hora")
    
    # Cálculo del salario bruto
    salario_base = horas_diurnas * valor_hora
    recargo_nocturno = horas_nocturnas * valor_hora * 1.35
    recargo_dominical = horas_dominicales * valor_hora * 1.75
    
    salario_bruto = salario_base + recargo_nocturno + recargo_dominical
    
    # Cálculo de descuentos según tipo de contrato
    if tipo_contrato == "tiempo_completo":
        salud = salario_bruto * 0.04
        pension = salario_bruto * 0.04
        cesantias = salario_bruto * 0.0833
    elif tipo_contrato == "medio_tiempo":
        salud = salario_bruto * 0.04
        pension = salario_bruto * 0.04
        cesantias = salario_bruto * 0.0417
    else:
        raise ValueError("Tipo de contrato inválido")
    
    total_descuentos = salud + pension + cesantias
    salario_neto = salario_bruto - total_descuentos
    
    # Estructura completa de retorno
    return {
        'salario_bruto': round(salario_bruto, 2),
        'descuentos': round(total_descuentos, 2),
        'salario_neto': round(salario_neto, 2),
        'tipo_contrato': tipo_contrato,
        'detalle_descuentos': {
            'salud': round(salud, 2),
            'pension': round(pension, 2),
            'cesantias': round(cesantias, 2)
        }
    }