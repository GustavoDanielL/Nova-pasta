"""
Formatadores automáticos para campos de entrada
"""

def formatar_cpf_cnpj(valor):
    """Formata CPF (###.###.###-##) ou CNPJ (##.###.###/####-##) automaticamente"""
    # Remove tudo que não é número
    numeros = ''.join(c for c in valor if c.isdigit())
    
    if len(numeros) <= 11:  # CPF
        # Formato: 000.000.000-00
        if len(numeros) <= 3:
            return numeros
        elif len(numeros) <= 6:
            return f"{numeros[:3]}.{numeros[3:]}"
        elif len(numeros) <= 9:
            return f"{numeros[:3]}.{numeros[3:6]}.{numeros[6:]}"
        else:
            return f"{numeros[:3]}.{numeros[3:6]}.{numeros[6:9]}-{numeros[9:11]}"
    else:  # CNPJ
        # Formato: 00.000.000/0000-00
        if len(numeros) <= 2:
            return numeros
        elif len(numeros) <= 5:
            return f"{numeros[:2]}.{numeros[2:]}"
        elif len(numeros) <= 8:
            return f"{numeros[:2]}.{numeros[2:5]}.{numeros[5:]}"
        elif len(numeros) <= 12:
            return f"{numeros[:2]}.{numeros[2:5]}.{numeros[5:8]}/{numeros[8:]}"
        else:
            return f"{numeros[:2]}.{numeros[2:5]}.{numeros[5:8]}/{numeros[8:12]}-{numeros[12:14]}"


def formatar_telefone(valor):
    """Formata telefone (##) #####-#### ou (##) ####-####"""
    # Remove tudo que não é número
    numeros = ''.join(c for c in valor if c.isdigit())
    
    if len(numeros) == 0:
        return ""
    elif len(numeros) <= 2:
        return f"({numeros}"
    elif len(numeros) <= 6:
        return f"({numeros[:2]}) {numeros[2:]}"
    elif len(numeros) <= 10:
        # Telefone fixo: (##) ####-####
        return f"({numeros[:2]}) {numeros[2:6]}-{numeros[6:]}"
    else:
        # Celular: (##) #####-####
        return f"({numeros[:2]}) {numeros[2:7]}-{numeros[7:11]}"


def formatar_moeda_input(valor):
    """Formata valor monetário enquanto digita: 1000.50 -> 1.000,50"""
    # Remove tudo exceto números e vírgula/ponto
    numeros = ''.join(c for c in valor if c.isdigit() or c in '.,')
    
    # Substitui vírgula por ponto temporariamente
    numeros = numeros.replace(',', '.')
    
    # Remove pontos duplicados
    partes = numeros.split('.')
    if len(partes) > 2:
        numeros = partes[0] + '.' + ''.join(partes[1:])
    
    try:
        # Converte para float e formata
        if '.' in numeros:
            valor_float = float(numeros)
        else:
            valor_float = float(numeros) if numeros else 0.0
        
        # Formata com separador de milhares
        parte_inteira = int(valor_float)
        parte_decimal = int((valor_float - parte_inteira) * 100)
        
        # Adiciona separador de milhares
        str_inteira = f"{parte_inteira:,}".replace(',', '.')
        
        if '.' in numeros or parte_decimal > 0:
            return f"{str_inteira},{parte_decimal:02d}"
        else:
            return str_inteira
    except:
        return valor


def formatar_data(valor):
    """Formata data DD/MM/AAAA automaticamente"""
    # Remove tudo que não é número
    numeros = ''.join(c for c in valor if c.isdigit())
    
    if len(numeros) == 0:
        return ""
    elif len(numeros) <= 2:
        return numeros
    elif len(numeros) <= 4:
        return f"{numeros[:2]}/{numeros[2:]}"
    else:
        return f"{numeros[:2]}/{numeros[2:4]}/{numeros[4:8]}"


def formatar_porcentagem(valor):
    """Formata porcentagem: 10.5 -> 10,5%"""
    # Remove tudo exceto números e vírgula/ponto
    numeros = ''.join(c for c in valor if c.isdigit() or c in '.,')
    
    if not numeros:
        return ""
    
    # Substitui vírgula por ponto
    numeros = numeros.replace(',', '.')
    
    try:
        valor_float = float(numeros)
        # Limita a 2 casas decimais
        if '.' in numeros:
            return f"{valor_float:.1f}".replace('.', ',')
        else:
            return numeros
    except:
        return valor


def limpar_formatacao(valor):
    """Remove formatação deixando apenas números e ponto decimal"""
    if not valor:
        return ""
    
    # Remove tudo exceto números e vírgula
    numeros = ''.join(c for c in str(valor) if c.isdigit() or c == ',')
    
    # Substitui vírgula por ponto
    return numeros.replace(',', '.')
