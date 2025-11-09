# D:\CQ_Lab\ui\main_menu.py

import customtkinter as ctk
from ui.solos_ui import SolosUI
from ui.concreto_ui import ConcretoUI
from ui.asfalto_ui import AsfaltoUI


class MainMenu:
    def __init__(self, master, usuario):
        self.master = master
        self.usuario = usuario

        # Frame principal centralizado
        self.frame = ctk.CTkFrame(master)
        self.frame.pack(expand=True, fill="both")

        # Frame central para label e botões
        self.center_frame = ctk.CTkFrame(
            self.frame, width=380, height=340, corner_radius=16)
        self.center_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.center_frame.pack_propagate(False)

        self.label = ctk.CTkLabel(
            self.center_frame, text=f"Bem-vindo, {usuario}!", font=("Arial", 22))
        self.label.pack(pady=(30, 20))

        # Botões principais
        self.btn_solos = ctk.CTkButton(
            self.center_frame, text="Solos", command=self.abrir_solos, width=220)
        self.btn_solos.pack(pady=10, padx=30)

        self.btn_concreto = ctk.CTkButton(
            self.center_frame, text="Concreto", command=self.abrir_concreto, width=220)
        self.btn_concreto.pack(pady=10, padx=30)

        self.btn_asfalto = ctk.CTkButton(
            self.center_frame, text="Asfalto", command=self.abrir_asfalto, width=220)
        self.btn_asfalto.pack(pady=10, padx=30)

        self.btn_sair = ctk.CTkButton(
            self.center_frame, text="Sair", command=self.sair, width=220)
        self.btn_sair.pack(pady=18, padx=30)

        # Frame maior e centralizado contendo o toggle de tema
        self.theme_frame = ctk.CTkFrame(
            self.center_frame, width=260, height=80, corner_radius=8)
        self.theme_frame.pack(pady=5)

        # Estado inicial do tema
        self.is_dark = ctk.get_appearance_mode() == "dark"
        texto_inicial = "Tema Claro" if self.is_dark else "Tema Escuro"

        self.theme_switch = ctk.CTkSwitch(
            self.theme_frame,
            text=texto_inicial,
            command=self.toggle_tema
        )
        self.theme_switch.pack(pady=5)

        # Centralizar a janela principal ao abrir (caso seja uma janela Toplevel)
        if hasattr(master, 'geometry') and hasattr(master, 'winfo_screenwidth'):
            master.update_idletasks()
            width = 800
            height = 600
            x = (master.winfo_screenwidth() // 2) - (width // 2)
            y = (master.winfo_screenheight() // 2) - (height // 2)
            master.geometry(f"{width}x{height}+{x}+{y}")

    def abrir_solos(self):
        self.frame.destroy()
        SolosUI(self.master, self.usuario)

    def abrir_concreto(self):
        self.frame.destroy()
        ConcretoUI(self.master, self.usuario)

    def abrir_asfalto(self):
        self.frame.destroy()
        AsfaltoUI(self.master, self.usuario)

    def sair(self):
        self.frame.destroy()
        from ui.login_ui import LoginUI  # import aqui dentro evita loop
        LoginUI(self.master)

    def toggle_tema(self):
        # Alterna entre modo claro e escuro
        self.is_dark = not self.is_dark
        novo_modo = "dark" if self.is_dark else "light"
        ctk.set_appearance_mode(novo_modo)

        # Atualiza o texto do botão de acordo com o tema atual
        self.theme_switch.configure(
            text="Tema Claro" if self.is_dark else "Tema Escuro")

# import customtkinter as ctk Modificado em 12/10/2025
# from utils.auth import autenticar_usuario
# from ui.main_menu import MainMenu  # Corrigido: Removido import circular

# class LoginUI:
#     def __init__(self, master):
#         self.master = master
#         self.frame = ctk.CTkFrame(master)
#         self.frame.pack(expand=True)

#         self.label_title = ctk.CTkLabel(self.frame, text="Login CQ_Lab", font=("Arial", 22))
#         self.label_title.pack(pady=20)

#         self.entry_user = ctk.CTkEntry(self.frame, placeholder_text="Usuário")
#         self.entry_user.pack(pady=10)

#         self.entry_pass = ctk.CTkEntry(self.frame, placeholder_text="Senha", show="*")
#         self.entry_pass.pack(pady=10)

#         self.button_login = ctk.CTkButton(self.frame, text="Entrar", command=self.login)
#         self.button_login.pack(pady=20)

#         self.label_status = ctk.CTkLabel(self.frame, text="", font=("Arial", 12))
#         self.label_status.pack(pady=10)

#     def login(self):
#         usuario = self.entry_user.get()
#         senha = self.entry_pass.get()

#         if autenticar_usuario(usuario, senha):
#             self.frame.destroy()
#             MainMenu(self.master, usuario)
#         else:
#             self.label_status.configure(text="Usuário ou senha inválidos", text_color="red")
