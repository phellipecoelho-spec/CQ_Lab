import customtkinter as ctk
from ui.login_ui import LoginUI

def main():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title("CQ_Lab - Controle Tecnológico")
    app.geometry("800x600")

    # Centralizar a janela principal na tela
    app.update_idletasks()
    width = 800
    height = 600
    x = (app.winfo_screenwidth() // 2) - (width // 2)
    y = (app.winfo_screenheight() // 2) - (height // 2)
    app.geometry(f"{width}x{height}+{x}+{y}")

    LoginUI(app)  # inicia pela tela de login

    app.mainloop()

if __name__ == "__main__":
    main()
