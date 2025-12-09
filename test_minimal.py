#!/usr/bin/env python3
"""
Script de teste minimalista para identificar o que causa crash
"""
import customtkinter as ctk

print("=== TESTE 1: Importando CustomTkinter ===")
print("OK")

print("\n=== TESTE 2: Criando janela básica ===")
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")
root = ctk.CTk()
root.title("Teste Básico")
root.geometry("400x300")
print("OK")

print("\n=== TESTE 3: Adicionando componentes básicos ===")
label = ctk.CTkLabel(root, text="Teste", font=("Arial", 20))
label.pack(pady=20)
print("OK")

print("\n=== TESTE 4: Adicionando botão ===")
btn = ctk.CTkButton(root, text="Clique aqui", fg_color="#3b82f6")
btn.pack(pady=10)
print("OK")

print("\n=== TESTE 5: Adicionando frame ===")
frame = ctk.CTkFrame(root, fg_color="#ffffff", border_width=2, border_color="#e5e7eb")
frame.pack(fill="both", expand=True, padx=20, pady=20)
print("OK")

print("\n=== TESTE 6: Iniciando loop ===")
print("Se o app crashar agora, o problema é no loop do Tkinter com tema Light")
print("Feche a janela manualmente para continuar")

try:
    root.mainloop()
    print("\n=== TESTE CONCLUÍDO: App fechou normalmente ===")
except Exception as e:
    print(f"\n=== ERRO: {e} ===")
    import traceback
    traceback.print_exc()
