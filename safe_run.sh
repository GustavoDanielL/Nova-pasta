#!/bin/bash
# Script para rodar o FinancePro com logs de debug

echo "=== Iniciando FinancePro com debug ==="
echo "Data: $(date)"
echo "Sistema: $(uname -a)"
echo "Python: $(python --version)"
echo ""

# Executar com logs detalhados
python -u main.py 2>&1 | tee financepro_debug.log

EXIT_CODE=$?
echo ""
echo "=== Aplicação encerrada com código: $EXIT_CODE ==="
echo "Log salvo em: financepro_debug.log"
