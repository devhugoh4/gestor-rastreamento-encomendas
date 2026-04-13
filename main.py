import customtkinter as ctk
from tkinter import messagebox
import sqlite3

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class SistemaRastreio(ctk.CTk): 
    def __init__(self):
        super().__init__()

        self.title("Sistema de Gestão de Encomendas")
        self.geometry("500x480")
        
        self.inicializar_banco()

        self.label_titulo = ctk.CTkLabel(self, text="📦 Rastreamento & Cadastro", font=("Roboto", 22, "bold"))
        self.label_titulo.pack(pady=20)

        self.frame_busca = ctk.CTkFrame(self)
        self.frame_busca.pack(pady=10, padx=20, fill="x")
        
        self.entry_codigo = ctk.CTkEntry(self.frame_busca, placeholder_text="Código de rastreio")
        self.entry_codigo.grid(row=0, column=0, padx=10, pady=15, sticky="ew")
        
        self.btn_rastrear = ctk.CTkButton(self.frame_busca, text="BUSCAR", command=self.rastrear_encomenda)
        self.btn_rastrear.grid(row=0, column=1, padx=10)

        self.label_cad = ctk.CTkLabel(self, text="Cadastrar/Atualizar Encomenda", font=("Roboto", 14, "bold"))
        self.label_cad.pack(pady=(20, 5))

        self.entry_novo_cod = ctk.CTkEntry(self, placeholder_text="Novo Código", width=300)
        self.entry_novo_cod.pack(pady=5)

        self.entry_status = ctk.CTkEntry(self, placeholder_text="Status (Ex: Postado, Em trânsito)", width=300)
        self.entry_status.pack(pady=5)

        self.btn_salvar = ctk.CTkButton(self, text="SALVAR", fg_color="green", hover_color="darkgreen", command=self.cadastrar_encomenda)
        self.btn_salvar.pack(pady=20)

    def inicializar_banco(self):
        conn = sqlite3.connect('rastreio.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS encomendas (
                codigo TEXT PRIMARY KEY,
                status TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def cadastrar_encomenda(self):
        cod = self.entry_novo_cod.get().strip()
        status = self.entry_status.get().strip()

        if not cod or not status:
            messagebox.showwarning("Atenção", "Preencha todos os campos.")
            return

        conn = sqlite3.connect('rastreio.db')
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO encomendas (codigo, status) VALUES (?, ?)", (cod, status))
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Sucesso", f"Encomenda {cod} salva/atualizada!")
        self.entry_novo_cod.delete(0, 'end')
        self.entry_status.delete(0, 'end')

    def rastrear_encomenda(self):
        codigo = self.entry_codigo.get().strip()
        
        if not codigo:
            messagebox.showwarning("Atenção", "Digite um código.")
            return

        conn = sqlite3.connect('rastreio.db')
        cursor = conn.cursor()
        cursor.execute("SELECT status FROM encomendas WHERE codigo = ?", (codigo,))
        resultado = cursor.fetchone()
        conn.close()

        if resultado:
            messagebox.showinfo("Resultado", f"Código: {codigo}\nStatus: {resultado[0]}")
        else:
            messagebox.showerror("Erro", "Código não encontrado no sistema.")

if __name__ == "__main__":
    app = SistemaRastreio()
    app.mainloop()