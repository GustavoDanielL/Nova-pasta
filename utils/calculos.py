def calcular_juros_compostos(capital, taxa_mensal, periodo_meses):
    """Calcula montante com juros compostos: M = C * (1 + i)^n"""
    return capital * ((1 + taxa_mensal) ** periodo_meses)

def calcular_juros_simples(capital, taxa_mensal, periodo_meses):
    """Calcula montante com juros simples: M = C * (1 + i * n)"""
    return capital * (1 + taxa_mensal * periodo_meses)

def calcular_parcela_fixa(capital, taxa_mensal, periodo_meses):
    """Calcula valor da parcela fixa usando fórmula Price"""
    if taxa_mensal == 0:
        return capital / periodo_meses
    
    return capital * (taxa_mensal * (1 + taxa_mensal) ** periodo_meses) / ((1 + taxa_mensal) ** periodo_meses - 1)

def formatar_moeda(valor):
    return f"R$ {valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')


def formatar_moeda_simplified(valor):
    """Legacy helper preserved for compatibility.
    Now returns a full two-decimal currency string (R$ 1.234,56).
    """
    try:
        return formatar_moeda(float(valor))
    except Exception:
        return formatar_moeda(0.0)


def formatar_moeda_short(valor):
    """Return a full currency string with two decimals.
    The compact short format was removed to keep consistent two-decimal displays.
    """
    try:
        return formatar_moeda(float(valor))
    except Exception:
        return formatar_moeda(0.0)