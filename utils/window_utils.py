"""
Utilidades para janelas modais
"""
import customtkinter as ctk


def configurar_janela_modal(janela: ctk.CTkToplevel, titulo: str, largura: int, altura: int, parent=None):
    """
    Configura uma janela modal para aparecer na frente e centralizada
    
    Args:
        janela: Janela CTkToplevel
        titulo: Título da janela
        largura: Largura em pixels
        altura: Altura em pixels
        parent: Widget pai (opcional, para centralizar relativo ao pai)
    """
    janela.title(titulo)
    janela.geometry(f"{largura}x{altura}")
    
    # Garantir que janela aparece na frente
    janela.lift()
    janela.focus_force()
    janela.grab_set()  # Modal - bloqueia interação com outras janelas
    janela.attributes('-topmost', True)  # Sempre no topo
    
    # Centralizar na tela ou relativo ao parent
    if parent:
        # Centralizar relativo ao widget pai
        janela.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - largura) // 2
        y = parent.winfo_y() + (parent.winfo_height() - altura) // 2
        janela.geometry(f"+{x}+{y}")
    else:
        # Centralizar na tela
        janela.update_idletasks()
        screen_width = janela.winfo_screenwidth()
        screen_height = janela.winfo_screenheight()
        x = (screen_width - largura) // 2
        y = (screen_height - altura) // 2
        janela.geometry(f"+{x}+{y}")
    
    # Após um momento, remover topmost para permitir outras janelas sobre ela se necessário
    janela.after(100, lambda: janela.attributes('-topmost', False))
    
    return janela
