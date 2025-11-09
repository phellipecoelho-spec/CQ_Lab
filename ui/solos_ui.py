import customtkinter as ctk

class SolosUI:
    def __init__(self, master, usuario):
        self.master = master
        self.usuario = usuario

        # Frame principal centralizado
        self.frame = ctk.CTkFrame(master)
        self.frame.pack(expand=True, fill="both")

        # Frame central para label e botões
        self.center_frame = ctk.CTkFrame(self.frame, width=380, height=220, corner_radius=16)
        self.center_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.center_frame.pack_propagate(False)

        self.label = ctk.CTkLabel(self.center_frame, text="Módulo Solos", font=("Arial", 18))
        self.label.pack(pady=(30, 20))

        self.btn_voltar = ctk.CTkButton(self.center_frame, text="Voltar", command=self.voltar_menu, width=180)
        self.btn_voltar.pack(pady=18, padx=30)

        # Centralizar a janela principal ao abrir (caso seja uma janela Toplevel)
        if hasattr(master, 'geometry') and hasattr(master, 'winfo_screenwidth'):
            master.update_idletasks()
            width = 800
            height = 600
            x = (master.winfo_screenwidth() // 2) - (width // 2)
            y = (master.winfo_screenheight() // 2) - (height // 2)
            master.geometry(f"{width}x{height}+{x}+{y}")

    def voltar_menu(self):
        from ui.main_menu import MainMenu
        self.frame.destroy()
        MainMenu(self.master, self.usuario)
