import qrcode
from PIL import Image
import customtkinter as ctk
from io import BytesIO
import tkinter as tk

class QRGenerator:
    @staticmethod
    def gerar_qr_code(valor, descricao=""):
        # Formatar dados para PIX
        dados_pix = f"""
        Valor: R$ {valor:.2f}
        Descrição: {descricao}
        Instruções: Pagamento via PIX
        """
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(dados_pix)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        return img
    
    @staticmethod
    def mostrar_qr_code(parent, valor, descricao):
        janela = ctk.CTkToplevel(parent)
        janela.title("QR Code para Pagamento")
        janela.geometry("400x500")
        janela.transient(parent)
        janela.grab_set()
        
        # Gerar QR Code
        img = QRGenerator.gerar_qr_code(valor, descricao)
        
        # Converter para formato que o CTk pode usar
        img_tk = QRGenerator.pil_to_ctk_image(img, (300, 300))
        
        # Exibir QR Code
        label_qr = ctk.CTkLabel(janela, image=img_tk, text="")
        label_qr.pack(pady=20)
        
        # Informações
        info_text = f"Valor: R$ {valor:.2f}\n{descricao}"
        label_info = ctk.CTkLabel(janela, text=info_text, font=("Arial", 14))
        label_info.pack(pady=10)
        
        # Botões
        frame_botoes = ctk.CTkFrame(janela)
        frame_botoes.pack(pady=10)
        
        def salvar_imagem():
            from tkinter import filedialog
            arquivo = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
            )
            if arquivo:
                img.save(arquivo)
        
        btn_salvar = ctk.CTkButton(frame_botoes, text="Salvar QR Code", command=salvar_imagem)
        btn_salvar.pack(side="left", padx=5)
        
        btn_fechar = ctk.CTkButton(frame_botoes, text="Fechar", command=janela.destroy)
        btn_fechar.pack(side="left", padx=5)
    
    @staticmethod
    def pil_to_ctk_image(pil_image, size):
        from PIL import ImageTk
        pil_image = pil_image.resize(size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(pil_image)