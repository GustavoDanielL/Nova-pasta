"""
Sistema de Logging Profissional
Configura logging com rotação e níveis adequados
"""
import logging
import logging.handlers
from pathlib import Path
from datetime import datetime


def configurar_logging(log_dir: Path = None, nivel=logging.INFO):
    """
    Configura sistema de logging da aplicação
    
    Args:
        log_dir: Diretório para salvar logs (padrão: logs/ no diretório de dados)
        nivel: Nível de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    # Diretório de logs
    if log_dir is None:
        log_dir = Path.home() / "Documentos" / "FinancePro" / "logs"
    
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Nome do arquivo de log
    log_file = log_dir / f"financepro_{datetime.now().strftime('%Y%m%d')}.log"
    
    # Formato do log
    log_format = logging.Formatter(
        fmt='%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler para arquivo com rotação (máx 10MB, manter 5 backups)
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(nivel)
    file_handler.setFormatter(log_format)
    
    # Handler para console (apenas WARNING e acima)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(log_format)
    
    # Configurar logger raiz
    root_logger = logging.getLogger()
    root_logger.setLevel(nivel)
    
    # Remover handlers antigos
    root_logger.handlers.clear()
    
    # Adicionar novos handlers
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    # Log inicial
    logger = logging.getLogger(__name__)
    logger.info("=" * 60)
    logger.info("FinancePro iniciado")
    logger.info(f"Logs salvos em: {log_file}")
    logger.info("=" * 60)
    
    return logger


def log_exception(logger, exception: Exception, mensagem: str = "Erro inesperado"):
    """
    Loga exceção com traceback completo
    
    Args:
        logger: Logger instance
        exception: Exceção capturada
        mensagem: Mensagem descritiva
    """
    logger.error(f"{mensagem}: {type(exception).__name__}: {str(exception)}", exc_info=True)


def log_operacao(logger, operacao: str, sucesso: bool, detalhes: str = ""):
    """
    Loga resultado de operação
    
    Args:
        logger: Logger instance
        operacao: Nome da operação (ex: "Cadastrar Cliente")
        sucesso: True se sucesso, False se erro
        detalhes: Detalhes adicionais
    """
    if sucesso:
        logger.info(f"✓ {operacao} - Sucesso {f'| {detalhes}' if detalhes else ''}")
    else:
        logger.error(f"✗ {operacao} - Falhou {f'| {detalhes}' if detalhes else ''}")


# Exemplo de uso:
if __name__ == "__main__":
    logger = configurar_logging()
    
    logger.debug("Mensagem de debug (desenvolvimento)")
    logger.info("Aplicação iniciada")
    logger.warning("Aviso: Configuração SMTP não encontrada")
    logger.error("Erro ao conectar com banco de dados")
    logger.critical("Erro crítico: Sistema indisponível")
    
    log_operacao(logger, "Cadastrar Cliente", True, "João Silva")
    log_operacao(logger, "Salvar Empréstimo", False, "Dados inválidos")
    
    try:
        1 / 0
    except Exception as e:
        log_exception(logger, e, "Erro no cálculo")
