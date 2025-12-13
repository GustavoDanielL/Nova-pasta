from datetime import datetime, timedelta
from utils.calculos import calcular_juros_compostos

class Emprestimo:
    def __init__(self, cliente_id, valor_emprestado, taxa_juros, data_emprestimo, prazo_meses, id=None, data_vencimento=None, metodo_calculo='compostos'):
        self.id = id or self.gerar_id()
        self.cliente_id = cliente_id
        self.valor_emprestado = float(valor_emprestado)
        self.taxa_juros = float(taxa_juros) / 100  # Convertendo para decimal
        self.data_emprestimo = data_emprestimo  # CORRIGIDO: era data_inicio
        self.prazo_meses = int(prazo_meses)
        self.data_vencimento = data_vencimento or self._calcular_data_vencimento()
        self.data_criacao = datetime.now().isoformat()
        self.ativo = True
        self.pagamentos = []
        self.metodo_calculo = metodo_calculo
        self.observacoes = ""
        
        # Calcular valores iniciais
        self.calcular_valores()
    
    def _calcular_data_vencimento(self):
        """Calcula automaticamente a data de vencimento baseado na data de empréstimo e prazo."""
        try:
            data_inicio_obj = datetime.fromisoformat(self.data_emprestimo)
            dias_total = self.prazo_meses * 30  # Aproximado: 30 dias por mês
            data_venc = data_inicio_obj + timedelta(days=dias_total)
            return data_venc.date().isoformat()
        except:
            return None
        
    def gerar_id(self):
        return f"EMP{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
    
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
    
    def esta_quitado(self):
        """Verifica se o empréstimo está quitado (saldo devedor zerado)"""
        return self.saldo_devedor <= 0
    
    def esta_atrasado(self):
        """Verifica se o empréstimo tem parcelas atrasadas"""
        if self.esta_quitado():
            return False
        
        try:
            data_venc = datetime.fromisoformat(self.data_vencimento).date() if isinstance(self.data_vencimento, str) else self.data_vencimento
            hoje = datetime.now().date()
            return hoje > data_venc
        except:
            return False
    
    def dias_atraso(self):
        """Retorna quantidade de dias de atraso (0 se não estiver atrasado)"""
        if not self.esta_atrasado():
            return 0
        
        try:
            data_venc = datetime.fromisoformat(self.data_vencimento).date() if isinstance(self.data_vencimento, str) else self.data_vencimento
            hoje = datetime.now().date()
            return (hoje - data_venc).days
        except:
            return 0
    
    def get_status_badge(self):
        """Retorna badge formatado com emoji e texto do status"""
        if self.esta_quitado():
            return "✅ QUITADO"
        elif self.esta_atrasado():
            dias = self.dias_atraso()
            return f"⚠️ ATRASADO ({dias} dias)"
        else:
            return "🔄 EM DIA"
    
    def to_dict(self):
        return {
            'id': self.id,
            'cliente_id': self.cliente_id,
            'valor_emprestado': self.valor_emprestado,
            'taxa_juros': self.taxa_juros,
            'data_emprestimo': self.data_emprestimo,
            'prazo_meses': self.prazo_meses,
            'data_vencimento': self.data_vencimento,
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
            data_emprestimo=data.get('data_emprestimo', data.get('data_inicio')),
            prazo_meses=data['prazo_meses'],
            id=data['id'],
            data_vencimento=data.get('data_vencimento')
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