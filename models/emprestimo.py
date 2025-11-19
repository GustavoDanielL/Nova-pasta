from datetime import datetime, timedelta
from utils.calculos import calcular_juros_compostos

class Emprestimo:
    def __init__(self, cliente_id, valor_emprestado, taxa_juros, data_inicio, prazo_meses, id=None):
        self.id = id or self.gerar_id()
        self.cliente_id = cliente_id
        self.valor_emprestado = float(valor_emprestado)
        self.taxa_juros = float(taxa_juros) / 100  # Convertendo para decimal
        self.data_inicio = data_inicio
        self.prazo_meses = int(prazo_meses)
        self.data_criacao = datetime.now().isoformat()
        self.ativo = True
        self.pagamentos = []
        
        # Calcular valores iniciais
        self.calcular_valores()
        
    def gerar_id(self):
        return f"EMP{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    def calcular_valores(self):
        # Valor total com juros compostos
        self.valor_total = calcular_juros_compostos(
            self.valor_emprestado, self.taxa_juros, self.prazo_meses
        )
        
        # Valor da parcela mensal
        self.valor_parcela = self.valor_total / self.prazo_meses
        
        # Saldo devedor inicial
        self.saldo_devedor = self.valor_total
        
        # Total de juros
        self.total_juros = self.valor_total - self.valor_emprestado
        
    def registrar_pagamento(self, valor, data=None, tipo="Parcela"):
        # Validação: rejeitar se já foi quitado
        if self.saldo_devedor <= 0:
            raise ValueError("Este empréstimo já foi totalmente quitado. Não é possível registrar novos pagamentos.")
        
        # Validação: rejeitar valor inválido
        if valor <= 0:
            raise ValueError("O valor do pagamento deve ser maior que zero.")
        
        pagamento = {
            'id': f"PGT{datetime.now().strftime('%Y%m%d%H%M%S')}",
            'valor': float(valor),
            'data': data or datetime.now().isoformat(),
            'tipo': tipo,
            'saldo_anterior': self.saldo_devedor
        }
        
        self.pagamentos.append(pagamento)
        self.saldo_devedor -= valor
        
        # Recalcular se pagamento exceder o saldo
        if self.saldo_devedor < 0:
            self.saldo_devedor = 0
            
        if self.saldo_devedor <= 0:
            self.ativo = False
    
    def get_historico_pagamentos(self):
        return sorted(self.pagamentos, key=lambda x: x['data'])
    
    def get_proxima_parcela(self):
        parcelas_pagas = len([p for p in self.pagamentos if p['tipo'] == 'Parcela'])
        return parcelas_pagas + 1 if parcelas_pagas < self.prazo_meses else None
    
    def to_dict(self):
        return {
            'id': self.id,
            'cliente_id': self.cliente_id,
            'valor_emprestado': self.valor_emprestado,
            'taxa_juros': self.taxa_juros,
            'data_inicio': self.data_inicio,
            'prazo_meses': self.prazo_meses,
            'data_criacao': self.data_criacao,
            'ativo': self.ativo,
            'valor_total': self.valor_total,
            'valor_parcela': self.valor_parcela,
            'saldo_devedor': self.saldo_devedor,
            'total_juros': self.total_juros,
            'pagamentos': self.pagamentos
        }
    
    @classmethod
    def from_dict(cls, data):
        emprestimo = cls(
            cliente_id=data['cliente_id'],
            valor_emprestado=data['valor_emprestado'],
            taxa_juros=data['taxa_juros'] * 100,  # Convertendo para percentual
            data_inicio=data['data_inicio'],
            prazo_meses=data['prazo_meses'],
            id=data['id']
        )
        
        emprestimo.data_criacao = data['data_criacao']
        emprestimo.ativo = data['ativo']
        emprestimo.pagamentos = data['pagamentos']
        
        # Manter valores calculados do JSON
        emprestimo.valor_total = data['valor_total']
        emprestimo.valor_parcela = data['valor_parcela']
        emprestimo.saldo_devedor = data['saldo_devedor']
        emprestimo.total_juros = data['total_juros']
        
        return emprestimo