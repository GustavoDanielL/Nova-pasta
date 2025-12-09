#!/usr/bin/env python3
"""
Teste do login e database
"""
import customtkinter as ctk
from models.database import Database

print("=== TESTE: Login e Database ===")

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

db = Database()
db.carregar_dados()
print(f"Database carregado: {len(db.clientes)} clientes, {len(db.emprestimos)} empréstimos")

root = ctk.CTk()
root.title("Teste Login")
root.geometry("600x400")

# Simular tela de login simples
frame = ctk.CTkFrame(root, fg_color="#ffffff")
frame.pack(fill="both", expand=True)

ctk.CTkLabel(frame, text="FinancePro", font=("Segoe UI", 28, "bold")).pack(pady=20)

entry = ctk.CTkEntry(frame, width=300)
entry.pack(pady=10)
entry.insert(0, "admin")

btn = ctk.CTkButton(frame, text="Entrar", fg_color="#3b82f6")
btn.pack(pady=10)

print("Janela de login criada. Feche para terminar o teste.")

try:
    root.mainloop()
    print("=== TESTE CONCLUÍDO ===")
except Exception as e:
    print(f"=== ERRO: {e} ===")
    import traceback
    traceback.print_exc()
