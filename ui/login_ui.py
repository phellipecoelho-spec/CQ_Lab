# D:\CQ_Lab\ui\login_ui.py

import customtkinter as ctk
from utils.auth import autenticar_usuario, criar_usuario, resetar_senha, validar_senha, normalize_user
from ui.main_menu import MainMenu

class LoginUI:

    def __init__(self, master):
        self.master = master
        # Frame centralizado, com largura maior e padding lateral
        self.frame = ctk.CTkFrame(master, width=400, height=400, corner_radius=16)
        self.frame.pack(expand=True)
        self.frame.pack_propagate(False)  # Impede o frame de encolher

        # Título
        self.label_title = ctk.CTkLabel(self.frame, text="Login CQ_Lab", font=("Arial", 22))
        self.label_title.pack(pady=(30, 20))

        # Campo Usuário
        self.entry_user = ctk.CTkEntry(self.frame, placeholder_text="Usuário", width=260)
        self.entry_user.pack(pady=10)
        # Normalizar usuário ao perder foco
        self.entry_user.bind("<FocusOut>", lambda e: self._normalize_user())

        # Campo Senha
        self.entry_pass = ctk.CTkEntry(self.frame, placeholder_text="Senha", show="*", width=260)
        self.entry_pass.pack(pady=10)

        # Botão Entrar
        self.button_login = ctk.CTkButton(self.frame, text="Entrar", command=self.login, width=180)
        self.button_login.pack(pady=15)

        # Botão Novo Usuário
        self.button_cadastro = ctk.CTkButton(self.frame, text="Novo Usuário", command=self.abrir_cadastro, width=180)
        self.button_cadastro.pack(pady=10)

        # Botão Esqueci a Senha
        self.button_reset = ctk.CTkButton(self.frame, text="Esqueci a senha", command=self.abrir_reset, width=180)
        self.button_reset.pack(pady=4)

        # Status
        self.label_status = ctk.CTkLabel(self.frame, text="", font=("Arial", 12))
        self.label_status.pack(pady=10)
        # Fim do visual melhorado

    # -----------------------
    # Função de login
    # -----------------------
    def login(self):
        usuario = self.entry_user.get().strip()
        senha = self.entry_pass.get().strip()

        if autenticar_usuario(usuario, senha):
            self.frame.destroy()
            MainMenu(self.master, usuario)
        else:
            self.label_status.configure(text="Usuário ou senha inválidos", text_color="red")

    # -----------------------
    # Janela de cadastro
    # -----------------------
    def abrir_cadastro(self):
        janela_cadastro = ctk.CTkToplevel(self.master)
        janela_cadastro.title("Cadastro de Novo Usuário")
        janela_cadastro.geometry("440x460")
        janela_cadastro.resizable(False, False)

        # Garante que a janela fique à frente e centralizada
        janela_cadastro.transient(self.master)  # Fica à frente da tela de login
        janela_cadastro.grab_set()  # Bloqueia interação com a tela de login
        janela_cadastro.focus_force()  # Foca na janela de cadastro

        # Centralizar a janela na tela principal
        self.master.update_idletasks()
        janela_cadastro.update_idletasks()
        w = 440
        h = 460
        x = self.master.winfo_x() + (self.master.winfo_width() // 2) - (w // 2)
        y = self.master.winfo_y() + (self.master.winfo_height() // 2) - (h // 2)
        janela_cadastro.geometry(f"{w}x{h}+{x}+{y}")

        # Frame centralizado e padronizado
        frame_cadastro = ctk.CTkFrame(janela_cadastro, width=420, height=440, corner_radius=16)
        frame_cadastro.pack(expand=True)
        frame_cadastro.pack_propagate(False)

        label_titulo = ctk.CTkLabel(frame_cadastro, text="Criar Novo Usuário", font=("Arial", 18))
        label_titulo.pack(pady=(30, 20))

        entry_novo_user = ctk.CTkEntry(frame_cadastro, placeholder_text="Usuário", width=240)
        entry_novo_user.pack(pady=10)

        entry_nova_senha = ctk.CTkEntry(frame_cadastro, placeholder_text="Senha", show="*", width=240)
        entry_nova_senha.pack(pady=10)

        entry_confirmar = ctk.CTkEntry(frame_cadastro, placeholder_text="Confirmar Senha", show="*", width=240)
        entry_confirmar.pack(pady=10)

        # Checklist dinâmico de requisitos de senha
        checklist_frame = ctk.CTkFrame(frame_cadastro)
        checklist_frame.pack(fill="y", padx=10, pady=(10,2))

        lbl_len = ctk.CTkLabel(checklist_frame, text="  • Mínimo 8 caracteres  ", text_color="white")
        lbl_len.pack(anchor="w")
        lbl_alpha = ctk.CTkLabel(checklist_frame, text="  • Contém letra  ", text_color="white")
        lbl_alpha.pack(anchor="w")
        lbl_digit = ctk.CTkLabel(checklist_frame, text="  • Contém número  ", text_color="white")
        lbl_digit.pack(anchor="w")

        def _update_checklist(event=None):
            s = entry_nova_senha.get()
            lbl_len.configure(text_color=("green" if len(s) >= 8 else "red"))
            lbl_alpha.configure(text_color=("green" if any(c.isalpha() for c in s) else "red"))
            lbl_digit.configure(text_color=("green" if any(c.isdigit() for c in s) else "red"))

        entry_nova_senha.bind("<KeyRelease>", _update_checklist)

        label_msg = ctk.CTkLabel(frame_cadastro, text="", font=("Arial", 12))
        label_msg.pack(pady=10)

        def cadastrar():
            user = entry_novo_user.get().strip()
            senha = entry_nova_senha.get().strip()
            confirmar = entry_confirmar.get().strip()

            if not user or not senha:
                label_msg.configure(text="Preencha todos os campos", text_color="red")
                return

            if senha != confirmar:
                label_msg.configure(text="As senhas não coincidem", text_color="red")
                return

            # Tentar criar usuário, tratar erros de validação
            try:
                created = criar_usuario(user, senha)
            except ValueError as ve:
                label_msg.configure(text=str(ve), text_color="red")
                return

            if created:
                label_msg.configure(text="Usuário criado com sucesso!", text_color="green")
                entry_novo_user.delete(0, "end")
                entry_nova_senha.delete(0, "end")
                entry_confirmar.delete(0, "end")
            else:
                label_msg.configure(text="Usuário já existe!", text_color="red")

        button_criar = ctk.CTkButton(frame_cadastro, text="Cadastrar", command=cadastrar, width=240)
        button_criar.pack(pady=5)

    def _normalize_user(self):
        val = self.entry_user.get()
        if val:
            self.entry_user.delete(0, 'end')
            self.entry_user.insert(0, normalize_user(val))

    def abrir_reset(self):
        janela = ctk.CTkToplevel(self.master)
        janela.title("Resetar Senha")
        janela.geometry("440x360")
        janela.transient(self.master)
        janela.grab_set()
        janela.focus_force()

        # centralizar
        self.master.update_idletasks()
        janela.update_idletasks()
        w = 440
        h = 400
        x = self.master.winfo_x() + (self.master.winfo_width() // 2) - (w // 2)
        y = self.master.winfo_y() + (self.master.winfo_height() // 2) - (h // 2)
        janela.geometry(f"{w}x{h}+{x}+{y}")

        frame = ctk.CTkFrame(janela, width=400, height=320, corner_radius=12)
        frame.pack(expand=True)
        frame.pack_propagate(False)

        lbl = ctk.CTkLabel(frame, text="Resetar Senha", font=("Arial", 16))
        lbl.pack(pady=(20,10))

        entry_user = ctk.CTkEntry(frame, placeholder_text="Usuário", width=260)
        entry_user.pack(pady=6)

        entry_nova = ctk.CTkEntry(frame, placeholder_text="Nova senha", show="*", width=260)
        entry_nova.pack(pady=6)

        entry_conf = ctk.CTkEntry(frame, placeholder_text="Confirmar nova senha", show="*", width=260)
        entry_conf.pack(pady=6)

        lbl_msg = ctk.CTkLabel(frame, text="", font=("Arial", 12))
        lbl_msg.pack(pady=6)

        def confirmar_reset():
            u = entry_user.get().strip()
            s = entry_nova.get().strip()
            c = entry_conf.get().strip()

            if not u or not s or not c:
                lbl_msg.configure(text="Preencha todos os campos", text_color="red")
                return
            if s != c:
                lbl_msg.configure(text="As senhas não coincidem", text_color="red")
                return
            if not validar_senha(s):
                lbl_msg.configure(text="Senha deve ter >=8 caracteres e conter letras e números", text_color="red")
                return
            # tentar resetar
            try:
                ok = resetar_senha(u, s)
                if ok:
                    lbl_msg.configure(text="Senha atualizada com sucesso", text_color="green")
                    entry_user.delete(0, 'end')
                    entry_nova.delete(0, 'end')
                    entry_conf.delete(0, 'end')
                else:
                    lbl_msg.configure(text="Usuário não encontrado", text_color="red")
            except ValueError as ve:
                lbl_msg.configure(text=str(ve), text_color="red")

        btn = ctk.CTkButton(frame, text="Confirmar", command=confirmar_reset, width=160)
        btn.pack(pady=6)
